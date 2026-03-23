from deep_translator import GoogleTranslator

def translate_text(text, target_language):

    if target_language == "en":
        return text

    translated = GoogleTranslator(
        source="auto",
        target=target_language
    ).translate(text)

    return translated