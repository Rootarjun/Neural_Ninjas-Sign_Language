import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import ttk  # Import ttk for themed widgets and styling
import threading
import speech_to_text 
from speech_to_text import continuous_listen, stop_listen, audio_file_to_text

class SpeechGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech To Text GUI")
        self.root.geometry("700x550") # Slightly increase window size for better spacing
        self.root.resizable(False, False) # Make window non-resizable for consistent look

        # --- THEME AND STYLING ---
        style = ttk.Style()
        style.theme_use('clam') # 'clam', 'alt', 'default', 'vista' (Windows), 'xpnative' (Windows)
        
        # Define a consistent background color for the main window and frames
        self.bg_color = "#2c3e50" # Dark blue-grey (similar to a modern dashboard)
        self.text_box_bg = "#34495e" # Slightly lighter dark blue-grey for text box
        self.text_color = "#ecf0f1" # Light grey for text
        self.accent_color_play = "#2ecc71" # Emerald green
        self.accent_color_stop = "#e74c3c" # Alizarin crimson (red)
        self.accent_color_default = "#3498db" # Peter river (blue)

        self.root.configure(bg=self.bg_color)

        # Style for the main text box
        style.configure("TScrolledText",
                        background=self.text_box_bg,
                        foreground=self.text_color,
                        font=("Segoe UI", 11),
                        borderwidth=0, # Remove border
                        relief="flat", # Flat appearance
                        insertbackground=self.text_color) # Cursor color

        # Style for main buttons
        style.configure("TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=8,
                        relief="flat",
                        background=self.accent_color_default,
                        foreground="#ffffff") # White text for buttons
        style.map("TButton",
                  background=[('active', self.accent_color_default)]) # Keep color on hover


        # Specific styles for Play and Stop buttons
        style.configure("Play.TButton", background=self.accent_color_play)
        style.map("Play.TButton", background=[('active', '#27ae60')]) # Darker green on hover

        style.configure("Stop.TButton", background=self.accent_color_stop)
        style.map("Stop.TButton", background=[('active', '#c0392b')]) # Darker red on hover

        # Style for the Progressbar
        style.configure("TProgressbar",
                        background=self.accent_color_play, # Color of the moving part
                        troughcolor=self.text_box_bg, # Color of the track
                        thickness=10) # Thickness of the bar

        # Style for the loading label
        style.configure("TLabel",
                        background=self.bg_color,
                        foreground=self.text_color,
                        font=("Segoe UI", 10, "italic"))

        # *** FIX 1: Configure the TFrame style to use the background color ***
        style.configure("TFrame", background=self.bg_color)


        # --- WIDGETS ---

        # Text Box
        self.text_box = scrolledtext.ScrolledText(root, 
                                                wrap=tk.WORD, 
                                                width=75, 
                                                height=20, 
                                                state=tk.DISABLED,
                                                background=self.text_box_bg, # Apply background here too for consistency
                                                foreground=self.text_color, # Apply foreground here too
                                                font=("Segoe UI", 11),
                                                insertbackground=self.text_color, # Cursor color
                                                borderwidth=0,
                                                relief="flat",
                                                highlightbackground=self.bg_color, # Remove highlight border
                                                highlightthickness=1) 
        self.text_box.pack(pady=(20, 10), padx=20, fill=tk.BOTH, expand=True)
        
        # Loading/Stopping Indicator Frame (initially hidden)
        # *** FIX 2: Removed 'background=...' parameter ***
        self.indicator_frame = ttk.Frame(root, style="TFrame")
        self.loading_label = ttk.Label(self.indicator_frame, text="")
        self.progress_bar = ttk.Progressbar(self.indicator_frame, mode='indeterminate', length=300)
        
        # Button Frame
        # *** FIX 3: Removed 'background=...' parameter ***
        button_frame = ttk.Frame(root, style="TFrame")
        button_frame.pack(pady=(0, 20)) # Added padding below buttons

        self.listen_btn = ttk.Button(button_frame, text="Play", style="Play.TButton", command=self.start_listening)
        self.listen_btn.grid(row=0, column=0, padx=8, ipadx=5, ipady=5) # Added internal padding

        self.stop_btn = ttk.Button(button_frame, text="Stop", style="Stop.TButton", state=tk.DISABLED, command=self.stop_listening)
        self.stop_btn.grid(row=0, column=1, padx=8, ipadx=5, ipady=5)

        self.clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_text)
        self.clear_btn.grid(row=0, column=2, padx=8, ipadx=5, ipady=5)

        self.upload_btn = ttk.Button(button_frame, text="Upload Audio", command=self.upload_file)
        self.upload_btn.grid(row=0, column=3, padx=8, ipadx=5, ipady=5)

    def display_message(self, message):
        """Helper to safely write to the disabled text box."""
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, message)
        self.text_box.see(tk.END)
        self.text_box.config(state=tk.DISABLED)

    def start_listening(self):
        self.listen_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)
        self.upload_btn.config(state=tk.DISABLED)
        
        self.loading_label.config(text="Loading environment...")
        self.indicator_frame.pack(pady=10)
        self.loading_label.pack()
        self.progress_bar.pack(pady=5)
        self.progress_bar.start()
        
        self.root.after(2000, self.start_listening_thread)

    def start_listening_thread(self):
        self.progress_bar.stop()
        self.indicator_frame.pack_forget() # Hide the entire frame
        self.loading_label.pack_forget()
        self.progress_bar.pack_forget()
        
        speech_to_text.stop_listening = False 
        self.stop_btn.config(state=tk.NORMAL) 
        
        threading.Thread(target=self.listen_loop, daemon=True).start()

    def listen_loop(self):
        for text in continuous_listen():
            self.display_message(text + "\n")

    def stop_listening(self):
        stop_listen() 
        
        self.stop_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)
        self.upload_btn.config(state=tk.DISABLED)
        
        self.loading_label.config(text="Stopping environment...")
        self.indicator_frame.pack(pady=10)
        self.loading_label.pack()
        self.progress_bar.pack(pady=5)
        self.progress_bar.start()
        
        self.root.after(2000, self.finish_stopping) 

    def finish_stopping(self):
        self.progress_bar.stop()
        self.indicator_frame.pack_forget() # Hide the entire frame
        self.loading_label.pack_forget()
        self.progress_bar.pack_forget()
        
        self.listen_btn.config(state=tk.NORMAL)
        self.clear_btn.config(state=tk.NORMAL)
        self.upload_btn.config(state=tk.NORMAL)

    def clear_text(self):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        self.text_box.config(state=tk.DISABLED)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.clear_btn.config(state=tk.DISABLED)
            self.listen_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.DISABLED)
            self.upload_btn.config(state=tk.DISABLED, text="Processing...")

            threading.Thread(target=self._transcribe_and_display, args=(file_path,), daemon=True).start()

    def _transcribe_and_display(self, file_path):
        self.display_message(f"\nTranscribing audio file: {file_path.split('/')[-1]}...\n") # Show file name
        
        # Show a temporary indicator for file upload processing
        self.loading_label.config(text="Transcribing audio...")
        self.indicator_frame.pack(pady=10)
        self.loading_label.pack()
        self.progress_bar.pack(pady=5)
        self.progress_bar.start()

        text = audio_file_to_text(file_path)
        
        self.progress_bar.stop()
        self.indicator_frame.pack_forget()
        self.loading_label.pack_forget()
        self.progress_bar.pack_forget()

        self.display_message(f"File transcription result: {text}\n")
        
        self.upload_btn.config(state=tk.NORMAL, text="Upload Audio")
        self.clear_btn.config(state=tk.NORMAL)
        self.listen_btn.config(state=tk.NORMAL)
        # stop_btn remains disabled unless listening
        

if __name__ == "__main__":
    root = tk.Tk()
    gui = SpeechGUI(root)
    root.mainloop()