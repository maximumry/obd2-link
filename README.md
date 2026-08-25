# obd2-link
ラズベリーパイでOBD2から車両情報を取得するプロジェクト

## AWS IoT Core

AWS IoT Coreで作成したThingの証明書と秘密鍵をラズベリーパイに配置し、`.env`に以下を設定する。

```dotenv
AWS_IOT_ENDPOINT=xxxxxxxxxxxxx-ats.iot.ap-northeast-1.amazonaws.com
AWS_IOT_CLIENT_ID=obd2-link-1
AWS_IOT_TOPIC=obd2/telemetry
AWS_IOT_CERT_PATH=secretes/device.pem.crt
AWS_IOT_PRIVATE_KEY_PATH=secretes/private.pem.key
AWS_IOT_ROOT_CA_PATH=secretes/AmazonRootCA1.pem
```

IoT Policyでは、上記クライアントIDの `iot:Connect` とトピックの `iot:Publish` を許可する。各端末の `AWS_IOT_CLIENT_ID` は重複させないこと。
