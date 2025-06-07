import streamlit as st
from streamlit_option_menu import option_menu

# Your existing imports, data, functions...

def page_home():
    st.title("Home")
    st.write("Welcome to the AI Admissions Counselor!")

def page_profile():
    st.title("Profile Input")
    # Place your profile input widgets here
    interests = st.text_input("Enter your academic interests (e.g., Computer Science, Data Science):")
    strengths = st.text_input("Enter your personal strengths (e.g., strong in math, good communicator):")
    preferences = st.text_input("Enter your preferences (e.g., location, program type):")
    # You can keep the rest of your logic here or refactor into functions

def page_report():
    st.title("Admissions Report")
    st.write("Show recommendations, SWOT analysis, advice here")

def main():
    # Add horizontal navbar at the top
    selected = option_menu(
        menu_title=None,
        options=["Home", "Profile", "Report"],
        icons=["house", "person", "file-earmark-text"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Home":
        page_home()
    elif selected == "Profile":
        page_profile()
    elif selected == "Report":
        page_report()

if __name__ == "__main__":
    main()
