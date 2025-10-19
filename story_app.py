import streamlit as st
import json
from io import BytesIO
from google.cloud import texttospeech

# Load stories
with open('stories.json', 'r', encoding='utf-8') as f:
    STORIES = json.load(f)

# Google Cloud TTS client
client = texttospeech.TextToSpeechClient.from_service_account_json("service_account_key.json")

def synthesize_story(text, lang_code):
    language_map = {"en": "en-IN", "hi": "hi-IN", "gu": "gu-IN"}

    # Wrap text in SSML with prosody for pitch & speed
    ssml_text = f"""
    <speak>
        <p><prosody pitch="x-high" rate="slow">{text}</prosody></p>
        <break time="500ms"/>
    </speak>
    """

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)  # Use SSML

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

    query = st.text_input("Search for a story (title keywords):")
    
    for sid, sdata in STORIES.items():
        title = sdata['title']
        if query.lower() in title.lower() or query == "":
            st.markdown(f"### {title}")
            if st.button(f"Read Story {sid}", key=sid):
                story_text = sdata['translations'].get(lang_code, sdata['translations'].get('en', 'Story not available'))
                st.write(story_text)
                audio_bytes = synthesize_story(story_text, lang_code)
                st.audio(audio_bytes)
