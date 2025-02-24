import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai
import datetime

# Set your OpenAI API Key
openai.api_key = "your-api-key-here"  # 🔹 Replace this with your OpenAI API key

# Initialize session state for storing workout data
if "workouts" not in st.session_state:
    st.session_state.workouts = []

# Function to generate AI motivational messages
def get_motivation(duration, intensity):
    prompt = f"I just completed a {duration}-minute workout with an intensity of {intensity}/10. Give me a short, powerful motivational message with a growth mindset approach."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a motivational fitness coach who encourages a growth mindset."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

# Sidebar Navigation
st.sidebar.title("🏋️ Growth Mindset Fitness Tracker")
page = st.sidebar.radio("Go to", ["🏠 Dashboard", "📝 Log Workout", "📈 Progress", "🎯 Set Goals", "🧠 Mindset Reflection"])

# Dashboard
if page == "🏠 Dashboard":
    st.title("Welcome to Your Fitness Journey!")
    st.write("Track your workouts, set goals, and build a **growth mindset**.")

    if st.session_state.workouts:
        st.write("### 🏋️ Recent Workouts")
        df = pd.DataFrame(st.session_state.workouts)
        st.write(df.tail(5))
    else:
        st.write("No workouts logged yet. Start by adding your first one!")

# Log Workout
elif page == "📝 Log Workout":
    st.title("📝 Log Your Workout")
    date = st.date_input("Workout Date", datetime.date.today())
    exercise = st.text_input("Exercise")
    duration = st.number_input("Duration (minutes)", min_value=1)
    intensity = st.slider("Intensity (1-10)", 1, 10)
    notes = st.text_area("Notes")

    if st.button("Add Workout"):
        st.session_state.workouts.append({"Date": date, "Exercise": exercise, "Duration": duration, "Intensity": intensity, "Notes": notes})
        st.success("✅ Workout added successfully!")
        
        # Generate AI Motivation
        motivation = get_motivation(duration, intensity)
        st.write("💪 **Your AI Motivation:**")
        st.write(motivation)

# Progress Tracker
elif page == "📈 Progress":
    st.title("📊 Your Progress Over Time")
    if st.session_state.workouts:
        df = pd.DataFrame(st.session_state.workouts)
        df["Date"] = pd.to_datetime(df["Date"])

        # Line chart for workout duration
        fig, ax = plt.subplots()
        ax.plot(df["Date"], df["Duration"], marker='o', linestyle='-', color="blue")
        ax.set_title("Workout Duration Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Duration (minutes)")
        st.pyplot(fig)
    else:
        st.write("No progress data yet. Log workouts first!")

# Goal Setting
elif page == "🎯 Set Goals":
    st.title("🎯 Set Your Fitness Goals")
    goal = st.text_input("Your Fitness Goal")
    deadline = st.date_input("Goal Deadline")
    if st.button("Save Goal"):
        st.write(f"✅ Goal set: **{goal}** by **{deadline}**")

# Mindset Reflection
elif page == "🧠 Mindset Reflection":
    st.title("🧠 Mindset Reflection")
    reflection = st.text_area("Write about today's challenges, progress, or mindset shifts.")
    if st.button("Save Reflection"):
        st.write("📝 Reflection saved!")
