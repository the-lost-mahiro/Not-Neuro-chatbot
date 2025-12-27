Lưu ý: Nội dung dưới đây là AI-Generated

🤖 Fake-Neuro AI VTuber (Phase 1: Brain & Command System)
Đây là bước đi đầu tiên trong lộ trình 4 năm để xây dựng một AI VTuber (giống Neuro-sama) cho đồ án tốt nghiệp. Hiện tại, dự án đã hoàn thành phần "Bộ não" cơ bản chạy trên Terminal.

✨ Tính năng hiện có
Hệ thống phản hồi: Sử dụng Gemini 2.5 Flash API (tối ưu tốc độ cho máy cấu hình thấp).

Hệ thống lệnh (Command System):

/status: Kiểm tra tình trạng kết nối và model.

/reset: Xóa sạch bộ nhớ tạm của AI.

/help: Xem danh sách lệnh.

Quản lý ký ức: Lưu lịch sử chat vào file memory.json.

Bảo mật: Quản lý API Key thông qua biến môi trường (.env).

🛠 Hướng dẫn cài đặt
Dự án được tối ưu để chạy nhẹ nhàng trên mọi cấu hình máy tính.

1. Cài đặt thư viện
Mở Terminal tại thư mục dự án và chạy lệnh sau để cài đặt các "vũ khí" cần thiết:

Bash

pip install -U google-genai python-dotenv
google-genai: SDK mới nhất để giao tiếp với bộ não AI.

python-dotenv: Giúp chương trình đọc Key bí mật từ file ẩn.

2. Cấu hình bảo mật
Vì lý do bảo mật, file chứa API Key không được upload lên GitHub. Bạn cần:

Copy file .env.example và đổi tên thành .env.

Mở file .env và dán API Key của bạn vào:

Plaintext

GEMINI_API_KEY=Dán_Key_Của_Bạn_Ở_Đây
🚀 Cách khởi chạy
Sau khi cài đặt xong, bạn chỉ cần gõ:

Bash

python brain.py
🗺️ Lộ trình phát triển (4 Năm)
[x] Năm 1: Xây dựng Logic AI & Hệ thống lệnh cơ bản.

[ ] Năm 2: Tích hợp Giọng nói (TTS) & Hình ảnh Live2D đơn giản.

[ ] Năm 3: Xây dựng RAG (Bộ nhớ dài hạn) & Tích hợp Twitch Chat.

[ ] Năm 4: Đồ án tốt nghiệp: Hoàn thiện nhân vật & Stream thực tế.
