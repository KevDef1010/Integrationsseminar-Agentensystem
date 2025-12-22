"""
Experiment Analyzer - Wissenschaftliche Auswertung
===================================================
Analysiert die Ergebnisse mehrerer Experimente und erstellt:
- Statistische Zusammenfassungen
- Vergleichstabellen
- Diagramme (optional mit matplotlib)
- LaTeX-Tabellen fuer Paper
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass
import statistics


@dataclass
class ExperimentSummary:
    """Zusammenfassung eines Experiments."""
    experiment_id: str
    experiment_name: str
    timestamp: str
    models: Dict[str, str]
    total_duration: float
    total_tokens: int
    success: bool
    agent_durations: Dict[str, float]
    agent_tokens: Dict[str, int]


def load_experiment(experiment_dir: Path) -> ExperimentSummary:
    """Laedt ein Experiment aus dem Ordner."""
    json_files = list(experiment_dir.glob("*_full.json"))
    if not json_files:
        raise FileNotFoundError(f"Keine Experiment-Daten in {experiment_dir}")
    
    with open(json_files[0], "r", encoding="utf-8") as f:
        data = json.load(f)
    
    agent_durations = {}
    agent_tokens = {}
    
    for metric in data.get("agent_metrics", []):
        role = metric["agent_role"]
        agent_durations[role] = metric["duration_seconds"]
        agent_tokens[role] = metric["estimated_output_tokens"]
    
    return ExperimentSummary(
        experiment_id=data["config"]["experiment_id"],
        experiment_name=data["config"]["experiment_name"],
        timestamp=data["config"]["timestamp"],
        models=data["config"]["models"],
        total_duration=data["total_duration_seconds"],
        total_tokens=data["total_estimated_tokens"],
        success=data["success"],
        agent_durations=agent_durations,
        agent_tokens=agent_tokens
    )


def load_all_experiments(base_dir: str = "experiments") -> List[ExperimentSummary]:
    """Laedt alle Experimente aus dem Basis-Ordner."""
    base_path = Path(base_dir)
    if not base_path.exists():
        print(f"⚠️ Ordner {base_dir} existiert nicht.")
        return []
    
    experiments = []
    for exp_dir in sorted(base_path.iterdir()):
        if exp_dir.is_dir():
            try:
                exp = load_experiment(exp_dir)
                experiments.append(exp)
            except Exception as e:
                print(f"⚠️ Konnte {exp_dir.name} nicht laden: {e}")
    
    return experiments


def calculate_statistics(values: List[float]) -> Dict[str, float]:
    """Berechnet statistische Kennzahlen."""
    if not values:
        return {"count": 0}
    
    stats = {
        "count": len(values),
        "mean": round(statistics.mean(values), 2),
        "min": round(min(values), 2),
        "max": round(max(values), 2),
    }
    
    if len(values) > 1:
        stats["std_dev"] = round(statistics.stdev(values), 2)
        stats["median"] = round(statistics.median(values), 2)
    
    return stats


def generate_comparison_report(experiments: List[ExperimentSummary], output_file: str = "analysis_report.md"):
    """Erstellt einen detaillierten Vergleichsreport."""
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Experiment-Analyse Report\n\n")
        f.write(f"**Generiert am:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Anzahl Experimente:** {len(experiments)}\n\n")
        
        # Uebersichtstabelle
        f.write("## Uebersicht aller Experimente\n\n")
        f.write("| # | Name | Developer Model | Dauer (s) | Tokens | Status |\n")
        f.write("|---|------|-----------------|-----------|--------|--------|\n")
        
        for i, exp in enumerate(experiments, 1):
            dev_model = exp.models.get("developer", "N/A")
            status = "✓" if exp.success else "✗"
            f.write(f"| {i} | {exp.experiment_name} | {dev_model} | {exp.total_duration} | {exp.total_tokens} | {status} |\n")
        
        # Statistische Auswertung
        f.write("\n## Statistische Auswertung\n\n")
        
        durations = [e.total_duration for e in experiments if e.success]
        tokens = [e.total_tokens for e in experiments if e.success]
        
        if durations:
            duration_stats = calculate_statistics(durations)
            f.write("### Ausfuehrungszeit (Sekunden)\n\n")
            f.write(f"- **Mittelwert:** {duration_stats['mean']}\n")
            f.write(f"- **Minimum:** {duration_stats['min']}\n")
            f.write(f"- **Maximum:** {duration_stats['max']}\n")
            if 'std_dev' in duration_stats:
                f.write(f"- **Standardabweichung:** {duration_stats['std_dev']}\n")
            f.write("\n")
        
        if tokens:
            token_stats = calculate_statistics([float(t) for t in tokens])
            f.write("### Token-Nutzung (geschaetzt)\n\n")
            f.write(f"- **Mittelwert:** {token_stats['mean']}\n")
            f.write(f"- **Minimum:** {token_stats['min']}\n")
            f.write(f"- **Maximum:** {token_stats['max']}\n")
            f.write("\n")
        
        # Modell-Vergleich
        f.write("## Modell-Vergleich\n\n")
        
        # Gruppiere nach Developer-Modell
        by_model: Dict[str, List[ExperimentSummary]] = {}
        for exp in experiments:
            model = exp.models.get("developer", "unknown")
            if model not in by_model:
                by_model[model] = []
            by_model[model].append(exp)
        
        f.write("| Developer Model | Anzahl | Avg Dauer (s) | Avg Tokens | Erfolgsrate |\n")
        f.write("|-----------------|--------|---------------|------------|-------------|\n")
        
        for model, exps in sorted(by_model.items()):
            successful = [e for e in exps if e.success]
            avg_duration = statistics.mean([e.total_duration for e in successful]) if successful else 0
            avg_tokens = statistics.mean([e.total_tokens for e in successful]) if successful else 0
            success_rate = len(successful) / len(exps) * 100
            
            f.write(f"| {model} | {len(exps)} | {avg_duration:.1f} | {int(avg_tokens)} | {success_rate:.0f}% |\n")
        
        # Agent-Analyse
        f.write("\n## Agent-Analyse\n\n")
        f.write("Durchschnittliche Dauer und Token-Nutzung pro Agent:\n\n")
        
        agent_roles = ["Product Owner", "Python Developer", "QA Engineer", "Technical Writer"]
        
        f.write("| Agent | Avg Dauer (s) | Avg Tokens |\n")
        f.write("|-------|---------------|------------|\n")
        
        for role in agent_roles:
            role_durations = [e.agent_durations.get(role, 0) for e in experiments if e.success]
            role_tokens = [e.agent_tokens.get(role, 0) for e in experiments if e.success]
            
            avg_dur = statistics.mean(role_durations) if role_durations else 0
            avg_tok = statistics.mean(role_tokens) if role_tokens else 0
            
            f.write(f"| {role} | {avg_dur:.1f} | {int(avg_tok)} |\n")
        
        # LaTeX Tabelle
        f.write("\n## LaTeX Tabelle (fuer Paper)\n\n")
        f.write("```latex\n")
        f.write("\\begin{table}[h]\n")
        f.write("\\centering\n")
        f.write("\\caption{Experiment-Ergebnisse}\n")
        f.write("\\begin{tabular}{|l|c|c|c|}\n")
        f.write("\\hline\n")
        f.write("Modell & Dauer (s) & Tokens & Erfolg \\\\\n")
        f.write("\\hline\n")
        
        for exp in experiments:
            dev = exp.models.get("developer", "N/A")
            status = "Ja" if exp.success else "Nein"
            f.write(f"{dev} & {exp.total_duration} & {exp.total_tokens} & {status} \\\\\n")
        
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n")
        f.write("```\n")
    
    print(f"✅ Report gespeichert: {output_file}")


def export_to_csv(experiments: List[ExperimentSummary], output_file: str = "experiments_data.csv"):
    """Exportiert alle Daten als CSV fuer weitere Analyse (Excel, SPSS, R)."""
    
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            "experiment_id",
            "experiment_name", 
            "timestamp",
            "model_product_owner",
            "model_developer",
            "model_qa",
            "model_writer",
            "total_duration_seconds",
            "total_tokens",
            "success",
            "duration_product_owner",
            "duration_developer",
            "duration_qa",
            "duration_writer",
            "tokens_product_owner",
            "tokens_developer",
            "tokens_qa",
            "tokens_writer"
        ])
        
        for exp in experiments:
            writer.writerow([
                exp.experiment_id,
                exp.experiment_name,
                exp.timestamp,
                exp.models.get("product_owner", ""),
                exp.models.get("developer", ""),
                exp.models.get("qa_engineer", ""),
                exp.models.get("technical_writer", ""),
                exp.total_duration,
                exp.total_tokens,
                1 if exp.success else 0,
                exp.agent_durations.get("Product Owner", 0),
                exp.agent_durations.get("Python Developer", 0),
                exp.agent_durations.get("QA Engineer", 0),
                exp.agent_durations.get("Technical Writer", 0),
                exp.agent_tokens.get("Product Owner", 0),
                exp.agent_tokens.get("Python Developer", 0),
                exp.agent_tokens.get("QA Engineer", 0),
                exp.agent_tokens.get("Technical Writer", 0)
            ])
    
    print(f"✅ CSV exportiert: {output_file}")


def generate_charts(experiments: List[ExperimentSummary], output_dir: str = "charts"):
    """Erstellt Diagramme (benoetigt matplotlib)."""
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Fuer Server ohne Display
    except ImportError:
        print("⚠️ matplotlib nicht installiert. Installieren mit: pip install matplotlib")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Balkendiagramm: Dauer pro Modell
    by_model = {}
    for exp in experiments:
        model = exp.models.get("developer", "unknown")
        if model not in by_model:
            by_model[model] = []
        if exp.success:
            by_model[model].append(exp.total_duration)
    
    models = list(by_model.keys())
    avg_durations = [statistics.mean(by_model[m]) if by_model[m] else 0 for m in models]
    
    plt.figure(figsize=(10, 6))
    plt.bar(models, avg_durations, color='steelblue')
    plt.xlabel('Developer Modell')
    plt.ylabel('Durchschnittliche Dauer (Sekunden)')
    plt.title('Ausfuehrungszeit nach Modell')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/duration_by_model.png", dpi=150)
    plt.close()
    
    # 2. Balkendiagramm: Tokens pro Agent
    agent_roles = ["Product Owner", "Python Developer", "QA Engineer", "Technical Writer"]
    avg_tokens = []
    
    for role in agent_roles:
        role_tokens = [e.agent_tokens.get(role, 0) for e in experiments if e.success]
        avg_tokens.append(statistics.mean(role_tokens) if role_tokens else 0)
    
    plt.figure(figsize=(10, 6))
    plt.bar(agent_roles, avg_tokens, color=['#2ecc71', '#3498db', '#e74c3c', '#9b59b6'])
    plt.xlabel('Agent')
    plt.ylabel('Durchschnittliche Tokens')
    plt.title('Token-Nutzung pro Agent')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/tokens_by_agent.png", dpi=150)
    plt.close()
    
    print(f"✅ Diagramme erstellt in: {output_dir}/")


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║              EXPERIMENT ANALYZER - Wissenschaftliche Analyse         ║
╠══════════════════════════════════════════════════════════════════════╣
║  1. Alle Experimente analysieren                                     ║
║  2. CSV exportieren (fuer Excel/SPSS)                                ║
║  3. Diagramme erstellen (benoetigt matplotlib)                       ║
║  4. Alles ausfuehren                                                 ║
║  5. Beenden                                                          ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    base_dir = input("Experiment-Ordner (Enter fuer 'experiments'): ").strip() or "experiments"
    
    experiments = load_all_experiments(base_dir)
    
    if not experiments:
        print("Keine Experimente gefunden.")
        exit()
    
    print(f"\n📊 {len(experiments)} Experimente gefunden.\n")
    
    choice = input("Auswahl (1-5): ").strip()
    
    if choice == "1":
        generate_comparison_report(experiments)
    elif choice == "2":
        export_to_csv(experiments)
    elif choice == "3":
        generate_charts(experiments)
    elif choice == "4":
        generate_comparison_report(experiments)
        export_to_csv(experiments)
        generate_charts(experiments)
    else:
        print("Beendet.")
