# Smart Cultural Storyteller — Streamlit Version (Text-Based, Multi-Language)

This version of the project uses Streamlit for deployment and shows multi-language stories in text format. No audio playback is included, making it simpler for Streamlit Cloud deployment.

---

## `app.py`

```python
import streamlit as st
import json

# Load stories
with open('stories.json', 'r', encoding='utf-8') as f:
    STORIES = json.load(f)

st.set_page_config(page_title="Smart Cultural Storyteller", page_icon="📖")

st.title("📖 Smart Cultural Storyteller")

# Language selection
lang = st.selectbox("Select Language", ['English', 'Hindi', 'Gujarati'], index=0)
lang_code = 'en' if lang=='English' else 'hi' if lang=='Hindi' else 'gu'

st.write(f"Selected language: {lang}")

# List available stories
st.subheader("Available Stories")
for sid, sdata in STORIES.items():
    st.markdown(f"### {sdata['title']}")
    if st.button(f"Read Story {sid}", key=sid):
        text = sdata['translations'].get(lang_code, sdata['translations'].get('en', 'Story not available'))
        st.write(text)
```

---

## `stories.json` (same as before)

```json
{
  "1": {
    "title": "The Clever Rabbit",
    "translations": {
      "en": "Once upon a time a clever rabbit outwitted a hungry tiger...",
      "hi": "एक समय की बात है, एक चतुर खरगोश ने एक भूखे बाघ को चकमा दिया...",
      "gu": "એક વખતની વાત છે, એક ચતુર ખિસકોલિયાએ ભૂખ્યા બાગરને ઠગ્યો..."
    }
  },
  "2": {
    "title": "The Sharing Tree",
    "translations": {
      "en": "A tree taught the village children the value of sharing...",
      "hi": "एक पेड़ ने गांव के बच्चों को साझा करने का महत्व सिखाया...",
      "gu": "એક વૃક્ષે ગામના બાળકોને વહેંચાવાનો મહત્વ શીખવ્યો..."
    }
  }
}
```

---

## `requirements.txt`

```
streamlit==1.26.0
```

---

## Deployment Instructions

1. Create a new GitHub repo (e.g., `smart-cultural-storyteller`).
2. Upload `app.py`, `stories.json`, `requirements.txt`.
3. Visit [https://share.streamlit.io/deploy](https://share.streamlit.io/deploy) and connect your GitHub repo.
4. Click **Deploy**, and your app will go live instantly.

---

## Notes

* This version is **text-only**; you can later add TTS audio using gTTS for a voice experience.
* Multi-language stories are supported directly from `stories.json`.
* Streamlit ensures easy deployment without setting up a backend server.

---

Once deployed, you can copy the **Streamlit app link** for your assignment submission PDF.
