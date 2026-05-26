import asyncio
import socket
import time

import pynmea2


class GPSConnection:
    def __init__(self, host="192.168.11.5", port=11123):
        self.host = host
        self.port = port
        self.socket = None
        self.running = True
        self.latest_gps_data = None

    async def start_background_receiver(self):
        while self.running:
            try:
                await asyncio.to_thread(self.connect)
                await asyncio.to_thread(self.receive_loop)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                print(f"GPS受信エラー: {e}")
                self.close()
                await asyncio.sleep(.5)

    def connect(self):
        if self.socket:
            return

        while self.running:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(5)
                self.socket.connect((self.host, self.port))
                self.socket.settimeout(1)
                print("GPS接続成功")
                return
            except (ConnectionRefusedError, TimeoutError, OSError) as e:
                print(f"GPS接続失敗: {e}")
                self.close()
                time.sleep(.5)

    def receive_loop(self):
        buffer = ""

        while self.running and self.socket:
            try:
                data = self.socket.recv(4096)
                if not data:
                    raise ConnectionError("GPS接続が切断されました")

                buffer += data.decode("ascii", errors="ignore")
                lines = buffer.splitlines()

                if buffer and not buffer.endswith(("\n", "\r")):
                    buffer = lines.pop() if lines else buffer
                else:
                    buffer = ""

                for line in lines:
                    self.update_gps_data(line.strip())
            except socket.timeout:
                continue

    def update_gps_data(self, nmea_sentence):
        if not nmea_sentence:
            return

        try:
            message = pynmea2.parse(nmea_sentence)
        except pynmea2.ParseError:
            return

        if not hasattr(message, "latitude") or not hasattr(message, "longitude"):
            return
        if not message.latitude or not message.longitude:
            return

        self.latest_gps_data = {
            "latitude": message.latitude,
            "longitude": message.longitude,
        }

    def get_gps_data(self):
        return self.latest_gps_data

    def close(self):
        if not self.socket:
            return

        try:
            self.socket.close()
        finally:
            self.socket = None
