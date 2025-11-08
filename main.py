import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os

def launch_script(script_name):
    """
    Launches a Python script in a new, independent process.
    This prevents the main menu from freezing.
    """
    print(f"Attempting to launch {script_name}...")
    try:
        # Use sys.executable to ensure we use the same Python interpreter
        # that this main.py script is running on.
        subprocess.Popen([sys.executable, script_name])
    except FileNotFoundError:
        print(f"Error: Could not find {script_name}. Make sure it's in the same directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Main Window Setup ---
root = tk.Tk()
root.title("Assistive Technology Suite")
root.geometry("500x380") # Set a fixed size for the launcher
root.resizable(False, False)

# --- Theme and Styling (Inspired by your GUIs) ---
style = ttk.Style()
style.theme_use('clam')

# Define the color palette based on your files
bg_color = "#2c3e50"
text_color = "#ecf0f1"
subtitle_color = "#b0b0b0"
sign_color = "#8a2be2" # Purple from camera_gui
speech_color = "#3498db" # Blue from speech_gui

root.configure(bg=bg_color)

# Style for frames and labels
style.configure("TFrame", background=bg_color)
style.configure("TLabel", 
                background=bg_color, 
                foreground=text_color, 
                font=("Segoe UI", 24, "bold"))
style.configure("Sub.TLabel", 
                background=bg_color, 
                foreground=subtitle_color,
                font=("Segoe UI", 12))

# Style for the "Sign" button
style.configure("Sign.TButton", 
                background=sign_color, 
                foreground=text_color, 
                font=("Segoe UI", 14, "bold"),
                padding=(20, 10),
                relief="flat")
style.map("Sign.TButton", 
          background=[('active', '#7b24cc')]) # Darker purple on hover

# Style for the "Speech" button
style.configure("Speech.TButton", 
                background=speech_color,
                
                foreground=text_color, 
                font=("Segoe UI", 14, "bold"),
                padding=(20, 10),
                relief="flat")

style.map("Speech.TButton", 
          background=[('active', '#2980b9')]) # Darker blue on hover

# --- Create Widgets ---

# Use a main frame to easily center and pad all content
main_frame = ttk.Frame(root, padding=40)
main_frame.pack(expand=True, fill="both")

# Title Label
title_label = ttk.Label(main_frame, text="Neural Ninjas", anchor="center")
title_label.pack(pady=(10, 5))

# Subtitle Label
subtitle_label = ttk.Label(main_frame, 
                           text="Assistive Technology Suite", 
                           style="Sub.TLabel", 
                           anchor="center")
subtitle_label.pack(pady=(0, 30))

# Button 1: Sign to Text/Speech
# This button will run camera_gui.py
sign_btn = ttk.Button(main_frame, 
                      text="Sign Language to Speech", 
                      style="Sign.TButton",
                      command=lambda: launch_script('camera_gui.py'))
sign_btn.pack(fill="x", pady=10, ipady=10) # ipady adds internal height

# Button 2: Speech to Text
# This button will run speech_gui.py
speech_btn = ttk.Button(main_frame, 
                        text="Speech to Text", 
                        style="Speech.TButton",
                        command=lambda: launch_script('speech_gui.py'))
speech_btn.pack(fill="x", pady=10, ipady=10)

# --- Run the Application ---
if __name__ == "__main__":
    # Ensure other scripts are present (optional check)
    if not (os.path.exists('camera_gui.py') and os.path.exists('speech_gui.py')):
        print("Warning: 'camera_gui.py' or 'speech_gui.py' not found in directory.")
        
    root.mainloop()