# Multi-Agent KI-Demo mit CrewAI

> **4 KI-Agenten arbeiten zusammen, um Code zu schreiben** - alles lokal auf deinem PC!

## Was macht das Projekt?

Dieses Projekt zeigt, wie mehrere KI-Agenten wie ein echtes Entwicklerteam zusammenarbeiten:

1. **Product Owner** - Schreibt die Anforderungen
2. **Developer** - Programmiert den Code  
3. **QA Engineer** - Findet Bugs und Fehler
4. **Technical Writer** - Schreibt die Dokumentation

**Das Besondere:** Alles läuft LOKAL auf deinem Computer - keine Cloud, kein API-Key nötig!

---

## Schnellstart (5 Minuten)

### Schritt 1: Ollama installieren

Gehe zu **https://ollama.ai** und lade den Installer herunter.

Nach der Installation: Oeffne ein **neues Terminal** und teste:
```bash
ollama --version
```

### Schritt 2: KI-Modelle herunterladen

```bash
ollama pull mistral:7b
ollama pull codellama:13b
```
**Achtung:** Das dauert ein paar Minuten und braucht ca. 12 GB Speicherplatz!

### Schritt 3: Repository klonen

```bash
git clone https://github.com/KevDef1010/Integrationsseminar-Agentensystem.git
cd Integrationsseminar-Agentensystem
```

### Schritt 4: Python Environment einrichten

**Option A: Mit UV (empfohlen)**
```bash
# UV installieren (falls noch nicht vorhanden)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Environment erstellen
uv venv --python 3.12
source .venv/Scripts/activate   # Windows Git Bash
# source .venv/bin/activate     # Linux/Mac

# Pakete installieren
uv pip install crewai litellm
```

**Option B: Mit normalem pip**
```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash
# source .venv/bin/activate     # Linux/Mac

pip install crewai litellm
```

### Schritt 5: Starten!

```bash
python multi_agent_crew.py
```

Die Ergebnisse findest du danach im Ordner `output/`.

---

## Haeufige Probleme

### "ollama: command not found"
Oeffne ein **neues Terminal** nach der Ollama-Installation

### "No space left on device"
Du brauchst ca. 12 GB freien Speicherplatz fuer die Modelle

### Es dauert sehr lange
Normal! Die grossen Modelle (7B, 13B) brauchen Zeit. Beim ersten Start werden auch Caches erstellt.

### Mein PC ist zu langsam
Benutze kleinere Modelle! Aendere in `multi_agent_crew.py`:
```python
# Statt mistral:7b und codellama:13b
model="ollama/llama3.2:1b"      # Kleiner, schneller
model="ollama/qwen2.5-coder:1.5b"  # Gut fuer Code
```

---

## Projektstruktur

```
Integrationsseminar-Agentensystem/
├── multi_agent_crew.py   <- Das Hauptskript (hier sind die Agenten definiert)
├── README.md             <- Diese Anleitung
├── requirements.txt      <- Python Abhaengigkeiten
├── LICENSE               <- MIT Lizenz
├── .gitignore
└── projekte/             <- Hier landen die generierten Projekte
    └── 01_snake_spiel/   <- Beispielprojekt
        ├── snake_game.py     <- Das Spiel (ausfuehrbar)
        ├── ergebnis.md       <- Generierter Code + QA-Report
        ├── dokumentation.md  <- Technische Dokumentation
        └── README.md         <- Projekt-Info
```

Beim Starten wirst du nach einem Projektnamen gefragt (z.B. `02_calculator`).

---

## Anpassen

Du kannst das Projekt einfach anpassen:

### Andere Aufgabe stellen
Aendere die Task-Beschreibungen in `multi_agent_crew.py`:
```python
define_requirements = Task(
    description="""Erstelle eine User Story fuer DEINE_IDEE...""",
    ...
)
```

### Andere Modelle verwenden
```python
developer_llm = LLM(
    model="ollama/MODELL_NAME",  # z.B. "ollama/llama3.2:3b"
    base_url="http://localhost:11434"
)
```

Verfuegbare Modelle siehst du mit: `ollama list`

---

## Voraussetzungen

- **Python 3.12+**
- **Ollama** installiert
- **16 GB RAM** empfohlen (8 GB geht auch mit kleineren Modellen)
- **12 GB Festplatte** fuer die KI-Modelle

---

## Verwendete Technologien

| Tool | Was es macht |
|------|--------------|
| [CrewAI](https://crewai.com/) | Framework fuer Multi-Agent Systeme |
| [Ollama](https://ollama.ai/) | Fuehrt KI-Modelle lokal aus |
| [Mistral 7B](https://mistral.ai/) | Starkes allgemeines Sprachmodell |
| [CodeLlama 13B](https://ai.meta.com/llama/) | Spezialisiert auf Code |

---

## KI-Modelle im Ueberblick

### In diesem Projekt verwendete Modelle

| Modell | Agent | Parameter | Groesse | RAM-Bedarf | Staerke |
|--------|-------|-----------|---------|------------|---------|
| mistral:7b | Product Owner, QA, Writer | 7.24B | 4.1 GB | 8 GB | Allrounder, gut fuer Text |
| codellama:13b | Developer | 13B | 7.4 GB | 16 GB | Spezialisiert auf Code |

### Alternative Modelle (fuer schwaeachere PCs)

| Modell | Parameter | Groesse | RAM-Bedarf | Empfehlung |
|--------|-----------|---------|------------|------------|
| llama3.2:1b | 1B | 1.3 GB | 4 GB | Sehr schnell, einfache Aufgaben |
| llama3.2:3b | 3B | 2.0 GB | 6 GB | Guter Kompromiss |
| qwen2.5-coder:1.5b | 1.5B | 986 MB | 4 GB | Gut fuer Code, sehr klein |
| qwen2.5-coder:3b | 3B | 1.9 GB | 6 GB | Besser fuer Code |
| qwen2.5-coder:7b | 7B | 4.7 GB | 10 GB | Sehr gut fuer Code |
| phi3:mini | 3.8B | 2.2 GB | 6 GB | Microsoft, schnell |
| gemma2:2b | 2B | 1.6 GB | 4 GB | Google, effizient |

### Grosse Modelle (fuer starke PCs)

| Modell | Parameter | Groesse | RAM-Bedarf | Empfehlung |
|--------|-----------|---------|------------|------------|
| llama3.1:8b | 8B | 4.7 GB | 10 GB | Meta, sehr gut |
| mistral:7b-instruct | 7B | 4.1 GB | 8 GB | Gut fuer Anweisungen |
| codellama:34b | 34B | 19 GB | 40 GB | Bester Code, braucht viel RAM |
| deepseek-coder:6.7b | 6.7B | 3.8 GB | 8 GB | Sehr gut fuer Code |
| mixtral:8x7b | 47B | 26 GB | 48 GB | Top-Qualitaet, sehr gross |

### Modell herunterladen

```bash
ollama pull MODELLNAME
# Beispiele:
ollama pull llama3.2:3b
ollama pull qwen2.5-coder:7b
```

### Installierte Modelle anzeigen

```bash
ollama list
```

---

## Lizenz

MIT - Mach damit was du willst!

---

**Fragen?** Erstelle ein Issue oder frag deinen Dozenten
