# Neural Ninjas - Assistive Technology Suite

A real-time application suite designed to bridge communication gaps, featuring a **Sign Language to Speech** module and a **Speech to Text** module.



## 🚀 Features

* **Main Launcher:** A clean, modern UI to launch either of the two main features.
* **Sign Language to Speech (`camera_gui.py`):**
    * Uses your webcam to capture hand gestures in real-time.
    * Powered by a MediaPipe hand landmark model.
    * Predicts 33 different signs (A-Z, space, period, and common phrases).
    * Builds words and sentences, then speaks them aloud using text-to-speech.
* **Speech to Text (`speech_gui.py`):**
    * Uses your microphone to capture continuous speech.
    * Transcribes speech into a read-only text box in real-time.
    * Supports transcribing audio from uploaded files.
    * Includes a modern, dark-themed UI with loading animations.

## 🛠️ Setup & Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

* Python 3.8 or newer
* A webcam (for the Sign Language module)
* A microphone (for the Speech to Text module)

### Step 1: Clone the Repository

First, clone the project to your local machine:

```bash
git clone [https://github.com/Rootarjun/Neural_Ninjas-Sign_Language.git](https://github.com/Rootarjun/Neural_Ninjas-Sign_Language.git)
cd Neural_Ninjas-Sign_Language