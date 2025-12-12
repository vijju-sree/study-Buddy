import streamlit as st
import pandas as pd
import random
import time

def run():
    st.title("⏰ Digital Mentor (DM) Blueprint")
    st.subheader("Simulated Analysis based on User-Submitted Task History")
    st.markdown("---")

    if 'dm_task_data' not in st.session_state:
        st.session_state.dm_task_data = pd.DataFrame({
            "Task": ["Algebra Practice"],
            "Effort_Level": ["High"],
            "Observed_Focus": ["Low (14:00)"]
        })

    with st.form("task_input_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_task = st.text_input("Task Name", value="History Reading", key="new_task")
            new_effort = st.selectbox("Effort Level", ["Low","Medium","High"], key="new_effort")
        with col2:
            new_focus = st.text_input("Observed Focus (e.g., Low (14:00))", value="High (10:00)", key="new_focus")
            st.write("*(Time is only for display/simulation)*")
        submitted = st.form_submit_button("Add Task to History")
        if submitted:
            st.session_state.dm_task_data = pd.concat(
                [st.session_state.dm_task_data, pd.DataFrame([{
                    "Task": new_task,
                    "Effort_Level": new_effort,
                    "Observed_Focus": new_focus
                }])], ignore_index=True
            )

    st.markdown("### 📊 Current Study History")
    st.dataframe(st.session_state.dm_task_data, use_container_width=True)

    def analyze_circadian_rhythm(task_history):
        low_start, low_end = 14, 16
        high_time = 10
        gain = random.randint(10,25)
        return low_start, low_end, high_time, gain

    if st.button("Run DM Analysis & Get Optimized Schedule"):
        low_start, low_end, high_time, gain = analyze_circadian_rhythm(st.session_state.dm_task_data)
        st.markdown("#### ✅ DM Actionable Output")
        msg = f"""
        Based on {len(st.session_state.dm_task_data)} tasks:
        Focus Decline Window: {low_start}:00 - {low_end}:00
        High-effort task should be scheduled at {high_time}:00
        Expected efficiency gain: {gain}%
        """
        st.markdown(f"<div style='padding:15px; background-color:#e6f7ff; border-radius:8px;'>{msg}</div>", unsafe_allow_html=True)
        st.balloons()
