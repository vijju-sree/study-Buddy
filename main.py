import streamlit as st
import importlib
from login import login_page

st.set_page_config(page_title="AI Study Buddy", layout="wide")

# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False


# ---------- Home Page ----------
def home_page():

    # ------------------ Top Right Login Button ------------------
    col1, col2, col3 = st.columns([6, 2, 1])
    with col3:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()

    st.markdown("<h1 style='font-size:70px; text-align:center;color:Blue;'>AI StudyBuddy</h1>", unsafe_allow_html=True)

    st.title("🧠 AI Study Buddy – Student Assistant")

    st.markdown("""
    Study Buddy helps you with:

    - 🎙 Speech to Text  
    - 📘 Smart Notes Generator  
    - 📝 Mock Exams  
    - 📅 Study Planner  
    - 👨‍🏫 Teachable Machine  
    - ⏱️ Time Table Generator  
    - ❓ Doubt Solver  
    - 🤖 Digital Mentor
    """)

    # ---------------------- SPEECH TO TEXT ----------------------
    st.markdown("<h1 style='font-size:30px;color:yellow;'>🎙 Speech To Text</h1>", unsafe_allow_html=True)
    st.markdown("""
    A Speech-to-Text (STT) tool converts spoken words into written text using AI.  
    You speak → the AI listens → and it automatically types the text for you.
    """)
    st.markdown("1️⃣ Fast Note Taking")
    st.markdown("2️⃣ Write Long Answers Easily")
    st.markdown("3️⃣ Helps During Online Classes")
    st.markdown("4️⃣ Useful for Students with Slow Typing")
    st.markdown("5️⃣ Hands-free Productivity")

    # ---------------------- SMART NOTES GENERATOR ----------------------
    st.markdown("<h1 style='font-size:30px;color:yellow;'>📘 Smart Notes Generator</h1>", unsafe_allow_html=True)
    st.markdown("Smart Notes Generator converts long chapters into exam-ready short notes.")
    st.markdown("1️⃣ Converts long chapters into small points")
    st.markdown("2️⃣ Creates summaries and mind maps")
    st.markdown("3️⃣ Saves revision time")
    st.markdown("4️⃣ Removes unwanted content")
    st.markdown("5️⃣ Best for last-minute revision")

    # ---------------------- MOCK EXAMS ----------------------
    st.markdown("<h1 style='font-size:30px;color:yellow;'>📝 Mock Exams</h1>", unsafe_allow_html=True)
    st.markdown("Mock Exam tool generates practice tests automatically from any topic.")
    st.markdown("1️⃣ Creates MCQs & True/False questions")
    st.markdown("2️⃣ Shows right & wrong answers")
    st.markdown("3️⃣ Gives explanations")
    st.markdown("4️⃣ Reduces exam fear")
    st.markdown("5️⃣ Improves accuracy and speed")

    # ---------------------- STUDY PLANNER ----------------------
    st.markdown("<h1 style='font-size:30px;color:yellow;'>📅 Study Planner</h1>", unsafe_allow_html=True)
    st.markdown("AI Study Planner generates a personalised daily learning schedule.")
    st.markdown("1️⃣ Creates daily study plan")
    st.markdown("2️⃣ Balanced subject time")
    st.markdown("3️⃣ No overload on one subject")
    st.markdown("4️⃣ Tracks progress")
    st.markdown("5️⃣ Improves consistency")

    # ---------------------- TEACHABLE MACHINE ----------------------
    st.markdown("<h1 style='font-size:30px;color:yellow;'>👨‍🏫 Teachable Machine</h1>", unsafe_allow_html=True)
    st.markdown("Train your own AI model using images, audio or poses without coding.")
    st.markdown("1️⃣ Learn how AI models work")
    st.markdown("2️⃣ Train your own classifier")
    st.markdown("3️⃣ Useful for science fairs & projects")
    st.markdown("4️⃣ Easy interface")
    st.markdown("5️⃣ Best for beginners in ML")

    # ---------------------- TIME TABLE GENERATOR ----------------------
    st.markdown("<h1 style='font-size:30px;color:yellow;'>⏱️ Time Table Generator</h1>", unsafe_allow_html=True)
    st.markdown("AI Time Table Generator creates an optimized weekly schedule.")
    st.markdown("1️⃣ Avoids repeating same subject timing")
    st.markdown("2️⃣ Distributes difficult subjects properly")
    st.markdown("3️⃣ Balanced weekly time table")
    st.markdown("4️⃣ Saves planning time")
    st.markdown("5️⃣ Improves time management")

    # ---------------------- DOUBT SOLVER ----------------------
    st.markdown("<h1 style='font-size:30px;color:yellow;'>❓ Doubt Solver</h1>", unsafe_allow_html=True)
    st.markdown("Doubt Solver uses RAG AI to answer questions from your uploaded notes.")
    st.markdown("1️⃣ Ask any doubt instantly")
    st.markdown("2️⃣ Searches inside your PDFs")
    st.markdown("3️⃣ Gives step-by-step explanation")
    st.markdown("4️⃣ Useful for maths, physics & coding doubts")
    st.markdown("5️⃣ 24/7 virtual tutor")

    # ---------------------- DIGITAL MENTOR ----------------------
    st.markdown("<h1 style='font-size:30px;color:yellow;'>🤖 Digital Mentor</h1>", unsafe_allow_html=True)
    st.markdown("Digital Mentor acts as your study & career guidance AI.")
    st.markdown("1️⃣ Career guidance & learning paths")
    st.markdown("2️⃣ Study tips for every subject")
    st.markdown("3️⃣ Daily motivation")
    st.markdown("4️⃣ Helps choose career (AI, Dev, Multimedia)")
    st.markdown("5️⃣ Provides roadmaps for new skills")



# ---------- Dashboard ----------
def dashboard():
    st.sidebar.title("📚 Available Tools")

    option = st.sidebar.radio(
        "Choose Tool",
        [
            "🏠 Home",
            "🎙 Speech to Text",
            "📘 Smart Notes",
            "📝 Mock Test",
            "📅 Study Planner",
            "👨‍🏫 Teachable Machine",
            "⏱️ Time Table Generator",
            "❓ Doubt Solver",
            "🤖 Digital Mentor"
        ]
    )

    # ---------- FIXED HOME PAGE WITH WORKFLOW ----------
    if option == "🏠 Home":
        st.title("Welcome to AI Study Buddy Dashboard 🎉")

        st.markdown("""
        ## 🧠 What is AI Study Buddy?

        AI Study Buddy is an all-in-one study assistant designed to help students learn smarter using AI tools.  
        It improves productivity, helps in exams, and makes studying easier.

        ### 🎯 Why Use AI Study Buddy?
        - Saves time  
        - Helps understand topics quickly  
        - Creates notes automatically  
        - Generates practice exams  
        - Helps manage your study routine  
        """)

        st.markdown("---")

        st.markdown("## 🔄 How to Use AI Study Buddy (Workflow Guide)")

        st.markdown("""
        ### **1. 🎙 Speech to Text — Convert Voice to Notes**
        Workflow:
        - Open *Speech to Text*
        - Record or upload audio
        - AI converts voice → text  

        Best for: Class recordings, long answers, fast note-taking  
        """)

        st.markdown("""
        ### **2. 📘 Smart Notes Generator**
        Workflow:
        - Open *Smart Notes*
        - Paste text or upload file
        - Choose summary type
        - AI generates notes  
        """)

        st.markdown("""
        ### **3. 📝 Mock Exams**
        Workflow:
        - Enter topic
        - AI creates MCQ, True/False
        - Submit → get results  
        """)

        st.markdown("""
        ### **4. 📅 Study Planner**
        Workflow:
        - Enter subjects + hours
        - AI creates daily plan  
        """)

        st.markdown("""
        ### **5. 👨‍🏫 Teachable Machine**
        Workflow:
        - Upload images/audio
        - Train your own classifier  
        """)

        st.markdown("""
        ### **6. ⏱ Time Table Generator**
        Workflow:
        - Enter subjects
        - AI creates weekly schedule  
        """)

        st.markdown("""
        ### **7. ❓ Doubt Solver**
        Workflow:
        - Upload notes
        - Ask doubt
        - AI answers from your PDF  
        """)

        st.markdown("""
        ### **8. 🤖 Digital Mentor**
        Workflow:
        - Ask career doubt
        - Get study roadmaps  
        """)

    # ---------- Other Tools ----------
    elif option == "🎙 Speech to Text":
        st.title("🎙 Speech to Text")
        importlib.import_module("Nene").run()

    elif option == "📘 Smart Notes":
        st.title("📘 Smart Notes Generator")
        importlib.import_module("notes_generator").run()

    elif option == "📝 Mock Test":
        st.title("📝 Mock Test Practice")
        importlib.import_module("exam_practice").run()

    elif option == "📅 Study Planner":
        st.title("📅 Study Planner")
        importlib.import_module("study").run()

    elif option == "👨‍🏫 Teachable Machine":
        st.title("👨‍🏫 Teachable Machine")
        importlib.import_module("Mee").run()

    elif option == "⏱️ Time Table Generator":
        st.title("⏱️ Time Table Generator")
        importlib.import_module("timetable_ai").run()

    elif option == "❓ Doubt Solver":
        st.title("❓ Doubt Solver")
        importlib.import_module("1_rag_solver").run()

    elif option == "🤖 Digital Mentor":
        st.title("🤖 Digital Mentor")
        importlib.import_module("2_digital_mentor").run()

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.show_login = False
        st.rerun()


# ---------- Flow ----------
if st.session_state.logged_in:
    dashboard()
elif st.session_state.show_login:
    login_page()
else:
    home_page()
