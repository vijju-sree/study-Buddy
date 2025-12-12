import streamlit as st
import os
import speech_recognition as sr
from datetime import datetime
from pydub import AudioSegment

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audios")
TEXT_DIR = os.path.join(BASE_DIR, "texts")
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)


def convert_to_wav(path):
    name, ext = os.path.splitext(path)
    if ext.lower() != ".wav":
        sound = AudioSegment.from_file(path)
        new = name + ".wav"
        sound.export(new, format="wav")
        return new
    return path


def transcribe(path):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(path) as src:
            audio = r.record(src)
        return r.recognize_google(audio)
    except:
        return "[Could not understand]"


def save_text(name, text):
    safe = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
    path = os.path.join(TEXT_DIR, safe + ".txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def run():
    st.header("🎙 Voice to Text")

    # ------------------- UPLOAD AUDIO -------------------
    file = st.file_uploader("Upload audio file (wav/mp3)", type=["wav", "mp3"])
    if file:
        upload_path = os.path.join(AUDIO_DIR, file.name)
        with open(upload_path, "wb") as f:
            f.write(file.getbuffer())

        upload_path = convert_to_wav(upload_path)
        st.audio(upload_path)

        txt = transcribe(upload_path)
        st.text_area("Generated Text", txt)

        save_name = st.text_input("Save as file name", "uploaded_text")

        if st.button("💾 Save Text"):
            path = save_text(save_name, txt)
            st.success(f"✅ Saved as: {path}")

    # ------------------- LOCAL MICROPHONE RECORDING -------------------
    if "local" in st.session_state:
        local = st.session_state.local
    else:
        local = False

    if st.button("🎤 Record from Mic (Local Only)"):
        local = True
        st.session_state.local = True

    if local:
        try:
            r = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                st.info("🎤 Recording (max 3 mins)...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=10, phrase_time_limit=180)
                t = datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_path = os.path.join(AUDIO_DIR, f"record_{t}.wav")
                with open(audio_path, "wb") as f:
                    f.write(audio.get_wav_data())
            st.success("✅ Recording finished")
            st.audio(audio_path)

            txt = transcribe(audio_path)
            st.text_area("Generated Text", txt)
            save_name = st.text_input("Save as file name", "speech_text")
            if st.button("💾 Save Recorded Text"):
                path = save_text(save_name, txt)
                st.success(f"✅ Saved as: {path}")
        except Exception as e:
            st.error("Microphone not supported on this platform. Upload audio instead.")
