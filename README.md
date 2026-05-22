# Frog Pet

This is your desktop frog pet app built with Python and PyQt5.

## Project Structure

- `frog_pet_qt.py` — main frog pet application script
- `frog_pet.py` — older or extra frog pet script
- `setup.py` — py2app build configuration
- `requirements.txt` — Python dependencies
- `frog_env/` — local Python virtual environment, not committed to GitHub
- `build/` — temporary build files created by py2app, not committed to GitHub
- `dist/` — generated macOS app bundle, not committed to GitHub
- `.eggs/` — build helper files used by py2app, not committed to GitHub

## Set up dependencies

Create a local virtual environment and install the app dependencies:

```bash
cd ~/frog_pet
python3 -m venv frog_env
./frog_env/bin/python3 -m pip install -r requirements.txt
```

## Run the app directly

Use the virtual environment to run the app without packaging:

```bash
cd ~/frog_pet
./frog_env/bin/python3 frog_pet_qt.py
```

## Build the app bundle

From the project folder, build a standalone macOS app bundle:

```bash
cd ~/frog_pet
./frog_env/bin/python3 setup.py py2app
```

Then open the app:

```bash
open ~/frog_pet/dist/Frog\ Pet.app
```

## Notes

- If macOS blocks the app, use System Settings > Privacy & Security to allow it.
- Recreate `frog_env` with the setup command above if you clone this repo on a new computer.
- You can move the folder anywhere else later, but update the paths in your commands accordingly.
