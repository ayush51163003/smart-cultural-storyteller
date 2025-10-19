import json
import streamlit as st
from google.oauth2 import service_account
from google.cloud import texttospeech
from io import BytesIO

# Load credentials from Streamlit Secrets
key_dict = json.loads(st.secrets["gcp_service_account"])
credentials = service_account.Credentials.from_service_account_info(key_dict)

# Initialize TTS client
client = texttospeech.TextToSpeechClient(credentials=credentials)

def synthesize_story(text, lang_code):
    language_map = {"en": "en-IN", "hi": "hi-IN", "gu": "gu-IN"}
    
    ssml_text = f"""
    <speak>
        <p><prosody pitch="x-high" rate="slow">{text}</prosody></p>
        <break time="500ms"/>
    </speak>
    """
    
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_map.get(lang_code, "en-IN"),
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return BytesIO(response.audio_content)

