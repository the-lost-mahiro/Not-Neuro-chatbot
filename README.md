**Lưu ý: Nội dung dưới đây 90% là AI-Generated**

---

<h1 align="center">Not-Neuro AI VTuber</h1>
<p align="center">
  <i>Mục tiêu: Xây dựng một AI VTuber có khả năng tương tác tự nhiên như Neuro-sama. Đây là bước đặt nền móng về tư duy lập trình và xử lý ngôn ngữ tự nhiên (NLP) trong lộ trình 4 năm đại học.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/AI-Gemini%202.5-red.svg?style=for-the-badge&logo=google-gemini&logoColor=white">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge">
  <img src="https://img.shields.io/badge/VTube_Studio-API-pink?style=for-the-badge">
</p>

---

## Tổng quan dự án
Dự án **Not-Neuro** là một nỗ lực nhằm tái hiện khả năng tương tác thông minh của Neuro-sama. Đây là đồ án giai đoạn Năm 1, hiện tại đã có thể kết nối với VTube Studio và sử dụng các biểu cảm đơn giản.

---

### Tech Stack (Công nghệ sử dụng)
<p align="left">
  <a href="https://python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
  <a href="https://ai.google.dev/" target="_blank"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Google_Gemini_icon_2025.svg/2048px-Google_Gemini_icon_2025.svg.png" alt="gemini" width="40" height="40"/> </a>
  <a href="https://git-scm.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a>
</p>

---

## Kiến trúc hệ thống (Architecture)
Dưới đây là luồng xử lý dữ liệu của Not-Neuro:

```mermaid
graph TD
    User_Mic([Người dùng - Mic]) -->|Giọng nói| Ear[ear.py - STT]
    User_Terminal([Người dùng - Terminal]) -->|Nhập liệu| ConsoleInput[Input Terminal]
    Fan_Chat([Khán giả YouTube]) -->|Bình luận| ChatReader[chat_reader.py]
    
    Ear --> InputHandler
    ConsoleInput --> InputHandler
    
    ChatReader -->|Lọc Cooldown & Đẩy| MessageQueue[(Hàng đợi: asyncio.Queue)]
    MessageQueue -->|Rút từng tin nhắn| InputHandler{Bộ xử lý đầu vào}
    
    Timer([Autonomy Timer]) -.->|User im lặng > 15p| InputHandler{Bộ xử lý đầu vào}
    
    InputHandler -->|Gửi Prompt| Brain[Gemini API]
    Brain -->|Trả về JSON| Parser[Bộ phân tích JSON]
    
    Parser -->|Lưu lịch sử| Memory[(memory.json)]
    
    subgraph "Hệ thống phản hồi (Output)"
        Parser -->|Cảm xúc| Mood[Mood Engine]
        Mood -->|Tính Rate/Pitch| Voice[Voice Box]
        Parser -->|Text + Emotion| Body[Body Controller]
        
        Voice -->|Tạo Audio| Speaker((Loa/Tai nghe))
        Body -->|Trigger Hotkey| VTS_Key["VTube Studio (Biểu cảm)"]
        Body -->|Lip Sync| VTS_Lip["VTube Studio (Nhép môi)"]
        
        Parser -->|Hiển thị Text| Terminal(Màn hình Console)
    end
```

---

## Tính năng hiện có
Dưới đây là những gì mà 1 Not-Neuro có thể làm hiện tại

* **Hệ thống phản hồi:** Sử dụng Gemini 2.5 Flash API (có thể sử dụng các model version khác).

* **Hệ thống lệnh (Command System):**

  * `/status`: Kiểm tra tình trạng kết nối và model.

  * `/reset`: Xóa sạch bộ nhớ tạm của AI.

  * `/help`: Xem danh sách lệnh.
 
  * `/exit`: Thoát chương trình.

* **Quản lý ký ức:** Lưu lịch sử chat vào file `memory.json`.

* **Bảo mật:** Quản lý API Key thông qua biến môi trường (`.env`).

* **Kết nối Cơ thể:** Điều khiển trực tiếp VTube Studio (Nhép môi, Biểu cảm vui/buồn/giận).

* **Chế độ Tự chủ (Autonomy):** Bot tự động bắt chuyện nếu bạn im lặng quá 15 phút.

* **Giọng nói (TTS):** Sử dụng ElevenLab API.

* <s> **Hệ thống Cảm xúc:** Giọng nói thay đổi tốc độ và cao độ tùy theo tâm trạng (Vui nói nhanh, Buồn nói chậm). </s> (Chỉ áp dụng khi dùng Edge-TTS)

---

## Hướng dẫn cài đặt và sử dụng

### Yêu cầu
- **Python 3.10** trở lên.
- **VTube Studio** (Cài trên Steam) đang bật.

### Cài đặt thư viện và khởi tạo môi trường
Để tránh xung đột thư viện, hãy chạy lệnh sau:
```bash
# Cài đặt các thư viện cần thiết
python -m pip install -r requirements.txt
```

### Thiết lập API key
Vì lý do bảo mật, file chứa API Key không được upload lên GitHub. Bạn cần:

* Copy file `.env.example` và đổi tên thành `.env`.

* Mở file .env và dán API Key của bạn vào:
```Plaintext
GEMINI_API_KEY=Dán_Key_Của_Bạn_Ở_Đây
ELEVENLABS_API_KEY=Dán_Key_Của_Bạn_Ở_Đây
ELEVENLABS_VOICE_ID=Dán_ID_Của_Bạn_Ở_Đây
```

* Tạo `character_background.txt` tại thư mục gốc để viết prompt tính cách nhân vật. File này, `.env`, `memory.json` và `vts_token.txt` là dữ liệu cá nhân, không đưa lên Git.

### Xin quyền điều khiển (Chạy 1 lần duy nhất)
Lần đầu tiên chạy, bạn cần xin phép VTube Studio:

```Bash
python -m modules.vts_auth
```
Nhìn vào màn hình VTube Studio và bấm "Allow". Sau khi xong, file vts_token.txt sẽ được tạo ra.

### Khởi chạy chương trình
Sau khi cài đặt xong, bạn chỉ cần gõ:
```Bash
python main.py
```

Chạy các lệnh từ thư mục gốc dự án. `main.py` hiện dùng Ollama với model `qwen3:8b`; cần chạy Ollama và có sẵn model này. Để dùng Gemini, đổi thành `VtuberBrain(local_ai=False)` trong `main.py` và thiết lập `GEMINI_API_KEY`.

### API và giao diện web (tùy chọn)

```bash
python -m web.app
```

Lệnh này chạy Flask tại cổng 5000 và mở `web/index.html` trong trình duyệt. Web dùng Gemini và đọc `.env` ở thư mục gốc. API `POST /chat` nhận JSON `{"message": "Xin chào"}`; phản hồi hiện chỉ có trường `status`, còn lời nói và nội dung được xử lý bởi `brain.py`. Giao diện HTML là bản thử nghiệm, vẫn chờ các trường `display_text` và `mood_bar` mà API chưa trả về.

Để gửi một yêu cầu thử, mở terminal thứ hai tại thư mục gốc:

```bash
python -m tests.test_client
```

Đây là client kiểm tra thủ công, cần server và các dịch vụ liên quan đang chạy. Import file hoặc chạy test discovery sẽ không tự gửi yêu cầu HTTP.

## Cấu trúc thư mục

```
Not-Neuro-chatbot/
├── main.py                  # Điểm khởi chạy terminal
├── brain.py                 # Điều phối hội thoại và Autonomy
├── paths.py                 # Đường dẫn thư mục gốc và dữ liệu cục bộ
├── llm_core/                # Giao tiếp với các mô hình ngôn ngữ
│   ├── __init__.py
│   ├── llm_base.py
│   ├── llm_gemini.py
│   └── llm_ollama.py
├── modules/                 # Giác quan, giọng nói và điều khiển nhân vật
│   ├── __init__.py
│   ├── ear.py
│   ├── eye.py
│   ├── chat_reader.py
│   ├── body.py
│   ├── voice.py
│   ├── mood.py
│   └── vts_auth.py
├── web/                     # API Flask và giao diện thử nghiệm
│   ├── __init__.py
│   ├── app.py
│   └── index.html
├── tests/
│   ├── __init__.py
│   └── test_client.py       # Client kiểm tra API thủ công
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── .env                     # API key (cục bộ)
├── vts_token.txt            # Token kết nối (tự tạo, cục bộ)
├── memory.json              # Bộ nhớ ngắn hạn (tự tạo, cục bộ)
└── character_background.txt # Prompt tính cách nhân vật (cục bộ)
```

Các thư mục Python có `__init__.py`; dùng `python -m ...` cho script bên trong package. Đường dẫn tới dữ liệu cục bộ được tính từ `paths.py`, không phụ thuộc thư mục làm việc. `.idea/` và các file sinh ra khi chạy chương trình được bỏ qua trong `.gitignore`.

---

## 🗺️ Lộ trình phát triển (4 Năm)

- [x] Năm 1: Xây dựng Logic AI & Hệ thống lệnh cơ bản.

- [x] Năm 2: Tích hợp Giọng nói (TTS) & Hình ảnh Live2D đơn giản.

- [ ] Năm 3: Xây dựng RAG (Bộ nhớ dài hạn) & Tích hợp Twitch Chat.

- [ ] Năm 4: Đồ án tốt nghiệp: Hoàn thiện nhân vật & Stream thực tế.

---

<p align="center"> From Mahirou with ❤️ - An AI freshman </p>
