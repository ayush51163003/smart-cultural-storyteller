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
# ------------------ Session State ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "page" not in st.session_state:
    st.session_state.page = "Login"   # default page

# ------------------ Sidebar ------------------
st.sidebar.title("Navigation")
languages = ["English", "Hindi", "Gujarati"]

# ------------------ Stories Page ------------------
    
   # Load stories safely
with open("stories.json", "r", encoding="utf-8") as f:
    STORIES_RAW = json.load(f)

# Ensure all stories are dicts
search_query = st.sidebar.text_input("Search Story")

# Ensure STORIES is a list of dicts
import streamlit as st

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Login", "Stories", "Favorites", "About"])

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

    # Filter stories based on search query
    filtered_stories = [
        s for s in STORIES_RAW
        if search_query.lower() in s.get("title", "").lower()
    ]
try:
    with open("stories.json", "r", encoding="utf-8") as f:
        STORIES_RAW = json.load(f)
except Exception as e:
    st.error(f"Error loading stories.json: {e}")
    STORIES_RAW = []

# Filter valid dictionaries
# Filter stories safely
filtered_stories = [
    s for s in STORIES if search_query.lower() in s.get("title", "").lower()
]

st.subheader(f"Available Stories ({len(filtered_stories)})")

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
        if st.button(f"Play {selected_lang} Voice", key=f"play_{idx}"):
            st.info("TTS would play here")
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
        st.warning("Please login first to view your favorites.")
    else:
        st.subheader("Your Favorite Stories")
        if st.session_state.favorites:
            for fav in st.session_state.favorites:
                st.write(f"- {fav}")
        else:
            st.info("No favorites yet!")


# ------------------ About Page ------------------
elif menu == "About":
    st.subheader("About Smart Cultural Storyteller")
    st.markdown("""
    - Multi-language AI storytelling app
    - Google Cloud Text-to-Speech for natural voice
    - Built with Python & Streamlit
    - Preserves Indian cultural heritage
    """)
