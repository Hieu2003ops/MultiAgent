from fastapi import FastAPI, Request
import uvicorn
from pyngrok import ngrok
from main import run_crewai_pipeline  # Giữ nguyên main.py
from dotenv import load_dotenv
import os

# Load environment variables từ file .env
load_dotenv()
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")

# Kiểm tra xem có token Ngrok không
if not NGROK_AUTH_TOKEN:
    raise ValueError("🚨 Ngrok Auth Token chưa được thiết lập trong .env!")

# Khởi động FastAPI
app = FastAPI()

# 🔥 API GET để kiểm tra Backend đang chạy
@app.get("/")
def root():
    return {"message": "🚀 CrewAI Backend is running!"}

# 🔥 API GET để test Ngrok URL
@app.get("/test")
def test_api():
    return {"message": "✅ API đang hoạt động!", "status": "success"}

# 🔥 API POST để nhận topic và chạy CrewAI
@app.post("/generate")
async def generate_content(request: Request):
    data = await request.json()
    topic = data.get("topic", "")
    if not topic:
        return {"error": "Topic is required"}
    
    result, file_path = run_crewai_pipeline(topic)  # Gọi CrewAI từ main.py
    return {"content": result, "markdown_file": file_path}

# 🔥 Khởi động Ngrok để expose API
def start_ngrok():
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)  # Đăng nhập bằng API Key
    tunnel = ngrok.connect(8000)  # Expose port 8000
    public_url = tunnel.public_url
    print(f"🚀 Ngrok Tunnel: {public_url}")
    return public_url

if __name__ == "__main__":
    ngrok_url = start_ngrok()  # Mở tunnel
    uvicorn.run(app, host="0.0.0.0", port=8000)
