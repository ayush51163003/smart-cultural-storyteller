import streamlit as st
import json
from io import BytesIO

# Google Cloud TTS
from google.cloud import texttospeech

# Load stories
with open('stories.json', 'r', encoding='utf-8') as f:
    STORIES = json.load(f)

# Initialize Google Cloud TTS client
# Make sure you have uploaded your service account JSON key in Streamlit secrets or path
client = texttospeech.TextToSpeechClient.from_service_account_json("service_account_key.json")

def synthesize_story(text, lang_code):
    # Map language code for Google Cloud TTS
    language_map = {"en": "en-IN", "hi": "hi-IN", "gu": "gu-IN"}
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_map.get(lang_code, "en-IN"),
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return BytesIO(response.audio_content)

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
                
                # Cloud TTS
                audio_bytes = synthesize_story(story_text, lang_code)
                st.audio(audio_bytes)
