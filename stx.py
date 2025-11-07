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
continuous_listen()
