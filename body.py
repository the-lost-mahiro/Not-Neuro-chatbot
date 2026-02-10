import os
import asyncio
import pyvts
import random

class VtuberBody:
    def __init__(self):
        self.token_path = os.path.abspath("vts_token.txt")
        self.plugin_info = {
            "plugin_name": "Not-Neuro-Brain",
            "developer": "Mahirou",
            "authentication_token_path": self.token_path
        }
        self.vts = None
        self.hotkey_cache = {}

    async def connect(self):
        """Khởi tạo kết nối persistent và Cache Hotkey"""
        if self.vts: return # Đã kết nối
        
        try:
            self.vts = pyvts.vts(plugin_info=self.plugin_info)

            await self.vts.connect()

            # Đọc token và Authenticate
            token = None
            if os.path.exists(self.token_path):
                with open(self.token_path, 'r') as f:
                    token = f.read().strip()
            
            if not token:
                print("❌ [BODY] Chưa có Token, vui lòng Authenticate trong plugin trước.")
                return

            await self.vts.request(self.vts.vts_request.authentication(token))

            # Cache danh sách Hotkey (Để trigger nhanh hơn)
            resp = await self.vts.request(self.vts.vts_request.requestHotKeyList())
            if 'data' in resp and 'availableHotkeys' in resp['data']:
                self.hotkey_cache = {h['name'].lower(): h['hotkeyID'] for h in resp['data']['availableHotkeys']}
                # print(f"✅ [BODY] Đã cache {len(self.hotkey_cache)} hotkeys.")
            
            return
            
        except Exception as e:
            print(f"❌ [BODY] Lỗi kết nối VTS: {e}")
            self.vts = None
            return

    async def trigger_hotkey(self, hotkey_name_input, duration=5):
        if not self.vts: await self.connect()
        if not self.vts: return 

        hotkey_id = self.hotkey_cache.get(hotkey_name_input.lower())

        if hotkey_id:
            try:
                await self.vts.request(self.vts.vts_request.requestTriggerHotKey(hotkey_id))
            except Exception as e:
                print(f"❌ [BODY] Lỗi gửi request Trigger: {e}")
        else:
            print(f"⚠️ [BODY] Không tìm thấy Hotkey: '{hotkey_name_input}'")

    async def lip_sync(self, voice_box_checker):
        if not self.vts: return

        try:
            parameter_name = "MouthOpen"
            while voice_box_checker():
                if not self.vts: break # Mất kết nối thì dừng
                
                open_value = random.uniform(0.0, 1.0)
                req = self.vts.vts_request.requestSetParameterValue(parameter_name, open_value)
                await self.vts.request(req)
                await asyncio.sleep(0.08)
            
            # Đóng miệng
            req_close = self.vts.vts_request.requestSetParameterValue(parameter_name, 0.0)
            await self.vts.request(req_close)

        except Exception as e:
            print(f"❌ Lỗi Lip Sync: {e}")

    async def close(self):
        if self.vts:
            await self.vts.close()
            self.vts = None