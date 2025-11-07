import speech_recognition as sr

import speech_recognition as sr

def continuous_listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Calibrating noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Start speaking. Ctrl+C to stop.")

        while True:
            try:
                audio = r.listen(source)
                text = r.recognize_google(audio)
                print("You said:", text)
            except sr.UnknownValueError:
                print("[Could not understand]")
            except sr.RequestError:
                print("[API unavailable]")
                
def audio_file_to_text(filepath):
    r = sr.Recognizer()

    try:
        with sr.AudioFile(filepath) as source:
            audio = r.record(source)   # read entire file
        return r.recognize_google(audio)

    except sr.UnknownValueError:
        return "[Could not understand audio]"

    except sr.RequestError:
        return "[API unavailable / Internet issue]"

    except FileNotFoundError:
        return "[File not found]"

    except Exception as e:
        return f"[Error: {e}]"
    
print(audio_file_to_text("test_2.wav"))