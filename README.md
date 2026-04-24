# Game Programmierung — SS26

**Macromedia University of Applied Sciences**
B-GD-ALL-GPG-26SS | Semester 4 | 5 ECTS

Dozent: Jonas Heinke | Lead: Prof. Dr. Reto Schoelly

---

## Worum geht's

Ihr baut ein echtes Spiel — ohne Engine. Kein Unity, kein Unreal, kein Godot. Nur Python, pygame-ce und euer eigener Code. Das Ziel: verstehen, was unter der Haube passiert.

## Toolchain

| Tool | Wofuer |
|------|--------|
| **Python 3.13+** | Die Sprache |
| **uv** | Paketmanager — installiert Libraries, verwaltet Environments |
| **pygame-ce** | Fenster, Zeichnen, Input, Audio |
| **VS Code** oder **Cursor** | Code-Editor |
| **Git** | Versionskontrolle + Abgabe |

### Schnellstart

```bash
# Python installieren: python.org/downloads (Windows: "Add to PATH" ankreuzen!)
# uv installieren:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"   # Windows
curl -LsSf https://astral.sh/uv/install.sh | sh                # Mac/Linux

# Projekt erstellen:
uv init mein-projekt
cd mein-projekt
uv add pygame-ce

# Datei ausfuehren:
uv run main.py
```

Ausfuehrliche Anleitung: [bootstrap.md](bootstrap.md)

## Uebungen

| # | Thema | Punkte | Abgabe |
|---|-------|--------|--------|
| [Uebung 001](uebung-001/) | Schleifen & Funktionen | 10 | Nur `.py`-Datei(en) |
| [Uebung 002](uebung-002/) | Jump & Run | 10 | Projekt-Ordner |
| [Uebung 003](uebung-003/) | RealFakeGame Teil 1 | 10 | Projekt-Ordner + `assets/` |
| [Uebung 004](uebung-004/) | RealFakeGame Teil 2 | 10 | Projekt-Ordner + `assets/` |

**Gesamt: 40 Punkte** aus den Uebungen + 40 Punkte Spiel + 20 Punkte Dokumentation.

## KI-Nutzung

Zwei Drittel selber schreiben, ein Drittel mit KI-Hilfe. Die KI erklaert, debuggt, hilft mit Boilerplate. Ihr entscheidet die Architektur, schreibt die Logik, versteht jeden Satz. Wer am Ende nicht erklaeren kann, was der eigene Code tut, hat zu viel ausgelagert.

## Abgabe

- Quellcode + selbst erstellte Assets + Build (kein ganzer `.venv/`-Ordner)
- Dokumentation als PDF
- Uebungsloesungen
- Alles in einer ZIP (max. 2.5 GB)

## Playgrounds

Kleine, lauffaehige Referenz-Projekte zum Reinschauen und Klauen:

- [jump-playground/](jump-playground/) — Mario-Style Jump mit allen "Game Feel"-Tricks einzeln togglebar (Coyote Time, Jump Buffer, Variable Jump Height, Apex Hangtime, Asymmetric Gravity, Fast Fall). Companion zur Unit-03 Slide-Demo.

## Links

- [pygame-ce Dokumentation](https://pyga.me/docs/)
- [Python Tutorial (offiziell)](https://docs.python.org/3/tutorial/)
- [uv Dokumentation](https://docs.astral.sh/uv/)
