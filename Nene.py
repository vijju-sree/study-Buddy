import streamlit as st
import speech_recognition as sr
import os

def transcribe_audio_file(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Could not understand audio"
        except sr.RequestError:
            text = "API unavailable"
    return text

def record_audio_file():
    """
    For local use only: record from microphone.
    """
    try:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            st.info("Recording...")
            audio_data = recognizer.listen(source, timeout=5)
        audio_path = "recorded_audio.wav"
        with open(audio_path, "wb") as f:
            f.write(audio_data.get_wav_data())
        return audio_path
    except Exception as e:
        st.warning("Microphone not available or PyAudio missing. Please upload audio instead.")
        return None

def run():
    st.header("🗣 Speech-to-Text")
    
    # Option 1: upload file
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    
    audio_path = None
    
    if uploaded_file is not None:
        # Save uploaded file
        audio_path = f"uploaded_{uploaded_file.name}"
        with open(audio_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    # Option 2: local microphone (only works locally)
    if st.button("Record from Microphone"):
        audio_path = record_audio_file()
    
    if audio_path:
        st.success(f"Processing {audio_path} ...")
        text = transcribe_audio_file(audio_path)
        st.text_area("Transcribed Text:", text, height=200)
        # Optionally delete the audio file after transcription
        if os.path.exists(audio_path):
            os.remove(audio_path)
