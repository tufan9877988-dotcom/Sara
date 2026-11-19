import subprocess
import json
import urllib.parse
import re

APPS = {
    "youtube": ["youtube", "यूट्यूब"],
    "whatsapp": ["whatsapp", "व्हाट्सएप", "व्हाट्स अप"],
    "chrome": ["chrome", "क्रोम"],
    "camera": ["camera", "कैमरा"],
    "gallery": ["gallery", "gallary", "गैलरी"],
    "photos": ["photos", "photo", "फोटो"],
    "facebook": ["facebook", "फेसबुक"],
    "free fire": ["free fire max", "free fire", "फ्री फायर"],
    "instagram": ["instagram", "इंस्टाग्राम"],
    "spotify": ["spotify", "स्पॉटिफाई"],
    "telegram": ["telegram", "टेलीग्राम"],
    "settings": ["settings", "setting", "सेटिंग"],
    "contacts": ["contacts", "contact", "कॉन्टैक्ट", "संपर्क"],
    "phone": ["phone", "dialer", "फोन", "डायलर"],
}

PACKAGES = {
    "youtube": "com.google.android.youtube",
    "whatsapp": "com.whatsapp",
    "chrome": "com.android.chrome",
    "camera": "com.oplus.camera",
    "gallery": "com.coloros.gallery3d",
    "photos": "com.google.android.apps.photos",
    "facebook": "com.facebook.katana",
    "free fire": "com.dts.freefiremax",
    "instagram": "com.instagram.android",
    "spotify": "com.spotify.music",
    "telegram": "org.telegram.messenger",
    "settings": "com.android.settings",
    "contacts": "com.google.android.contacts",
}

KNOWN_ACTIVITIES = {
    "youtube": "com.google.android.youtube/.app.honeycomb.Shell$HomeActivity",
    "whatsapp": "com.whatsapp/.Main",
    "camera": "com.oplus.camera/.Camera",
    "gallery": "com.coloros.gallery3d/.app.MainActivity",
    "contacts": "com.google.android.contacts/com.android.contacts.activities.PeopleActivity",
}

PHONE_ACTIVITY = "com.android.contacts/.DialtactsActivityAlias"


def run_command(args):
    try:
        return subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=15
        )
    except Exception as e:
        print("Command error:", e)
        return None


def launch_component(component):
    result = run_command([
        "am", "start", "--user", "0",
        "-n", component
    ])

    if result is None:
        return False

    output = (result.stdout or "") + (result.stderr or "")
    print(output)

    return (
        result.returncode == 0
        and "Error:" not in output
        and "unable to resolve" not in output.lower()
    )


def open_app(app):
    if app == "phone":
        result = run_command([
            "am", "start", "--user", "0",
            "-n", PHONE_ACTIVITY,
            "-a", "android.intent.action.DIAL"
        ])
        return result is not None and result.returncode == 0

    if app == "gallery":
        return launch_component(
            "com.coloros.gallery3d/.app.MainActivity"
        )

    if app in KNOWN_ACTIVITIES:
        return launch_component(KNOWN_ACTIVITIES[app])

    package = PACKAGES.get(app)
    if not package:
        return False

    result = run_command([
        "cmd", "package", "resolve-activity",
        "--brief", "--user", "0",
        "-a", "android.intent.action.MAIN",
        "-c", "android.intent.category.LAUNCHER",
        "-p", package
    ])

    if result is None or result.returncode != 0:
        return False

    lines = [
        line.strip()
        for line in result.stdout.splitlines()
        if "/" in line and not line.startswith("priority=")
    ]

    if not lines:
        return False

    component = lines[-1]
    if not component.startswith(package + "/"):
        return False

    return launch_component(component)


def open_any_app(heard):
    text = heard.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = " ".join(text.split())

    for app, aliases in APPS.items():
        for alias in aliases:
            if alias.lower() in text:
                if open_app(app):
                    return f"Ji, {app} khol rahi hoon."

                return f"{app} nahi khul paya. App ya launcher check karein."

    return None


def find_contact(name):
    result = run_command(["termux-contact-list"])

    if result is None or result.returncode != 0:
        return None

    try:
        contacts = json.loads(result.stdout)
    except Exception:
        return None

    wanted = name.lower().strip()

    for contact in contacts:
        if contact.get("name", "").lower().strip() == wanted:
            return contact

    matches = [
        c for c in contacts
        if wanted and wanted in c.get("name", "").lower()
    ]

    if len(matches) == 1:
        return matches[0]

    return None


def call_contact(name):
    contact = find_contact(name)

    if not contact:
        return "Contact nahi mila ya ek se zyada naam match hue."

    number = contact.get("number", "").strip()

    if not number:
        return "Phone number nahi mila."

    result = run_command([
        "am", "start", "--user", "0",
        "-a", "android.intent.action.DIAL",
        "-d", "tel:" + number
    ])

    if result is None or result.returncode != 0:
        return "Dialer nahi khul paya."

    return f"{contact['name']} ka number dialer mein khol diya hai. Call button aap dabayein."


def whatsapp_message(name, message):
    contact = find_contact(name)

    if not contact:
        return "Contact nahi mila ya ek se zyada naam match hue."

    number = contact.get("number", "").strip()
    number = re.sub(r"[^0-9+]", "", number)

    if not number:
        return "Phone number nahi mila."

    if number.startswith("+"):
        number = number[1:]
    elif len(number) == 10:
        number = "91" + number
    elif len(number) == 11 and number.startswith("0"):
        number = "91" + number[1:]

    url = "https://wa.me/" + number + "?text=" + urllib.parse.quote(message)

    run_command([
        "am", "start", "--user", "0",
        "-a", "android.intent.action.VIEW",
        "-d", url
    ])

    return f"{contact['name']} ke liye WhatsApp message taiyar hai. Check karke Send dabayein."


def youtube_search(song):
    query = urllib.parse.quote(song)
    url = "https://www.youtube.com/results?search_query=" + query

    run_command([
        "am", "start", "--user", "0",
        "-a", "android.intent.action.VIEW",
        "-d", url
    ])

    return f"YouTube par {song} search kar rahi hoon."


def handle_command(heard):
    if not heard:
        return None

    text = heard.lower().strip()

    if any(word in text for word in [
        "youtube par", "youtube pe",
        "गाना खोजो", "song search"
    ]):
        song = text

        for word in [
            "youtube par", "youtube pe",
            "गाना खोजो", "song search",
            "search", "karo", "करो"
        ]:
            song = song.replace(word, "")

        if song.strip():
            return youtube_search(song.strip())

    call_match = re.search(
        r"(?:call|phone|कॉल)\s+(?:karo|करो)?\s*(.+)",
        text
    )

    if call_match:
        return call_contact(call_match.group(1).strip())

    msg_match = re.search(
        r"(?:whatsapp message|message|मैसेज)\s+(.+?)\s+(?:ko|को)\s+(.+)",
        text
    )

    if msg_match:
        return whatsapp_message(
            msg_match.group(1).strip(),
            msg_match.group(2).strip()
        )

    return open_any_app(text)
