"""Optional Anki Vector adapter; the core application does not require the SDK."""

import os


def is_enabled() -> bool:
    return os.getenv("VECTOR_ENABLED", "0") == "1"


def speak(text: str) -> None:
    if not is_enabled():
        raise RuntimeError("Vector integration is disabled.")
    try:
        import anki_vector
    except ImportError as exc:
        raise RuntimeError("Install requirements-vector.txt to use Vector.") from exc

    with anki_vector.Robot() as robot:
        robot.behavior.say_text(text)

