import streamlit as st
import sqlite3
from openai import OpenAI
from streamlit_mic_recorder import mic_recorder

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Atlas AI",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# OPENAI CLIENT
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# DATABASE (PERSISTENT MEMORY)
# -----------------------------
conn = sqlite3.connect("memory.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS chats(
id INTEGER PRIMARY KEY AUTOINCREMENT,
role TEXT,
content TEXT
)
""")
conn.commit()

# -----------------------------
# LOAD CHAT HISTORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

    rows = c.execute("SELECT role, content FROM chats").fetchall()
    for role, content in rows:
        st.session_state.messages.append(
            {"role": role, "content": content}
        )

# -----------------------------
# SAVE MESSAGE FUNCTION
# -----------------------------
def save_message(role, content):
    c.execute(
        "INSERT INTO chats (role, content) VALUES (?,?)",
        (role, content)
    )
    conn.commit()

# -----------------------------
# LLM STREAMING FUNCTION
# -----------------------------
def ask_llm(prompt):
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are Atlas, a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )

# -----------------------------
# UI TITLE
# -----------------------------
st.title("🤖 Atlas AI Assistant")

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# VOICE INPUT
# -----------------------------
audio = mic_recorder(
    start_prompt="🎤 Speak",
    stop_prompt="Stop Recording",
    key="recorder"
)

if audio:
    st.info("Voice captured (speech-to-text can be added later).")

# -----------------------------
# USER INPUT
# -----------------------------
if prompt := st.chat_input("Ask Atlas anything..."):

    # USER MESSAGE
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    save_message("user", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    # ASSISTANT MESSAGE
    with st.chat_message("assistant"):

        stream = ask_llm(prompt)

        full_response = ""
        placeholder = st.empty()

        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full_response += delta
            placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

        # Browser TTS
        st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance({repr(full_response)});
        window.speechSynthesis.speak(msg);
        </script>
        """, height=0)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
    save_message("assistant", full_response)
