
def sara_reply(text):
    text = text.lower().strip()

    # Greeting
    if any(word in text for word in ["hello", "hi", "नमस्ते", "namaste"]):
        return "Namaste! Main SARA hoon. Aapki kya madad kar sakti hoon?"

    # Name
    elif any(word in text for word in ["naam", "name", "नाम"]):
        return "Mera naam SARA hai."

    # Who are you?
    elif any(word in text for word in [
        "tum kaun ho",
        "tum kon ho",
        "aap kaun ho",
        "aap kon ho",
        "who are you",
        "who r u",
        "तुम कौन हो",
        "आप कौन हो"
    ]):
        return "Main SARA hoon, aapki personal AI voice assistant. Main aapki madad ke liye taiyaar hoon!"

    # Time
    elif any(word in text for word in ["samay", "time", "waqt", "समय"]):
        from datetime import datetime
        return "Abhi samay hai " + datetime.now().strftime("%I:%M %p")

    # How are you?
    elif any(word in text for word in ["kaise ho", "kaisi ho", "कैसे हो"]):
        return "Main bilkul theek hoon! Aap kaise hain?"

    # Goodbye
    elif any(word in text for word in ["bye", "alvida", "बाय"]):
        return "Alvida! Phir milenge."

    else:
        return "Main aapki baat samajhne ki koshish kar rahi hoon. Thoda aur bataiye."

