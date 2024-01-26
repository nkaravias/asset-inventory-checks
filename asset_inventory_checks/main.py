from asset_inventory_checks.checks.check_factory import CheckFactory
#from asset_inventory_checks.actions.action_factory import ActionFactory
from asset_inventory_checks.logger_config import setup_logger
import base64

logger = setup_logger()


#def pubsub_handler(event, context):
def pubsub_handler(cloud_event):
    print(f"Received event with ID: {cloud_event['id']} and data {cloud_event.data}")
    """
    Cloud Function to be triggered by Pub/Sub.
    :param event: Pub/Sub message
    :param context: Metadata for the event.
    """
    # Extract the Pub/Sub data and attributes from the CloudEvent
    pubsub_message = cloud_event.data.get("message", {})

    # Get the actual message data (base64-decoded)
    message_data = base64.b64decode(pubsub_message.get("data", "")).decode("utf-8")

    # Get the attributes
    attributes = pubsub_message.get("attributes", {})

    # Your logic here using message_data and attributes
    print(f"Received message with data: {message_data} and attributes: {attributes}")


    # Extract attributes from the message
    #attributes = event.get('attributes', {})

    # Use CheckFactory to determine the check type and create the
    # appropriate Check object
    check = CheckFactory.create_check(attributes)
    check.process()


def mock_pubsub_handler():
    # Extract attributes from the message
    # attributes = {"check_type": "DataflowMachine"}
    attributes = {"check_type": "ServiceAccountKey"}

    # Use CheckFactory to determine the check type and create the
    # appropriate Check object
    check = CheckFactory.create_check(attributes)
    check.process()
    #print(check.findings)
    #print(f"expired_findings: {check.expired_findings}")
    #print(f"soon expiring: {check.expiring_soon_findings}")




if __name__ == "__main__":
    mock_pubsub_handler()