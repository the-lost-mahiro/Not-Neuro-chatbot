import os
import json
import time
import asyncio
import re
from google import genai
from google.genai import types

from mood import VtuberMood
from body import VtuberBody
from voice import VtuberVoice

class VtuberBrain:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Lỗi: Không tìm thấy GEMINI_API_KEY trong file .env!")

        self.client = genai.Client(api_key = api_key)

        self.history_file = 'memory.json'
        self.history = self._load_memory() # Tải lại ký ức khi khởi động

        with open("character_background.txt", "r", encoding="utf-8") as f: # Mở file background
                system_instruction_content = f.read().strip()

        self.model_id = "gemini-2.5-flash-lite"
        self.config = types.GenerateContentConfig(
            system_instruction = system_instruction_content,
            response_mime_type = "application/json", #Ép trả về JSON chuẩn (không có 3 nháy)
            temperature = 0.7 #Creativity
        )

        self.last_interaction_time = time.time() # Lần cuối tương tác
        self.idle_threhold = 900 # 900s ~ 15p
        self.is_processing = False
        
        # Sử dụng client.aio để tạo phiên chat Async
        self.chat = self.client.aio.chats.create(model = self.model_id, 
                                                        config = self.config,
                                                        history = self.history)

        self.voice_box = VtuberVoice() # Voice

        self.mood_engine = VtuberMood() # Hệ thống cảm xúc

        self.body = VtuberBody()

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

    def _parse_response(self, response_text: str) -> dict:
        try:
            # Decode JSON
            return json.loads(response_text)
        
        except json.JSONDecodeError:
            # Nếu lỗi, thử lọc bỏ Markdown (```json ... ```)
            try:
                clean_json = re.sub(r'```json|```', '', response_text).strip()
                return json.loads(clean_json)
            
            except:
                # Nếu nát quá thì coi như là text thuần
                print(f"⚠️ Lỗi JSON, dùng chế độ Fallback. Text gốc: {response_text[:50]}...")
                return {
                    "display_text": response_text, 
                    "voice_text": response_text, 
                    "emotion": "default"
                }

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
    
    @staticmethod
    async def typewriter_print(text, delay = 0.05):
        # In chữ theo kiểu máy đánh chữ
        print("Not-Neuro: ", end='', flush = True)

        for char in text:
            print(char, end='', flush = True)
            await asyncio.sleep(delay)

        print("\n")
    
    async def perform_action(self, data: dict):
        display_text = data.get("display_text", "Mahiro ơi lỗi rồi!")
        voice_text = data.get("voice_text", "Mahiro ơi lỗi rồi!")
        emotion = data.get("emotion", "default")

        # Cập nhật mood và giọng
        self.mood_engine.update(emotion)
        rate, pitch = self.mood_engine.convert()
        mood_info = self.mood_engine.get_mood_bar()
        print(f"\n{mood_info}")

        # 1. Chuẩn bị Audio
        clean_voice = self.voice_box.clean_text(voice_text)
        is_audio_ready = await self.voice_box.prepare_audio(clean_voice, rate, pitch)

        if is_audio_ready:
            # 2. Audio xong -> Đổi mặt
            hotkey_map = {
                "happy": "Happy", 
                "sad": "Sad", 
                "angry": "Angry", 
                "default": "Default"
            }
            target_hotkey = hotkey_map.get(emotion)
            
            if target_hotkey:
                await self.body.trigger_hotkey(target_hotkey, duration=7)

            # 3. Phát tiếng + Nhép môi
            self.voice_box.play()
            
            # Tạo task nhép môi chạy song song
            sync_task = asyncio.create_task(self.body.lip_sync(self.voice_box.is_playing))
            
            # Chạy chữ kiểu máy đánh chữ
            await self.typewriter_print(display_text)

            # Chờ nói xong
            while self.voice_box.is_playing():
                await asyncio.sleep(0.1)

            await sync_task # Dừng nhép môi
            self.voice_box.stop_and_clear()

            # Tắt biểu cảm
            if target_hotkey:
                await self.body.trigger_hotkey(target_hotkey)
        else:
            # Nếu lỗi Audio thì chỉ hiện text
            await self.typewriter_print(display_text)
        
    async def autonomy_mode(self):
        while True:
            await asyncio.sleep(5)

            current_time = time.time()
            silence_duration = current_time - self.last_interaction_time

            if not self.is_processing and silence_duration > self.idle_threhold:
                self.is_processing = True # Lock

                try:
                    autonomy_prompt = (
                        "User đã im lặng 15 phút rồi. "
                        "Hãy tự nghĩ ra một câu nói ngắn (dưới 20 từ) để bắt chuyện một cách tự nhiên. "
                        "Ví dụ: than thở chán, hỏi user đang làm gì, hoặc kể một fact ngắn thú vị. "
                        "Đừng lặp lại câu cũ."
                        "Trả về định dạng JSON chuẩn như mọi khi."
                    )
                    response = await self.chat.send_message(autonomy_prompt)
                    
                    data = self._parse_response(response.text)

                    print(f"🤖 [Bot Tự Nghĩ]: {data.get('display_text')}")

                    self.history.append({"role": "model", "parts": [{"text": data.get("display_text")}]})

                    self._save_memory() # Optional

                    await self.perform_action(data)

                except Exception as e:
                    print(f"❌ Lỗi Autonomy: {e}")

                finally:
                    self.last_interaction_time = time.time()
                    self.is_processing = False # Unlock
                    

    async def process_chat(self, user_input: str):
        # Đảm bảo cơ thể đã kết nối ONE-TIME
        if not self.body.vts:
            await self.body.connect()

        self.is_processing = True
        try:
            response = await self.chat.send_message(user_input) # Gửi tin nhắn cho Gemini

            data = self._parse_response(response.text)
            
            # Cập nhật lịch sử mới
            self.history.append({"role": "user", "parts": [{"text": user_input}]})
            self.history.append({"role": "model", "parts": [{"text": data.get('display_text')}]})

            self._save_memory()

            await self.perform_action(data)

            return {"status": "success"}
        
        except Exception as e:
            print(f"❌ Lỗi chat: {e}")
            return {"status": "error"}

        finally:
            self.last_interaction_time = time.time() # Reset time
            self.is_processing = False

    async def run(self):
        print("=== TERMINAL ===")

        await self.body.connect()
        
        asyncio.create_task(self.autonomy_mode())

        while True:
            print("User: ", end='', flush=True)
            # run_in_executor -> input không chặn Autonomy loop
            loop = asyncio.get_running_loop()
            user_input = await loop.run_in_executor(None, input)

            self.last_interaction_time = time.time()

            if not user_input: continue #Empty String

            if user_input.startswith('/'): #Check command
                if user_input == '/exit':
                    await self.body.close()
                    break

                result = self.commands(user_input)
                print(f'SYSTEM: {result}\n')

            else:
                await self.process_chat(user_input)