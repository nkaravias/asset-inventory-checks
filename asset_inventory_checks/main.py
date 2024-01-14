from checks.check_factory import CheckFactory
from actions.action_factory import ActionFactory


def pubsub_handler(event, context):
    """
    Cloud Function to be triggered by Pub/Sub.
    :param event: Pub/Sub message
    :param context: Metadata for the event.
    """
    # Extract attributes from the message
    attributes = event.get('attributes', {})

    # Use CheckFactory to determine the check type and create the
    # appropriate Check object
    check = CheckFactory.create_check(attributes)
    check.process()
    action = ActionFactory.create_action(check.actionType)
    action.execute()
