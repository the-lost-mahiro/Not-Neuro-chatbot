import re
import asyncio
import json
import os
import edge_tts
import pygame
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class VtuberVoice:
    def __init__(self, voice_name = 'vi-VN-HoaiMyNeural'):
        self.voice = voice_name
        pygame.mixer.init()

    def clean_text(self, text):
        """Lọc bỏ icon để tránh TTS đọc lỗi"""
        return re.sub(r'[^\w\s,.?!]', '', text)
    
    async def talk(self, text: str, emotion: str):
        # Thiết lập thông số dựa trên cảm xúc
        rate = "+0%"
        pitch = "+0Hz"
        
        if emotion == "happy":
            rate = "+20%"  # Nói nhanh hơn khi vui
            pitch = "+10Hz" # Giọng cao hơn
        elif emotion == "sad":
            rate = "-15%"  # Nói chậm lại
            pitch = "-5Hz"  # Giọng trầm xuống

        audio_file = 'speech.mp3'

        communicate = edge_tts.Communicate(text, self.voice, rate = rate, pitch = pitch) #Gọi API
        await communicate.save(audio_file)

        pygame.mixer.music.load(audio_file) #Phát file
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy(): #Chờ nói xong
            await asyncio.sleep(0.1)

        pygame.mixer.music.unload() #Giải phóng file

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
            system_instruction = 'Bạn là một AI VTuber tên là Not-Neuro.' \
            'Bạn xưng là em, tính cách tinh nghịch, vui tính.' \
            'LUÔN TRẢ LỜI DƯỚI DẠNG JSON với cấu trúc:' \
            '{"display_text": "nội dung kèm icon",' \
            '"voice_text": "nội dung chỉ có chữ",' \
            '"emotion": "happy/sad/angry/default"}',
            response_mime_type = "application/json", #Ép trả về JSON chuẩn (không có 3 nháy)
            temperature = 0.7 #Creativity
        )

        self.voice_box = VtuberVoice() #Voice

    def clean_text(self, text):
        # Xóa các ký tự không phải chữ cái, số hoặc dấu câu cơ bản
        return re.sub(r'[^\w\s,.?!]', '', text)

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
        
    async def run(self):
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
                try:
                    chat = self.client.chats.create(model = self.model_id, 
                                                        config = self.config,
                                                        history = self.history)
                    response = chat.send_message(user_input)
                    
                    # Phân tích JSON từ AI
                    data: dict = json.loads(response.text)
                    display_text = data.get("display_text", "Em đang bận một tí...")
                    voice_text = data.get("voice_text", "Em đang bận một tí...")
                    emotion = data.get("emotion", "default")

                    # Cập nhật lịch sử mới
                    self.history.append({"role": "user", "parts": [{"text": user_input}]})
                    self.history.append({"role": "model", "parts": [{"text": display_text}]})
                    
                    self._save_memory() # Lưu lại ngay lập tức
                    
                    print(f"Not-Neuro: {display_text}\n")

                    clean_voice = self.voice_box.clean_text(voice_text) #Nói
                    await self.voice_box.talk(clean_voice, emotion)

                except json.JSONDecodeError:
                    # Phòng trường hợp AI không trả về đúng định dạng JSON
                    print("Hệ thống xử lý JSON gặp sự cố, đang dùng chế độ dự phòng...")
                    # Nếu AI vẫn lỡ tay trả về chuỗi lạ, ta sẽ lọc bỏ Markdown bằng Regex
                    clean_json = re.sub(r'```json|```', '', response.text).strip()
                    data = json.loads(clean_json)
                    print(f"Not-Neuro: {response.text}")
                    await self.voice_box.talk(self.clean_text(response.text), "default")
                            
                except Exception as e:
                    return f'Lỗi: {e}'

if __name__ == "__main__":
    my_vtuber = VtuberBrain()
    asyncio.run(my_vtuber.run())