from core.obd_connection import OBDConnection
from core.pubsub_client import PubSubClient

def main():
    pubsub_client = PubSubClient()
    obd_connection = OBDConnection()

    while(True):
        # OBD2接続
        car_data = obd_connection.connect()

        if isinstance(car_data, dict):
            pubsub_client.publish(car_data)
        elif isinstance(car_data, KeyboardInterrupt):
            print("プログラム終了")
        elif car_data == "Not Connected":
            print("接続失敗")
        elif car_data == "ELM Connected":
            print("接続出来たが、車両と未接続")
        elif car_data == "OBD Connected":
            print("車両とは繋がっているが、イグニッションがOFF")

if __name__ == "__main__":
    main()