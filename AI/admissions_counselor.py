import streamlit as st
from streamlit_option_menu import option_menu
import openai
import os
from streamlit_lottie import st_lottie
import requests

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_advice_from_openai(profile, matched_programs):
    interests = ", ".join(profile["interests"])
    strengths = ", ".join(profile["strengths"])
    preferences = profile["preferences"]

    programs_text = "\n".join([f"- {p['program']} at {p['university']} in {p['location'].title()}" for p in matched_programs]) or "No matched programs"

    prompt = f"""
    The student has these interests: {interests}
    Strengths: {strengths}
    Preferences: {preferences}

    Based on this, provide advice and recommend how they should approach their applications.
    Consider the following programs:
    {programs_text}
    """

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7,
        )
        advice = response.choices[0].text.strip()
        return advice
    except Exception as e:
        return f"Error: {e}"

# Example program data (replace with real data if you want)
program_data = [
    {
        "university": "Tech University",
        "program": "Bachelor in Computer Science",
        "keywords": ["computer science", "programming", "software engineering"],
        "location": "new york",
        "program_type": "undergraduate"
    },
    {
        "university": "Data Institute",
        "program": "Master in Data Science",
        "keywords": ["data science", "machine learning", "ai"],
        "location": "california",
        "program_type": "postgraduate"
    },
]

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def page_home():
    st.markdown("""
    <h1 style="text-align:center; color:#f0f0f0;">🎓 Welcome to AI Admissions Counselor</h1>
    <p style="text-align:center; font-size:18px; color:#ddd;">
    Your personalized guide for academic program recommendations and application advice.
    </p>
    """, unsafe_allow_html=True)

    lottie_animation = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_touohxv0.json")
    if lottie_animation:
        st_lottie(lottie_animation, speed=1, width=400, height=400)

def page_profile(session_state):
    st.subheader("Profile Input")

    col1, col2 = st.columns(2)

    with col1:
        interests = st.text_input(
            "Academic Interests (comma separated)", 
            value=session_state.get("interests_input", ""), 
            placeholder="e.g., Computer Science, Data Science"
        )
        strengths = st.text_input(
            "Personal Strengths (comma separated)", 
            value=session_state.get("strengths_input", ""), 
            placeholder="e.g., strong in math, good communicator"
        )

    with col2:
        preferences = st.text_input(
            "Preferences (location, program type)", 
            value=session_state.get("preferences_input", ""), 
            placeholder="e.g., California, postgraduate"
        )

    if st.button("Save Profile"):
        if not interests.strip() or not strengths.strip():
            st.warning("⚠️ Please enter valid interests and strengths.")
            return False

        session_state["interests_input"] = interests
        session_state["strengths_input"] = strengths
        session_state["preferences_input"] = preferences

        # Process inputs into lists and strings (lowercase)
        session_state["profile"] = {
            "interests": [i.strip().lower() for i in interests.split(",") if i.strip()],
            "strengths": [s.strip().lower() for s in strengths.split(",") if s.strip()],
            "preferences": preferences.lower().strip(),
        }
        st.success("✅ Profile saved! Now go to Recommendations tab.")
        return True
    return False

def page_recommendations(session_state):
    if "profile" not in session_state or not session_state["profile"]:
        st.info("Please fill out your profile first on the Profile tab.")
        return
    
    profile = session_state["profile"]
    
    matched_programs = []
    for p in program_data:
        if any(interest in p["keywords"] for interest in profile["interests"]):
            # Check preferences match if provided
            if profile["preferences"]:
                if profile["preferences"] in p["location"] or profile["preferences"] in p["program_type"]:
                    matched_programs.append(p)
            else:
                matched_programs.append(p)

    st.subheader("Recommended Programs")
    if matched_programs:
        for i, prog in enumerate(matched_programs, 1):
            st.markdown(
                f"""
                <div class="program-card">
                    <strong>{i}. {prog['program']}</strong> at <em>{prog['university']}</em><br>
                    📍 Location: {prog['location'].title()}<br>
                    🎯 Program Type: {prog['program_type'].capitalize()}
                </div>
                """, unsafe_allow_html=True
            )
    else:
        st.info("⚠️ No matching programs found. Try adjusting your profile.")

    with st.spinner("Getting AI-generated advice..."):
        advice = get_advice_from_openai(profile, matched_programs)
    st.subheader("AI-Generated Application Advice 💡")
    st.write(advice)

def main():
    st.set_page_config(page_title="AI Admissions Counselor", page_icon="🎓", layout="centered")

    # Inject custom CSS styles for improved UI
    st.markdown("""
    <style>
    /* Body background */
    .stApp {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: #f0f0f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Headers */
    h1, h2, h3 {
        font-weight: 700;
    }

    /* Input boxes */
    div.stTextInput > div > input {
        background-color: #2e2e2e;
        color: white;
        border-radius: 8px;
        padding: 8px;
        border: 1px solid #555;
    }

    /* Buttons */
    .stButton > button {
        background: #6c63ff;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background: #5548c8;
        color: #fff;
    }

    /* Recommended program cards */
    .program-card {
        background-color: #3b3b98;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 10px;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    # Use Session State to keep user inputs across pages
    if "interests_input" not in st.session_state:
        st.session_state["interests_input"] = ""
    if "strengths_input" not in st.session_state:
        st.session_state["strengths_input"] = ""
    if "preferences_input" not in st.session_state:
        st.session_state["preferences_input"] = ""
    if "profile" not in st.session_state:
        st.session_state["profile"] = None

    selected = option_menu(
        menu_title=None,
        options=["Home", "Profile", "Recommendations"],
        icons=["house", "person", "check2-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Home":
        page_home()
    elif selected == "Profile":
        page_profile(st.session_state)
    elif selected == "Recommendations":
        page_recommendations(st.session_state)

if __name__ == "__main__":
    main()
