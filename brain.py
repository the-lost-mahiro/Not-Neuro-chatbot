import json
import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv()

class VtuberBrain:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Lỗi: Không tìm thấy GEMINI_API_KEY trong file .env!")

        self.client = genai.Client(api_key = api_key)

        self.history_file = 'memory.json'
        self.history = self._load_memory() # Tải lại ký ức khi khởi động

        self.model_id = "gemini-2.5-flash"
        self.config = types.GenerateContentConfig(
            system_instruction = "Bạn là một AI VTuber tên là Not-Neuro. Bạn xưng là em, tính cách tinh nghịch, vui tính", 
            temperature = 0.7 #Creativity
        )

    def _load_memory(self):
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return [] # Nếu chưa có file thì bắt đầu với bộ nhớ trống

    def _save_memory(self):
        with open(self.history_file, "w", encoding = "utf-8") as f:
            json.dump(self.history, f, ensure_ascii = False, indent = 4)

    def commands(self, cmd: str): #Local command
        cmd = cmd.lower().strip()

        if cmd == '/reset':
            self.history = []
            self._save_memory()
            return '🧹 Hệ thống đã được xóa sạch bộ nhớ!'
        
        elif cmd == '/status':
            return f"🤖 Model: {self.model_id} | Memory: {len(self.history)} messages."
        
        elif cmd == "/help":
            return "📌 Lệnh hiện có: /reset, /status, /help, /exit"
        
        else:
            return "❓ Lệnh không hợp lệ. Gõ /help để xem danh sách."

    def gen_response(self, prompt: str):
        try:
            chat = self.client.chats.create(model = self.model_id, 
                                                 config = self.config,
                                                 history = self.history)
            response = chat.send_message(prompt)

            # Cập nhật lịch sử mới
            self.history.append({"role": "user", "parts": [{"text": user_input}]})
            self.history.append({"role": "model", "parts": [{"text": response.text}]})
            
            self._save_memory() # Lưu lại ngay lập tức

            return response.text
        
        except Exception as e:
            return f'Lỗi: {e}'

if __name__ == "__main__":
    my_vtuber = VtuberBrain()
    
    print("===TERMINAL===")
    while True:
        user_input = input("User: ").strip()

        if not user_input: continue #Empty String

        if user_input.startswith('/'): #Check command
            if user_input == '/exit':
                break

            result = my_vtuber.commands(user_input)
            print(f'SYSTEM: {result}\n')

        else:
            answer = my_vtuber.gen_response(user_input)
            print(f"Not-Neuro: {answer}\n")