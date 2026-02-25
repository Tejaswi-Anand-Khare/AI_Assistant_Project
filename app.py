import streamlit as st
import random
import datetime
import requests
import re
import wikipediaapi
from deep_translator import GoogleTranslator

# ------------------------
# PAGE CONFIG (Dark style)
# ------------------------
st.set_page_config(page_title="Atlas AI", page_icon="🤖", layout="centered")

# ------------------------
# WIKIPEDIA
# ------------------------
wiki = wikipediaapi.Wikipedia(
    user_agent="AtlasAI/1.0",
    language="en"
)

def fetch_wikipedia_summary(query):
    page = wiki.page(query)
    if page.exists():
        return page.summary[:400]
    return "No Wikipedia result found."

# ------------------------
# TOOLS
# ------------------------
def fetch_word_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    data = requests.get(url).json()
    if isinstance(data, list):
        return data[0]["meanings"][0]["definitions"][0]["definition"]
    return "Meaning not found."

def translate_text(text, lang):
    try:
        return GoogleTranslator(source='auto', target=lang).translate(text)
    except:
        return "Translation failed."

# ------------------------
# AI LOGIC
# ------------------------
def process_command(command):
    command = command.lower()

    meaning = re.search(r"meaning of (\w+)", command)
    if meaning:
        return fetch_word_meaning(meaning.group(1))

    translate = re.search(r"translate (.+) to (\w+)", command)
    if translate:
        return translate_text(translate.group(1), translate.group(2))

    if "time" in command:
        return datetime.datetime.now().strftime("%I:%M %p")

    if "date" in command:
        return datetime.datetime.now().strftime("%d %B %Y")

    if "joke" in command:
        return random.choice([
            "Why don’t scientists trust atoms? Because they make up everything!",
            "I told my computer I needed a break, it said no problem — it will go to sleep."
        ])

    if "wikipedia" in command:
        query = command.replace("wikipedia", "")
        return fetch_wikipedia_summary(query)

    return "I didn't understand that yet."

# ------------------------
# CHAT MEMORY
# ------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Atlas AI Assistant")

# ------------------------
# SHOW CHAT HISTORY
# ------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------------
# USER INPUT
# ------------------------
if prompt := st.chat_input("Ask Atlas anything..."):

    # show user
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # AI response
    response = process_command(prompt)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.markdown(response)

        # -------- Browser TTS ----------
        st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{response}");
        window.speechSynthesis.speak(msg);
        </script>
        """, height=0)
