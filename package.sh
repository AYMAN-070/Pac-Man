#!/bin/bash
echo "Début du packaging du jeu Pac-Man..."

# installer pyinstaller if not done
uv pip install pyinstaller

# Use 'python -m PyInstaller'
uv run python -m PyInstaller --onefile --add-data "config.json:." src/pac-man.py

echo "Packaging terminé ! L'exécutable se trouve dans le dossier /dist"
