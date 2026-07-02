#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

python3 -m venv .venv
".venv/bin/python" -m pip install --upgrade pip
".venv/bin/pip" install -r requirements.txt
".venv/bin/python" -m dictation_polisher.app --init-config
chmod +x "$PROJECT_DIR/dictation-polisher"
chmod +x "$PROJECT_DIR/voiceink"
chmod +x "$PROJECT_DIR/VoiceInk.app/Contents/MacOS/VoiceInk"
chmod +x "$PROJECT_DIR/scripts/create-app.sh"
chmod +x "$PROJECT_DIR/scripts/install-app.sh"
chmod +x "$PROJECT_DIR/scripts/generate-icon.py"

cat <<'MSG'

Setup complete.

Next:
1. Install Ollama from https://ollama.com if it is not installed.
2. Run: ollama pull llama3.2:3b
3. Start VoiceInk: ./voiceink

macOS will ask for Microphone and Accessibility permissions the first time you use it.
MSG
