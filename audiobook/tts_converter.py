import pyttsx3

def get_available_voices() -> dict[str, str]:
    """Return a dict of {display_name: voice_id} for all system voices."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.stop()
    return {v.name: v.id for v in voices} if voices else {}

def text_to_speech(text, output_file, rate=150, voice_id=None):
    """Convert text to speech and save as audio file.
    
    Args:
        voice_id: specific voice ID to use. If None, prefers a female voice,
                  falling back to the first available voice.
    """
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        engine.setProperty('volume', 1.0)

        voices = engine.getProperty('voices')
        if voices:
            if voice_id:
                selected = voice_id
            else:
                # Prefer a female voice by checking common keywords in name/id
                female = next(
                    (v for v in voices if any(
                        kw in (v.name + v.id).lower()
                        for kw in ("zira", "hazel", "female", "woman", "girl", "susan", "catherine", "victoria", "samantha")
                    )),
                    None
                )
                selected = female.id if female else voices[0].id
            engine.setProperty('voice', selected)

        engine.save_to_file(text, output_file)
        engine.runAndWait()

    except Exception as e:
        raise Exception(f"TTS conversion failed: {e}")
