import streamlit as st

# Predefined username/password
USERS = {"ayush": "1234", "guest": "guest"}

def login_user():
    st.subheader("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")
    
    if login_btn:
        if username in USERS and USERS[username] == password:
            st.success(f"Welcome {username}!")
            return True
        else:
            st.error("Invalid username or password")
            return False
    return False
