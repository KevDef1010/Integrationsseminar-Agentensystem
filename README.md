# ��� Multi-Agent KI-Demo mit CrewAI

> **4 KI-Agenten arbeiten zusammen, um Code zu schreiben** - alles lokal auf deinem PC!

## Was macht das Projekt?

Dieses Projekt zeigt, wie mehrere KI-Agenten wie ein echtes Entwicklerteam zusammenarbeiten:

1.  **Product Owner** - Schreibt die Anforderungen
2.  **Developer** - Programmiert den Code  
3.  **QA Engineer** - Findet Bugs und Fehler
4.  **Technical Writer** - Schreibt die Dokumentation

**Das Besondere:** Alles läuft LOKAL auf deinem Computer - keine Cloud, kein API-Key nötig!

---

## ��� Schnellstart (5 Minuten)

### Schritt 1: Ollama installieren

Gehe zu **https://ollama.ai** und lade den Installer herunter.

Nach der Installation: Öffne ein **neues Terminal** und teste:
```bash
ollama --version
```

### Schritt 2: KI-Modelle herunterladen

```bash
ollama pull mistral:7b
ollama pull codellama:13b
```
⚠️ **Achtung:** Das dauert ein paar Minuten und braucht ca. 12 GB Speicherplatz!

### Schritt 3: Repository klonen

```bash
git clone https://github.com/DEIN_USERNAME/integrationsseminar.git
cd integrationsseminar
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

### Schritt 5: Starten! ���

```bash
python multi_agent_crew.py
```

Die Ergebnisse findest du danach im Ordner `output/`.

---

## ❓ Häufige Probleme

### "ollama: command not found"
→ Öffne ein **neues Terminal** nach der Ollama-Installation

### "No space left on device"
→ Du brauchst ca. 12 GB freien Speicherplatz für die Modelle

### Es dauert sehr lange
→ Normal! Die großen Modelle (7B, 13B) brauchen Zeit. Beim ersten Start werden auch Caches erstellt.

### Mein PC ist zu langsam
→ Benutze kleinere Modelle! Ändere in `multi_agent_crew.py`:
```python
# Statt mistral:7b und codellama:13b
model="ollama/llama3.2:1b"      # Kleiner, schneller
model="ollama/qwen2.5-coder:1.5b"  # Gut für Code
```

---

## ��� Projektstruktur

```
integrationsseminar/
├── multi_agent_crew.py   ← Das Hauptskript (hier sind die Agenten definiert)
├── README.md             ← Diese Anleitung
├── .gitignore
└── output/               ← Hier landen die Ergebnisse
    ├── ergebnis.md       ← Generierter Code + QA-Report
    └── dokumentation.md  ← Technische Dokumentation
```

---

## ��� Anpassen

Du kannst das Projekt einfach anpassen:

### Andere Aufgabe stellen
Ändere die Task-Beschreibungen in `multi_agent_crew.py`:
```python
define_requirements = Task(
    description="""Erstelle eine User Story für DEINE_IDEE...""",
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

Verfügbare Modelle siehst du mit: `ollama list`

---

## ��� Voraussetzungen

- **Python 3.12+**
- **Ollama** installiert
- **16 GB RAM** empfohlen (8 GB geht auch mit kleineren Modellen)
- **12 GB Festplatte** für die KI-Modelle

---

## ���️ Verwendete Technologien

| Tool | Was es macht |
|------|--------------|
| [CrewAI](https://crewai.com/) | Framework für Multi-Agent Systeme |
| [Ollama](https://ollama.ai/) | Führt KI-Modelle lokal aus |
| [Mistral 7B](https://mistral.ai/) | Starkes allgemeines Sprachmodell |
| [CodeLlama 13B](https://ai.meta.com/llama/) | Spezialisiert auf Code |

---

## ��� Lizenz

MIT - Mach damit was du willst!

---

**Fragen?** Erstelle ein Issue oder frag deinen Dozenten ���
