# app_modern.py
import streamlit as st
import json
from google.cloud import texttospeech
from google.oauth2 import service_account
from io import BytesIO

# ------------------ Setup ------------------
st.set_page_config(page_title="Smart Cultural Storyteller", layout="wide")
st.markdown("<h1 style='text-align:center;color:navy;'>Smart Cultural Storyteller</h1>", unsafe_allow_html=True)

# Load GCP credentials from secrets
key_dict = json.loads(st.secrets["gcp_service_account"])
credentials = service_account.Credentials.from_service_account_info(key_dict)
tts_client = texttospeech.TextToSpeechClient(credentials=credentials)

# ------------------ Sidebar ------------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Login", "Stories", "Favorites", "About"])

languages = ["English", "Hindi", "Gujarati"]

# ------------------ Login Page ------------------
if menu == "Login":
    st.sidebar.subheader("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username and password:
            st.success(f"Welcome {username}!")
        else:
            st.error("Enter username & password")

# ------------------ Stories Page ------------------
elif menu == "Stories":
    st.sidebar.subheader("Filter Stories")
    selected_lang = st.sidebar.selectbox("Language", languages)

    # Load stories from JSON
    with open("stories.json", "r") as f:
        STORIES = json.load(f)

    search_query = st.sidebar.text_input("Search Story")
    filtered_stories = [s for s in STORIES if search_query.lower() in s["title"].lower()]

    # Display stories in card format
    for story in filtered_stories:
        st.markdown(f"### {story['title']}")
        st.markdown(f"*{story['description']}*")
        lang_text = story.get(selected_lang, story["English"])
        if st.button(f"Play {selected_lang} Voice for '{story['title']}'"):
            # Generate TTS
            input_text = texttospeech.SynthesisInput(text=lang_text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US" if selected_lang=="English" else "hi-IN",
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            response = tts_client.synthesize_speech(
                input=input_text, voice=voice, audio_config=audio_config
            )
            st.audio(BytesIO(response.audio_content), format="audio/mp3")

# ------------------ Favorites ------------------
elif menu == "Favorites":
    st.subheader("Your Favorite Stories")
    st.info("Add your favorite stories feature coming soon!")

# ------------------ About ------------------
elif menu == "About":
    st.subheader("About Smart Cultural Storyteller")
    st.markdown(
        """
        - Multi-language AI storytelling app
        - Google Cloud TTS for natural voice
        - Built with Python & Streamlit
        - Preserves Indian cultural heritage
        """
    )
