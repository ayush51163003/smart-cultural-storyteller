# This version of the project uses Streamlit for deployment and shows multi-language stories in text format.
# No audio playback is included, making it simpler for Streamlit Cloud deployment.

## `app.py`

import streamlit as st
import streamlit as st
import json

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
