import streamlit as st
import os
from dotenv import load_dotenv
# from Final_Project.ai_agents import main

import sys
print(sys.path)


# Load CSS
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Set up page
    st.set_page_config(page_title="AI Content Generator", page_icon="📝", layout="centered")

    # Load custom CSS
    css_path = os.path.join(os.path.dirname(__file__), 'style.css')
    load_css(css_path)

    # App UI
    st.markdown("<div class='header'>🚀 AI Content Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader'>Enter a topic and let AI generate content for you!</div>", unsafe_allow_html=True)

    topic = st.text_input("Enter your topic:", placeholder="Type your topic here...")

    if st.button("Generate Content"):
        if topic:
            with st.spinner("Generating content... ⏳"):
                markdown_result, md_file_path = main.run_crewai_pipeline(topic)
            
            # Display result
            st.markdown("<div class='output-header'>Generated Content:</div>", unsafe_allow_html=True)
            st.markdown(markdown_result, unsafe_allow_html=True)

            # Display Markdown file download link
            if os.path.exists(md_file_path):
                with open(md_file_path, "r", encoding="utf-8") as f:
                    md_content = f.read()
                st.download_button("📥 Download Markdown", md_content, file_name="generated_content.md", mime="text/markdown")

        else:
            st.warning("⚠️ Please enter a topic before generating content.")

if __name__ == "__main__":
    main()
