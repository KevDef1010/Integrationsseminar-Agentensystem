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

# Agent 5: 2. developer
developer2 = Agent(
    role="Senior Python Developer",
    goal="Komplexe Softwarearchitekturen entwerfen und implementieren",
    backstory="""Du bist ein erfahrener Senior Python Developer mit umfangreicher 
    Erfahrung in der Entwicklung von skalierbaren Anwendungen. Du arbeitest eng 
    mit dem Product Owner zusammen, um technische Lösungen zu entwerfen und 
    umzusetzen.""",
    llm=developer_llm,
    verbose=True
)

# Task 1: Anforderungen definieren
define_requirements = Task(
    description="""Erstelle eine detaillierte Spezifikation für ein einfaches Snake-Spiel mit GUI.
    
    Das Spiel soll folgende Features haben:
    - Snake die sich mit Pfeiltasten steuern lässt
    - Essen das zufällig erscheint
    - Snake wächst wenn sie Essen frisst
    - Punktestand der angezeigt wird
    - Game Over wenn Snake sich selbst oder die Wand trifft
    - Neustart-Möglichkeit
    
    Definiere:
    - Spielmechanik und Regeln
    - Welche Klassen gebraucht werden (Snake, Food, Game)
    - Welche Bibliothek für die GUI (tkinter - ist bei Python dabei!)
    - Tastatursteuerung""",
    expected_output="Detaillierte Spielspezifikation mit Klassen und Mechanik",
    agent=product_owner
)

# Task 2: Code implementieren
implement_code = Task(
    description="""Basierend auf den Anforderungen des Product Owners, 
    implementiere ein vollständiges Snake-Spiel in Python mit tkinter GUI.
    
    WICHTIG: Schreibe ECHTEN, AUSFÜHRBAREN Python-Code!
    
    Der Code MUSS enthalten:
    1. Imports: nur tkinter und random (sind bei Python dabei!)
    
    2. Eine Game-Klasse mit:
       - Canvas für das Spielfeld
       - Snake als Liste von Koordinaten
       - Food Position
       - Score Anzeige
       - Game Loop mit after()
    
    3. Steuerung:
       - Pfeiltasten für Richtungswechsel
       - Leertaste oder Button für Neustart
    
    4. Spiellogik:
       - Kollisionserkennung (Wand und Selbst)
       - Essen einsammeln und wachsen
       - Score erhöhen
    
    5. Am Ende: if __name__ == "__main__": um das Spiel zu starten
    
    Gib den KOMPLETTEN, AUSFÜHRBAREN Python-Code aus!
    Das Spiel muss mit "python spiel.py" direkt starten!""",
    expected_output="Vollständiger, ausführbarer Python-Code für Snake-Spiel mit tkinter",
    agent=developer,
    context=[define_requirements]
)

# Task 3: Code Review und Abnahme
review_code = Task(
    description="""Prüfe den vom Developer erstellten Snake-Spiel Code gründlich:
    
    1. **Funktionalität**: Läuft das Spiel? Funktioniert die Steuerung?
    2. **Fehlerbehandlung**: 
       - Was passiert bei Game Over?
       - Kann man neu starten?
    3. **Code-Qualität**: 
       - Ist der Code sauber und lesbar?
       - Sind die Klassen sinnvoll strukturiert?
    4. **Spielbarkeit**: Macht das Spiel Spass?
    5. **Bugs**: Gibt es offensichtliche Fehler?
    
    Erstelle einen QA-Bericht mit:
    - Gefundene Probleme
    - Verbesserungsvorschläge
    - Finale Abnahme-Entscheidung (APPROVED / REJECTED)""",
    expected_output="QA-Bericht mit Abnahme-Entscheidung",
    agent=qa_engineer,
    context=[define_requirements, implement_code]
)

# Task 4: Dokumentation erstellen
write_documentation = Task(
    description="""Erstelle eine Anleitung für das Snake-Spiel.
    
    Die Dokumentation soll enthalten:
    
    1. **Spielbeschreibung**
       - Was ist das Ziel?
       - Wie gewinnt/verliert man?
    
    2. **Steuerung**
       - Welche Tasten werden verwendet?
    
    3. **Installation**
       - Wie startet man das Spiel?
    
    4. **Code-Übersicht**
       - Welche Klassen gibt es?
       - Was machen sie?
    
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
    import os
    import sys
    
    # Projektname abfragen oder als Argument uebergeben
    if len(sys.argv) > 1:
        projekt_name = sys.argv[1]
    else:
        print("=" * 60)
        print("📁 PROJEKT-SETUP")
        print("=" * 60)
        projekt_name = input("Projektname eingeben (z.B. 02_calculator): ").strip()
        if not projekt_name:
            projekt_name = "neues_projekt"
    
    # Projektordner erstellen
    OUTPUT_DIR = f"projekte/{projekt_name}"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 60)
    print("🚀 Starte Multi-Agent Crew mit Ollama")
    print(f"   Projekt: {projekt_name}")
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
    
    # Ergebnisse in Projektordner speichern
    with open(f"{OUTPUT_DIR}/ergebnis.md", "w", encoding="utf-8") as f:
        f.write(f"# {projekt_name} - Code & QA Report\n\n")
        f.write("## Generiert von CrewAI Multi-Agent System\n\n")
        f.write("### Agenten:\n")
        f.write("- Product Owner: mistral:7b\n")
        f.write("- Developer: codellama:13b\n")
        f.write("- QA Engineer: mistral:7b\n")
        f.write("- Technical Writer: mistral:7b\n\n")
        f.write("---\n\n")
        f.write(str(result))
    print(f"\n✅ Code & QA-Report wurde in '{OUTPUT_DIR}/ergebnis.md' gespeichert!")
    
    # Dokumentation separat speichern
    if hasattr(result, 'tasks_output') and len(result.tasks_output) >= 4:
        doc_output = result.tasks_output[3].raw
        with open(f"{OUTPUT_DIR}/dokumentation.md", "w", encoding="utf-8") as f:
            f.write(doc_output)
        print(f"✅ Dokumentation wurde in '{OUTPUT_DIR}/dokumentation.md' gespeichert!")
    else:
        with open(f"{OUTPUT_DIR}/dokumentation.md", "w", encoding="utf-8") as f:
            f.write(f"# {projekt_name} - Dokumentation\n\n")
            f.write(str(result))
        print(f"✅ Dokumentation wurde in '{OUTPUT_DIR}/dokumentation.md' gespeichert!")
    
    # Projekt-README erstellen
    with open(f"{OUTPUT_DIR}/README.md", "w", encoding="utf-8") as f:
        f.write(f"# {projekt_name}\n\n")
        f.write("> Generiert vom Multi-Agent CrewAI System\n\n")
        f.write("## Dateien\n\n")
        f.write("- `ergebnis.md` - Generierter Code + QA-Report\n")
        f.write("- `dokumentation.md` - Technische Dokumentation\n\n")
        f.write("## Generiert mit\n\n")
        f.write("- Product Owner: mistral:7b\n")
        f.write("- Developer: codellama:13b\n")
        f.write("- QA Engineer: mistral:7b\n")
        f.write("- Technical Writer: mistral:7b\n")
    print(f"✅ README wurde in '{OUTPUT_DIR}/README.md' gespeichert!")
    
    print(f"\n📁 Alle Dateien im Ordner: {OUTPUT_DIR}/")
