import streamlit as st
import sqlite3
from groq import Groq
from streamlit_mic_recorder import mic_recorder

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Quagmire",
    page_icon="🤖",
    layout="centered"
)

# --------------------------------
# GROQ CLIENT (LLAMA ONLINE)
# --------------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --------------------------------
# DATABASE (PERSISTENT MEMORY)
# --------------------------------
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

# --------------------------------
# LOAD HISTORY
# --------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
    rows = c.execute("SELECT role, content FROM chats").fetchall()

    for role, content in rows:
        st.session_state.messages.append(
            {"role": role, "content": content}
        )

# --------------------------------
# SAVE FUNCTION
# --------------------------------
def save_message(role, content):
    c.execute(
        "INSERT INTO chats (role, content) VALUES (?,?)",
        (role, content)
    )
    conn.commit()

# --------------------------------
# STREAMING LLM
# --------------------------------
def ask_llm(prompt):
    return client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system",
             "content": "You are Quagmire, a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )

# --------------------------------
# UI TITLE
# --------------------------------
st.title("🤖 Quagmire")

# --------------------------------
# SHOW CHAT HISTORY
# --------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------
# BROWSER VOICE INPUT (NEW)
# --------------------------------
st.markdown("### 🎤 Voice Input")

voice_html = """
<button onclick="startRecognition()">Start Voice Input</button>

<script>
function startRecognition() {
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.start();

    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;

        const streamlitDoc = window.parent.document;
        const textarea = streamlitDoc.querySelector('textarea');

        if(textarea){
            textarea.value = text;
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
        }
    };
}
</script>
"""

st.components.v1.html(voice_html, height=80)

# --------------------------------
# OPTIONAL MIC RECORDER (kept)
# --------------------------------
audio = mic_recorder(
    start_prompt="🎤 Speak",
    stop_prompt="Stop",
    key="mic"
)

if audio:
    st.info("Voice captured.")

# --------------------------------
# USER INPUT
# --------------------------------
if prompt := st.chat_input("Ask Quagmire anything..."):

    # USER MESSAGE
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    save_message("user", prompt)

    with st.chat_message("user"):
        st.markdown(prompt)

    # ASSISTANT RESPONSE
    with st.chat_message("assistant"):

        stream = ask_llm(prompt)

        full_response = ""
        placeholder = st.empty()

        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full_response += delta
            placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

        # Browser TTS (VOICE OUTPUT)
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
