from __future__ import annotations

from typing import Any, Dict


class Rewriter:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def rewrite(self, transcript: str) -> str:
        if not transcript.strip():
            return ""

        provider = self.config.get("provider", "ollama")
        if provider == "none":
            return transcript.strip()
        if provider != "ollama":
            raise ValueError(f"Unsupported rewriter provider: {provider}")

        return self._rewrite_with_ollama(transcript)

    def _rewrite_with_ollama(self, transcript: str) -> str:
        import requests

        style = self.config.get("style", "polished and concise")
        preserve_intent = self.config.get("preserve_intent", True)
        preserve_instruction = (
            "Preserve the speaker's meaning, facts, names, technical terms, and intent."
            if preserve_intent
            else "Improve the text while keeping it faithful to the input."
        )
        prompt = f"""Rewrite the dictated text into {style} language.
{preserve_instruction}
Do not add facts that are not present.
Return only the rewritten text, with no preamble, labels, markdown fences, or explanation.

Dictated text:
{transcript}
"""

        payload = {
            "model": self.config["model"],
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 700,
            },
        }
        response = requests.post(
            self.config["ollama_url"],
            json=payload,
            timeout=self.config.get("timeout_seconds", 90),
        )
        response.raise_for_status()
        data = response.json()
        rewritten = data.get("response", "").strip()
        return strip_wrapping_quotes(rewritten) or transcript.strip()


def strip_wrapping_quotes(text: str) -> str:
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {'"', "'"}:
        return text[1:-1].strip()
    return text
