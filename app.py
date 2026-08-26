"""
CodeAlpha - Task 1: Language Translation Tool
------------------------------------------------
A simple, user-friendly translation web app built with Streamlit.

Features:
- Text input box
- Source & target language selection
- Uses deep-translator (Google Translate engine) - free, no API key required
- Displays translated text clearly
- Optional: Copy button + Text-to-Speech playback
"""

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="AI Language Translator | CodeAlpha",
    page_icon="🌐",
    layout="centered"
)

# ----------------------------
# Supported Languages
# ----------------------------
LANGUAGES = GoogleTranslator().get_supported_languages(as_dict=True)
# LANGUAGES -> {'english': 'en', 'arabic': 'ar', ...}
LANGUAGE_NAMES = sorted(LANGUAGES.keys())

# ----------------------------
# Header
# ----------------------------
st.title("🌐 AI Language Translation Tool")
st.caption("CodeAlpha Artificial Intelligence Internship — Task 1")
st.write(
    "Enter text below, choose the source and target languages, "
    "and get an instant translation."
)

st.divider()

# ----------------------------
# Language Selection
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "Source Language",
        options=["auto"] + LANGUAGE_NAMES,
        index=0,
        help="Choose 'auto' to let the tool detect the language automatically."
    )

with col2:
    target_lang = st.selectbox(
        "Target Language",
        options=LANGUAGE_NAMES,
        index=LANGUAGE_NAMES.index("arabic") if "arabic" in LANGUAGE_NAMES else 0
    )

# ----------------------------
# Text Input
# ----------------------------
input_text = st.text_area(
    "Enter text to translate",
    height=150,
    placeholder="Type or paste your text here..."
)

translate_btn = st.button("🔁 Translate", type="primary", use_container_width=True)

# ----------------------------
# Translation Logic
# ----------------------------
if translate_btn:
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        try:
            src_code = "auto" if source_lang == "auto" else LANGUAGES[source_lang]
            tgt_code = LANGUAGES[target_lang]

            translated = GoogleTranslator(
                source=src_code,
                target=tgt_code
            ).translate(input_text)

            st.session_state["translated_text"] = translated
            st.session_state["tgt_code"] = tgt_code

        except Exception as e:
            st.error(f"Translation failed: {e}")

# ----------------------------
# Display Result
# ----------------------------
if "translated_text" in st.session_state and st.session_state["translated_text"]:
    st.divider()
    st.subheader("✅ Translated Text")
    st.text_area(
        "Result",
        value=st.session_state["translated_text"],
        height=150,
        label_visibility="collapsed"
    )

    col_a, col_b = st.columns(2)

    with col_a:
        # Copy-friendly display using st.code (shows a built-in copy icon)
        st.caption("Click the icon in the box below to copy:")
        st.code(st.session_state["translated_text"], language=None)

    with col_b:
        st.caption("🔊 Listen to the translation:")
        try:
            tts = gTTS(
                text=st.session_state["translated_text"],
                lang=st.session_state["tgt_code"]
            )
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception:
            st.info("Text-to-speech is not available for this language.")

st.divider()
st.caption("Built for the CodeAlpha AI Internship — Task 1: Language Translation Tool")
