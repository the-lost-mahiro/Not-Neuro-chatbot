import webbrowser
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from brain import VtuberBrain
from paths import PROJECT_ROOT

load_dotenv(PROJECT_ROOT / ".env")

app = Flask(__name__)
CORS(app) # Cho phép kết nối từ trình duyệt/Live2D

brain = VtuberBrain()

@app.route('/', methods=['GET'])
def home():
    return "<h1>Not-Neuro Server is ONLINE!</h1><p>Vui lòng dùng POST request gửi đến /chat để trò chuyện.</p>"

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    # Nhận dữ liệu JSON từ Client gửi lên
    data = request.json
    user_msg = data.get("message", "")

    if not user_msg:
        return jsonify({"status": "error", "message": "Tin nhắn trống!"}), 400

    # Chạy logic xử lý thông qua Brain (Dùng loop của Flask)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response_data = loop.run_until_complete(brain.process_chat(user_msg))
    loop.close()

    # Trả kết quả JSON về cho Client
    return jsonify(response_data)

if __name__ == "__main__":
    # Giao diện nằm cạnh app.py trong package web.
    file_path = Path(__file__).resolve().with_name("index.html")
    
    # Tạo lệnh mở file trên trình duyệt
    # 'file://' -> để trình duyệt hiểu đây là file cục bộ
    webbrowser.open(file_path.as_uri())
    
    # Chạy Server
    print("🚀 Server đang khởi động và mở trình duyệt...")
    app.run(host='0.0.0.0', port=5000, debug=False)
