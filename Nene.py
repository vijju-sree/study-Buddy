import streamlit as st
import speech_recognition as sr
import os
from datetime import datetime
from pydub import AudioSegment
import zipfile

# ------------------ Folders ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audios")
TEXT_DIR = os.path.join(BASE_DIR, "texts")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

# ---------------- Functions ----------------
def record_audio(path):
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.info("🎤 Recording... Speak (max 3 mins)")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=180)

        with open(path, "wb") as f:
            f.write(audio.get_wav_data())


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


def list_texts():
    return [f for f in os.listdir(TEXT_DIR) if f.endswith(".txt")]


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def export_all():
    zip_path = os.path.join(EXPORT_DIR, "all_texts.zip")
    with zipfile.ZipFile(zip_path, "w") as z:
        for f in list_texts():
            z.write(os.path.join(TEXT_DIR, f), f)
    return zip_path


# ---------------- RUN FUNCTION ----------------  
def run():
    st.title("🎙️ Voice to Text App")

    # ----------- RECORD -----------
    st.header("🎤 Record Voice")

    if st.button("Start Recording"):
        t = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = os.path.join(AUDIO_DIR, f"record_{t}.wav")

        record_audio(audio_path)
        st.session_state.last_audio = audio_path

        text = transcribe(audio_path)
        st.session_state.last_text = text

        st.success("✅ Recording completed")

    if "last_audio" in st.session_state and st.session_state.last_audio:
        audio_path = st.session_state.last_audio
        if os.path.exists(audio_path):
            st.audio(audio_path)

    if "last_text" in st.session_state and st.session_state.last_text:
        st.text_area("Generated Text", st.session_state.last_text)

    filename = st.text_input("Save Text File Name", "speech_text")

    if st.button("💾 Save Text"):
        path = save_text(filename, st.session_state.last_text)
        st.success(f"✅ Saved: {path}")

    # ----------- UPLOAD AUDIO -----------
    st.header("📁 Upload Audio File")

    file = st.file_uploader("Upload audio", type=["wav", "mp3"])

    if file:
        upload_path = os.path.join(AUDIO_DIR, file.name)

        with open(upload_path, "wb") as f:
            f.write(file.getbuffer())

        upload_path = convert_to_wav(upload_path)

        st.audio(upload_path)

        txt = transcribe(upload_path)
        st.text_area("Generated Text", txt)

        save_name = st.text_input("File name", "uploaded_text")

        if st.button("💾 Save Uploaded Text"):
            path = save_text(save_name, txt)
            st.success(f"✅ Saved: {path}")

    # ----------- HISTORY -----------
    st.header("📜 Saved Text Files")

    files = list_texts()

    for f in files:
        full = os.path.join(TEXT_DIR, f)

        with open(full, "r", encoding="utf-8") as file_data:
            content = file_data.read()

        with st.expander(f):
            st.text_area("Preview", content, height=200)

            if st.button(f"🗑️ Delete {f}"):
                delete_file(full)
                st.rerun()

    # ----------- EXPORT -----------
    st.header("📦 Export All Text Files")

    if st.button("Export as ZIP"):
        z = export_all()
        st.success("ZIP ready ✅")

        with open(z, "rb") as f:
            st.download_button("Download ZIP", f, file_name="all_texts.zip")
