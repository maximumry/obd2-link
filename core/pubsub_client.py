from google.cloud import pubsub_v1
import os
import json

class PubSubClient:
    def __init__(self):
        try:
            # 環境変数の設定
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./secretes/my-obd2link-stg-7e1ffe5dd1a2.json"

            # GCPのプロジェクトIDと、トピック名を指定
            PROJECT_ID = "my-obd2link-stg"
            TOPIC_ID = "obd2-telemetry-topic"

            # クライアントの初期化
            self.publisher = pubsub_v1.PublisherClient()
            # トピックのフルパスを作成
            self.topic_path = self.publisher.topic_path(PROJECT_ID, TOPIC_ID)
        except Exception as e:
            print(e)
            pass
    def publish(self, car_data: dict):
        try:
            # JSON形式に変換
            json_data = json.dumps(car_data)
            # メッセージはbytes型で送る
            data_bytes = json_data.encode("utf-8")

            # メッセージの送信
            future = self.publisher.publish(self.topic_path, data_bytes, origin="python-obd2-link")

            print(f"Published message ID: {future.result()}")
        except Exception as e:
            print(e)
            pass