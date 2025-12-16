"""
CrewAI Multi-Agent Demo mit verschiedenen Ollama-Modellen

- Product Owner: mistral:7b - definiert Anforderungen
- Developer: codellama:13b - implementiert Code
- QA Engineer: mistral:7b - prüft Code auf Fehler und nimmt ab
- Technical Writer: mistral:7b - erstellt Dokumentation
"""

from crewai import Agent, Task, Crew, LLM

# Ollama LLMs konfigurieren
product_owner_llm = LLM(
    model="ollama/mistral:7b",
    base_url="http://localhost:11434"
)

developer_llm = LLM(
    model="ollama/codellama:13b",
    base_url="http://localhost:11434"
)

qa_llm = LLM(
    model="ollama/mistral:7b",
    base_url="http://localhost:11434"
)

writer_llm = LLM(
    model="ollama/mistral:7b",
    base_url="http://localhost:11434"
)

# Agent 1: Product Owner
product_owner = Agent(
    role="Product Owner",
    goal="Klare und präzise Anforderungen für Software-Features definieren",
    backstory="""Du bist ein erfahrener Product Owner mit tiefem Verständnis 
    für Nutzerbedürfnisse. Du formulierst klare User Stories und Akzeptanzkriterien.""",
    llm=product_owner_llm,
    verbose=True
)

# Agent 2: Developer
developer = Agent(
    role="Python Developer",
    goal="Sauberen, funktionalen Python-Code schreiben der die Anforderungen erfüllt",
    backstory="""Du bist ein erfahrener Python-Entwickler der best practices 
    befolgt und gut dokumentierten Code schreibt.""",
    llm=developer_llm,
    verbose=True
)

# Agent 3: QA Engineer
qa_engineer = Agent(
    role="QA Engineer",
    goal="Code gründlich auf Fehler, Bugs und Qualitätsprobleme prüfen und abnehmen",
    backstory="""Du bist ein erfahrener Qualitätssicherungs-Ingenieur mit einem 
    scharfen Auge für Bugs, Edge Cases und Code-Qualität. Du prüfst Code auf:
    - Syntaxfehler
    - Logikfehler
    - Fehlende Fehlerbehandlung
    - Code-Style und Best Practices
    - Vollständigkeit der Dokumentation
    Du gibst konstruktives Feedback und eine klare Abnahme-Entscheidung.""",
    llm=qa_llm,
    verbose=True
)

# Agent 4: Technical Writer
technical_writer = Agent(
    role="Technical Writer",
    goal="Klare, vollständige und benutzerfreundliche technische Dokumentation erstellen",
    backstory="""Du bist ein erfahrener Technical Writer der komplexe Software 
    verständlich dokumentiert. Du erstellst:
    - README mit Projektübersicht
    - Installationsanleitung
    - API-Dokumentation mit Beispielen
    - Anwendungsbeispiele
    Deine Dokumentation ist klar strukturiert und für Entwickler leicht verständlich.""",
    llm=writer_llm,
    verbose=True
)

# Task 1: Anforderungen definieren
define_requirements = Task(
    description="""Erstelle eine detaillierte User Story für ein Task-Management-System (To-Do App).
    
    Das System soll folgende Features haben:
    - Tasks erstellen, bearbeiten, löschen
    - Tasks mit Priorität (hoch/mittel/niedrig) versehen
    - Tasks mit Deadline versehen
    - Tasks als erledigt markieren
    - Tasks nach Priorität oder Deadline sortieren
    - Tasks in Kategorien organisieren
    
    Definiere:
    - User Stories im Format "Als... möchte ich... damit..."
    - Mindestens 5 Akzeptanzkriterien
    - Datenstruktur für Tasks
    - Welche Methoden die API haben soll""",
    expected_output="Detaillierte User Stories mit Akzeptanzkriterien und API-Spezifikation",
    agent=product_owner
)

# Task 2: Code implementieren
implement_code = Task(
    description="""Basierend auf den Anforderungen des Product Owners, 
    implementiere ein vollständiges Task-Management-System in Python.
    
    WICHTIG: Schreibe ECHTEN, AUSFÜHRBAREN Python-Code!
    
    Der Code MUSS enthalten:
    1. Eine Task-Klasse mit:
       - id, title, description, priority, deadline, completed, category
       - __init__, __str__, to_dict Methoden
    
    2. Eine TaskManager-Klasse mit:
       - add_task(title, priority, deadline, category)
       - get_task(task_id)
       - update_task(task_id, **kwargs)
       - delete_task(task_id)
       - complete_task(task_id)
       - get_all_tasks()
       - get_tasks_by_priority(priority)
       - get_tasks_by_category(category)
       - sort_by_priority()
       - sort_by_deadline()
    
    3. Fehlerbehandlung für ungültige Eingaben
    
    4. Am Ende: Beispielcode der zeigt wie man das System verwendet
    
    Gib den KOMPLETTEN Python-Code aus, nicht nur eine Beschreibung!""",
    expected_output="Vollständiger, ausführbarer Python-Code mit allen Klassen und Beispielnutzung",
    agent=developer,
    context=[define_requirements]
)

# Task 3: Code Review und Abnahme
review_code = Task(
    description="""Prüfe den vom Developer erstellten Code gründlich:
    
    1. **Funktionalität**: Erfüllt der Code alle Anforderungen des Product Owners?
    2. **Fehlerbehandlung**: Werden alle Edge Cases abgedeckt?
       - Ungültige Prioritäten
       - Leere Task-Titel
       - Deadlines in der Vergangenheit
       - Nicht existierende Task-IDs
    3. **Code-Qualität**: 
       - Ist der Code sauber und lesbar?
       - Werden Best Practices befolgt?
       - Sind Type Hints korrekt?
    4. **Dokumentation**: Sind alle Klassen und Methoden dokumentiert?
    5. **Bugs**: Gibt es offensichtliche Fehler oder Probleme?
    
    Erstelle einen detaillierten QA-Bericht mit:
    - Liste aller gefundenen Probleme mit Schweregrad (kritisch/mittel/niedrig)
    - Konkrete Verbesserungsvorschläge mit Code-Beispielen
    - Finale Abnahme-Entscheidung (APPROVED / REJECTED mit Begründung)""",
    expected_output="Detaillierter QA-Bericht mit Problembeschreibungen und Abnahme-Entscheidung",
    agent=qa_engineer,
    context=[define_requirements, implement_code]
)

# Task 4: Dokumentation erstellen
write_documentation = Task(
    description="""Erstelle eine vollständige technische Dokumentation für das Task-Management-System.
    
    Die Dokumentation soll enthalten:
    
    1. **Projektübersicht**
       - Was macht das System?
       - Hauptfeatures
    
    2. **Installation**
       - Voraussetzungen
       - Installationsschritte
    
    3. **API-Dokumentation**
       - Alle Klassen mit ihren Attributen
       - Alle Methoden mit Parametern und Rückgabewerten
       - Exceptions die geworfen werden können
    
    4. **Anwendungsbeispiele**
       - Task erstellen
       - Tasks filtern und sortieren
       - Tasks verwalten
    
    5. **Best Practices**
       - Tipps zur Verwendung
    
    Formatiere alles in Markdown.""",
    expected_output="Vollständige Markdown-Dokumentation",
    agent=technical_writer,
    context=[define_requirements, implement_code, review_code]
)

# Crew erstellen
crew = Crew(
    agents=[product_owner, developer, qa_engineer, technical_writer],
    tasks=[define_requirements, implement_code, review_code, write_documentation],
    verbose=True
)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starte Multi-Agent Crew mit Ollama")
    print("   Product Owner: mistral:7b")
    print("   Developer: codellama:13b")
    print("   QA Engineer: mistral:7b")
    print("   Technical Writer: mistral:7b")
    print("=" * 60)
    
    result = crew.kickoff()
    
    print("\n" + "=" * 60)
    print("📋 ENDERGEBNIS:")
    print("=" * 60)
    print(result)
    
    # Ergebnisse in separate Dateien speichern
    # Code in ergebnis.md
    with open("ergebnis.md", "w", encoding="utf-8") as f:
        f.write("# Task-Management-System - Code & QA Report\n\n")
        f.write("## Generiert von CrewAI Multi-Agent System\n\n")
        f.write("### Agenten:\n")
        f.write("- Product Owner: mistral:7b\n")
        f.write("- Developer: codellama:13b\n")
        f.write("- QA Engineer: mistral:7b\n")
        f.write("- Technical Writer: mistral:7b\n\n")
        f.write("---\n\n")
        f.write(str(result))
    print("\n✅ Code & QA-Report wurde in 'ergebnis.md' gespeichert!")
    
    # Dokumentation separat speichern (aus Task 4)
    if hasattr(result, 'tasks_output') and len(result.tasks_output) >= 4:
        doc_output = result.tasks_output[3].raw
        with open("dokumentation.md", "w", encoding="utf-8") as f:
            f.write(doc_output)
        print("✅ Dokumentation wurde in 'dokumentation.md' gespeichert!")
    else:
        # Fallback: Gesamtergebnis auch als Dokumentation
        with open("dokumentation.md", "w", encoding="utf-8") as f:
            f.write("# Task-Management-System - Dokumentation\n\n")
            f.write(str(result))
        print("✅ Dokumentation wurde in 'dokumentation.md' gespeichert!")
