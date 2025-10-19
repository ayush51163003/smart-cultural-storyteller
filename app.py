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
if "page" not in st.session_state:
    st.session_state.page = "Login"

# ------------------ Load stories safely ------------------
try:
    with open("stories.json", "r", encoding="utf-8") as f:
        STORIES_RAW = json.load(f)
except FileNotFoundError:
    st.error("`stories.json` file not found. Please create one.")
    STORIES_RAW = []

# ------------------ Sidebar Navigation ------------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Menu", ["Login", "Stories", "Favorites", "About"], index=["Login", "Stories", "Favorites", "About"].index(st.session_state.page))
languages = ["English", "Hindi", "Gujarati"]
tts_client = texttospeech.TextToSpeechClient()

# Update page state when a menu item is clicked
st.session_state.page = menu

# ------------------ Main Content Area - Renders based on menu selection ------------------

# ---- Login Page ----
if st.session_state.page == "Login":
    st.subheader("Login Page")
    if st.session_state.logged_in:
        st.success(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.page = "Login"  # Return to login page after logout
            st.rerun()
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "ayush" and password == "12345":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "Stories"  # Redirect to stories page
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# ---- Stories Page ----
elif st.session_state.page == "Stories":
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

                # Add to Favorites button, only visible if logged in
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
                        lang_code = "en-US" if selected_lang == "English" else "hi-IN" if selected_lang == "Hindi" else "gu-IN"
                        voice = texttospeech.VoiceSelectionParams(
                            language_code=lang_code,
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
elif st.session_state.page == "Favorites":
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
elif st.session_state.page == "About":
    st.subheader("About Smart Cultural Storyteller")
    st.markdown("""
    - Multi-language AI storytelling app
    - Google Cloud Text-to-Speech for natural voice
    - Built with Python & Streamlit
    - Preserves Indian cultural heritage
    """)
