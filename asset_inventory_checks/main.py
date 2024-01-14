from asset_inventory_checks.checks.check_factory import CheckFactory
from asset_inventory_checks.actions.action_factory import ActionFactory


def pubsub_handler(event, context):
    """
    Cloud Function to be triggered by Pub/Sub.
    :param event: Pub/Sub message
    :param context: Metadata for the event.
    """
    message_data = event['data']
    check_type = determine_check_type(message_data)  # Implement this function
    check = CheckFactory.create_check(check_type)
    check.process()
    check.process()
    action = ActionFactory.create_action(check)
    action.execute()


def determine_check_type(message_data):
    # Logic to determine the type of check
    pass
