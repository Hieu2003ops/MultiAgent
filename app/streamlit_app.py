import streamlit as st
import requests
import os

# 🔥 Ngrok URL của Backend (CẬP NHẬT nếu restart Ngrok)
NGROK_URL = "https://6619-2001-ee1-db09-8120-5433-3898-237-ef2e.ngrok-free.app"

# Load CSS
def load_css(css_file):
    """Hàm load file CSS để custom giao diện."""
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main_ui():
    """Hàm chính để chạy UI Streamlit."""
    # Cấu hình trang Streamlit
    st.set_page_config(page_title="AI Content Generator", page_icon="📝", layout="centered")

    # Load CSS
    css_path = os.path.join(os.path.dirname(__file__), 'style.css')
    load_css(css_path)

    # Hiển thị tiêu đề
    st.markdown("<div class='header'>🚀 AI Content Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader'>Nhập chủ đề và để AI tạo nội dung cho bạn!</div>", unsafe_allow_html=True)

    # Ô nhập chủ đề từ người dùng
    topic = st.text_input("🔍 Nhập chủ đề:", placeholder="Nhập chủ đề tại đây...")

    if st.button("🚀 Generate Content"):
        if topic:
            with st.spinner("⏳ Đang tạo nội dung..."):
                try:
                    response = requests.post(f"{NGROK_URL}/generate", json={"topic": topic})
                    if response.status_code == 200:
                        data = response.json()
                        st.markdown("<div class='output-header'>📜 Nội dung đã tạo:</div>", unsafe_allow_html=True)
                        st.markdown(data["content"], unsafe_allow_html=True)

                        # Hiển thị nút tải file Markdown nếu có
                        if "markdown_file" in data:
                            with open(data["markdown_file"], "r", encoding="utf-8") as f:
                                md_content = f.read()
                            st.download_button("📥 Tải Markdown", md_content, file_name="generated_content.md", mime="text/markdown")

                    else:
                        st.error(f"🚨 Lỗi khi gọi API Backend! Mã lỗi: {response.status_code}")

                except Exception as e:
                    st.error(f"🚨 Lỗi kết nối đến Backend! Chi tiết: {str(e)}")

        else:
            st.warning("⚠️ Vui lòng nhập chủ đề!")

if __name__ == "__main__":
    main_ui()
