import streamlit as st
import requests

# --- Data Sample ---
program_data = [
    {
        "university": "Massachusetts Institute of Technology",
        "program": "Computer Science and Engineering",
        "location": "cambridge, ma",
        "program_type": "master",
        "keywords": ["computer science", "engineering", "ai", "ml", "cs"],
    },
    {
        "university": "Stanford University",
        "program": "Artificial Intelligence Master Program",
        "location": "stanford, ca",
        "program_type": "master",
        "keywords": ["ai", "artificial intelligence", "ml", "machine learning"],
    },
    {
        "university": "Harvard University",
        "program": "Data Science Certificate",
        "location": "cambridge, ma",
        "program_type": "certificate",
        "keywords": ["data science", "statistics", "ml", "analytics"],
    },
    {
        "university": "University of California, Berkeley",
        "program": "Full Stack Development Bootcamp",
        "location": "berkeley, ca",
        "program_type": "certificate",
        "keywords": ["web development", "full stack", "javascript", "react"],
    },
]

# --- Utility functions ---
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            st.error(f"Failed to load animation. Status code: {r.status_code}")
            return None
        return r.json()
    except Exception as e:
        st.error(f"Error loading animation: {e}")
        return None

# --- CSS Styling ---
def local_css():
    st.markdown(
        """
    <style>
    /* Body */
    .stApp {
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Card style */
    .program-card {
        background: #3b3b98;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 15px;
        box-shadow: 4px 4px 12px rgba(0,0,0,0.4);
        color: white;
    }
    /* Sidebar header */
    .sidebar .sidebar-content {
        background-color: #2f2f5e;
        color: white;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

# --- Pages ---
def page_home():
    st.title("🎓 AI Admissions Counselor")
    st.markdown(
        "Welcome! Use this AI-powered app to discover the best college and program matches for you based on your interests and preferences."
    )
    lottie_welcome = load_lottie_url(
        "https://assets1.lottiefiles.com/packages/lf20_w51pcehl.json"
    )
    if lottie_welcome:
        st_lottie(lottie_welcome, speed=1, height=250)
    st.markdown(
        """
    ---
    **How to use:**
    - Fill your profile with your interests, strengths, and preferences
    - Explore personalized program recommendations
    - Check your dashboard for quick insights
    - Reach out if you need more help!
    """
    )


def page_profile(session_state):
    st.title("📝 Your Profile")
    with st.form("profile_form"):
        name = st.text_input("Full Name", value=session_state.get("profile", {}).get("name", ""))
        email = st.text_input("Email", value=session_state.get("profile", {}).get("email", ""))
        interests = st.multiselect(
            "Select your interests",
            [
                "Computer Science",
                "Artificial Intelligence",
                "Machine Learning",
                "Data Science",
                "Web Development",
                "Robotics",
                "Electrical Engineering",
                "Mechanical Engineering",
                "Business",
                "Psychology",
                "Biology",
                "Chemistry",
                "Mathematics",
            ],
            default=session_state.get("profile", {}).get("interests", []),
        )
        strengths = st.multiselect(
            "Your Strengths",
            [
                "Programming",
                "Mathematics",
                "Writing",
                "Research",
                "Communication",
                "Creativity",
                "Leadership",
            ],
            default=session_state.get("profile", {}).get("strengths", []),
        )
        location_pref = st.selectbox(
            "Preferred Location",
            ["Any", "Cambridge, MA", "Stanford, CA", "Berkeley, CA", "Online"],
            index=0,
        )
        program_type_pref = st.selectbox(
            "Preferred Program Type",
            ["Any", "Master", "Certificate", "Bootcamp"],
            index=0,
        )
        budget = st.selectbox("Budget Range", ["Any", "Low", "Medium", "High"], index=0)
        online_pref = st.radio("Prefer Online Programs?", ["No Preference", "Yes", "No"], index=0)

        submitted = st.form_submit_button("Save Profile")
        if submitted:
            session_state["profile"] = {
                "name": name,
                "email": email,
                "interests": [i.lower() for i in interests],
                "strengths": [s.lower() for s in strengths],
                "preferences": [location_pref.lower(), program_type_pref.lower()],
                "budget": budget.lower(),
                "online_preference": online_pref.lower(),
            }
            st.success("Profile saved successfully!")


def page_dashboard(session_state):
    st.title("📊 Dashboard")
    if "profile" not in session_state or not session_state["profile"]:
        st.info("Please complete your profile first under the Profile tab.")
        return

    profile = session_state["profile"]
    interests = profile.get("interests", [])
    strengths = profile.get("strengths", [])
    prefs = profile.get("preferences", ["any", "any"])

    st.markdown(f"**Name:** {profile.get('name', '')}")
    st.markdown(f"**Email:** {profile.get('email', '')}")
    st.markdown(f"**Interests:** {', '.join([i.title() for i in interests])}")
    st.markdown(f"**Strengths:** {', '.join([s.title() for s in strengths])}")
    st.markdown(
        f"**Preferences:** Location - {prefs[0].title()}, Program Type - {prefs[1].title()}"
    )
    st.markdown("---")

    matched_programs = []
    pref_location = prefs[0]
    pref_prog_type = prefs[1]

    for p in program_data:
        # Match interests keywords
        if any(interest in p["keywords"] for interest in interests):
            location_match = pref_location == "any" or pref_location in p["location"]
            program_type_match = pref_prog_type == "any" or pref_prog_type == p["program_type"]
            if location_match and program_type_match:
                matched_programs.append(p)

    st.markdown(f"### Matched Programs: {len(matched_programs)}")

    for prog in matched_programs:
        st.markdown(
            f"- **{prog['program']}** at *{prog['university']}* ({prog['location'].title()})"
        )

    st.success("Keep your profile updated for better recommendations!")

    lottie_dash = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_jcikwtux.json")
    if lottie_dash:
        st_lottie(lottie_dash, speed=1, height=150)


def page_recommendations(session_state):
    st.title("✅ Program Recommendations")
    if "profile" not in session_state or not session_state["profile"]:
        st.info("Please complete your profile first under the Profile tab.")
        return

    interests = session_state["profile"].get("interests", [])
    prefs = session_state["profile"].get("preferences", ["any", "any"])
    pref_location = prefs[0]
    pref_prog_type = prefs[1]

    filtered_programs = []
    for p in program_data:
        if any(interest in p["keywords"] for interest in interests):
            location_match = pref_location == "any" or pref_location in p["location"]
            program_type_match = pref_prog_type == "any" or pref_prog_type == p["program_type"]
            if location_match and program_type_match:
                filtered_programs.append(p)

    if not filtered_programs:
        st.warning("No programs matched your profile. Try updating your interests or preferences.")
        return

    for prog in filtered_programs:
        st.markdown(
            f'<div class="program-card">'
            f'<h4>{prog["program"]}</h4>'
            f'<p><strong>University:</strong> {prog["university"]}</p>'
            f'<p><strong>Location:</strong> {prog["location"].title()}</p>'
            f'<p><strong>Program Type:</strong> {prog["program_type"].title()}</p>'
            "</div>",
            unsafe_allow_html=True,
        )


def page_testimonials():
    st.title("💬 Testimonials")
    testimonials = [
        {"name": "Alice", "comment": "This app helped me find the perfect program! Highly recommend."},
        {"name": "Bob", "comment": "AI advice was spot-on and really boosted my confidence."},
        {"name": "Chloe", "comment": "Easy to use and very helpful for planning my studies."},
    ]
    for t in testimonials:
        st.markdown(f"**{t['name']}** says: _\"{t['comment']}\"_")


def page_about():
    st.title("ℹ️ About & FAQ")
    st.markdown(
        """
    **About:**  
    AI Admissions Counselor is designed to help you find college programs tailored to your interests and goals.

    **FAQ:**  
    - *How does the AI recommend programs?*  
      It matches your interests and preferences against a curated dataset of programs.  
    - *Is this app free to use?*  
      Yes, completely free!  
    - *Can I update my profile anytime?*  
      Yes, just go to the Profile tab and save changes.
    """
    )


def page_contact():
    st.title("📞 Contact Us")
    st.markdown(
        """
    For support or inquiries, email us at:  
    [support@aiadmissionscounselor.app](mailto:sagarmann954@gmail.com)
    """
    )


# --- Main App ---
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu


def set_theme(dark_mode: bool):
    if dark_mode:
        st.markdown(
            """
        <style>
        .stApp {
            background-color: #121212;
            color: #e0e0e0;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
        <style>
        .stApp {
            background-color: white;
            color: black;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )


def main():
    st.set_page_config(page_title="AI Admissions Counselor", layout="wide")
    local_css()

    if "profile" not in st.session_state:
        st.session_state["profile"] = {}

    dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=True)
    set_theme(dark_mode)

    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=[
                "Home",
                "Profile",
                "Dashboard",
                "Recommendations",
                "Testimonials",
                "About",
                "Contact",
            ],
            icons=[
                "house",
                "person",
                "bar-chart-line",
                "check2-circle",
                "chat-quote",
                "info-circle",
                "envelope",
            ],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Home":
        page_home()
    elif selected == "Profile":
        page_profile(st.session_state)
    elif selected == "Dashboard":
        page_dashboard(st.session_state)
    elif selected == "Recommendations":
        page_recommendations(st.session_state)
    elif selected == "Testimonials":
        page_testimonials()
    elif selected == "About":
        page_about()
    elif selected == "Contact":
        page_contact()


if __name__ == "__main__":
    main()
