# File: notes_generator.py

import streamlit as st
from pypdf import PdfReader
import os
import re
from datetime import datetime
import zipfile

# ---------------- RUN FUNCTION ------------------
def run():
    st.write("📘 Notes Generator Running!")

    # ------------------ Folders ------------------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    NOTES_DIR = os.path.join(BASE_DIR, "notes")
    EXPORT_DIR = os.path.join(BASE_DIR, "exports")

    os.makedirs(NOTES_DIR, exist_ok=True)
    os.makedirs(EXPORT_DIR, exist_ok=True)

    # ---------------- Functions ------------------
    def generate_notes(text):
        text = re.sub(r'\s+', ' ', text)
        sentences = re.split(r'\.|\?|\!', text)
        notes = []
        for s in sentences:
            s = s.strip()
            if len(s) > 20:
                notes.append("• " + s)

        keywords = ["important", "key", "must", "definition", "formula"]
        highlighted = []

        for n in notes:
            for k in keywords:
                n = re.sub(k, f"**{k.upper()}**", n, flags=re.IGNORECASE)
            highlighted.append(n)

        return highlighted

    def save_notes(name, notes_list):
        safe = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
        filename = f"{safe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = os.path.join(NOTES_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(notes_list))
        return filename

    def list_notes():
        return [f for f in os.listdir(NOTES_DIR) if f.endswith(".txt")]

    def delete_note(path):
        if os.path.exists(path):
            os.remove(path)

    def export_all_notes():
        zip_path = os.path.join(EXPORT_DIR, "all_notes.zip")
        with zipfile.ZipFile(zip_path, "w") as z:
            for f in list_notes():
                z.write(os.path.join(NOTES_DIR, f), f)
        return zip_path

    # ---------------- Streamlit UI ------------------
    st.title("🧠 Smart Notes Generator")

    # ---------- Input ----------
    option = st.radio("Choose Input Type", ["Topic Text", "Upload PDF"])
    content = ""

    if option == "Topic Text":
        content = st.text_area("Enter topic or content", placeholder="Example: Unit 1 easy notes ivvu...")

    if option == "Upload PDF":
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
        if pdf_file:
            try:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        content += text
            except:
                st.error("❌ PDF reading error! Check the file or try another PDF.")

    # ---------- Generate & Save Notes ----------
    if st.button("Generate Smart Notes"):
        if not content.strip():
            st.warning("Please enter text or upload PDF!")
        else:
            notes = generate_notes(content)
            st.subheader("✅ Generated Notes")

            for n in notes:
                st.markdown(n)

            filename = st.text_input("Save Notes As", "smart_notes")
            if filename.strip() != "":
                saved_filename = save_notes(filename, notes)
                st.success(f"✅ Notes saved: {saved_filename}")

    # ---------- Saved Notes ----------
    st.header("📜 Saved Notes")
    notes_files = list_notes()

    if not notes_files:
        st.info("No saved notes yet.")
    else:
        for f in notes_files:
            full_path = os.path.join(NOTES_DIR, f)
            with open(full_path, "r", encoding="utf-8") as file_data:
                content = file_data.read()

            with st.expander(f):
                st.text_area("Preview", content, height=200)

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"🗑️ Delete {f}"):
                        delete_note(full_path)
                        st.experimental_rerun()

                with col2:
                    st.download_button("Download", full_path, file_name=f)

    # ---------- Export All ----------
    st.header("📦 Export All Notes")

    if st.button("Export All as ZIP"):
        zip_path = export_all_notes()
        st.success("ZIP ready ✅")
        with open(zip_path, "rb") as f:
            st.download_button("Download ZIP", f, file_name="all_notes.zip")
