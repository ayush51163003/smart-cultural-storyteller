import streamlit as st
import json
from io import BytesIO
from google.oauth2 import service_account
from google.cloud import texttospeech

# Load stories
with open('stories.json', 'r', encoding='utf-8') as f:
    STORIES = json.load(f)

# Load credentials from Streamlit Secrets
key_dict = json.loads(st.secrets["gcp_service_account"])
credentials = service_account.Credentials.from_service_account_info(key_dict)

# Initialize Cloud TTS
client = texttospeech.TextToSpeechClient(credentials=credentials)

def synthesize_story(text, lang_code):
    language_map = {"en": "en-IN", "hi": "hi-IN", "gu": "gu-IN"}
    
    ssml_text = """<speak><p><prosody pitch="x-high" rate="slow">{text}</prosody></p><break time="500ms"/></speak>"""
    
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_map.get(lang_code, "en-IN"),
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return BytesIO(response.audio_content)

def show_stories():
    lang = st.selectbox("Select Language", ['English', 'Hindi', 'Gujarati'])
    lang_code = 'en' if lang=='English' else 'hi' if lang=='Hindi' else 'gu'
    
    query = st.text_input("Search for a story (keywords or title):")
    
    for sid, sdata in STORIES.items():
        title = sdata['title']
        keywords = sdata.get('keywords', [])
        if query.lower() in title.lower() or any(query.lower() in k for k in keywords) or query == "":
            st.markdown(f"### {title}")
            if st.button(f"Listen to Story {sid}", key=sid):
                story_text = sdata['translations'].get(lang_code, sdata['translations'].get('en', 'Story not available'))
                st.write(story_text)
                audio_bytes = synthesize_story(story_text, lang_code)
                st.audio(audio_bytes)
