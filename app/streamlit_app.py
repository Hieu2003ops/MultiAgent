import streamlit as st
import os

def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Set the page configuration
    st.set_page_config(page_title="Topic Placeholder App", page_icon="🔧", layout="centered")

    # Load the external CSS file
    css_path = os.path.join(os.path.dirname(__file__), 'style.css')
    load_css(css_path)

    # Add a header to the app
    st.markdown("<div class='header'>Write Your Topic</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader'>Type your topic in the placeholder below and hit enter!</div>", unsafe_allow_html=True)

    # Text input with placeholder
    topic = st.text_input("", placeholder="Type your topic here...")

    # Display the user's topic after they input it
    if topic:
        st.markdown("<div class='output-header'>Your Topic:</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='output'>{topic}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
