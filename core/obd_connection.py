import time
import obd
from obd import OBDStatus

class OBDConnection:

    def __init__(self):
        self.connection = obd.OBD()
        
    def connect(self):
        if self.connection.status() == OBDStatus.CAR_CONNECTED:
            print(f"接続成功")

            # 計測開始
            start = time.perf_counter()
            while(True):
                try:
                    rpm = self.connection.query(obd.commands.RPM).value.magnitude
                    speed = self.connection.query(obd.commands.SPEED).value.magnitude
                    coolant_temp = self.connection.query(obd.commands.COOLANT_TEMP).value.magnitude
                    throttle_pos = self.connection.query(obd.commands.THROTTLE_POS).value.magnitude

                    print(f"エンジン回転数：{rpm}\n速度：{speed}\n水温：{coolant_temp}\nスロットル開度：{throttle_pos}")

                    time.sleep(.2)
                    # if 60 <= time.perf_counter() - start:
                    #     return True
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