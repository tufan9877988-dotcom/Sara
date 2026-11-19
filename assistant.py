import subprocess
from datetime import datetime
from offline_chat import sara_reply
from commands import handle_command

def speak(text):
    print("SARA:", text)
    subprocess.run(["termux-tts-speak", text])

def listen():
    try:
        result = subprocess.run(
            ["termux-speech-to-text"],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip().lower()
    except Exception as e:
        print("Listening error:", e)
        return ""

def reply(heard):
    if any(word in heard for word in ["time", "samay", "waqt", "समय"]):
        now = datetime.now().strftime("%I:%M %p")
        return "Abhi samay hai " + now

    if any(word in heard for word in ["date", "tarikh", "tareekh", "तारीख"]):
        today = datetime.now().strftime("%d %B %Y")
        return "Aaj ki tarikh hai " + today

    return sara_reply(heard)

def main():
    speak("SARA taiyaar hai. Aap kya karna chahte hain?")

    while True:
        heard = listen()

        if not heard:
            continue

        print("Aapne kaha:", heard)

        if any(word in heard for word in ["band karo", "stop", "bye", "बंद करो"]):
            speak("Theek hai, phir milte hain.")
            break

        try:
            command_response = handle_command(heard)

            if command_response:
                speak(command_response)
                continue

            speak(reply(heard))

        except Exception as e:
            print("Command error:", e)
            speak("Maaf kijiye, is command mein problem aa gayi.")

if __name__ == "__main__":
    main()
