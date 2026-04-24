# Mario Jump Playground — Python reference

A tunable 2D platformer sandbox. Every "game feel" trick can be toggled
independently so you can feel exactly what each one does.

Companion to the web playground in the Unit 03 slide deck.

## Run it

```bash
uv sync
uv run main.py
```

No extra assets — everything is drawn procedurally. Single file. Read it
top-to-bottom, steal what you want.

## Controls

| Key                 | What                              |
|---------------------|-----------------------------------|
| `A` / `D` or ← / →  | move                              |
| `Space` / `W` / ↑   | jump (variable height if on)      |
| `S` / ↓             | fast fall                         |
| `R`                 | reset                             |
| `H`                 | toggle help overlay               |
| `G`                 | toggle graph strip                |
| `1` – `6`           | toggle individual tricks          |
| `7`                 | toggle "realistic" (all off)      |
| `[` / `]`           | decrease / increase gravity       |
| `-` / `=`           | decrease / increase jump strength |

## What each trick does

1. **Variable jump height** — release the jump key while still rising, cut
   the upward velocity. Tap = hop, hold = full jump.
2. **Coyote time** — you can jump for a few frames *after* walking off a
   ledge. Rescues off-by-one ledge fails.
3. **Jump buffer** — press jump a few frames *before* you land, it still
   fires. Rescues impatient jumps.
4. **Apex hangtime** — gravity halves near the peak of the jump. Floaty,
   controllable, feels good.
5. **Asymmetric gravity** — gravity is higher while falling than rising.
   Snappy, not mushy.
6. **Fast fall** — hold ↓ in the air to accelerate down.
7. **Realistic mode** — turn all tricks off, watch it feel terrible.

## The point

> Real physics feels terrible.
> Modern platformers stack half a dozen cheats to feel good.
> Each cheat is a boolean flag plus a few lines of code.

Flip them one at a time. See what changes. Steal the ones you like. Tune
the numbers until your jump feels like *yours*.

## File layout

- `main.py` — the whole thing, procedural style (no classes, no magic)
- `pyproject.toml` — `uv` config + dependency (pygame-ce)
- `README.md` — you are here
