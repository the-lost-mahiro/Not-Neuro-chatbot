import requests

def main():
    """Gửi tin nhắn thử khi server web đang chạy; không chạy khi import."""
    url = "http://127.0.0.1:5000/chat"
    data = {"message": "Chào Not-Neuro, em khỏe không?"}

    # Gửi yêu cầu POST kèm dữ liệu JSON
    response = requests.post(url, json=data, timeout=120)

    if response.status_code == 200:
        result = response.json()
        print(f"Trạng thái: {result['status']}")
    else:
        print(f"Lỗi: {response.status_code}")


if __name__ == "__main__":
    main()
