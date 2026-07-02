# VoiceInk

VoiceInk is a lightweight macOS tool that lets you dictate into any focused input field. It records audio on a hotkey, transcribes it locally with Whisper, rewrites it with a local Ollama model when enabled, and pastes the polished result into the active app.

## What It Uses

- `faster-whisper` for local speech-to-text.
- Ollama for local rewriting.
- macOS clipboard + `Cmd+V` to insert text into browser forms, editors, and documents.
- `pynput` for a configurable global hotkey.

No cloud API is used by the app. The first setup may download Python packages, the Whisper model, and the Ollama model. After those are installed, transcription and rewriting run locally.

## Setup

```bash
cd local-dictation-polisher
chmod +x scripts/setup.sh
./scripts/setup.sh
```

Regenerate the app icon if needed:

```bash
./scripts/generate-icon.py
```

Install Ollama if needed, then pull a small local model:

```bash
ollama pull llama3.2:3b
```

## Run

```bash
cd local-dictation-polisher
./voiceink
```

You can also launch VoiceInk without Terminal by opening:

```text
VoiceInk.app
```

From Finder, you can drag `VoiceInk.app` to the Dock. It runs in the background and uses the same hotkey.

If macOS blocks the app from reading files in `Documents`, install it into your user Applications folder:

```bash
./scripts/install-app.sh
```

Then open:

```text
~/Applications/VoiceInk.app
```

Default hotkey:

```text
Command + Shift + D
```

Press the hotkey once to start recording. Press it again to stop. The polished text is pasted into the active input field.

For a one-off terminal test:

```bash
./voiceink --once --print-only
```

## Customize

Create or edit:

```text
~/.dictation-polisher/config.json
```

Useful settings:

```json
{
  "hotkey": "<cmd>+<shift>+d",
  "whisper": {
    "model": "tiny.en"
  },
  "rewriter": {
    "provider": "none",
    "model": "llama3.2:3b",
    "style": "polished, concise, and well structured"
  },
  "paste": {
    "restore_clipboard": false
  }
}
```

Hotkey examples:

```text
<cmd>+<shift>+d
<ctrl>+<alt>+<space>
<ctrl>+<shift>+f12
```

Whisper model examples:

```text
tiny.en
base.en
small.en
medium.en
```

Smaller models are faster. Larger models are more accurate.

To disable rewriting and paste the transcript directly:

```json
{
  "rewriter": {
    "provider": "none"
  }
}
```

## Start Automatically On Login

```bash
cd local-dictation-polisher
chmod +x scripts/install-launch-agent.sh scripts/uninstall-launch-agent.sh
./scripts/install-launch-agent.sh
```

Uninstall:

```bash
./scripts/uninstall-launch-agent.sh
```

Logs:

```text
~/Library/Logs/voiceink/
```

## macOS Permissions

The tool needs:

- Microphone access for recording.
- Accessibility access so it can trigger `Cmd+V` in the active app.

If pasting does not work, open:

```text
System Settings -> Privacy & Security -> Accessibility
```

Then allow the terminal app you use, or the Python executable inside this project.

If you launch `VoiceInk.app`, allow `VoiceInk` in these permission screens when macOS asks.

If the hotkey does not trigger, also check:

```text
System Settings -> Privacy & Security -> Input Monitoring
```

Then allow the terminal app you use. You can verify key events with:

```bash
./voiceink --debug-keys
```

## Notes

- Ollama must be running for rewriting. If Ollama is unavailable, set `"provider": "none"` to paste raw transcripts.
- The first transcription can take longer while the Whisper model is downloaded and cached.
- Universal insertion is implemented with clipboard paste because it works across browsers, editors, and document apps.
