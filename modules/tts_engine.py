from gtts import gTTS

def text_to_speech(text, speed, output_file="audiobook.mp3"):
    try:
        # Speed control
        slow = True if speed == "Slow" else False

        tts = gTTS(text=text, lang="en", slow=slow)

        tts.save(output_file)
        return output_file
    except Exception as e:
        return None

# def text_to_speech(text, speed, output_file="audiobook.mp3"):

#     # Speed control
#     slow = True if speed == "Slow" else False

#     tts = gTTS(text=text, lang="en", slow=slow)

#     tts.save(output_file)

#     return output_file