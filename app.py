import os
import ctypes
import platform

# Manually load the problematic DLL before anything else
if platform.system() == "Windows":
    try:
        # This helps Windows find the hidden dependencies of PyTorch
        ctypes.WinDLL("vcruntime140.dll")
        ctypes.WinDLL("msvcp140.dll")
    except Exception:
        pass

import streamlit as st
import whisper
# ... the rest of your code
import streamlit as st
import whisper
from textblob import TextBlob

# Page Config for a "Good Frontend"
st.set_page_config(page_title="Whisper Insights", page_icon="🎙️")

st.title("🎙️ Whisper Sentiment Analyzer")
st.write("Upload an audio file to transcribe it and analyze the mood.")

# Loading the model (Base is fast and accurate enough)
@st.cache_resource
def load_model():
    return whisper.load_model("small")

model = load_model()

audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

if audio_file is not None:
    st.audio(audio_file)
    
    with st.spinner("Transcribing..."):
        # Save temporary file to disk for Whisper to read
        with open("temp_audio.mp3", "wb") as f:
            f.write(audio_file.getbuffer())
        
        result = model.transcribe("temp_audio.mp3")
        text = result["text"]
        
    st.subheader("Transcribed Text:")
    st.info(text)

    # Sentiment Analysis
    sentiment = TextBlob(text).sentiment.polarity
    st.download_button(
    label="📥 Download Lyrics as TXT",
    data=text,
    file_name="transcription.txt",
    mime="text/plain"
)
    
    st.subheader("Sentiment Analysis:")
    if sentiment > 0:
        st.success(f"Positive Mood (Score: {sentiment:.2f})")
    elif sentiment < 0:
        st.error(f"Negative Mood (Score: {sentiment:.2f})")
    else:
        st.warning("Neutral Mood")
        st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)