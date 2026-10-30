import pyautogui
from paths import PROJECT_ROOT

class VtuberEye:
    def __init__(self, output_path: str = str(PROJECT_ROOT / "vision.jpg")):
        # Đường dẫn file ảnh đầu ra
        self.output_path = output_path

    def take_screenshot(self):
        """Chụp toàn bộ màn hình chính và lưu ảnh."""
        try:
            # Chụp màn hình bằng pyautogui
            screenshot = pyautogui.screenshot()
            
            # Lưu file ảnh (chuyển sang hệ màu RGB để tránh lỗi lưu JPEG)
            screenshot = screenshot.convert('RGB')
            screenshot.save(self.output_path, format="JPEG")
            
            print(f"✅ [EYE] Đã chụp ảnh màn hình: {self.output_path}")
            return True
            
        except Exception as e:
            print(f"❌ [EYE] Lỗi khi chụp màn hình: {e}")
            return False

# --- ĐOẠN NÀY ĐỂ TEST THỬ MẮT ---
if __name__ == "__main__":
    eye = VtuberEye()
    eye.take_screenshot()
