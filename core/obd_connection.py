import time
import obd
from obd import OBDStatus

class OBDConnection:

    def __init__(self):
        self.connection = obd.OBD()
        
    def connect(self, publish_callback=None):
        if self.connection.status() == OBDStatus.CAR_CONNECTED:

            # 計測開始
            start = time.perf_counter()
            while(True):
                try:
                    rpm = self.connection.query(obd.commands.RPM).value.magnitude
                    speed = self.connection.query(obd.commands.SPEED).value.magnitude
                    coolant_temp = self.connection.query(obd.commands.COOLANT_TEMP).value.magnitude
                    throttle_pos = self.connection.query(obd.commands.THROTTLE_POS).value.magnitude

                    print(f"エンジン回転数：{rpm}\n速度：{speed}\n水温：{coolant_temp}\nスロットル開度：{throttle_pos}")

                    data = {
                        "rpm": rpm,
                        "speed": speed,
                        "coolant_temp": coolant_temp,
                        "throttle_pos": throttle_pos,
                        "timestamp": time.time(),
                        "device_id": "1",
                        "trip_id": "1"
                    }
                    time.sleep(.2)
                    return data
                except KeyboardInterrupt as e:
                    # プログラム終了の対応
                    return e
                except AttributeError as e:
                    # 正常値が入らなかった時の対応
                    time.sleep(.2)
                    pass
                except Exception as e:
                    # その他のエラーの対応
                    time.sleep(.2)
                    pass
        elif self.connection.status() == obd.OBDStatus.NOT_CONNECTED:
            return self.connection.status()
        elif self.connection.status() == obd.OBDStatus.ELM_CONNECTED:
            return self.connection.status()
        elif self.connection.status() == obd.OBDStatus.OBD_CONNECTED:
            return self.connection.status()