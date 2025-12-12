# File: study.py
import streamlit as st
import json
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ------------------ EMAIL CONFIG ------------------
EMAIL_ADDRESS = "your_email@gmail.com"       # replace with your email
EMAIL_PASSWORD = "your_app_password"         # Gmail App Password
RECIPIENT_EMAIL = "recipient_email@gmail.com"  # who will get the reminder

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# ------------------ DATA FILE ------------------
DATA_FILE = "study_plan.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ------------------ CREATE PLAN ------------------
def create_schedule(subject, hours, date, start_time_str):
    start_time = datetime.strptime(f"{date} {start_time_str}", "%Y-%m-%d %H:%M")
    end_time = start_time + timedelta(hours=hours)
    return {
        "subject": subject,
        "hours": hours,
        "start": start_time.strftime("%H:%M"),
        "end": end_time.strftime("%H:%M"),
        "date": date
    }

# ------------------ STREAMLIT UI ------------------
def run():
    st.write("📅 Study Planner Running!")

    st.set_page_config(page_title="📘 Study Buddy - Planner")
    st.title("📘 Study Buddy - Daily Study Planner")

    # Input Section
    st.header("📝 Add Study Goals")
    date_selected = st.date_input("Select Date", value=datetime.now())
    subject = st.text_input("Subject Name (Maths, Python etc)")
    time_hr = st.number_input("Study Time (hours)", min_value=1, max_value=12, value=1)
    start_time_input = st.text_input("Start Time (HH:MM, 24hr format)", "08:00")

    if st.button("➕ Add to Plan"):
        if subject.strip() == "":
            st.error("Please enter a subject name")
        else:
            plans = load_data()
            new_plan = create_schedule(subject, time_hr, date_selected.strftime("%Y-%m-%d"), start_time_input)
            plans.append(new_plan)
            save_data(plans)
            st.success(f"✅ Study plan saved for {date_selected.strftime('%Y-%m-%d')}!")

    # Show Plans
    st.header("📅 View Study Plans")
    view_date = st.date_input("Select Date to View", value=datetime.now())
    plans = load_data()
    plans_for_date = [p for p in plans if p["date"] == view_date.strftime("%Y-%m-%d")]

    if len(plans_for_date) == 0:
        st.info(f"No study plans for {view_date.strftime('%Y-%m-%d')}.")
    else:
        for i, plan in enumerate(plans_for_date):
            with st.expander(f"{plan['subject']} ({plan['start']} → {plan['end']})"):
                st.write(f"📚 Subject: {plan['subject']}")
                st.write(f"⏱ Time: {plan['hours']} hours")
                st.write(f"🕒 Start: {plan['start']}")
                st.write(f"🕒 End: {plan['end']}")

    # ------------------ SEND EMAIL REMINDERS ------------------
    current_time = datetime.now()
    for plan in plans_for_date:
        plan_start = datetime.strptime(f"{plan['date']} {plan['start']}", "%Y-%m-%d %H:%M")
        # If 5 minutes before start
        if plan_start - timedelta(minutes=5) <= current_time < plan_start:
            send_email(RECIPIENT_EMAIL, 
                       "Study Reminder",
                       f"Your study session '{plan['subject']}' starts at {plan['start']}.")

