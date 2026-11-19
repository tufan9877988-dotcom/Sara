import subprocess
import json


def speak(text):
    subprocess.run(["termux-tts-speak", text])


def listen():
    result = subprocess.run(
        ["termux-speech-to-text"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


speak("Bataiye, main sun rahi hoon")
heard = listen()
print("Aapne kaha:", heard)

if heard:
    speak("Aapne kaha " + heard)
else:
    speak("Mujhe kuch sunai nahi diya")
