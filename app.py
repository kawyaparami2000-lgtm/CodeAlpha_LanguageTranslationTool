import streamlit as st
import requests
import os
import io
import html

from dotenv import load_dotenv
from gtts import gTTS

# ==========================================
# 1. LOAD AZURE CREDENTIALS
# ==========================================

load_dotenv()

AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION")

# ==========================================
# 2. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="LingoTranslate",
    page_icon="🌍",
    layout="wide"
)

# ==========================================
# 3. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main Application Background */
.stApp {
    background: #DDE3F5 !important;
    color: #1E293B !important;
}

/* Main Container */
.block-container {
    max-inline-size: 1100px;
    padding-block-start: 2rem;
    padding-block-end: 2rem;
}

/* Main Heading */
h1 {
    color: #4338CA !important;
    text-align: center;
    font-size: 45px !important;
    font-weight: 800 !important;
}

/* Subtitle */
.subtitle {
    color: #475569 !important;
    text-align: center;
    font-size: 17px;
    margin-block-end: 30px;
}

/* Section Headings */
.section-title {
    color: #4338CA !important;
    font-size: 21px;
    font-weight: bold;
}

/* General Text */
.stApp p,
.stApp label,
.stApp span {
    color: #1E293B;
}

/* Text Area */
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #1E293B !important;
    -webkit-text-fill-color: #1E293B !important;
    border: 2px solid #A5B4FC !important;
    border-radius: 12px !important;
}

/* Text Area Placeholder */
.stTextArea textarea::placeholder {
    color: #64748B !important;
    -webkit-text-fill-color: #64748B !important;
}

/* Select Box */
.stSelectbox div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border-radius: 10px !important;
}

.stSelectbox div[data-baseweb="select"] * {
    color: #1E293B !important;
}

/* Buttons */
.stButton button {
    background: #4F46E5 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 12px !important;
}

/* Button Text */
.stButton button p {
    color: #FFFFFF !important;
}

/* Button Hover */
.stButton button:hover {
    background: #3730A3 !important;
    color: #FFFFFF !important;
}

/* Download Button */
.stDownloadButton button {
    background: #4F46E5 !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    border: none !important;
}

.stDownloadButton button p {
    color: #FFFFFF !important;
}

/* Translation Result Card */
.translation-card {
    background: #FFFFFF !important;
    color: #1E293B !important;
    padding: 22px;
    border-radius: 15px;
    border-inline-start: 5px solid #6366F1;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    font-size: 18px;
    line-height: 1.7;
    overflow-wrap: anywhere;
}

/* Success Message Box */
div[data-testid="stAlert"] {
    background-color: #FFF9C4 !important;
    background: #FFF9C4 !important;
    border: 1px solid #FDE68A !important;
    border-radius: 10px !important;
}

/* Success Message Text */
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748B !important;
    font-size: 13px;
    margin-block-start: 40px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. HEADER
# ==========================================

st.markdown(
    '<h1>🌍 LingoTranslate</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Break language barriers with intelligent translation.</p>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 5. AVAILABLE LANGUAGES
# ==========================================

languages = {
    "English": "en",
    "Sinhala": "si",
    "Tamil": "ta",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-Hans",
    "Hindi": "hi",
    "Arabic": "ar",
    "Italian": "it"
}


# ==========================================
# 6. AZURE TRANSLATION FUNCTION
# ==========================================

def translate_text(text, source, target):

    url = AZURE_TRANSLATOR_ENDPOINT.rstrip("/") + "/translate"

    params = {
        "api-version": "3.0",
        "from": source,
        "to": target
    }

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-Type": "application/json"
    }

    body = [{"Text": text}]

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=body,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    return result[0]["translations"][0]["text"]


# ==========================================
# 7. LANGUAGE SELECTION
# ==========================================

st.markdown(
    '<p class="section-title">🌐 Choose Languages</p>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([5, 1, 5])

with col1:

    source_language = st.selectbox(
        "Translate From",
        list(languages.keys()),
        index=0
    )

with col2:

    st.markdown(
        "<h2 style='text-align:center; padding-block-start:20px; color:#4338CA;'>⇄</h2>",
        unsafe_allow_html=True
    )

with col3:

    target_language = st.selectbox(
        "Translate To",
        list(languages.keys()),
        index=1
    )

st.divider()


# ==========================================
# 8. TEXT INPUT
# ==========================================

st.markdown(
    '<p class="section-title">✍️ Enter Your Text</p>',
    unsafe_allow_html=True
)

input_text = st.text_area(
    "Text to translate",
    placeholder="Type or paste your text here...",
    height=180,
    label_visibility="collapsed"
)

st.caption(f"Characters: {len(input_text)}")


# ==========================================
# 9. TRANSLATION BUTTON
# ==========================================

if st.button("🌐 Translate Text", use_container_width=True):

    if not AZURE_TRANSLATOR_KEY or not AZURE_TRANSLATOR_ENDPOINT:

        st.error("Azure credentials are missing. Please check your .env file.")

    elif not input_text.strip():

        st.warning("Please enter some text to translate.")

    elif source_language == target_language:

        st.warning("Please select two different languages.")

    else:

        try:

            with st.spinner("Translating your text..."):

                translated_text = translate_text(
                    input_text,
                    languages[source_language],
                    languages[target_language]
                )

                st.session_state["translated_text"] = translated_text
                st.session_state["target_language"] = target_language

                # Remove previous audio after a new translation
                st.session_state.pop("audio_bytes", None)

            st.success("Translation completed successfully!")

        except requests.exceptions.HTTPError as e:

            st.error(f"Azure API Error: {e.response.text}")

        except requests.exceptions.RequestException as e:

            st.error(f"Connection Error: {str(e)}")

        except Exception as e:

            st.error(f"Something went wrong: {str(e)}")


# ==========================================
# 10. DISPLAY TRANSLATION RESULT
# ==========================================

if "translated_text" in st.session_state:

    st.divider()

    st.markdown(
        '<p class="section-title">📝 Translated Result</p>',
        unsafe_allow_html=True
    )

    translated_text = st.session_state["translated_text"]

    # Translation Card
    safe_text = html.escape(translated_text).replace("\n", "<br>")

    st.markdown(
        f'<div class="translation-card">{safe_text}</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # Download and Copy
    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="⬇️ Download Translation",
            data=translated_text,
            file_name="translated_text.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:

        st.code(translated_text, language=None)

    st.divider()


    # ======================================
    # 11. TEXT TO SPEECH
    # ======================================

    st.markdown(
        '<p class="section-title">🔊 Listen to Translation</p>',
        unsafe_allow_html=True
    )

    if st.button("▶️ Generate Audio", use_container_width=True):

        try:

            audio_language = languages[
                st.session_state["target_language"]
            ]

            with st.spinner("Generating audio..."):

                audio = gTTS(
                    text=translated_text,
                    lang=audio_language
                )

                audio_bytes = io.BytesIO()

                audio.write_to_fp(audio_bytes)

                st.session_state["audio_bytes"] = audio_bytes.getvalue()

            st.success("Audio generated successfully!")

        except Exception as e:

            st.warning(
                f"Audio is not available for this language: {str(e)}"
            )

    if "audio_bytes" in st.session_state:

        st.audio(
            st.session_state["audio_bytes"],
            format="audio/mp3"
        )


# ==========================================
# 12. FOOTER
# ==========================================

st.divider()

st.markdown("""
<div class="footer">
    <p>🌍 LingoTranslate</p>
    <p>Powered by Microsoft Azure Translator</p>
    <p>Developed as part of the CodeAlpha AI Internship</p>
</div>
""", unsafe_allow_html=True)