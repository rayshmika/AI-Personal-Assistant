import spacy

nlp = spacy.load("en_core_web_sm")

def get_intent(command, last_intent=None):
    command = command.lower()

    # Small talk
    if any(phrase in command for phrase in ["hello", "hi", "hey", "howdy"]):
        return "small_talk"
    elif any(phrase in command for phrase in ["bye", "goodbye", "see you"]):
        return "exit"
    elif any(phrase in command for phrase in ["how are you", "how's it going"]):
        return "small_talk"
    elif any(phrase in command for phrase in ["tell me a joke", "what can you do", "who are you", "compliment", "fun fact"]):
        return "small_talk"
    elif last_intent == "small_talk" and any(phrase in command for phrase in ["good", "great", "fine", "not bad", "doing well"]):
        return "small_talk"

    # Functional tasks
    elif "email" in command:
        return "send_email"
    elif "reminder" in command or "remind me" in command:
        return "set_reminder"
    elif "schedule" in command or "meeting" in command or "appointment" in command:
        return "schedule_appointment"
    elif "search" in command or "google" in command:
        return "web_search"
    elif "news" in command or "headlines" in command:
        return "news_update"
    elif "weather" in command or "temperature" in command or "forecast" in command:
        return "weather_update"
    elif "exit" in command or "quit" in command:
        return "exit"

    return "unknown"
