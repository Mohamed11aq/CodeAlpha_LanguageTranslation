"""
CodeAlpha - Task 1: Language Translation Tool
------------------------------------------------
A polished, professionally-styled translation web app built with Streamlit.

Design concept: "Passport" — the visual language of travel documents and
customs stamps. Every translation gets a postmark showing the language
pair, like a stamp confirming a border crossing. Deep ink navy + warm
brass/gold accent, a characterful serif for the display type, and a clean
utility sans for the interface itself.

Features:
- Text input box
- Source & target language selection
- Uses deep-translator (Google Translate, with a MyMemory fallback engine)
- Displays translated text clearly, with a "postmark" showing the language pair
- Optional: Copy button + Text-to-speech playback
"""

import streamlit as st
from deep_translator import GoogleTranslator, MyMemoryTranslator
from gtts import gTTS
import io

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Passport — AI Language Translator | CodeAlpha",
    page_icon="🖋️",
    layout="centered"
)

# ----------------------------
# Design system (CSS)
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap');

:root {
    --ink: #12213A;
    --ink-soft: #2C3E5C;
    --paper: #EEF1F6;
    --card: #FFFFFF;
    --brass: #B9822F;
    --brass-deep: #8C611F;
    --teal: #1F6F6B;
    --muted: #62697A;
    --border: #DCE1E8;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--paper) !important;
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}

[data-testid="stHeader"] { background: transparent; }

.block-container {
    max-width: 760px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* ---------- Hero header ---------- */
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--brass-deep);
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.6rem;
}
.hero-eyebrow::before {
    content: "";
    width: 22px;
    height: 1px;
    background: var(--brass-deep);
    display: inline-block;
}
.hero-title {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 2.6rem;
    line-height: 1.12;
    color: var(--ink);
    margin: 0 0 0.6rem 0;
}
.hero-title em {
    font-style: italic;
    color: var(--brass);
}
.hero-sub {
    font-size: 0.98rem;
    color: var(--muted);
    max-width: 46ch;
    line-height: 1.55;
    margin-bottom: 1.6rem;
}

hr, [data-testid="stDivider"] {
    border-top: 1px solid var(--border) !important;
    margin: 1.6rem 0 !important;
}

/* ---------- Section labels ---------- */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
    display: block;
}

/* ---------- Language selects ---------- */
[data-testid="stSelectbox"] label p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
}
[data-testid="stSelectbox"] > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}
.lang-arrow {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    height: 100%;
    padding-bottom: 0.55rem;
    font-family: 'Fraunces', serif;
    font-size: 1.4rem;
    font-style: italic;
    color: var(--brass);
}

/* ---------- Text areas ---------- */
[data-testid="stTextArea"] label p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
}
[data-testid="stTextArea"] textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.98rem !important;
    color: var(--ink) !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--brass) !important;
    box-shadow: 0 0 0 1px var(--brass) !important;
}

/* ---------- Translate button ---------- */
[data-testid="stButton"] button {
    background: var(--ink) !important;
    color: #F4F1EA !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.7rem 1rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    transition: background 0.15s ease, transform 0.1s ease;
}
[data-testid="stButton"] button:hover {
    background: var(--brass-deep) !important;
    color: #FFFFFF !important;
}
[data-testid="stButton"] button:active { transform: scale(0.99); }

/* ---------- Postmark stamp ---------- */
.postmark-row { display: flex; justify-content: center; margin: 0 0 0.9rem 0; }
.postmark {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--teal);
    border: 1.5px dashed var(--teal);
    border-radius: 999px;
    padding: 0.35rem 1rem;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transform: rotate(-2deg);
    background: rgba(31, 111, 107, 0.05);
}
.postmark .dot { width: 5px; height: 5px; border-radius: 50%; background: var(--teal); }

/* ---------- Result heading ---------- */
.result-heading {
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-size: 1.3rem;
    color: var(--ink);
    text-align: center;
    margin-bottom: 0.9rem;
}

/* ---------- Captions ---------- */
[data-testid="stCaptionContainer"] p, .stCaption {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* ---------- Code block (copy area) ---------- */
[data-testid="stCode"] {
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
}

/* ---------- Alerts ---------- */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
}

/* ---------- Footer ---------- */
.footer-note {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Supported Languages
# ----------------------------
LANGUAGES = GoogleTranslator().get_supported_languages(as_dict=True)
# LANGUAGES -> {'english': 'en', 'arabic': 'ar', ...}
LANGUAGE_NAMES = sorted(LANGUAGES.keys())

# ----------------------------
# Hero header
# ----------------------------
st.markdown("""
<div class="hero-eyebrow">CodeAlpha · Artificial Intelligence Internship</div>
<h1 class="hero-title">Carry your words<br><em>across the border.</em></h1>
<p class="hero-sub">
    Enter a passage below, choose where it's coming from and where it's
    going, and get an instant, stamped translation.
</p>
""", unsafe_allow_html=True)

st.divider()

# ----------------------------
# Language code mapping for the MyMemory fallback engine
# (MyMemory expects region-tagged codes like 'ar-SA', not just 'ar')
# ----------------------------
MYMEMORY_CODE_MAP = {
    "ar": "ar-SA", "en": "en-GB", "fr": "fr-FR", "es": "es-ES",
    "de": "de-DE", "it": "it-IT", "pt": "pt-PT", "ru": "ru-RU",
    "zh-CN": "zh-CN", "zh-TW": "zh-TW", "ja": "ja-JP", "ko": "ko-KR",
    "tr": "tr-TR", "nl": "nl-NL", "pl": "pl-PL", "sv": "sv-SE",
    "el": "el-GR", "he": "he-IL", "hi": "hi-IN", "id": "id-ID",
    "th": "th-TH", "vi": "vi-VN", "uk": "uk-UA", "cs": "cs-CZ",
    "ro": "ro-RO", "hu": "hu-HU", "fi": "fi-FI", "da": "da-DK",
    "no": "no-NO", "sk": "sk-SK", "bg": "bg-BG", "ur": "ur-PK",
    "fa": "fa-IR",
}


def to_mymemory_code(code: str) -> str:
    """Convert a deep-translator language code into a MyMemory-friendly code."""
    return MYMEMORY_CODE_MAP.get(code, code)


# ----------------------------
# Language Selection
# ----------------------------
col1, col_arrow, col2 = st.columns([5, 0.6, 5])

with col1:
    source_lang = st.selectbox(
        "From",
        options=["auto"] + LANGUAGE_NAMES,
        index=0,
        help="Choose 'auto' to let the tool detect the language automatically."
    )

with col_arrow:
    st.markdown('<div class="lang-arrow">→</div>', unsafe_allow_html=True)

with col2:
    target_lang = st.selectbox(
        "To",
        options=LANGUAGE_NAMES,
        index=LANGUAGE_NAMES.index("arabic") if "arabic" in LANGUAGE_NAMES else 0
    )

# ----------------------------
# Text Input
# ----------------------------
input_text = st.text_area(
    "Passage",
    height=150,
    placeholder="Type or paste your text here..."
)

translate_btn = st.button("Translate  →", type="primary", use_container_width=True)

# ----------------------------
# Translation Logic
# ----------------------------
if translate_btn:
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        src_code = "auto" if source_lang == "auto" else LANGUAGES[source_lang]
        tgt_code = LANGUAGES[target_lang]

        translated = None

        # Primary engine: Google Translate (via deep-translator)
        try:
            translated = GoogleTranslator(
                source=src_code,
                target=tgt_code
            ).translate(input_text)
        except Exception:
            translated = None

        # Fallback engine: MyMemory (used automatically if Google fails,
        # e.g. temporary Error 500 / rate limiting)
        if not translated:
            try:
                mm_source = "en-GB" if src_code == "auto" else to_mymemory_code(src_code)
                mm_target = to_mymemory_code(tgt_code)
                translated = MyMemoryTranslator(
                    source=mm_source,
                    target=mm_target
                ).translate(input_text)
            except Exception as e:
                st.error(f"Translation failed with both engines: {e}")

        if translated:
            st.session_state["translated_text"] = translated
            st.session_state["tgt_code"] = tgt_code
            st.session_state["src_label"] = source_lang
            st.session_state["tgt_label"] = target_lang

# ----------------------------
# Display Result
# ----------------------------
if "translated_text" in st.session_state and st.session_state["translated_text"]:
    st.divider()

    st.markdown(f"""
    <div class="postmark-row">
        <div class="postmark">
            <span class="dot"></span>
            {st.session_state.get("src_label", "auto")} → {st.session_state.get("tgt_label", "")}
        </div>
    </div>
    <div class="result-heading">Your translation is ready</div>
    """, unsafe_allow_html=True)

    st.text_area(
        "Result",
        value=st.session_state["translated_text"],
        height=150,
        label_visibility="collapsed"
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.caption("Copy")
        st.code(st.session_state["translated_text"], language=None)

    with col_b:
        st.caption("Listen")
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
st.markdown(
    '<div class="footer-note">Built for the CodeAlpha AI Internship — Task 1</div>',
    unsafe_allow_html=True
)
