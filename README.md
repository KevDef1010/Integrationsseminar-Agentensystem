# 🤖 Multi-Agent CrewAI Demo

Ein Demonstrationsprojekt für **Multi-Agent Systeme** mit [CrewAI](https://crewai.com/) und lokalen [Ollama](https://ollama.ai/) LLMs.

## 📋 Projektübersicht

Dieses Projekt zeigt, wie mehrere KI-Agenten zusammenarbeiten können, um Software zu entwickeln:

| Agent | Modell | Aufgabe |
|-------|--------|---------|
| 🎯 **Product Owner** | Mistral 7B | Definiert User Stories & Anforderungen |
| 💻 **Developer** | CodeLlama 13B | Implementiert den Code |
| 🔍 **QA Engineer** | Mistral 7B | Code Review & Qualitätssicherung |
| 📝 **Technical Writer** | Mistral 7B | Erstellt Dokumentation |

## 🚀 Features

- **Lokale LLMs**: Alle Modelle laufen lokal über Ollama - keine Cloud-API nötig
- **Multi-Agent Workflow**: Agenten arbeiten sequentiell zusammen
- **Automatische Code-Generierung**: Vom Requirement zum fertigen Code
- **QA-Prozess**: Automatische Code-Reviews mit Fehleranalyse
- **Dokumentation**: Automatisch generierte technische Dokumentation

## 📦 Installation

### Voraussetzungen

- Python 3.12+
- [Ollama](https://ollama.ai/) installiert
- Ausreichend RAM (mind. 16 GB empfohlen für 13B Modelle)

### Setup

```bash
# 1. Repository klonen
git clone https://github.com/DEIN_USERNAME/integrationsseminar.git
cd integrationsseminar

# 2. Virtual Environment erstellen
uv venv --python 3.12
source .venv/Scripts/activate  # Windows/Git Bash
# oder: source .venv/bin/activate  # Linux/Mac

# 3. Abhängigkeiten installieren
uv pip install crewai litellm

# 4. Ollama Modelle herunterladen
ollama pull mistral:7b
ollama pull codellama:13b
```

## 🎮 Verwendung

```bash
# Virtual Environment aktivieren
source .venv/Scripts/activate

# Crew starten
python multi_agent_crew.py
```

Die Ergebnisse werden in folgenden Dateien gespeichert:
- `ergebnis.md` - Generierter Code & QA-Report
- `dokumentation.md` - Technische Dokumentation

## 📁 Projektstruktur

```
integrationsseminar/
├── multi_agent_crew.py    # Hauptskript mit Agent-Definitionen
├── ergebnis.md            # Generierter Code & QA-Report
├── dokumentation.md       # Technische Dokumentation
├── README.md              # Diese Datei
└── .venv/                 # Virtual Environment
```

## 🔧 Konfiguration

### Andere Modelle verwenden

Du kannst die Modelle in `multi_agent_crew.py` anpassen:

```python
# Beispiel: Kleinere Modelle für weniger RAM
product_owner_llm = LLM(
    model="ollama/llama3.2:1b",
    base_url="http://localhost:11434"
)
```

### Verfügbare Ollama Modelle

| Modell | Größe | RAM |
|--------|-------|-----|
| `llama3.2:1b` | ~1.3 GB | ~4 GB |
| `qwen2.5-coder:1.5b` | ~1 GB | ~4 GB |
| `mistral:7b` | ~4.1 GB | ~8 GB |
| `codellama:13b` | ~7.4 GB | ~16 GB |

## 📊 Beispiel-Output

Das System generiert automatisch:

1. **User Stories** vom Product Owner
2. **Python Code** vom Developer (z.B. Flask REST API)
3. **QA-Report** mit gefundenen Problemen
4. **Dokumentation** mit API-Beschreibung

## 🛠️ Technologien

- [CrewAI](https://crewai.com/) - Multi-Agent Framework
- [Ollama](https://ollama.ai/) - Lokale LLM Runtime
- [LiteLLM](https://github.com/BerriAI/litellm) - LLM API Wrapper
- [UV](https://github.com/astral-sh/uv) - Schneller Python Package Manager

## 📄 Lizenz

MIT License

## 👤 Autor

Erstellt für das Integrationsseminar 2025
