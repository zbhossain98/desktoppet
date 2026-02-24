# Desktop Pet Application

A complete desktop pet app built with Python + Tkinter. It creates a floating animated pet that moves around, talks, responds to clicks, can be dragged, and has a right-click action menu.

## Features

- Animated bouncing pet with mood system (`happy`, `curious`, `sleepy`, `playful`)
- Dynamic speech bubble text based on mood
- Energy mechanic (pet gets tired over time)
- Interactions:
  - Left click: chirp reaction
  - Drag: reposition your pet
  - Right click menu:
    - Feed
    - Rename
    - Change color
    - About
    - Quit
- Persistent user preferences (name, color, speed) stored at `~/.desktop_pet_config.json`
- Windows executable build support (`DesktopPet.exe`)

## Run from source

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Build EXE (Windows)

> Build on a Windows machine to get a native `.exe`.

1. Open **Command Prompt** in the project root.
2. Run:

```bat
scripts\build_exe.bat
```

3. Your executable will be generated at:

```text
dist\DesktopPet.exe
```

## Test

```bash
pytest -q
```

## Project Structure

- `main.py`: UI, animation loop, interactions
- `pet/logic.py`: pure pet state logic (movement, mood transitions, feeding)
- `pet/config.py`: config load/save helpers
- `desktop_pet.spec`: PyInstaller spec for generating `DesktopPet.exe`
- `scripts/build_exe.bat`: one-command Windows build script
- `tests/test_logic.py`: unit tests for core logic
