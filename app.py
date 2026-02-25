import streamlit as st
import random
import datetime
import requests
from googletrans import Translator, LANGUAGES
import re
import wikipediaapi

# ------------------------
# Wikipedia
# ------------------------
wiki = wikipediaapi.Wikipedia('english')

def fetch_wikipedia_summary(query, max_sentences=2):
    page = wiki.page(query)
    if page.exists():
        summary = page.summary.split('. ')[:max_sentences]
        return '. '.join(summary) + "."
    return "Sorry, I couldn't find it."

# ------------------------
# APIs
# ------------------------
def fetch_word_meaning(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(url)
    data = response.json()
    if isinstance(data, list):
        meanings = data[0]['meanings']
        definition = [m['definitions'][0]['definition'] for m in meanings]
        return " ".join(definition)
    return "Meaning not found."

def translate_text(text, dest_language):
    translator = Translator()
    return translator.translate(text, dest=dest_language).text

def fetch_weather(location):
    api_key = "YOUR_API_KEY"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") == 200:
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"{location}: {weather}, {temp}°C"
    return "Weather not found."

# ------------------------
# Intents
# ------------------------
intents = {
    "greeting": ["hello","hi","hey"],
    "time": ["time"],
    "date": ["date"],
    "joke": ["joke"],
}

responses = {
    "greeting": ["Hi there!", "Hello!", "Hey!"],
    "time": ["Current time: " + datetime.datetime.now().strftime("%I:%M %p")],
    "date": ["Today is " + datetime.datetime.now().strftime("%d %B %Y")],
    "joke": ["Why don’t scientists trust atoms? Because they make up everything!"]
}

# ------------------------
# MAIN AI LOGIC
# ------------------------
def process_command(command):
    command = command.lower()

    meaning_match = re.search(r'meaning of (\w+)', command)
    if meaning_match:
        return fetch_word_meaning(meaning_match.group(1))

    translate_match = re.search(r'translate (.+) to (\w+)', command)
    if translate_match:
        text = translate_match.group(1)
        lang = translate_match.group(2)
        return translate_text(text, lang)

    weather_match = re.search(r'weather in (\w+)', command)
    if weather_match:
        return fetch_weather(weather_match.group(1))

    if "wikipedia" in command:
        query = command.replace("wikipedia","").strip()
        return fetch_wikipedia_summary(query)

    for intent, keywords in intents.items():
        if any(k in command for k in keywords):
            return random.choice(responses[intent])

    return "Sorry, I didn't understand."

# ------------------------
# STREAMLIT UI (LIVE PART)
# ------------------------
st.title("Quagmire AI Assistant 🤖")

user_input = st.text_input("Ask Quagmire something:")

if user_input:
    response = process_command(user_input)
    st.write("**Quagmire:**", response)
