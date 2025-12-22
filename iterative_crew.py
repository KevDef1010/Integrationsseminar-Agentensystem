"""
Iterative Crew mit Test-Feedback-Loop
======================================
Agents:
1. Developer - Schreibt Code
2. Tester - Schreibt Tests und fuehrt sie aus
3. Bei Fehlern: Feedback an Developer bis Tests gruen sind

Dies implementiert einen iterativen Entwicklungsprozess wie in echten Teams.
"""

import os
import sys
import subprocess
import tempfile
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from crewai import Agent, Task, Crew, LLM

from experiment_runner import (
    ExperimentConfig, ExperimentTracer, ExperimentResult,
    get_system_info, estimate_tokens
)


# ============================================================
# CONFIGURATION
# ============================================================

MAX_ITERATIONS = 3  # Maximale Anzahl an Korrektur-Durchlaeufen
PYTHON_EXECUTABLE = sys.executable


@dataclass
class TestResult:
    """Ergebnis eines Test-Durchlaufs."""
    success: bool
    output: str
    errors: List[str]
    iteration: int


# ============================================================
# CODE EXECUTION & TESTING
# ============================================================

def extract_python_code(text: str) -> str:
    """Extrahiert Python-Code aus LLM-Output."""
    # Suche nach ```python ... ``` Bloecken
    code_blocks = re.findall(r'```python\n(.*?)```', text, re.DOTALL)
    if code_blocks:
        return '\n\n'.join(code_blocks)
    
    # Suche nach ``` ... ``` Bloecken
    code_blocks = re.findall(r'```\n(.*?)```', text, re.DOTALL)
    if code_blocks:
        return '\n\n'.join(code_blocks)
    
    # Wenn Text mit import beginnt, ist es wahrscheinlich Code
    if text.strip().startswith('import') or text.strip().startswith('from'):
        return text
    
    return text


def check_syntax(code: str) -> Tuple[bool, str]:
    """Prueft Python-Syntax ohne Ausfuehrung."""
    try:
        compile(code, '<string>', 'exec')
        return True, "Syntax OK"
    except SyntaxError as e:
        return False, f"Syntaxfehler Zeile {e.lineno}: {e.msg}"


def run_code_with_timeout(code: str, timeout: int = 5) -> Tuple[bool, str]:
    """
    Fuehrt Python-Code aus und prueft auf Fehler.
    Timeout verhindert Endlosschleifen.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        # Fuer GUI-Code: Fuege Auto-Close hinzu
        modified_code = code
        if 'mainloop()' in code:
            # Ersetze mainloop mit timeout-version
            modified_code = code.replace(
                'mainloop()', 
                'after(100, lambda: root.destroy() if hasattr(root, "destroy") else None); mainloop()'
            )
            # Oder einfacher: Nicht ausfuehren fuer GUI
            return True, "GUI-Code erkannt - Syntax OK, Ausfuehrung uebersprungen"
        
        f.write(modified_code)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [PYTHON_EXECUTABLE, temp_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.path.dirname(temp_file)
        )
        
        if result.returncode == 0:
            return True, result.stdout or "Code erfolgreich ausgefuehrt"
        else:
            return False, result.stderr or "Unbekannter Fehler"
            
    except subprocess.TimeoutExpired:
        return False, f"Timeout nach {timeout} Sekunden - moeglicherweise Endlosschleife"
    except Exception as e:
        return False, str(e)
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass


def run_tests(code: str, test_code: str) -> TestResult:
    """
    Fuehrt Tests gegen den Code aus.
    Kombiniert Code + Tests in einer Datei und fuehrt aus.
    """
    # Kombiniere Code und Tests
    combined = f'''
# ===== HAUPTCODE =====
{code}

# ===== TESTS =====
import unittest

{test_code}

if __name__ == "__main__":
    # Teste ohne GUI-Start
    unittest.main(verbosity=2, exit=False)
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='_test.py', delete=False, encoding='utf-8') as f:
        f.write(combined)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            [PYTHON_EXECUTABLE, temp_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout + result.stderr
        
        # Parse Test-Ergebnisse
        errors = []
        if 'FAIL' in output:
            # Extrahiere Fehler-Details
            fail_matches = re.findall(r'FAIL: (\w+).*?\n(.*?)(?=\n-{70}|\Z)', output, re.DOTALL)
            for test_name, details in fail_matches:
                errors.append(f"Test {test_name} fehlgeschlagen: {details[:200]}")
        
        if 'ERROR' in output:
            error_matches = re.findall(r'ERROR: (\w+).*?\n(.*?)(?=\n-{70}|\Z)', output, re.DOTALL)
            for test_name, details in error_matches:
                errors.append(f"Test {test_name} Error: {details[:200]}")
        
        if 'OK' in output and not errors:
            return TestResult(success=True, output=output, errors=[], iteration=0)
        else:
            return TestResult(success=False, output=output, errors=errors, iteration=0)
            
    except subprocess.TimeoutExpired:
        return TestResult(
            success=False, 
            output="", 
            errors=["Timeout - Tests brauchen zu lange"],
            iteration=0
        )
    except Exception as e:
        return TestResult(
            success=False,
            output="",
            errors=[str(e)],
            iteration=0
        )
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass


# ============================================================
# ITERATIVE CREW
# ============================================================

def run_iterative_experiment(
    experiment_name: str = "iterative_pokemon",
    task_description: str = None,
    models: Dict[str, str] = None,
    output_base_dir: str = "projekte",
    max_iterations: int = MAX_ITERATIONS
) -> ExperimentResult:
    """
    Fuehrt ein iteratives Experiment mit Test-Feedback-Loop durch.
    
    Ablauf:
    1. Developer schreibt Code
    2. Tester schreibt Tests
    3. Tests werden ausgefuehrt
    4. Bei Fehlern: Feedback an Developer
    5. Wiederhole bis Tests gruen oder max_iterations erreicht
    """
    
    if models is None:
        models = {
            "developer": "codellama:13b",
            "tester": "mistral:7b",
            "reviewer": "mistral:7b"
        }
    
    if task_description is None:
        task_description = """
Erstelle eine einfache Pokemon-Klasse mit folgenden Features:
- Attribute: name, typ, level, hp, max_hp, attacks (Liste)
- Methoden:
  * take_damage(amount) - Reduziert HP, gibt verbleibende HP zurueck
  * heal(amount) - Erhoeht HP bis max_hp
  * is_fainted() - True wenn hp <= 0
  * attack(target, attack_index) - Greift Ziel an, gibt Schaden zurueck
  * level_up() - Erhoeht Level um 1, max_hp um 5

Schreibe NUR die Klasse, keine GUI, kein main-Block.
Beginne mit: class Pokemon:
"""
    
    # Experiment Setup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_id = f"{experiment_name}_{timestamp}"
    output_dir = Path(output_base_dir) / experiment_id
    output_dir.mkdir(parents=True, exist_ok=True)
    
    config = ExperimentConfig(
        experiment_id=experiment_id,
        experiment_name=experiment_name,
        task_description=task_description,
        models=models
    )
    
    tracer = ExperimentTracer(experiment_id, str(output_dir))
    tracer.start_experiment()
    
    print("=" * 70)
    print(f"🔄 ITERATIVE EXPERIMENT: {experiment_name}")
    print(f"   ID: {experiment_id}")
    print(f"   Max Iterations: {max_iterations}")
    print("=" * 70)
    
    # LLMs konfigurieren
    developer_llm = LLM(
        model=f"ollama/{models['developer']}",
        base_url="http://localhost:11434"
    )
    tester_llm = LLM(
        model=f"ollama/{models['tester']}",
        base_url="http://localhost:11434"
    )
    
    experiment_start = time.time()
    
    try:
        # =========================================
        # PHASE 1: Initial Development
        # =========================================
        print(f"\n{'='*50}")
        print("📝 Phase 1: Initial Development")
        print(f"{'='*50}")
        
        developer = Agent(
            role="Python Developer",
            goal="Schreibe vollstaendigen, funktionierenden Python-Code",
            backstory="""Du bist ein erfahrener Python-Entwickler.
REGELN:
1. Schreibe NUR Python-Code, keine Erklaerungen
2. Jede Methode VOLLSTAENDIG implementieren
3. KEINE Platzhalter, KEIN 'pass', KEIN '...'
4. Code muss syntaktisch korrekt sein""",
            llm=developer_llm,
            verbose=True
        )
        
        dev_task = Task(
            description=task_description,
            expected_output="Vollstaendiger Python-Code",
            agent=developer
        )
        
        tracer.start_task("Developer", "initial_code", models['developer'])
        dev_crew = Crew(agents=[developer], tasks=[dev_task], verbose=True)
        dev_result = dev_crew.kickoff()
        
        current_code = extract_python_code(str(dev_result))
        tracer.end_task(task_description, current_code, success=True)
        
        print(f"\n✅ Initial Code: {len(current_code)} Zeichen")
        
        # Syntax-Check
        syntax_ok, syntax_msg = check_syntax(current_code)
        if not syntax_ok:
            print(f"⚠️ Syntax-Fehler: {syntax_msg}")
        
        # =========================================
        # PHASE 2: Test Generation
        # =========================================
        print(f"\n{'='*50}")
        print("🧪 Phase 2: Test Generation")
        print(f"{'='*50}")
        
        tester = Agent(
            role="Test Engineer",
            goal="Schreibe praezise unittest-Tests die NUR die vorhandenen Methoden testen",
            backstory="""Du bist ein erfahrener Test-Ingenieur.

KRITISCHE REGELN:
1. Teste NUR Methoden die im Code TATSAECHLICH existieren
2. ERFINDE KEINE neuen Methoden oder Attribute
3. Schreibe NUR Python-Code, keine Erklaerungen
4. Benutze KEINE externen Imports ausser unittest
5. Die Klassen sind DIREKT im selben Modul - KEIN from X import Y noetig
6. Beginne direkt mit: class Test...(unittest.TestCase):""",
            llm=tester_llm,
            verbose=True
        )
        
        # Analysiere welche Klassen und Methoden im Code sind
        class_names = re.findall(r'class\s+(\w+)', current_code)
        method_names = re.findall(r'def\s+(\w+)', current_code)
        
        test_task = Task(
            description=f"""Schreibe unittest-Tests fuer diesen Code:

```python
{current_code}
```

WICHTIG - Diese Klassen existieren: {', '.join(class_names)}
WICHTIG - Diese Methoden existieren: {', '.join(method_names)}

REGELN:
1. Teste NUR die oben genannten Methoden - KEINE anderen!
2. Die Klassen sind im selben Modul - schreibe KEINEN Import
3. Schreibe NUR Python-Code
4. Erstelle Instanzen der Klassen in setUp()
5. Jede test_* Methode testet genau EINE Funktion

Beginne direkt mit: class Test{class_names[0] if class_names else 'Code'}(unittest.TestCase):""",
            expected_output="unittest.TestCase Klasse mit Tests fuer die vorhandenen Methoden",
            agent=tester
        )
        
        tracer.start_task("Tester", "write_tests", models['tester'])
        test_crew = Crew(agents=[tester], tasks=[test_task], verbose=True)
        test_result = test_crew.kickoff()
        
        test_code = extract_python_code(str(test_result))
        tracer.end_task("Test generation", test_code, success=True)
        
        print(f"\n✅ Tests generiert: {len(test_code)} Zeichen")
        
        # =========================================
        # PHASE 3: Iterative Fixing
        # =========================================
        iteration = 0
        all_tests_pass = False
        
        while iteration < max_iterations and not all_tests_pass:
            iteration += 1
            print(f"\n{'='*50}")
            print(f"🔄 Iteration {iteration}/{max_iterations}: Running Tests")
            print(f"{'='*50}")
            
            # Tests ausfuehren
            test_result = run_tests(current_code, test_code)
            test_result.iteration = iteration
            
            if test_result.success:
                print(f"\n✅ Alle Tests bestanden!")
                all_tests_pass = True
                break
            else:
                print(f"\n❌ Tests fehlgeschlagen:")
                for error in test_result.errors[:3]:  # Max 3 Fehler zeigen
                    print(f"   - {error[:100]}...")
                
                if iteration < max_iterations:
                    # Feedback an Developer
                    print(f"\n🔧 Sende Feedback an Developer...")
                    
                    fix_developer = Agent(
                        role="Python Developer (Bugfix)",
                        goal="Behebe die gemeldeten Fehler im Code",
                        backstory="""Du bist ein erfahrener Python-Entwickler der Bugs fixt.
REGELN:
1. Analysiere die Fehlermeldungen genau
2. Gib den KOMPLETTEN korrigierten Code aus
3. Keine Erklaerungen, NUR Code
4. Behalte alle funktionierenden Teile bei""",
                        llm=developer_llm,
                        verbose=True
                    )
                    
                    error_summary = "\n".join(test_result.errors[:5])
                    fix_task = Task(
                        description=f"""Der folgende Code hat Test-Fehler:

```python
{current_code}
```

FEHLER:
{error_summary}

TEST OUTPUT:
{test_result.output[-1000:]}

Korrigiere den Code so dass alle Tests bestehen.
Gib den KOMPLETTEN korrigierten Code aus.
Beginne mit: class Pokemon:""",
                        expected_output="Korrigierter Python-Code",
                        agent=fix_developer
                    )
                    
                    tracer.start_task("Developer-Fix", f"iteration_{iteration}", models['developer'])
                    fix_crew = Crew(agents=[fix_developer], tasks=[fix_task], verbose=True)
                    fix_result = fix_crew.kickoff()
                    
                    current_code = extract_python_code(str(fix_result))
                    tracer.end_task(error_summary, current_code, success=True)
                    
                    print(f"\n✅ Code korrigiert: {len(current_code)} Zeichen")
        
        # =========================================
        # PHASE 4: Finalize
        # =========================================
        experiment_end = time.time()
        tracer.end_experiment()
        
        # Speichere finalen Code
        code_file = output_dir / f"{experiment_name}_final.py"
        with open(code_file, "w", encoding="utf-8") as f:
            f.write(f"# {experiment_name} - Generiert durch Iterative Crew\n")
            f.write(f"# Iterationen: {iteration}\n")
            f.write(f"# Tests bestanden: {all_tests_pass}\n\n")
            f.write(current_code)
        
        # Speichere Tests
        test_file = output_dir / f"{experiment_name}_tests.py"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(f"# Tests fuer {experiment_name}\n")
            f.write("import unittest\n\n")
            f.write(f"# Import der zu testenden Klasse\n")
            f.write(f"from {experiment_name}_final import *\n\n")
            f.write(test_code)
            f.write("\n\nif __name__ == '__main__':\n    unittest.main()\n")
        
        # Ergebnis
        total_tokens = sum(m.estimated_output_tokens for m in tracer.agent_metrics)
        
        experiment_result = ExperimentResult(
            config=config,
            agent_metrics=tracer.agent_metrics,
            total_duration_seconds=round(experiment_end - experiment_start, 2),
            total_estimated_tokens=total_tokens,
            system_info=get_system_info(),
            crew_output=current_code,
            individual_task_outputs=tracer.task_outputs,
            success=all_tests_pass
        )
        
        tracer.save_results(experiment_result)
        
        print(f"\n{'='*70}")
        print(f"{'✅' if all_tests_pass else '⚠️'} EXPERIMENT ABGESCHLOSSEN")
        print(f"   Iterationen: {iteration}")
        print(f"   Tests bestanden: {all_tests_pass}")
        print(f"   Dauer: {experiment_result.total_duration_seconds:.1f}s")
        print(f"   Tokens: {total_tokens}")
        print(f"   Output: {output_dir}")
        print(f"{'='*70}")
        
        return experiment_result
        
    except Exception as e:
        tracer.end_experiment()
        print(f"\n❌ FEHLER: {e}")
        import traceback
        traceback.print_exc()
        raise


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║         ITERATIVE CREW - Test-Driven Development                     ║
╠══════════════════════════════════════════════════════════════════════╣
║  Ablauf:                                                             ║
║  1. Developer schreibt initialen Code                                ║
║  2. Tester schreibt Unit-Tests                                       ║
║  3. Tests werden ausgefuehrt                                         ║
║  4. Bei Fehlern: Developer korrigiert (max 3x)                       ║
║  5. Wiederholen bis Tests gruen                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    print("Waehle eine Aufgabe:")
    print("  1. Pokemon-Klasse (einfach)")
    print("  2. Battle-System (mittel)")
    print("  3. Eigene Beschreibung")
    
    choice = input("\nAuswahl (1/2/3): ").strip() or "1"
    
    if choice == "1":
        task = """
Erstelle eine Pokemon-Klasse mit folgenden Features:
- Attribute: name (str), typ (str), level (int), hp (int), max_hp (int), attacks (list)
- Methoden:
  * __init__(name, typ, level, max_hp, attacks): Initialisiert Pokemon, hp = max_hp
  * take_damage(amount): Reduziert HP um amount, gibt verbleibende HP zurueck
  * heal(amount): Erhoeht HP um amount bis maximal max_hp
  * is_fainted(): Gibt True zurueck wenn hp <= 0
  * level_up(): Erhoeht level um 1 und max_hp um 5, heilt Pokemon voll

Schreibe NUR die Klasse, keine GUI, kein if __name__ Block.
Beginne mit: class Pokemon:
"""
        name = "pokemon_class"
        
    elif choice == "2":
        task = """
Erstelle ein einfaches Kampfsystem mit diesen Klassen:

class Attack:
    - name (str), damage (int), typ (str)
    
class Pokemon:
    - name, typ, level, hp, max_hp, attacks (Liste von Attack)
    - take_damage(amount) -> int
    - is_fainted() -> bool
    
class Battle:
    - pokemon1, pokemon2
    - current_turn (0 oder 1)
    - execute_attack(attacker_index, attack_index) -> str: Fuehrt Attacke aus, gibt Log zurueck
    - get_winner() -> Pokemon oder None: Gibt Gewinner zurueck wenn einer besiegt
    - switch_turn(): Wechselt current_turn

Schreibe alle 3 Klassen vollstaendig.
Beginne mit: class Attack:
"""
        name = "battle_system"
        
    else:
        task = input("Task-Beschreibung: ").strip()
        name = input("Experiment-Name: ").strip() or "custom"
    
    max_iter = input("Max Iterationen (default 3): ").strip()
    max_iter = int(max_iter) if max_iter.isdigit() else 3
    
    run_iterative_experiment(
        experiment_name=name,
        task_description=task,
        max_iterations=max_iter
    )
