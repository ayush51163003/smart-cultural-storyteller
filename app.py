import streamlit as st
from login import login_user
from story_app import show_stories

st.set_page_config(page_title="Smart Cultural Storyteller", page_icon="📖")
st.title("📖 Smart Cultural Storyteller")

if login_user():
    show_stories()
