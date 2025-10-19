# app_upgraded.py
import streamlit as st
import json
from io import BytesIO
from google.cloud import texttospeech
from google.oauth2 import service_account

# ------------------ Page Setup ------------------
st.set_page_config(page_title="Smart Cultural Storyteller", layout="wide")
st.markdown("<h1 style='text-align:center;color:navy;'>Smart Cultural Storyteller</h1>", unsafe_allow_html=True)

# ------------------ Session State ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ------------------ Sidebar ------------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Login", "Stories", "Favorites", "About"])
languages = ["English", "Hindi", "Gujarati"]

# ------------------ Login Page ------------------
if menu == "Login":
    st.subheader("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Example credentials, replace with proper auth or stauth
        if username == "ayush" and password == "12345":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password")

# ------------------ Stories Page ------------------
elif menu == "Stories":
    if not st.session_state.logged_in:
        st.warning("Please login to access stories.")
        st.stop()

    st.sidebar.subheader("Filter Stories")
    selected_lang = st.sidebar.selectbox("Language", languages)
    
   # Load stories safely
with open("stories.json", "r", encoding="utf-8") as f:
    STORIES_RAW = json.load(f)

# Ensure all stories are dicts
search_query = st.sidebar.text_input("Search Story")

# Ensure STORIES is a list of dicts
menu = st.sidebar.radio("Menu", ["Login", "Stories", "Favorites", "About"])

if menu == "Login":
    st.subheader("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "ayush" and password == "12345":
            st.success("Logged in!")
        else:
            st.error("Invalid credentials")

elif menu == "Stories":
    st.subheader("Stories Page")
    # load and display stories here

elif menu == "Favorites":
    st.subheader("Favorites Page")

elif menu == "About":
    st.subheader("About Page")

    # Filter stories
    filtered_stories = [
        s for s in STORIES
        if search_query.lower() in s.get("title", "").lower()
    ]

    st.subheader(f"Available Stories ({len(filtered_stories)})")

    for idx, story in enumerate(filtered_stories):
        with st.expander(story.get("title", "Untitled Story")):
            st.write(story.get("description", ""))
            lang_text = story.get(selected_lang, story.get("English", ""))
            if st.button(f"Play {selected_lang} Voice", key=f"play_{idx}"):
                # TTS placeholder
                st.info("TTS will play here")


    
    # Display stories in cards
    for idx, story in enumerate(filtered_stories):
        with st.expander(f"{story['title']}"):
            st.write(story["description"])
            lang_text = story.get(selected_lang, story["English"])
            if st.button(f"Play {selected_lang} Voice", key=f"play_{idx}"):
                # TTS request
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
    if not st.session_state.logged_in:
        st.warning("Please login first!")
        st.stop()
    st.subheader("Your Favorite Stories")
    st.info("Feature coming soon!")

# ------------------ About Page ------------------
elif menu == "About":
    st.subheader("About Smart Cultural Storyteller")
    st.markdown("""
    - Multi-language AI storytelling app
    - Google Cloud Text-to-Speech for natural voice
    - Built with Python & Streamlit
    - Preserves Indian cultural heritage
    """)
