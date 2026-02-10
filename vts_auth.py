import asyncio
import pyvts

# Thông tin định danh của bot bạn
plugin_info = {
    "plugin_name": "Not-Neuro-Brain",
    "developer": "Mahirou",
    "authentication_token_path": "vts_token.txt" # Nơi lưu chìa khóa
}

async def authenticate():
    vts = pyvts.vts(plugin_info=plugin_info)
    await vts.connect()
    
    # Gửi yêu cầu cấp quyền (Lúc này VTS sẽ hiện thông báo xác nhận)
    await vts.request_authenticate_token()

    # Code sẽ dừng lại ở đây để đợi thao tác
    input(">>> HÃY NHẤN 'ALLOW' TRÊN VTUBE STUDIO, SAU ĐÓ BẤM ENTER TẠI ĐÂY ĐỂ TIẾP TỤC...")
    
    # Nhấn "Allow" trong VTS rồi xác thực
    await vts.request_authenticate()
    
    print("✅ Kết nối thành công! Chìa khóa đã được lưu vào vts_token.txt")
    await vts.close()

if __name__ == "__main__":
    asyncio.run(authenticate())