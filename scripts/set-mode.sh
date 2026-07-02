#!/usr/bin/env bash
set -euo pipefail

CONFIG_PATH="$HOME/.dictation-polisher/config.json"
MODE="${1:-}"

if [[ "$MODE" != "light" && "$MODE" != "polish" ]]; then
  echo "Usage: $0 light|polish"
  exit 2
fi

if [[ ! -f "$CONFIG_PATH" ]]; then
  echo "Config not found: $CONFIG_PATH"
  echo "Run ./scripts/setup.sh first."
  exit 1
fi

if [[ "$MODE" == "light" ]]; then
  perl -0pi -e 's/"provider"\s*:\s*"[^"]+"/"provider": "none"/; s/"model"\s*:\s*"[^"]+"/"model": "tiny.en"/' "$CONFIG_PATH"
  echo "Mode set to light: tiny.en transcription, no rewriting."
else
  perl -0pi -e 's/"provider"\s*:\s*"[^"]+"/"provider": "ollama"/; s/"model"\s*:\s*"llama3\.2:3b"/"model": "llama3.2:1b"/' "$CONFIG_PATH"
  echo "Mode set to polish: tiny.en transcription, Ollama llama3.2:1b rewriting."
fi
