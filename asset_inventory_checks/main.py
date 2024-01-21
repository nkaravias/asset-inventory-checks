from asset_inventory_checks.checks.check_factory import CheckFactory
from asset_inventory_checks.actions.action_factory import ActionFactory


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


def mock_pubsub_handler():
    # Extract attributes from the message
    attributes = {"check_type": "DataflowMachine"}
    #attributes = {"check_type": "ServiceAccountKey"}

    # Use CheckFactory to determine the check type and create the
    # appropriate Check object
    check = CheckFactory.create_check(attributes)
    check.process()
    print(check.findings)
    #print(f"expired_findings: {check.expired_findings}")
    #print(f"soon expiring: {check.expiring_soon_findings}")
    # action = ActionFactory.create_action(check.actionType)
    # action.execute()


if __name__ == "__main__":
    mock_pubsub_handler()