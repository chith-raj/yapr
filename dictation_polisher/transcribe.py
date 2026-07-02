from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from faster_whisper import WhisperModel


class Transcriber:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._model: WhisperModel | None = None

    def _get_model(self) -> WhisperModel:
        if self._model is None:
            self._model = WhisperModel(
                self.config["model"],
                device=self.config["device"],
                compute_type=self.config["compute_type"],
            )
        return self._model

    def transcribe(self, audio_path: Path) -> str:
        model = self._get_model()
        segments, _info = model.transcribe(
            str(audio_path),
            language=self.config.get("language") or None,
            vad_filter=True,
            beam_size=5,
        )
        text = " ".join(segment.text.strip() for segment in segments).strip()
        return normalize_spacing(text)


def normalize_spacing(text: str) -> str:
    return " ".join(text.split())
