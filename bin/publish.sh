curl -d '{
    "specversion" : "1.0",
    "type" : "com.google.cloud.pubsub.topic.publish",
    "source" : "//pubsub.googleapis.com/projects/myproject/topics/mytopic",
    "id" : "1234-1234-1234",
    "time" : "2020-09-05T03:56:24Z",
    "datacontenttype" : "application/json",
    "data" : {
        "message": {
            "data": "bGFsYWxhbGEK",
            "attributes": {"check_type": "ServiceAccountKey"},
            "messageId": "1234567890",
            "publishTime": "2020-08-14T20:50:04.994Z"
        }
    }
}' -H "Content-Type: application/json" -X POST http://localhost:8090
