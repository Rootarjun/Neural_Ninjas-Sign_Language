import pickle
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import tkinter as tk
from tkinter import StringVar, Label, Frame
from PIL import Image, ImageTk
import threading
import time
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5, max_num_hands=1)

engine = pyttsx3.init()

labels_dict = {
        0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
        10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
        19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: ' ',
        27: '.', 28: ' THANK YOU ', 29: ' I LOVE YOU ', 30: ' SORRY ', 31: ' PLEASE ',
        32: ' YOU ARE WELCOME'
    }

expected_features = 42

stabilization_buffer = []
stable_char = None
word_buffer = ""
sentence = ""
sentence_started = False 

def speak_text(text):
    def tts_thread():
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=tts_thread, daemon=True).start()


# GUI Setup
root = tk.Tk()
root.title("Sign Language to Speech Conversion")
root.geometry("1200x700")
root.configure(bg="#1e1e2e")  
root.resizable(False, False)

current_alphabet = StringVar(value="Waiting for sign...")
current_word = StringVar(value="")
current_sentence = StringVar(value="")

title_frame = Frame(root, bg="#1e1e2e")
title_frame.pack(pady=20)

title_label = Label(title_frame, text="Sign Language to Speech", font=("Arial", 32, "bold"), 
                    fg="#8a2be2", bg="#1e1e2e")  # Purple color
title_label.pack()

subtitle_label = Label(title_frame, text="Real-time gesture recognition and speech synthesis", 
                      font=("Arial", 14), fg="#b0b0b0", bg="#1e1e2e")
subtitle_label.pack(pady=(5, 0))

main_frame = Frame(root, bg="#1e1e2e")
main_frame.pack(fill="both", expand=True, padx=40, pady=20)

video_container = Frame(main_frame, bg="#2d2d44", bd=0, relief="flat", 
                        highlightbackground="#8a2be2", highlightthickness=2)
video_container.pack(side="left", padx=(0, 40))

video_header = Label(video_container, text="Camera Feed", font=("Arial", 18, "bold"), 
                     fg="#ffffff", bg="#2d2d44")
video_header.pack(pady=15)

video_frame = Frame(video_container, bg="#2d2d44", width=500, height=400)
video_frame.pack(padx=20, pady=(0, 20))
video_frame.pack_propagate(False)

video_label = tk.Label(video_frame, bg="#2d2d44")
video_label.pack(expand=True)

info_frame = Frame(main_frame, bg="#1e1e2e")
info_frame.pack(side="right", fill="both", expand=True)

status_frame = Frame(info_frame, bg="#1e1e2e")
status_frame.pack(fill="x", pady=(0, 30))

alphabet_frame = Frame(status_frame, bg="#2d2d44", relief="flat", 
                       highlightbackground="#8a2be2", highlightthickness=1)
alphabet_frame.pack(fill="x", pady=10)

Label(alphabet_frame, text="CURRENT SIGN", font=("Arial", 12), 
      fg="#b0b0b0", bg="#2d2d44").pack(anchor="w", padx=15, pady=(10, 0))
Label(alphabet_frame, textvariable=current_alphabet, font=("Arial", 36, "bold"), 
      fg="#8a2be2", bg="#2d2d44").pack(pady=(5, 15))

word_frame = Frame(status_frame, bg="#2d2d44", relief="flat", 
                   highlightbackground="#8a2be2", highlightthickness=1)
word_frame.pack(fill="x", pady=10)

Label(word_frame, text="CURRENT WORD", font=("Arial", 12), 
      fg="#b0b0b0", bg="#2d2d44").pack(anchor="w", padx=15, pady=(10, 0))
Label(word_frame, textvariable=current_word, font=("Arial", 24), 
      fg="#ffffff", bg="#2d2d44", wraplength=400, justify="left").pack(pady=(5, 15))

sentence_frame = Frame(status_frame, bg="#2d2d44", relief="flat", 
                       highlightbackground="#8a2be2", highlightthickness=1)
sentence_frame.pack(fill="x", pady=10)

Label(sentence_frame, text="SENTENCE", font=("Arial", 12), 
      fg="#b0b0b0", bg="#2d2d44").pack(anchor="w", padx=15, pady=(10, 0))
Label(sentence_frame, textvariable=current_sentence, font=("Arial", 18), 
      fg="#ffffff", bg="#2d2d44", wraplength=400, justify="left").pack(pady=(5, 15))

instructions_frame = Frame(info_frame, bg="#1e1e2e")
instructions_frame.pack(fill="x", pady=20)

instructions_text = """
Instructions:
• Use SPACE sign to separate words
• Use PERIOD sign to end sentence
"""

instructions_label = Label(instructions_frame, text=instructions_text, 
                          font=("Arial", 12), fg="#b0b0b0", bg="#1e1e2e", justify="left")
instructions_label.pack(anchor="w")

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

last_registered_time = time.time()
registration_delay = 1.5  

def format_sentence(text):
    """Format sentence with proper capitalization and spacing"""
    if not text:
        return text
    
    text = ' '.join(text.split())
    if text:
        text = text[0].upper() + text[1:].lower()
    return text

def process_frame():
    global stabilization_buffer, stable_char, word_buffer, sentence, sentence_started, last_registered_time

    ret, frame = cap.read()
    if not ret:
        return

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            data_aux = []
            x_ = []
            y_ = []

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

            if len(data_aux) < expected_features:
                data_aux.extend([0] * (expected_features - len(data_aux)))
            elif len(data_aux) > expected_features:
                data_aux = data_aux[:expected_features]

            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]

            stabilization_buffer.append(predicted_character)
            if len(stabilization_buffer) > 30: 
                stabilization_buffer.pop(0)

            if stabilization_buffer.count(predicted_character) > 25:
                current_time = time.time()
                if current_time - last_registered_time > registration_delay:
                    stable_char = predicted_character
                    last_registered_time = current_time 
                    
                    
                    if stable_char == ' ':
                        if word_buffer.strip():  
                            if sentence and not sentence.endswith(' '):
                                sentence += ' ' + word_buffer
                            else:
                                sentence += word_buffer
                            current_sentence.set(format_sentence(sentence))
                        word_buffer = ""
                        current_word.set("")
                    elif stable_char == '.':
                        if word_buffer.strip():  
                            if sentence and not sentence.endswith(' '):
                                sentence += ' ' + word_buffer
                            else:
                                sentence += word_buffer
                        
                        formatted_sentence = format_sentence(sentence)
                        if formatted_sentence:
                            speak_text(formatted_sentence)
                            current_sentence.set(formatted_sentence + ".")
                        
                        word_buffer = ""
                        sentence = ""
                        sentence_started = False
                        current_word.set("")
                        current_alphabet.set("Waiting for sign...")
                    else:
                        word_buffer += stable_char
                        current_word.set(word_buffer)
                        current_alphabet.set(stable_char)

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                      mp_drawing_styles.get_default_hand_landmarks_style(),
                                      mp_drawing_styles.get_default_hand_connections_style())
            
    cv2.putText(frame, f"Sign: {current_alphabet.get()}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (138, 43, 226), 2)  
    cv2.putText(frame, f"Word: {current_word.get()}", (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)  

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = img_tk
    video_label.configure(image=img_tk)

    root.after(10, process_frame)

process_frame()
root.mainloop()