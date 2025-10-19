# app_upgraded.py
import streamlit as st
import json
from io import BytesIO
from google.cloud import texttospeech
from google.oauth2 import service_account

# ------------------ Page Setup ------------------
st.set_page_config(page_title="Smart Cultural Storyteller", layout="wide")
st.markdown("<h1 style='text-align:center;color:navy;'>Smart Cultural Storyteller</h1>", unsafe_allow_html=True)

# ------------------ Session State Initialization ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# ------------------ Load stories safely ------------------
try:
    with open("stories.json", "r", encoding="utf-8") as f:
        STORIES_RAW = json.load(f)
except FileNotFoundError:
    st.error("`stories.json` file not found.")
    STORIES_RAW = []

# ------------------ Sidebar Navigation ------------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Menu", ["Login", "Stories", "Favorites", "About"])
languages = ["English", "Hindi", "Gujarati"]
tts_client = texttospeech.TextToSpeechClient()

# ------------------ Main Content Area ------------------

# ---- Login Page ----
if menu == "Login":
    st.subheader("Login Page")
    if st.session_state.logged_in:
        st.success(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # This is hardcoded logic. Replace with a real authentication system.
            if username == "ayush" and password == "12345":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# ---- Stories Page ----
elif menu == "Stories":
    st.subheader("Stories Page")
    search_query = st.sidebar.text_input("Search Story")
    selected_lang = st.sidebar.selectbox("Select Language", languages)

    # Filter stories based on search query
    filtered_stories = [
        s for s in STORIES_RAW
        if search_query.lower() in s.get("title", "").lower()
    ]

    st.subheader(f"Available Stories ({len(filtered_stories)})")
    if filtered_stories:
        for idx, story in enumerate(filtered_stories):
            with st.expander(story.get("title", "Untitled Story")):
                st.write(story.get("description", ""))
                
                # Add to Favorites button
                if st.session_state.logged_in:
                    if story["title"] in st.session_state.favorites:
                        st.write("⭐ Already in favorites")
                    elif st.button("Add to Favorites", key=f"fav_{idx}"):
                        st.session_state.favorites.append(story["title"])
                        st.success("Added to favorites!")
                
                # Text-to-speech button
                lang_text = story.get(selected_lang, story.get("English", ""))
                if lang_text and st.button(f"Play {selected_lang} Voice", key=f"play_{idx}"):
                    try:
                        input_text = texttospeech.SynthesisInput(text=lang_text)
                        voice = texttospeech.VoiceSelectionParams(
                            language_code="en-US" if selected_lang == "English" else "hi-IN",
                            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
                        )
                        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
                        response = tts_client.synthesize_speech(
                            input=input_text, voice=voice, audio_config=audio_config
                        )
                        st.audio(BytesIO(response.audio_content), format="audio/mp3")
                    except Exception as e:
                        st.error(f"Error generating speech: {e}")
    else:
        st.info("No stories found.")

# ---- Favorites Page ----
elif menu == "Favorites":
    if not st.session_state.logged_in:
        st.warning("Please login first to view your favorites.")
    else:
        st.subheader("Your Favorite Stories")
        if st.session_state.favorites:
            for fav in st.session_state.favorites:
                st.write(f"- {fav}")
        else:
            st.info("No favorites yet!")

# ---- About Page ----
elif menu == "About":
    st.subheader("About Smart Cultural Storyteller")
    st.markdown("""
    - Multi-language AI storytelling app
    - Google Cloud Text-to-Speech for natural voice
    - Built with Python & Streamlit
    - Preserves Indian cultural heritage
    """)
