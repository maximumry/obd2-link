from core.obd_connection import OBDConnection
from core.pubsub_client import PubSubClient
from core.gps_connection import GPSConnection
import asyncio
from obd import OBDStatus

async def main():
    pubsub_client = PubSubClient()
    obd_connection = OBDConnection()
    gps_connection = GPSConnection()

    # GPSのバックグラウンド受信タスクを開始
    gps_task = asyncio.create_task(gps_connection.start_background_receiver())

    try:
        while True:
            # OBD2接続
            car_data = await obd_connection.connect_async()
            gps_data = gps_connection.get_gps_data()

            if isinstance(car_data, dict):
                if gps_data:
                    car_data.update(gps_data)
                    print(f"GPSデータ追加: {gps_data}")
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
        print("終了処理中...")
        gps_connection.running = False
        gps_connection.close()
        gps_task.cancel()
        try:
            await gps_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(main())
