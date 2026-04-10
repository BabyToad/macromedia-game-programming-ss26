# Before Your First Session

Install these three things before Friday. We do the rest together in class.

## 1. Python 3.13+

Download from [python.org/downloads](https://www.python.org/downloads/).

**Windows:** tick **"Add Python to PATH"** in the installer. This is the single most common source of problems.

**Mac:** the installer works. Or: `brew install python@3.13`.

**Linux:** `python3 --version` — you probably have it. If not: `sudo apt install python3 python3-venv`.

Verify: open a terminal and run `python --version`. You should see `Python 3.13.x`.

## 2. uv

**Windows (PowerShell):**
```
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Mac / Linux:**
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen your terminal after installing. Verify: `uv --version`.

## 3. VS Code or Cursor

Pick one:
- [VS Code](https://code.visualstudio.com/) — free, standard, what most studios use
- [Cursor](https://cursor.com/) — VS Code with better AI, free tier exists

Install the **Python** extension (by Microsoft) after opening.

## That's it

We install pygame-ce and set up your first project together in class. If something went sideways, bring your laptop and we'll fix it on the spot.
