# -*- coding: utf-8 -*-
"""Lazy multilingual speech helpers used by the existing Streamlit chat."""

import asyncio
import os
import tempfile
from pathlib import Path


_whisper_model = None


def transcribe_audio(audio_path: str) -> dict:
    """Transcribe with multilingual Whisper; run on CPU when no GPU is available."""
    global _whisper_model
    import whisper
    import torch

    if _whisper_model is None:
        model_name = os.getenv("WHISPER_MODEL", "base")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        _whisper_model = whisper.load_model(model_name, device=device)
    result = _whisper_model.transcribe(
        audio_path,
        task="transcribe",
        language=None,
        fp16=bool(torch.cuda.is_available()),
        temperature=0,
        condition_on_previous_text=False,
    )
    return {
        "text": (result.get("text") or "").strip(),
        "language": result.get("language") or "",
    }


def roman_urdu_to_urdu(text: str) -> str:
    """Render Roman Urdu in Urdu script without rewriting its message or advice."""
    from langchain_core.messages import HumanMessage, SystemMessage
    from app.services.rag_chat_service import llm

    result = llm.invoke([
        SystemMessage(content=(
            "You are a transliterator, not a translator. Convert Pakistani Roman Urdu "
            "to Urdu script. Preserve every meaning, safety statement, helpline number, "
            "and English code-switched phrase verbatim where possible. Add nothing. "
            "Output only the Urdu-script rendering."
        )),
        HumanMessage(content=text),
    ])
    return (result.content if hasattr(result, "content") else str(result)).strip()


async def _edge_audio(text: str, voice: str, path: str) -> None:
    import edge_tts

    await edge_tts.Communicate(text, voice).save(path)


def synthesize_speech(text: str, language: str, roman_urdu: bool = False) -> str:
    """Return an MP3 path. Edge TTS is online; gTTS is online fallback only."""
    language = (language or "english").lower()
    spoken_text = text
    if roman_urdu:
        try:
            spoken_text = roman_urdu_to_urdu(text)
        except Exception:
            return ""

    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    if language in {"urdu", "roman_urdu"}:
        voice = os.getenv("EDGE_TTS_URDU_VOICE", "ur-PK-UzmaNeural")
    else:
        voice = os.getenv("EDGE_TTS_ENGLISH_VOICE", "en-US-JennyNeural")
    try:
        asyncio.run(_edge_audio(spoken_text, voice, path))
        return path
    except Exception:
        try:
            from gtts import gTTS
            # gTTS is an online fallback. Urdu script supported; Roman Urdu is not.
            lang_code = "ur" if language == "urdu" else "en"
            gTTS(text=spoken_text, lang=lang_code).save(path)
            return path
        except Exception:
            Path(path).unlink(missing_ok=True)
            return ""
