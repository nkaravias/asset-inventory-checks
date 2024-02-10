from asset_inventory_checks.checks.check_factory import CheckFactory
#from asset_inventory_checks.actions.action_factory import ActionFactory
from asset_inventory_checks.logger_config import setup_logger
import base64
import os
import json
from asset_inventory_checks.actions.slack_message_action import SlackMessageAction


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



def mock_slack_action():
    # Example usage of SlackMessageAction
    slack_token = os.environ.get("SLACK_TOKEN")
    print(f"slack_token:{slack_token}")
    message = "Hello from Bob the Bot!"
    slack_channel_name = "#everything-and-nothing"  # Replace with your target Slack channel name

    findings = {'organization': 'foo.com', 'appcodes': {'abc0': {'custodian': 'nik@foo.com', 'LOB': 'Technology', 'L3': 'bob@foo.com', 'L4': 'russell@foo.com', 'L5': 'eunice@foo.com', 'projects': {'997': {'label': '', 'data_classification': 'restricted', 'description': 'Security architecture testing', 'contacts': ['sophe@foo.com'], 'approved': True, 'assignment_group': 'balh@foo.com'}}}, 'unknown': {'custodian': 'unknown@foo.com', 'LOB': 'Nothing', 'L3': 'bob@foo.com', 'L4': 'russell@foo.com', 'L5': 'eunice@foo.com', 'projects': {'997': {'label': '', 'data_classification': 'restricted', 'description': 'Security architecture testing', 'contacts': ['sophe@foo.com'], 'approved': True, 'assignment_group': 'balh@foo.com'}}}}}

    # 'NORMAL' | 'WARNING'
    action_normal = SlackMessageAction(findings=findings, slack_channel_name=slack_channel_name, token=slack_token, message_type="WARNING", bot_name="Findings Bot")
    action_normal.execute()


if __name__ == "__main__":
    mock_slack_action()
    # mock_pubsub_handler()