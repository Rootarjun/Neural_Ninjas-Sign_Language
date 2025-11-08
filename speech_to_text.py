import speech_recognition as sr

stop_listening = False

# ---------------- CONTINUOUS LISTEN ----------------
def continuous_listen():
    global stop_listening
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)

        while not stop_listening:
            try:
                audio = r.listen(source, timeout=1, phrase_time_limit=4)
                text = r.recognize_google(audio)
                yield f"{text}"
            except sr.UnknownValueError:
                pass
            except sr.WaitTimeoutError:
                pass
            except sr.RequestError:
                yield "[API unavailable]"
                break

# ---------------- STOP LISTENING ----------------
def stop_listen():
    global stop_listening
    stop_listening = True

# ---------------- FILE TRANSCRIPTION ----------------
def audio_file_to_text(filepath):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(filepath) as source:
            audio = r.record(source)
        return r.recognize_google(audio)
    except Exception:
        return "[Could not process file]"
