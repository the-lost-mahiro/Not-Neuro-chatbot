**Lưu ý: Nội dung dưới đây là AI-Generated**

---

# 🤖 Fake-Neuro AI VTuber (Phase 1: Brain & Command System)
### Mục tiêu: Xây dựng một AI VTuber có khả năng tương tác tự nhiên như Neuro-sama. Đây là bước đặt nền móng về tư duy lập trình và xử lý ngôn ngữ tự nhiên (NLP) trong lộ trình 4 năm đại học.

---

## ✨ Tính năng hiện có
Dưới đây là những gì mà 1 Fake-Neuro có thể làm hiện tại

* **Hệ thống phản hồi:** Sử dụng Gemini 2.5 Flash API (tối ưu tốc độ cho máy cấu hình thấp).

* **Hệ thống lệnh (Command System):**

  * `/status`: Kiểm tra tình trạng kết nối và model.

  * `/reset`: Xóa sạch bộ nhớ tạm của AI.

  * `/help`: Xem danh sách lệnh.

* **Quản lý ký ức:** Lưu lịch sử chat vào file `memory.json`.

* **Bảo mật:** Quản lý API Key thông qua biến môi trường (`.env`).

---

## 🛠 Công nghệ & Kỹ thuật
| Thành phần | Công nghệ | Mục tiêu học thuật |
| :--- | :--- | :--- |
| **Ngôn ngữ** | Python 3.9+ | Tư duy lập trình hướng đối tượng (**OOP**) |
| **AI Model** | Google GenAI | Làm quen với **Prompt Engineering** |
| **Database** | JSON File | Hiểu về **Cấu trúc dữ liệu & Giải thuật** |
| **Environment** | Dotenv | Kỹ năng **Quản lý cấu hình phần mềm** |

---

## 🚀 Hướng dẫn cài đặt
Dự án được tối ưu để chạy nhẹ nhàng trên mọi cấu hình máy tính.

### 1️⃣ Khởi tạo môi trường
Để tránh xung đột thư viện, hãy chạy lệnh sau:
```bash
# Cài đặt các thư viện cần thiết
pip install -U google-genai python-dotenv
```
google-genai: SDK mới nhất để giao tiếp với bộ não AI.
python-dotenv: Giúp chương trình đọc Key bí mật từ file ẩn.

### 2️⃣ Cấu hình bí mật
Vì lý do bảo mật, file chứa API Key không được upload lên GitHub. Bạn cần:

* Copy file `.env.example` và đổi tên thành `.env`.

* Mở file .env và dán API Key của bạn vào:
```Plaintext
GEMINI_API_KEY=Dán_Key_Của_Bạn_Ở_Đây
```

### 3️⃣ Khởi chạy
Sau khi cài đặt xong, bạn chỉ cần gõ:
```Bash
python brain.py
```

---

## 🗺️ Lộ trình phát triển (4 Năm)

- [x] Năm 1: Xây dựng Logic AI & Hệ thống lệnh cơ bản.

- [ ] Năm 2: Tích hợp Giọng nói (TTS) & Hình ảnh Live2D đơn giản.

-  [ ] Năm 3: Xây dựng RAG (Bộ nhớ dài hạn) & Tích hợp Twitch Chat.

- [ ] Năm 4: Đồ án tốt nghiệp: Hoàn thiện nhân vật & Stream thực tế.

---

**Cảm ơn đã đọc hết!**
