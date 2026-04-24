from core.obd_connection import OBDConnection
import os
from google.cloud import bigquery

# 環境変数の設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/kawaguchiryo/IdeaProjects/obd2_link/secretes/my-obd2link-stg-7e1ffe5dd1a2.json"
client = bigquery.Client()

def main():
    obd_connection = OBDConnection()
    # OBD2接続
    obd_connection_status = obd_connection.connect()

    if obd_connection_status == True:
        print("接続成功")
    elif isinstance(obd_connection_status, KeyboardInterrupt):
        print("プログラム終了")
    elif obd_connection_status == "Not Connected":
        print("接続失敗")
    elif obd_connection_status == "ELM Connected":
        print("接続出来たが、車両と未接続")
    elif obd_connection_status == "OBD Connected":
        print("車両とは繋がっているが、イグニッションがOFF")

if __name__ == "__main__":
    main()