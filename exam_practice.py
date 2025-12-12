# File: exam_practice.py

import streamlit as st
from pypdf import PdfReader
import docx
import re
import random
from difflib import SequenceMatcher
from datetime import datetime

# ---------------- RUN FUNCTION ------------------
def run():
    st.write("📝 Mock Exam Tool Running!")
    st.title("📝 Exam Practice — Mock Test Generator")

    # ---------------- Helpers ----------------
    def extract_text_from_pdf(uploaded_file):
        content = ""
        try:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                txt = page.extract_text()
                if txt:
                    content += txt + " "
        except:
            st.error("PDF could not be read.")
        return content.strip()

    def extract_text_from_docx(uploaded_file):
        content = ""
        try:
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                content += para.text + " "
        except:
            st.error("DOCX could not be read.")
        return content.strip()

    def clean_sentences(text):
        text = re.sub(r'\s+', ' ', text)
        sents = re.split(r'(?<=[.!?]) +', text)
        return [s.strip() for s in sents if len(s.split()) > 5]

    def choose_key_word(sent):
        words = re.findall(r"\w+", sent)
        words = [w for w in words if len(w) > 3]
        return random.choice(words) if words else None

    def generate_mcq_from_sentence(sent, text_corpus):
        key = choose_key_word(sent)
        if not key:
            return None
        question = sent.replace(key, "______")
        correct = key

        words = list(set(re.findall(r"\w+", text_corpus)))
        words = [w for w in words if w.lower() != key.lower()]
        distractors = random.sample(words, min(3, len(words)))

        options = [correct] + distractors
        random.shuffle(options)

        return {"q": question, "options": options, "ans": correct}

    def similarity(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    # ---------------- Input ----------------
    input_type = st.radio("Input Source", ["Paste Text", "Upload File"], key="exam_input")
    text_data = ""

    if input_type == "Paste Text":
        text_data = st.text_area("Paste your content here 👇", height=200, key="paste_exam")
    else:
        file = st.file_uploader("Upload PDF / DOCX / TXT", type=["pdf", "docx", "txt"], key="upload_exam")
        if file:
            ext = file.name.split(".")[-1].lower()
            if ext == "pdf":
                text_data = extract_text_from_pdf(file)
            elif ext == "docx":
                text_data = extract_text_from_docx(file)
            elif ext == "txt":
                text_data = file.read().decode("utf-8")

    if not text_data.strip():
        st.warning("Please paste text or upload file.")
        st.stop()

    # ---------------- Settings ----------------
    c1, c2, c3 = st.columns(3)
    with c1:
        num_mcq = st.number_input("MCQs count", 1, 50, 5, key="mcq_count")
    with c2:
        num_short = st.number_input("Short Qs count", 0, 20, 3, key="short_count")
    with c3:
        mark_mcq = st.selectbox("Marks per MCQ", [1, 2], key="mcq_marks")
        mark_short = st.selectbox("Marks per Short Q", [2, 4, 5], key="short_marks")

    # ---------------- Generate Button ----------------
    if st.button("🎯 Generate Mock Test", key="generate_exam"):
        sentences = clean_sentences(text_data)

        st.session_state["mcqs"] = []
        st.session_state["shorts"] = []

        for _ in range(num_mcq):
            s = random.choice(sentences)
            q = generate_mcq_from_sentence(s, text_data)
            if q:
                st.session_state["mcqs"].append(q)

        for _ in range(num_short):
            s = random.choice(sentences)
            st.session_state["shorts"].append({"q": s, "ans": s})

        st.session_state["test_ready"] = True
        st.success("✅ Mock test generated. Scroll down ⬇")

    # ---------------- Display Test ----------------
    if st.session_state.get("test_ready"):
        st.header("🧾 Mock Test")

        user_mcq = []
        st.subheader("MCQs")
        for i, q in enumerate(st.session_state["mcqs"]):
            st.write(f"Q{i+1}. {q['q']}")
            ans = st.radio(f"Answer {i}", q["options"], key=f"mcq_{i}")
            user_mcq.append(ans)

        user_short = []
        st.subheader("Short Answer Questions")
        for i, q in enumerate(st.session_state["shorts"]):
            st.write(f"S{i+1}. Explain: {q['q']}")
            ans = st.text_area(f"Your answer {i}", key=f"short_{i}")
            user_short.append(ans)

        # ---------------- Submit Button ----------------
        if st.button("✅ Submit Test", key="submit_exam"):
            total = 0
            max_marks = len(st.session_state["mcqs"]) * mark_mcq + len(st.session_state["shorts"]) * mark_short

            st.header("📊 Result")

            # MCQ Result
            for i, q in enumerate(st.session_state["mcqs"]):
                if user_mcq[i] == q["ans"]:
                    total += mark_mcq
                    st.success(f"Q{i+1} ✅ Correct")
                else:
                    st.error(f"Q{i+1} ❌ Wrong | Correct: {q['ans']}")

            # Short Result
            for i, q in enumerate(st.session_state["shorts"]):
                score = similarity(user_short[i], q["ans"])
                if score > 0.7:
                    total += mark_short
                    st.success(f"S{i+1} ✅ Good Answer")
                elif score > 0.4:
                    total += mark_short // 2
                    st.warning(f"S{i+1} ⚠️ Partial Answer")
                else:
                    st.error(f"S{i+1} ❌ Poor Answer")

            st.subheader(f"🏆 Your Score: {total} / {max_marks}")
