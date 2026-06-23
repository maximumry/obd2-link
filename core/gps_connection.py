import socket
import pynmea2
import asyncio
import time
import os
import re
from dotenv import load_dotenv
load_dotenv()

class GPSConnection:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    async def connect_async(self):
        return await asyncio.to_thread(self.connect)

    def connect(self):
        try:
            self.socket.connect((os.getenv("GPS_HOST"), int(os.getenv("GPS_PORT"))))
        except ConnectionRefusedError:
            self.socket.close()
            self.__init__()
            return False
        except OSError as e:
            self.socket.close()
            self.__init__()
            return False
    
    async def get_gps_data_async(self):
        return await asyncio.to_thread(self.get_gps_data)

    def get_gps_data(self):
        gps_data = self.socket.recv(1024).decode("utf-8", errors="ignore")
        data = gps_data.split("\r\n")

        for line in data:
            try:
                msg = pynmea2.parse(line)
                if msg.sentence_type == "GGA" and msg.gps_qual > 0:
                    return {
                        "latitude": msg.latitude,
                        "longitude": msg.longitude
                    }
            except:
                pass

        return None

    def cancel(self):
        if self.socket:
            self.socket.close()