import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import random

def run():
    st.title("🗓 Intelligent Timetable Maker (AI Scheduler)")

    # ---------------- Input ----------------
    subjects_input = st.text_area(
        "Enter subjects separated by commas", "Math, Physics, English, Chemistry, Biology"
    )
    subjects = [s.strip() for s in subjects_input.split(",") if s.strip()]

    start_hour = st.number_input("Start Hour (24h format)", 6, 12, 8)
    hours_per_day = st.number_input("Study hours per day", 1, min(12, len(subjects)), len(subjects))
    num_days = st.number_input("Number of days to schedule", 1, 14, 7)

    if st.button("Generate Random Timetable"):
        if not subjects:
            st.error("Enter at least one subject")
        elif hours_per_day > len(subjects):
            st.error("Hours per day cannot exceed number of subjects (no repeats allowed)")
        else:
            timetable = []
            days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

            for day_index in range(num_days):
                day_schedule = {"Day": days_of_week[day_index % 7]}
                time_pointer = datetime.strptime(f"{start_hour}:00", "%H:%M")
                
                # Randomize subjects without repetition
                daily_subjects = random.sample(subjects, k=hours_per_day)

                for subj in daily_subjects:
                    slot = f"{time_pointer.strftime('%H:%M')} - {(time_pointer + timedelta(hours=1)).strftime('%H:%M')}"
                    day_schedule[slot] = subj
                    time_pointer += timedelta(hours=1)

                timetable.append(day_schedule)

            df = pd.DataFrame(timetable)
            st.subheader("📝 Generated Random Timetable (No Repeats)")
            st.dataframe(df)

# Run directly
if __name__ == "__main__":
    run()
