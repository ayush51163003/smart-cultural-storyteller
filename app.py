# This version of the project uses Streamlit for deployment and shows multi-language stories in text format.
# No audio playback is included, making it simpler for Streamlit Cloud deployment.

## `app.py`

import streamlit as st
import streamlit as st
import json
from gtts import gTTS
import base64
import os 

text = "Your story text here"
print(text)

# After the story text is displayed
if text:
    st.write(text)
    tts = gTTS(text, lang=lang_code)
    tts.save("story.mp3")

    # Convert to base64 for playback in Streamlit
    with open("story.mp3", "rb") as f:
        audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3")

# Load stories from JSON file
with open('stories.json', 'r', encoding='utf-8') as f:
    STORIES = json.load(f)

# Set Streamlit page config
st.set_page_config(page_title="Smart Cultural Storyteller", page_icon="📖")

# App title
st.title("📖 Smart Cultural Storyteller")

# App description
st.markdown("""
Welcome to the Smart Cultural Storyteller! 🎉

This app displays multi-language cultural stories in text format. Audio playback is not included in this version, making it simpler for Streamlit Cloud deployment.
""")

# Language selection dropdown
lang = st.selectbox("Select Language", ['English', 'Hindi', 'Gujarati'])
lang_code = 'en' if lang == 'English' else 'hi' if lang == 'Hindi' else 'gu'

st.write(f"Selected language: {lang}")

# Display available stories
st.subheader("Available Stories")
for sid, sdata in STORIES.items():
    st.markdown(f"### {sdata['title']}")
    if st.button(f"Read Story {sid}", key=sid):
        text = sdata['translations'].get(lang_code, sdata['translations'].get('en', 'Story not available'))
        st.write(text)

