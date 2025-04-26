import pyttsx3
import dateparser, random
import webbrowser, urllib.parse, requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import speech_recognition as sr
from send_email import send_email
from google_calendar import create_event

# Initialize the TTS engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech and speak it."""
    print(text)
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice input and return the text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

def get_text_input(prompt):
    """Get text input from the user with proper prompt and speech."""
    speak(prompt)
    return input(f"{prompt}\n> ")

def assistant_handle_send_email(input_method='t'):
    def get_input(prompt):
        if input_method == 't':
            speak(prompt)
            return input(f"{prompt}\n> ")
        else:
            speak(prompt)
            return listen()

    to_email = get_input("Who should I send the email to?")
    subject = get_input("What should be the subject of the email?")
    body = get_input("What should I include in the body of the email?")

    send_email(to_email, subject, body)

def handle_set_reminder(input_method='t'):
    def get_input(prompt):
        return get_text_input(prompt) if input_method == 't' else (speak(prompt) or listen())

    message = get_input("What should I remind you about?")
    time_input = get_input("When should I remind you?")

    parsed_time = dateparser.parse(time_input)

    if parsed_time:
        formatted_time = parsed_time.strftime("%Y-%m-%d %H:%M")
        create_event(message, parsed_time)
        speak(f"✅ Reminder set for {formatted_time}")
        print(f"Reminder set for {formatted_time}: {message}")
    else:
        speak("Sorry, I couldn't understand the time you said. Please try again.")


def analyze_sentiment(command):
    """Analyze sentiment and categorize as positive, negative, or neutral."""
    blob = TextBlob(command)
    sentiment = blob.sentiment.polarity  # Sentiment polarity ranges from -1 to 1

    if sentiment > 0:
        return "positive"
    elif sentiment < 0:
        return "negative"

def handle_small_talk(command):
    """Handles simple conversations and casual talk."""
    
    # Analyzing sentiment
    sentiment = analyze_sentiment(command)
    
    # Responses based on sentiment
    if sentiment == "positive":
        sentiment_response = "You're in a great mood today! 😄"
    elif sentiment == "negative":
        sentiment_response = "I'm sorry you're feeling down. How can I help? 😔"
    else:
        sentiment_response = "How can I assist you? 🤔"
    
    greetings = ["hi", "hello", "hey", "howdy", "hiya"]
    farewells = ["bye", "goodbye", "see you", "take care", "catch you later"]
    how_are_you = ["how are you", "how's it going", "how are you doing"]
    compliments = ["you're awesome", "you're great", "I like your style", "you're amazing"]

    # Responses to greetings
    if any(greeting in command.lower() for greeting in greetings):
        return random.choice([
            "Hi there! How can I assist you today?",
            "Hello! What can I do for you today?",
            "Hey! How's your day going?",
            "Howdy! What can I help you with?"
        ]) + " " + sentiment_response
    
    # Responses to farewells
    elif any(farewell in command.lower() for farewell in farewells):
        return random.choice([
            "Goodbye! Take care! 😄",
            "See you later! Have a wonderful day!",
            "Catch you later! 😎",
            "Goodbye! Don't hesitate to come back for help!"
        ]) + " " + sentiment_response
    
    # Responses to "How are you?"
    elif any(phrase in command.lower() for phrase in how_are_you):
        return random.choice([
            "I'm doing great! Thanks for asking. How about you?",
            "I'm operating at full capacity! How are you?",
            "I'm fantastic! How's everything going with you?",
            "I'm doing wonderfully! What's up with you?"
        ]) + " " + sentiment_response
    
    # Responses to compliments
    elif any(phrase in command.lower() for phrase in compliments):
        return random.choice([
            "Aw, thanks! You're pretty awesome yourself! 😁",
            "You're making me blush! 😅 Thanks!",
            "You're too kind! Keep those compliments coming! 😎",
            "I appreciate that! You're great too! 😄"
        ]) + " " + sentiment_response
    
    # Jokes
    elif "tell me a joke" in command.lower():
        return random.choice([
            "Why don’t skeletons fight each other? They don’t have the guts.",
            "I told my computer I needed a break, and now it won’t stop sending me KitKats.",
            "Why was the math book sad? Because it had too many problems.",
            "I’m reading a book on anti-gravity. It’s impossible to put down!",
            "I used to play piano by ear, but now I use my hands."
        ]) + " " + sentiment_response
    
    # Responses for "What can you do?"
    elif "what can you do" in command.lower():
        return random.choice([
            "I can send emails, set reminders, schedule appointments, search the web, and much more!",
            "I can do a lot of things! Just tell me what you need, and I'll try to help.",
            "I can assist you with emails, reminders, setting appointments, and much more!",
            "I have a variety of tasks I can do, from sending emails to setting reminders. Just ask!"
        ]) + " " + sentiment_response

    # Fun facts
    elif "tell me a fun fact" in command.lower():
        return random.choice([
            "Did you know? Honey never spoils! Archaeologists have found pots of honey in ancient tombs that are over 3,000 years old.",
            "Here's a fun fact: A group of flamingos is called a 'flamboyance.'",
            "Did you know that octopuses have three hearts? That's a lot of love!",
            "Fun fact: There are more stars in the universe than grains of sand on all the Earth's beaches combined!"
        ]) + " " + sentiment_response

    # Responses for "Who are you?"
    elif "who are you" in command.lower():
        return random.choice([
            "I am your personal assistant, here to make your life easier!",
            "I am your friendly AI assistant, always ready to help you with whatever you need.",
            "I am your virtual helper, here to assist you with tasks, reminders, and much more!",
            "I’m your personal assistant! Need help with anything?"
        ]) + " " + sentiment_response

    # Default response if no small talk recognized
    else:
        return None  # Proceed with task-specific intents if no small talk is recognized

def handle_web_search(command):
    """Search DuckDuckGo and show title, snippet, and real link, with selection."""
    if "search for" in command:
        query = command.split("search for")[-1]
    elif "search" in command:
        query = command.split("search")[-1]
    elif "google" in command:
        query = command.split("google")[-1]
    else:
        query = command

    query = query.strip()
    if not query:
        speak("What would you like me to search for?")
        return

    url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for result in soup.find_all('a', class_='result__a', href=True):
        title = result.get_text().strip()
        href = result['href']
        
        # Decode redirect to get real URL
        parsed_href = urllib.parse.urlparse(href)
        query_params = urllib.parse.parse_qs(parsed_href.query)
        real_url = query_params.get('uddg', [href])[0]

        # Extract snippet (description) from the result block
        snippet_tag = result.find_parent().find_next_sibling('a', class_='result__snippet')
        snippet = snippet_tag.get_text().strip() if snippet_tag else "No description available."

        results.append((title, real_url, snippet))

    if not results:
        speak("Sorry, I couldn’t find any results.")
        return

    speak(f"Here are some results for {query}:")
    for idx, (title, link, snippet) in enumerate(results[:5], start=1):
        print(f"{idx}. {title}\n   {link}\n   {snippet}\n")

    choice = input("Enter the number of the result you'd like to open, or 'n' to skip:\n> ")
    if choice.isdigit():
        index = int(choice)
        if 1 <= index <= len(results[:5]):
            selected = results[index - 1]
            speak(f"Opening {selected[0]}")
            webbrowser.open(selected[1])
        else:
            speak("That number is out of range.")
    else:
        speak("Okay, skipping it.")

def handle_weather():
    speak("Fetching current weather...")
    url = "https://wttr.in/?format=3"
    try:
        response = requests.get(url)
        weather = response.text
        speak(weather)
    except Exception as e:
        speak("Sorry, I couldn't fetch the weather right now.")
        print(e)

def handle_news():
    speak("Here are the top news headlines:")
    query = "top news India site:news.google.com"
    try:
        results = list(search(query, num_results=5))
        for i, link in enumerate(results, 1):
            print(f"{i}. {link}")
            speak(f"News {i}: {link}")
    except Exception as e:
        speak("Sorry, I couldn't fetch news right now.")
        print(e)
