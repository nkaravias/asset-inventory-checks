import pytest
from asset_inventory_checks.main import pubsub_handler

def test_pubsub_handler(mocker):
    # Create a mock cloud event object
    mock_cloud_event = mocker.MagicMock()
    mock_cloud_event.specversion = "1.0"
    mock_cloud_event.type = "com.google.cloud.pubsub.topic.publish"
    mock_cloud_event.source = "//pubsub.googleapis.com/projects/YOUR_PROJECT_ID/topics/YOUR_TOPIC_ID"
    mock_cloud_event.id = "1234-1234-1234"
    mock_cloud_event.time = "2020-09-05T03:56:24Z"
    mock_cloud_event.datacontenttype = "application/json"
    mock_cloud_event.data = {
        "message": {
            "data": "bGFsYWxhbGEK",  # base64-encoded data
            "attributes": {
                "key1": "value1",
                "key2": "value2"
            },
            "messageId": "1234567890",
            "publishTime": "2020-08-14T20:50:04.994Z"
        }
    }

    # Mock CheckFactory to control its behavior
    mock_create_check = mocker.patch('asset_inventory_checks.checks.check_factory.CheckFactory.create_check')
    mock_check = mock_create_check.return_value
    mock_check.process.return_value = None

    # Call the pubsub_handler with the mock cloud event
    pubsub_handler(mock_cloud_event)

    # Assertions
    mock_create_check.assert_called_with({'key1': 'value1', 'key2': 'value2'})
    mock_check.process.assert_called()
