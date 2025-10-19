import streamlit as st
import json
from gtts import gTTS
from io import BytesIO

# Load stories
with open('stories.json', 'r', encoding='utf-8') as f:
    STORIES = json.load(f)

def show_stories():
    # Language selection
    lang = st.selectbox("Select Language", ['English', 'Hindi', 'Gujarati'])
    lang_code = 'en' if lang=='English' else 'hi' if lang=='Hindi' else 'gu'
    
    # Search box
    query = st.text_input("Search for a story (title keywords):")
    
    # Display stories
    for sid, sdata in STORIES.items():
        title = sdata['title']
        if query.lower() in title.lower() or query == "":
            st.markdown(f"### {title}")
            if st.button(f"Read Story {sid}", key=sid):
                story_text = sdata['translations'].get(lang_code, sdata['translations'].get('en', 'Story not available'))
                st.write(story_text)
                
                # Voice narration
                tts = gTTS(text=story_text, lang=lang_code)
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes)
