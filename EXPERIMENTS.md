# Wissenschaftliches Monitoring & Tracing

Dieses Modul ermoeglicht die systematische Durchfuehrung und Auswertung von Multi-Agent Experimenten fuer wissenschaftliche Arbeiten.

## Schnellstart

```bash
# Einzelnes Experiment ausfuehren
python experiment_runner.py

# Ergebnisse analysieren
python experiment_analyzer.py
```

## Was wird getrackt?

### Pro Experiment
- **Ausfuehrungszeit** (gesamt und pro Agent)
- **Token-Nutzung** (geschaetzt: ~4 Zeichen = 1 Token)
- **Systemressourcen** (CPU, RAM vor/nach jedem Task)
- **Alle Zwischenergebnisse** (Output jedes Agents)
- **Erfolg/Fehlschlag** mit Fehlerdetails

### Systeminfo (fuer Reproduzierbarkeit)
- Betriebssystem, Version
- Python-Version
- CPU-Kerne, RAM
- Hostname, Timestamp

## Output-Dateien

Nach jedem Experiment in `experiments/EXPERIMENT_ID/`:

| Datei | Inhalt | Verwendung |
|-------|--------|------------|
| `*_full.json` | Alle Daten | Programmatische Auswertung |
| `*_metrics.csv` | Agent-Metriken | Excel, SPSS, R |
| `*_resources.csv` | CPU/RAM Snapshots | Ressourcen-Analyse |
| `*_summary.md` | Zusammenfassung | Schneller Ueberblick |
| `*_trace.jsonl` | Event-Log | Detaillierte Nachverfolgung |
| `*_output.md` | Generierter Code | Qualitaets-Bewertung |

## Modell-Vergleich

Fuer systematische Vergleiche verschiedener Modelle:

```bash
python experiment_runner.py
# Option 2 waehlen: "Modell-Vergleich durchfuehren"
```

Vergleicht automatisch:
1. **Kleine Modelle** (llama3.2:1b, qwen2.5-coder:1.5b)
2. **Mittlere Modelle** (llama3.2:3b, qwen2.5-coder:3b)
3. **Grosse Modelle** (mistral:7b, codellama:13b)

## Analyse

```bash
python experiment_analyzer.py
```

Erstellt:
- **Markdown Report** mit Statistiken
- **CSV Export** fuer Excel/SPSS/R
- **Diagramme** (PNG)
- **LaTeX Tabelle** fuer Paper

## Beispiel: Forschungsfrage

> "Wie wirkt sich die Modellgroesse auf die Code-Qualitaet und Ausfuehrungszeit aus?"

### Vorgehen:
1. Gleiche Aufgabe mit verschiedenen Modellen durchfuehren
2. Metriken automatisch tracken
3. Ergebnisse analysieren
4. Diagramme fuer Paper generieren

### Metriken:
- **Quantitativ:** Dauer, Token-Anzahl, Erfolgsrate
- **Qualitativ:** Code-Laenge, Anzahl Klassen/Funktionen (manuell)

## Eigene Konfiguration

In `experiment_runner.py` anpassen:

```python
# Eigene Modell-Konfigurationen
configs = [
    {
        "product_owner": "llama3.2:1b",
        "developer": "qwen2.5-coder:7b",  # Nur Developer gross
        "qa_engineer": "llama3.2:1b",
        "technical_writer": "llama3.2:1b"
    },
    # weitere Konfigurationen...
]
```

## Tipps

1. **Mehrere Durchlaeufe** pro Konfiguration fuer statistische Signifikanz
2. **Gleiche Hardware** fuer alle Experimente
3. **Pausen** zwischen Experimenten (GPU abkuehlen lassen)
4. **Baseline** definieren (z.B. grösste Modelle)
