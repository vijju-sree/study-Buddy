import streamlit as st
import os
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_DIR = os.path.join(BASE_DIR, "texts")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")

os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

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

def run():
    st.title("📜 Notes Manager")

    # ----------- VIEW AND DELETE FILES -----------
    files = list_texts()
    for i, f in enumerate(files):
        full = os.path.join(TEXT_DIR, f)
        with open(full, "r", encoding="utf-8") as file_data:
            content = file_data.read()

        with st.expander(f):
            st.text_area("Preview", content, height=200, key=f"text_{i}")
            if st.button(f"🗑️ Delete {f}", key=f"del_{i}"):
                delete_file(full)
                st.experimental_rerun()

    # ----------- EXPORT ALL -----------
    st.header("📦 Export All Text Files")
    if st.button("Export as ZIP", key="export_zip_notes"):
        zip_file = export_all()
        st.success("ZIP ready ✅")
        with open(zip_file, "rb") as f:
            st.download_button("Download ZIP", f, file_name="all_texts.zip")
