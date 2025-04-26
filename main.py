from assistant import listen, get_text_input, speak, handle_set_reminder, handle_small_talk, assistant_handle_send_email, handle_web_search, handle_news, handle_weather
from nlp_module import get_intent
from weather_module import get_weather
from news_module import get_news

speak("Hello! I'm your assistant. Would you like to speak or type your commands?")

# Ask only once
user_choice = input("Would you like to speak or type? (s/t): ").strip().lower()
if user_choice not in ['s', 't']:
    speak("I didn't get that, so we'll use typing for now.")
    user_choice = 't'

def get_command():
    if user_choice == 's':
        return listen()
    else:
        return get_text_input("")

speak("I'm ready whenever you are!")
last_intent = None

while True:
    command = get_command()
    if not command:
        continue
    intent = get_intent(command, last_intent=last_intent)
    print("Intent recognized:", intent)

    if intent == "send_email":
        assistant_handle_send_email(input_method=user_choice)
    elif intent == "set_reminder":
        handle_set_reminder(input_method=user_choice)
    elif intent == "schedule_appointment":
        speak("Sure! I’ll help you with that soon.")
    elif intent == "web_search":
        handle_web_search(command)
    elif intent == "weather_update":
        location = get_text_input("Which location?")
        weather_info = get_weather(location)
        speak(weather_info)
    elif intent == "news_update":
        topic = get_text_input("Which topic or country do you want news about?")
        news_info = get_news(query=topic if len(topic) > 2 else None, country=topic if len(topic) == 2 else "us")
        speak(news_info)
    elif intent == "exit":
        speak("It was great talking to you. Bye!")
        break
    elif intent == "small_talk":
        response = handle_small_talk(command)
        speak(response)
    else:
        speak("Hmm, I’m not sure what you meant. Could you say that again?")

    # Ask for the next command naturally
    last_intent = intent
    speak("What would you like me to do next?")
