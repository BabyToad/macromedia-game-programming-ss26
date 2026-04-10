# Uebung 002 (10 Punkte)

**Game Programmierung mit Python + pygame-ce**
Basierend auf dem Original von Prof. Dr. Reto Schoelly

---

Bitte den gesamten Projekt-Ordner einreichen!

## Jump & Run (1 Punkt pro erledigter Aufgabe)

Im Skeleton (`main.py`) gibt es ein grundlegendes Modell fuer ein Jump & Run-Game. Es ist bereits alles drin, was man braucht, nur ist es noch nicht vollstaendig ausgefuehrt. Daher die folgenden Aufgaben:

1. **Gravitation.** Fuege Gravitation hinzu, sodass der Player nach unten faellt. Der Code hierfuer ist fast derselbe wie der fuer den Kreis, der ja bereits im Level herumspringt.

2. **Kollisionsfunktion.** Schreibe eine Funktion, die als Parameter ein Rechteck (`pygame.Rect`) uebernimmt, und prueft, ob der Player mit dem Rechteck kollidiert. Der Rueckgabewert sollte `True` sein (falls es eine Kollision gibt), oder `False`, wenn es keine gibt. Tipp: `pygame.Rect` hat eine Methode `colliderect()`.

3. **Boden-Kollision.** Mit der Gravitation aktiv faellt der Player derzeit durch den Boden durch. Leveldesign beinhaltet eben auch Coding! Erweitere die Update-Phase dahingehend, dass der Player nicht durch den Boden oder die anderen Hindernisse in der `obstacles`-Liste durch kann. Aus dem Level fallen sollte er auch nicht.

4. **Springen.** Fuege ein Jump-Feature hinzu, sodass man mit der Taste `W` oder der `SPACE`-Taste springen kann.

5. **Kollisions-Text.** Aendere den Code so, dass der Text, der aktuell "Wheee!" ausgibt, eine Kollision von Player und dem Circle kommentiert. Sowas wie "Ouch!".

6. **Sound.** Nutze `pygame.mixer.Sound`, um einen Sound einzubauen, der ertoent, wenn der Player springt. Sounddateien im `assets/`-Ordner ablegen. Freie Sounds gibt es z.B. auf [freesound.org](https://freesound.org/). Tipp: [pygame.mixer Docs](https://pyga.me/docs/ref/mixer.html)

7. **Spieler-Grafik.** Zeichne einen Player als Pixel-Art, speichere die Datei als PNG ab, und ersetze den gruenen Kreis mit deiner Grafik, sodass dein Charakter Charakter hat. Tipp: `pygame.image.load()` und [pygame.image Docs](https://pyga.me/docs/ref/image.html)

8. **Level-Design.** Mach ein komplexeres Level mit mindestens 5 Plattformen.

9. **Sammelobjekte.** Lass von oben langsam rote Kugeln herunterschweben, welche der Player aufsammeln muss. Fuege einen zweiten Text ein, der die Zahl der gesammelten Kugeln angibt.

10. **Zeitlimit & Spielende.** Lass die Kugeln verschwinden, wenn sie mit einer Plattform kollidieren. Bau ein Zeitlimit ein (Tipp: `pygame.time.get_ticks()` gibt die vergangene Zeit in Millisekunden zurueck). Nach dem Zeitlimit sollte das Spiel stoppen und die Gesamtpunktzahl angezeigt werden.

## Setup

```bash
uv init uebung-002
cd uebung-002
uv add pygame-ce
# main.py aus diesem Ordner in dein Projekt kopieren
uv run main.py
```

## Steuerung (Skeleton)

- `A` / `D` — links / rechts bewegen

## Docs

- [pygame-ce Dokumentation](https://pyga.me/docs/)
- [pygame.draw](https://pyga.me/docs/ref/draw.html) — Zeichenfunktionen
- [pygame.mixer](https://pyga.me/docs/ref/mixer.html) — Sound
- [pygame.image](https://pyga.me/docs/ref/image.html) — Bilder laden
- [pygame.time](https://pyga.me/docs/ref/time.html) — Zeit und Timer
