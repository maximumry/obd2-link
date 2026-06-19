from core.obd_connection import OBDConnection
from core.pubsub_client import PubSubClient
from core.gps_connection import GPSConnection
import asyncio
from obd import OBDStatus

async def main():
    pubsub_client = PubSubClient()
    obd_connection = OBDConnection()
    gps_connection = GPSConnection()
    await gps_connection.connect_async()

    try:
        while True:
            # OBD2接続
            car_data = await obd_connection.connect_async()
            
            if isinstance(car_data, dict):
                # GPS接続
                gps_data = await gps_connection.get_gps_data_async()
                if gps_data is None:
                    car_data["gps_data"] = None
                    continue
                car_data["gps_data"] = [gps_data.get("latitude"), gps_data.get("longitude")]

                await pubsub_client.publish_async(car_data)
            elif isinstance(car_data, KeyboardInterrupt):
                print("プログラム終了")
                break
            elif car_data == OBDStatus.NOT_CONNECTED:
                print("OBD2に接続出来ていない")
                await asyncio.sleep(.5)
            elif car_data == OBDStatus.ELM_CONNECTED:
                print("接続出来たが、車両と未接続")
                await asyncio.sleep(.5)
            elif car_data == OBDStatus.OBD_CONNECTED:
                print("車両とは繋がっているが、イグニッションがOFF")
                await asyncio.sleep(.5)
    finally:
        obd_connection.cancel()
        gps_connection.cancel()

if __name__ == "__main__":
    asyncio.run(main())
