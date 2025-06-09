import threading  
import tkinter as tk  
from tkinter import scrolledtext, ttk  
import random  
import speech_recognition as sr  
import winsound  
import pyttsx3 
import datetime  
import requests  
from googletrans import Translator, LANGUAGES 
import re  
import wikipediaapi 
import os  
import ctypes  


engine = pyttsx3.init()


rate = engine.getProperty('rate')  
print(f"Current speech rate: {rate}") 
engine.setProperty('rate', 145)  


volume = engine.getProperty('volume')  
print(f"Current volume level: {volume}")  
engine.setProperty('volume', 1.0)  

def speak(text):
    """Convert text to speech and speak it out."""
    engine.say(text)  
    engine.runAndWait() 


wiki = wikipediaapi.Wikipedia('english')

def fetch_wikipedia_summary(query, max_sentences=2):
    """Fetch a summary of the Wikipedia page for the given query."""
    wiki = wikipediaapi.Wikipedia('english', extract_format=wikipediaapi.ExtractFormat.WIKI)  
    page = wiki.page(query) 
    if page.exists():  
        summary = page.summary.split('. ')[:max_sentences]  
        summary_text = '. '.join(summary)  
        return summary_text + "."  
    else:
        return f"Sorry, I couldn't find any information on '{query}' on Wikipedia."  

intents = {
    'greeting': ['hello', 'hi', 'hey'],
    'farewell': ['bye', 'goodbye'],
    'gratitude': ['thank you', 'thanks'],
    'query': ['how are you', 'what are you doing'],
    'weather': ['weather', 'temperature', 'forecast'],
    'time': ['time', 'current time'],
    'date': ['date', 'current date', "Date"],
    'reminder': ['reminder', 'remind me'],
    'joke': ['joke', 'tell me a joke'],
    'fact': ['fact', 'interesting fact'],
    'meaning': ['meaning of'],
    'translate': ['translate'],
    'who_are_you': ['who are you', 'what is your name', 'who r u'],
    'what is your name': ['What is your name?', 'what is ur name'],
    'wikipedia': ['wikipedia', 'wiki', 'information', 'search'],
    'lock': ['lock windows', 'lock']
}


responses = {
    'wikipedia': ['Here is some information from Wikipedia:', 'I found this on Wikipedia:', 'According to Wikipedia:'],
    'greeting': ['Hi there!', 'Hello!', 'Hey!'],
    'farewell': ['Goodbye!', 'See you later!', 'Bye!'],
    'gratitude': ['You\'re welcome!', 'No problem!', 'My pleasure!'],
    'query': ['I\'m doing well, thank you!', 'Just assisting you!', 'Feeling great, thank you for asking!'],
    'weather': ['The weather is sunny today.', 'It\'s cloudy with a chance of rain.'],
    'time': ['The current time is ' + datetime.datetime.now().strftime("%I:%M %p")],  
    'date': ['Today, the date is: ' + datetime.datetime.now().strftime("%d %B %Y")],  
    'reminder': ['Sure, I will remind you.', 'Reminder set successfully.'],
    'joke': ['Why don\'t scientists trust atoms? Because they make up everything!', 'I\'m reading a book on anti-gravity. It\'s impossible to put down!'],
    'fact': ['Did you know that the shortest war in history was between Britain and Zanzibar on August 27, 1896? It lasted only 38 minutes!'],
    'translate': ['Can you please provide a specific word or sentence to translate and the specified language.'],
    'who_are_you': ['I am Atlas, your Female AI assistant.'],
    'what is your name': ['My name is Atlas.']
}


def lock_windows():
    ctypes.windll.user32.LockWorkStation()  

def fetch_word_meaning(word):
    """Fetch the meaning of a word from a dictionary API."""
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'  
    response = requests.get(url)  
    data = response.json()  
    if isinstance(data, list) and 'meanings' in data[0]:  
        meanings = data[0]['meanings']  
        definition = [meaning['definitions'][0]['definition'] for meaning in meanings]  
        return " ".join(definition)  
    else:
        return "Sorry, I couldn't find the meaning of that word."  

def translate_text(text, dest_language):
    """Translate the given text to the specified language."""
    translator = Translator()  
    translated_text = translator.translate(text, dest_language).text  
    return translated_text  

def fetch_weather(location):
    """Fetch the current weather for a given location."""
    api_key = '7e760b7138d38407c12adc03973acb37'  
    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'  
    response = requests.get(url)  
    data = response.json()  
    if data['cod'] == 200:  
        weather = data['weather'][0]['description']  
        temperature = data['main']['temp']  
        return f"The current weather in {location} is {weather} with a temperature of {temperature}°C."  
    else:
        return "Sorry, I couldn't fetch the weather for that location."  
def process_command(command):
    """Process text commands given by the user."""
    command = command.lower()  
    found_intent = False  
    
    
    if 'lock' in command:
        found_intent = True  
        speak("locking your device") 
        lock_windows() 
        display_response("User: " + command + "\n" + "Atlas: Windows locked." + "\n\n")  
    
    
    meaning_match = re.search(r'meaning of (\w+)', command)  
    if meaning_match:
        found_intent = True  
        word = meaning_match.group(1)  
        meaning = fetch_word_meaning(word)  
        speak(meaning)  
        display_response("User: " + command + "\n" + "Atlas: " + meaning + "\n\n")  
    
    
    translate_match = re.search(r'translate (.+) to (\w+)', command)  
    if translate_match:
        found_intent = True  
        text_to_translate = translate_match.group(1)  
        dest_language = translate_match.group(2)  

        
        if dest_language in LANGUAGES.values():
            translated_text = translate_text(text_to_translate, dest_language)
        else:
            dest_language_code = next((code for code, lang in LANGUAGES.items() if lang == dest_language), None)
            if dest_language_code:
                translated_text = translate_text(text_to_translate, dest_language_code)
            else:
                translated_text = f"Sorry, I don't recognize the language '{dest_language}'."

        speak(translated_text)  
        display_response("User: " + command + "\n" + "Atlas: " + translated_text + "\n\n")  
    
    
    weather_match = re.search(r'weather in (\w+)', command)  
    if weather_match:
        found_intent = True  
        location = weather_match.group(1)  
        weather = fetch_weather(location)  
        display_response("User: " + command + "\n" + "Atlas: " + weather + "\n\n")  
    
    
    if 'wikipedia' in command:
        found_intent = True  
        query = command.replace('wikipedia', '').strip()  


        summary = fetch_wikipedia_summary(query)  
        speak(summary)  
        display_response("User: " + command + "\n" + "Atlas: " + summary + "\n\n")  
    
   
    if not found_intent:  
        for intent, keywords in intents.items():  
            if any(keyword in command for keyword in keywords):  
                found_intent = True  
                response = random.choice(responses[intent])  
                speak(response) 
                display_response("User: " + command + "\n" + "Atlas: " + response + "\n\n")  
                break  
    
    if not found_intent:  
        response = "Sorry, I didn't understand the command"  
        speak(response)  
        display_response("User: " + command + "\n" + "Atlas: " + response + "\n\n")  





#GUI from here(line 107 separate)
def display_response(response):
    """Display user input and Atlas response in the GUI."""
    conversation_log.tag_configure("user", justify='left')  
    conversation_log.tag_configure("atlas", justify='right')  

    if response.startswith("User:"): 
        conversation_log.insert(tk.END, response, "user")  
    elif response.startswith("Atlas:"):  
        conversation_log.insert(tk.END, response, "atlas")  
    conversation_log.insert(tk.END, "\n")  
    conversation_log.see(tk.END)  


WAKE_WORD = "atlas"  
STOP_WORD = "stop"  
listening = False  

def wake_up():
    """Activate listening mode."""
    global listening  
    listening = True  
    play_beep_sound()  
    speak("Yes, how can I help you?")  

def sleep():
    """Deactivate listening mode."""
    global listening  
    listening = False  
    speak("Goodbye!")  

def process_voice_commands():
    """Process voice commands using speech recognition."""
    global listening  
    recognizer = sr.Recognizer()  
    with sr.Microphone() as source:  
        recognizer.adjust_for_ambient_noise(source)  
        
        while True:  
            if not listening:  
                print("Listening for the wake word...")  
                audio = recognizer.listen(source, timeout=5)  
                print("Recognizing wake word...")  
                try:
                    command = recognizer.recognize_google(audio).lower()  
                    print("You said:", command)  
                    if WAKE_WORD in command:  
                        wake_up()  
                except sr.UnknownValueError:
                    pass  
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")  
            else: 
                print("Listening for commands...")  
                audio = recognizer.listen(source)  
                print("Recognizing command...")  
                try:
                    command = recognizer.recognize_google(audio).lower()  
                    print("You said:", command)  
                    if STOP_WORD in command:  
                        sleep()  
                    else:
                        process_command(command)  
                except sr.UnknownValueError:
                    print("Could not understand audio")  
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")  

def play_beep_sound():
    """Play a beep sound."""
    winsound.Beep(500, 100)  




style = ttk.Style()  
style.theme_use('clam') 
style.configure("response.TLabel", font=("Helvetica", 12), wraplength=600)  


conversation_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30, font=("Helvetica", 12))  
conversation_log.grid(column=0, row=0, padx=10, pady=10)  


threading.Thread(target=process_voice_commands).start()  

root.mainloop()  





