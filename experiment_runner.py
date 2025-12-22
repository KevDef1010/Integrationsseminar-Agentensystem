"""
Experiment Runner fuer wissenschaftliche Auswertung
====================================================
Dieses Skript fuehrt Multi-Agent Experimente durch und trackt:
- Ausfuehrungszeiten pro Agent/Task
- Token-Nutzung (geschaetzt)
- Qualitaetsmetriken
- Alle Zwischenergebnisse
- Systemressourcen (RAM, CPU)

Ergebnisse werden als JSON und CSV exportiert fuer statistische Analyse.
"""

import os
import sys
import json
import csv
import time
import platform
import psutil
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from pathlib import Path

# CrewAI imports
from crewai import Agent, Task, Crew, LLM


# ============================================================
# KONFIGURATION
# ============================================================

@dataclass
class ExperimentConfig:
    """Konfiguration fuer ein Experiment."""
    experiment_id: str
    experiment_name: str
    task_description: str
    models: Dict[str, str]  # {"agent_role": "model_name"}
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


@dataclass
class AgentMetrics:
    """Metriken fuer einen einzelnen Agent."""
    agent_role: str
    model: str
    task_name: str
    start_time: float
    end_time: float
    duration_seconds: float
    input_chars: int
    output_chars: int
    estimated_input_tokens: int
    estimated_output_tokens: int
    success: bool
    error_message: Optional[str] = None


@dataclass
class ExperimentResult:
    """Gesamtergebnis eines Experiments."""
    config: ExperimentConfig
    agent_metrics: List[AgentMetrics]
    total_duration_seconds: float
    total_estimated_tokens: int
    system_info: Dict[str, Any]
    crew_output: str
    individual_task_outputs: List[Dict[str, str]]
    success: bool
    error_message: Optional[str] = None


# ============================================================
# SYSTEM INFO
# ============================================================

def get_system_info() -> Dict[str, Any]:
    """Sammelt Systeminformationen fuer Reproduzierbarkeit."""
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version(),
        "processor": platform.processor(),
        "cpu_count": psutil.cpu_count(),
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "ram_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
        "hostname": platform.node(),
        "timestamp": datetime.now().isoformat()
    }


def get_resource_snapshot() -> Dict[str, float]:
    """Momentaufnahme der Systemressourcen."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_used_gb": round(psutil.virtual_memory().used / (1024**3), 2)
    }


# ============================================================
# TOKEN ESTIMATION
# ============================================================

def estimate_tokens(text: str) -> int:
    """
    Schaetzt die Anzahl der Tokens (grobe Naeherung).
    Regel: ~4 Zeichen = 1 Token (fuer Englisch/Deutsch)
    """
    if not text:
        return 0
    return len(text) // 4


# ============================================================
# TRACING CALLBACK
# ============================================================

class ExperimentTracer:
    """Trackt alle Agent-Aktivitaeten waehrend eines Experiments."""
    
    def __init__(self, experiment_id: str, output_dir: str):
        self.experiment_id = experiment_id
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.agent_metrics: List[AgentMetrics] = []
        self.task_outputs: List[Dict[str, str]] = []
        self.resource_snapshots: List[Dict[str, Any]] = []
        self.logs: List[Dict[str, Any]] = []
        
        self.current_task_start: Optional[float] = None
        self.current_agent: Optional[str] = None
        self.current_task: Optional[str] = None
        
    def log(self, event: str, data: Dict[str, Any] = None):
        """Loggt ein Event mit Timestamp."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "elapsed_seconds": time.time() - self.start_time if hasattr(self, 'start_time') else 0,
            "event": event,
            "data": data or {}
        }
        self.logs.append(entry)
        
        # Auch in Logdatei schreiben
        log_file = self.output_dir / f"{self.experiment_id}_trace.jsonl"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    def start_experiment(self):
        """Markiert den Start eines Experiments."""
        self.start_time = time.time()
        self.log("experiment_started", {"system_info": get_system_info()})
    
    def end_experiment(self):
        """Markiert das Ende eines Experiments."""
        self.end_time = time.time()
        self.log("experiment_ended", {
            "total_duration": self.end_time - self.start_time
        })
    
    def start_task(self, agent_role: str, task_name: str, model: str):
        """Markiert den Start eines Tasks."""
        self.current_task_start = time.time()
        self.current_agent = agent_role
        self.current_task = task_name
        self.current_model = model
        
        snapshot = get_resource_snapshot()
        self.resource_snapshots.append({
            "phase": "task_start",
            "agent": agent_role,
            "task": task_name,
            **snapshot
        })
        
        self.log("task_started", {
            "agent": agent_role,
            "task": task_name,
            "model": model,
            "resources": snapshot
        })
    
    def end_task(self, input_text: str, output_text: str, success: bool = True, error: str = None):
        """Markiert das Ende eines Tasks mit Metriken."""
        end_time = time.time()
        duration = end_time - self.current_task_start
        
        input_chars = len(input_text) if input_text else 0
        output_chars = len(output_text) if output_text else 0
        
        metrics = AgentMetrics(
            agent_role=self.current_agent,
            model=self.current_model,
            task_name=self.current_task,
            start_time=self.current_task_start,
            end_time=end_time,
            duration_seconds=round(duration, 2),
            input_chars=input_chars,
            output_chars=output_chars,
            estimated_input_tokens=estimate_tokens(input_text),
            estimated_output_tokens=estimate_tokens(output_text),
            success=success,
            error_message=error
        )
        self.agent_metrics.append(metrics)
        
        self.task_outputs.append({
            "agent": self.current_agent,
            "task": self.current_task,
            "output": output_text[:5000] if output_text else ""  # Truncate for storage
        })
        
        snapshot = get_resource_snapshot()
        self.resource_snapshots.append({
            "phase": "task_end",
            "agent": self.current_agent,
            "task": self.current_task,
            **snapshot
        })
        
        self.log("task_completed", {
            "agent": self.current_agent,
            "task": self.current_task,
            "duration_seconds": round(duration, 2),
            "output_chars": output_chars,
            "estimated_tokens": estimate_tokens(output_text),
            "success": success,
            "resources": snapshot
        })
        
        return metrics
    
    def save_results(self, result: ExperimentResult):
        """Speichert alle Ergebnisse in verschiedenen Formaten."""
        
        # 1. Vollstaendiges JSON
        json_file = self.output_dir / f"{self.experiment_id}_full.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump({
                "config": asdict(result.config),
                "agent_metrics": [asdict(m) for m in result.agent_metrics],
                "total_duration_seconds": result.total_duration_seconds,
                "total_estimated_tokens": result.total_estimated_tokens,
                "system_info": result.system_info,
                "success": result.success,
                "error_message": result.error_message
            }, f, indent=2, ensure_ascii=False)
        
        # 2. CSV fuer Metriken (einfach in Excel/SPSS importierbar)
        csv_file = self.output_dir / f"{self.experiment_id}_metrics.csv"
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            if result.agent_metrics:
                writer = csv.DictWriter(f, fieldnames=asdict(result.agent_metrics[0]).keys())
                writer.writeheader()
                for m in result.agent_metrics:
                    writer.writerow(asdict(m))
        
        # 3. Ressourcen-Snapshots CSV
        resources_csv = self.output_dir / f"{self.experiment_id}_resources.csv"
        with open(resources_csv, "w", newline="", encoding="utf-8") as f:
            if self.resource_snapshots:
                writer = csv.DictWriter(f, fieldnames=self.resource_snapshots[0].keys())
                writer.writeheader()
                writer.writerows(self.resource_snapshots)
        
        # 4. Zusammenfassung als Markdown
        summary_file = self.output_dir / f"{self.experiment_id}_summary.md"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"# Experiment: {result.config.experiment_name}\n\n")
            f.write(f"**ID:** {result.config.experiment_id}\n\n")
            f.write(f"**Timestamp:** {result.config.timestamp}\n\n")
            f.write(f"**Status:** {'Erfolgreich' if result.success else 'Fehlgeschlagen'}\n\n")
            
            f.write("## Systeminfo\n\n")
            f.write(f"- Platform: {result.system_info.get('platform')}\n")
            f.write(f"- Python: {result.system_info.get('python_version')}\n")
            f.write(f"- CPU Cores: {result.system_info.get('cpu_count')}\n")
            f.write(f"- RAM Total: {result.system_info.get('ram_total_gb')} GB\n\n")
            
            f.write("## Verwendete Modelle\n\n")
            f.write("| Agent | Modell |\n")
            f.write("|-------|--------|\n")
            for agent, model in result.config.models.items():
                f.write(f"| {agent} | {model} |\n")
            
            f.write("\n## Metriken\n\n")
            f.write("| Agent | Task | Dauer (s) | Output Tokens | Erfolg |\n")
            f.write("|-------|------|-----------|---------------|--------|\n")
            for m in result.agent_metrics:
                status = "✓" if m.success else "✗"
                f.write(f"| {m.agent_role} | {m.task_name} | {m.duration_seconds} | {m.estimated_output_tokens} | {status} |\n")
            
            f.write(f"\n## Gesamtergebnis\n\n")
            f.write(f"- **Gesamtdauer:** {result.total_duration_seconds:.2f} Sekunden\n")
            f.write(f"- **Geschaetzte Tokens:** {result.total_estimated_tokens}\n")
            
            if result.error_message:
                f.write(f"\n## Fehler\n\n```\n{result.error_message}\n```\n")
        
        # 5. Crew Output
        output_file = self.output_dir / f"{self.experiment_id}_output.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# Output: {result.config.experiment_name}\n\n")
            f.write(result.crew_output)
        
        print(f"\n📊 Ergebnisse gespeichert in: {self.output_dir}/")
        print(f"   - {self.experiment_id}_full.json (vollstaendige Daten)")
        print(f"   - {self.experiment_id}_metrics.csv (fuer Excel/SPSS)")
        print(f"   - {self.experiment_id}_resources.csv (Ressourcen)")
        print(f"   - {self.experiment_id}_summary.md (Zusammenfassung)")
        print(f"   - {self.experiment_id}_trace.jsonl (Event-Log)")


# ============================================================
# EXPERIMENT RUNNER
# ============================================================

def run_experiment(
    experiment_name: str,
    task_description: str = None,
    models: Dict[str, str] = None,
    output_base_dir: str = "projekte"
) -> ExperimentResult:
    """
    Fuehrt ein vollstaendig getrackte Experiment durch.
    Speichert Spiel UND Metriken im selben Ordner unter projekte/.
    
    Args:
        experiment_name: Name des Experiments (z.B. "01_pokemon_spiel")
        task_description: Optionale eigene Task-Beschreibung
        models: Dict mit Agent-Modell-Zuordnung, z.B.:
                {"product_owner": "mistral:7b", "developer": "codellama:13b"}
        output_base_dir: Basis-Ordner fuer Ergebnisse (default: projekte/)
    
    Returns:
        ExperimentResult mit allen Metriken
    """
    
    # Experiment ID generieren
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_id = f"{experiment_name}_{timestamp}"
    output_dir = Path(output_base_dir) / experiment_id
    
    # Default Modelle
    if models is None:
        models = {
            "product_owner": "mistral:7b",
            "developer": "codellama:13b",
            "qa_engineer": "mistral:7b",
            "technical_writer": "mistral:7b"
        }
    
    # Config erstellen
    config = ExperimentConfig(
        experiment_id=experiment_id,
        experiment_name=experiment_name,
        task_description=task_description or "Snake-Spiel mit GUI",
        models=models
    )
    
    # Tracer initialisieren
    tracer = ExperimentTracer(experiment_id, str(output_dir))
    tracer.start_experiment()
    
    print("=" * 70)
    print(f"🔬 EXPERIMENT: {experiment_name}")
    print(f"   ID: {experiment_id}")
    print(f"   Output: {output_dir}")
    print("=" * 70)
    
    try:
        # LLMs konfigurieren
        product_owner_llm = LLM(
            model=f"ollama/{models['product_owner']}",
            base_url="http://localhost:11434"
        )
        developer_llm = LLM(
            model=f"ollama/{models['developer']}",
            base_url="http://localhost:11434"
        )
        qa_llm = LLM(
            model=f"ollama/{models.get('qa_engineer', models['product_owner'])}",
            base_url="http://localhost:11434"
        )
        writer_llm = LLM(
            model=f"ollama/{models.get('technical_writer', models['product_owner'])}",
            base_url="http://localhost:11434"
        )
        
        # Agenten erstellen
        product_owner = Agent(
            role="Product Owner",
            goal="Klare und praezise Anforderungen fuer Software-Features definieren",
            backstory="Du bist ein erfahrener Product Owner mit tiefem Verstaendnis fuer Nutzerbeduerfnisse.",
            llm=product_owner_llm,
            verbose=True
        )
        
        developer = Agent(
            role="Python Developer",
            goal="VOLLSTAENDIGEN, AUSFUEHRBAREN Python-Code schreiben. Immer kompletten Code ausgeben, nie Platzhalter oder '...' verwenden!",
            backstory="""Du bist ein erfahrener Python-Spieleentwickler mit 10 Jahren Erfahrung.
            
            KRITISCHE REGELN - NIEMALS BRECHEN:
            1. Du schreibst IMMER vollstaendigen, ausfuehrbaren Code
            2. KEINE Platzhalter wie '...' oder 'TODO' oder 'pass'
            3. KEINE Erklaerungen vor oder nach dem Code
            4. Jede Klasse und Funktion ist VOLLSTAENDIG implementiert
            5. Code muss mit 'python datei.py' direkt startbar sein
            6. IMMER 'if __name__ == "__main__":' am Ende
            7. Nur Standardbibliotheken: tkinter, random, json
            8. Bei komplexen Spielen: Mindestens 400 Zeilen Code
            9. Alle Features aus der Spezifikation muessen implementiert sein
            10. Saubere Klassenstruktur mit klaren Verantwortlichkeiten""",
            llm=developer_llm,
            verbose=True
        )
        
        qa_engineer = Agent(
            role="QA Engineer",
            goal="Code gruendlich auf Fehler pruefen und konkrete Fixes vorschlagen",
            backstory="""Du bist ein erfahrener QA-Ingenieur mit scharfem Auge fuer Bugs.
            Pruefe auf: Syntaxfehler, fehlende Imports, Logikfehler, fehlende Funktionen.
            Gib konkrete Code-Fixes an, nicht nur Beschreibungen.""",
            llm=qa_llm,
            verbose=True
        )
        
        technical_writer = Agent(
            role="Technical Writer",
            goal="Klare technische Dokumentation erstellen",
            backstory="Du bist ein erfahrener Technical Writer.",
            llm=writer_llm,
            verbose=True
        )
        
        # Tasks erstellen
        task_desc = config.task_description
        
        define_requirements = Task(
            description=f"""Erstelle eine KURZE, PRAEZISE Spezifikation fuer: {task_desc}
            
            Beschreibe NUR:
            1. Welche Klassen gebraucht werden (Name, Attribute, Methoden)
            2. Welche GUI-Elemente (Buttons, Labels, Canvas)
            3. Spielablauf in 5-10 Stichpunkten
            
            KEINE Code-Beispiele, nur Anforderungen!""",
            expected_output="Kurze Spezifikation mit Klassen und GUI-Elementen",
            agent=product_owner
        )
        
        implement_code = Task(
            description=f"""Schreibe VOLLSTAENDIGEN, AUSFUEHRBAREN Python-Code fuer: {task_desc}
            
            WICHTIGE REGELN:
            1. NUR Python-Code ausgeben, keine Erklaerungen davor oder danach
            2. Code muss mit 'python datei.py' DIREKT starten
            3. Verwende NUR tkinter, random und json (sind bei Python dabei)
            4. IMMER 'if __name__ == "__main__":' am Ende
            5. KEINE Platzhalter wie '...' oder 'pass' oder 'TODO'
            6. JEDE Funktion und Klasse muss vollstaendig implementiert sein
            7. Bei komplexen Spielen: Mindestens 400 Zeilen Code
            8. ALLE Features aus der Spezifikation muessen funktionieren
            9. Teste gedanklich jeden Code-Pfad bevor du ihn schreibst
            
            Beginne direkt mit: import tkinter as tk""",
            expected_output="Vollstaendiger Python-Code (400+ Zeilen fuer komplexe Spiele) der sofort ausfuehrbar ist",
            agent=developer,
            context=[define_requirements]
        )
        
        review_code = Task(
            description="""Pruefe den Code auf diese Fehler:
            1. Fehlende Imports?
            2. Syntaxfehler?
            3. Funktionen die aufgerufen aber nicht definiert sind?
            4. Variablen die nicht existieren?
            5. Ist 'if __name__ == "__main__":' vorhanden?
            
            Gib fuer JEDEN Fehler den korrigierten Code-Ausschnitt an.""",
            expected_output="QA-Report mit konkreten Code-Fixes",
            agent=qa_engineer,
            context=[define_requirements, implement_code]
        )
        
        write_documentation = Task(
            description="Erstelle eine vollstaendige Dokumentation",
            expected_output="Technische Dokumentation in Markdown",
            agent=technical_writer,
            context=[define_requirements, implement_code, review_code]
        )
        
        # Crew erstellen und ausfuehren
        crew = Crew(
            agents=[product_owner, developer, qa_engineer, technical_writer],
            tasks=[define_requirements, implement_code, review_code, write_documentation],
            verbose=True
        )
        
        # Task-Tracking manuell (da CrewAI keine nativen Callbacks hat)
        task_info = [
            ("Product Owner", "define_requirements", models['product_owner']),
            ("Python Developer", "implement_code", models['developer']),
            ("QA Engineer", "review_code", models.get('qa_engineer', models['product_owner'])),
            ("Technical Writer", "write_documentation", models.get('technical_writer', models['product_owner']))
        ]
        
        # Alle Tasks auf einmal tracken (Start)
        experiment_start = time.time()
        
        # Crew ausfuehren
        result = crew.kickoff()
        
        experiment_end = time.time()
        
        # Task-Outputs extrahieren und Metriken erstellen
        if hasattr(result, 'tasks_output'):
            for i, (agent_role, task_name, model) in enumerate(task_info):
                if i < len(result.tasks_output):
                    task_output = result.tasks_output[i]
                    output_text = task_output.raw if hasattr(task_output, 'raw') else str(task_output)
                    
                    # Geschaetzte Dauer (gleichmaessig verteilt als Fallback)
                    task_duration = (experiment_end - experiment_start) / len(task_info)
                    
                    tracer.start_task(agent_role, task_name, model)
                    tracer.current_task_start = experiment_start + (i * task_duration)
                    tracer.end_task(
                        input_text=config.task_description,
                        output_text=output_text,
                        success=True
                    )
        
        tracer.end_experiment()
        
        # Ergebnis zusammenstellen
        total_tokens = sum(m.estimated_output_tokens for m in tracer.agent_metrics)
        
        experiment_result = ExperimentResult(
            config=config,
            agent_metrics=tracer.agent_metrics,
            total_duration_seconds=round(experiment_end - experiment_start, 2),
            total_estimated_tokens=total_tokens,
            system_info=get_system_info(),
            crew_output=str(result),
            individual_task_outputs=tracer.task_outputs,
            success=True
        )
        
        # Speichern
        tracer.save_results(experiment_result)
        
        print("\n" + "=" * 70)
        print("✅ EXPERIMENT ERFOLGREICH ABGESCHLOSSEN")
        print(f"   Dauer: {experiment_result.total_duration_seconds:.2f} Sekunden")
        print(f"   Tokens: ~{total_tokens}")
        print("=" * 70)
        
        return experiment_result
        
    except Exception as e:
        tracer.end_experiment()
        tracer.log("experiment_failed", {"error": str(e)})
        
        experiment_result = ExperimentResult(
            config=config,
            agent_metrics=tracer.agent_metrics,
            total_duration_seconds=time.time() - tracer.start_time,
            total_estimated_tokens=0,
            system_info=get_system_info(),
            crew_output="",
            individual_task_outputs=[],
            success=False,
            error_message=str(e)
        )
        
        tracer.save_results(experiment_result)
        
        print(f"\n❌ EXPERIMENT FEHLGESCHLAGEN: {e}")
        raise


# ============================================================
# BATCH EXPERIMENTS (fuer Vergleichsstudien)
# ============================================================

def run_model_comparison(
    experiment_name: str,
    task_description: str,
    model_configs: List[Dict[str, str]],
    output_base_dir: str = "experiments"
) -> List[ExperimentResult]:
    """
    Fuehrt mehrere Experimente mit verschiedenen Modell-Konfigurationen durch.
    Ideal fuer Vergleichsstudien.
    
    Args:
        experiment_name: Basis-Name fuer alle Experimente
        task_description: Die zu loesende Aufgabe
        model_configs: Liste von Modell-Konfigurationen zum Vergleichen
        output_base_dir: Basis-Ordner fuer alle Ergebnisse
    
    Returns:
        Liste aller ExperimentResults
    """
    results = []
    
    print("=" * 70)
    print(f"🔬 BATCH EXPERIMENT: {experiment_name}")
    print(f"   {len(model_configs)} Konfigurationen zum Testen")
    print("=" * 70)
    
    for i, models in enumerate(model_configs, 1):
        print(f"\n--- Konfiguration {i}/{len(model_configs)} ---")
        print(f"    Modelle: {models}")
        
        try:
            result = run_experiment(
                experiment_name=f"{experiment_name}_config{i}",
                task_description=task_description,
                models=models,
                output_base_dir=output_base_dir
            )
            results.append(result)
            
            # Pause zwischen Experimenten (GPU/RAM abkuehlen lassen)
            if i < len(model_configs):
                print("\n⏳ Warte 10 Sekunden vor naechstem Experiment...")
                time.sleep(10)
                
        except Exception as e:
            print(f"❌ Konfiguration {i} fehlgeschlagen: {e}")
    
    # Vergleichs-Report erstellen
    comparison_file = Path(output_base_dir) / f"{experiment_name}_comparison.md"
    with open(comparison_file, "w", encoding="utf-8") as f:
        f.write(f"# Modell-Vergleich: {experiment_name}\n\n")
        f.write(f"**Task:** {task_description}\n\n")
        f.write(f"**Anzahl Experimente:** {len(results)}\n\n")
        
        f.write("## Ergebnisse\n\n")
        f.write("| Config | Developer Model | Dauer (s) | Tokens | Erfolg |\n")
        f.write("|--------|-----------------|-----------|--------|--------|\n")
        
        for i, r in enumerate(results, 1):
            dev_model = r.config.models.get('developer', 'N/A')
            status = "✓" if r.success else "✗"
            f.write(f"| {i} | {dev_model} | {r.total_duration_seconds} | {r.total_estimated_tokens} | {status} |\n")
    
    print(f"\n📊 Vergleichs-Report: {comparison_file}")
    
    return results


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║           EXPERIMENT RUNNER - Wissenschaftliche Auswertung           ║
╠══════════════════════════════════════════════════════════════════════╣
║  1. Einzelnes Experiment starten                                     ║
║  2. Modell-Vergleich durchfuehren                                    ║
║  3. Beenden                                                          ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    choice = input("Auswahl (1/2/3): ").strip()
    
    if choice == "1":
        name = input("Experiment-Name (z.B. snake_test): ").strip() or "experiment"
        
        print("\nVerfuegbare Vorlagen:")
        print("  1. Snake-Spiel (einfach)")
        print("  2. Pokemon-Diamant RPG (komplex)")
        print("  3. Eigene Beschreibung")
        
        template_choice = input("Vorlage (1/2/3): ").strip() or "1"
        
        if template_choice == "2":
            task = """
POKEMON DIAMANT-INSPIRIERTES RPG-SPIEL
======================================

Erstelle ein vollstaendiges Pokemon-RPG mit tkinter, das folgende Features hat:

=== STARTBILDSCHIRM ===
- Titelbildschirm mit "Pokemon Abenteuer" Logo (ASCII-Art oder Text)
- "Neues Spiel" Button
- Professor beguesst den Spieler und fragt nach seinem Namen
- Auswahl aus 3 Starter-Pokemon:
  * Chelast (Pflanze) - HP: 55, Attacken: Tackle, Rankenhieb, Rasierblatt, Synthese
  * Panflam (Feuer) - HP: 52, Attacken: Kratzer, Glut, Flammenwurf, Ruckzuckhieb  
  * Plinfa (Wasser) - HP: 53, Attacken: Pfund, Blubber, Aquawelle, Schnabel

=== SPIELWELT (Bewegung) ===
- 400x400 Pixel Canvas mit Gras-Tiles (gruene Rechtecke) und Wegen (braun)
- Spieler als rotes Quadrat (oder einfache Figur)
- Steuerung mit WASD oder Pfeiltasten
- Mindestens 3 verschiedene Bereiche:
  * Startstadt (sicherer Bereich, keine Kaempfe)
  * Route 1 (Gras mit wilden Pokemon)
  * Route 2 (staerkere wilde Pokemon)
- Wenn Spieler auf Gras laeuft: 20% Chance auf wildes Pokemon

=== WILDE POKEMON ===
- Mindestens 6 verschiedene wilde Pokemon mit unterschiedlichen Leveln:
  * Staralili (Normal/Flug) - Level 2-4
  * Sheinux (Elektro) - Level 3-5
  * Bidiza (Normal) - Level 2-3
  * Zirpurze (Kaefer) - Level 2-4
  * Knospi (Pflanze) - Level 4-6
  * Ponita (Feuer) - Level 5-7
- Jedes Pokemon hat 4 Attacken

=== KAMPFSYSTEM (Rundenbasiert) ===
- Wechsel zu Kampfbildschirm bei Begegnung
- Anzeige beider Pokemon mit:
  * Namen und Level
  * HP-Balken (gruen/gelb/rot je nach HP)
  * Aktueller HP-Wert
- 4 Buttons fuer Attacken des eigenen Pokemons
- "Flucht" Button (50% Erfolgschance)
- "Pokemon wechseln" Button (wenn mehrere Pokemon)
- Schadensberechnung: Basis-Schaden * Random(0.85-1.0) * Typeneffektivitaet
- Typeneffektivitaet:
  * Feuer > Pflanze > Wasser > Feuer
  * Normal ist neutral gegen alles

=== POKEMON FANGEN ===
- "Pokeball werfen" Button im Kampf
- Fangchance basiert auf HP des Gegners: (1 - gegner_hp/max_hp) * 0.5
- Bei Erfolg: Pokemon wird zum Team hinzugefuegt (max 6 Pokemon)
- Pokeball-Inventar: Starte mit 10 Pokeballs

=== TEAM UND LEVELING ===
- Team-Anzeige (Taste T druecken) zeigt alle eigenen Pokemon
- XP-System: Besiegte Pokemon geben XP = gegner_level * 10
- Level-Up bei XP >= level * 50
- Bei Level-Up: +5 Max-HP, +2 Angriffsstaerke

=== NPC TRAINER ===
- Mindestens 2 NPC-Trainer auf der Map (blaue Quadrate)
- Trainer haben 2-3 Pokemon
- Kampf startet bei Beruehrung
- Trainer geben Geld bei Sieg: trainer_pokemon_count * 100

=== HUD UND MENUES ===
- Oben: Spielername, Geld, Pokeball-Anzahl
- ESC-Menue mit: Team anzeigen, Speichern (in JSON), Beenden
- Gewinn-Bildschirm nach Besiegen aller Trainer

=== TECHNISCHE ANFORDERUNGEN ===
- ALLES in einer einzigen Python-Datei
- NUR tkinter und random (plus json fuer Speichern)
- Mindestens 400 Zeilen Code
- Saubere Klassenstruktur:
  * class Pokemon: name, typ, level, hp, max_hp, attacks, xp
  * class Attack: name, typ, damage
  * class Player: name, team, position, money, pokeballs
  * class GameWorld: canvas, tiles, npcs, wild_pokemon_zones
  * class Battle: player_pokemon, enemy_pokemon, is_trainer_battle
  * class Game: Hauptklasse die alles verbindet
- if __name__ == "__main__": am Ende
"""
            name = "pokemon_diamant_rpg"
        elif template_choice == "3":
            task = input("Task-Beschreibung: ").strip()
        else:
            task = "Snake-Spiel mit tkinter GUI"
        
        run_experiment(
            experiment_name=name,
            task_description=task
        )
        
    elif choice == "2":
        name = input("Experiment-Name (z.B. model_comparison): ").strip() or "comparison"
        task = input("Task-Beschreibung: ").strip() or "Snake-Spiel mit tkinter GUI"
        
        # Verschiedene Modell-Konfigurationen zum Vergleichen
        configs = [
            # Kleine Modelle
            {
                "product_owner": "llama3.2:1b",
                "developer": "qwen2.5-coder:1.5b",
                "qa_engineer": "llama3.2:1b",
                "technical_writer": "llama3.2:1b"
            },
            # Mittlere Modelle
            {
                "product_owner": "llama3.2:3b",
                "developer": "qwen2.5-coder:3b",
                "qa_engineer": "llama3.2:3b",
                "technical_writer": "llama3.2:3b"
            },
            # Grosse Modelle (aktuell verwendet)
            {
                "product_owner": "mistral:7b",
                "developer": "codellama:13b",
                "qa_engineer": "mistral:7b",
                "technical_writer": "mistral:7b"
            }
        ]
        
        print("\nVerfuegbare Konfigurationen:")
        for i, c in enumerate(configs, 1):
            print(f"  {i}. Developer: {c['developer']}")
        
        run_model_comparison(
            experiment_name=name,
            task_description=task,
            model_configs=configs
        )
        
    else:
        print("Beendet.")
