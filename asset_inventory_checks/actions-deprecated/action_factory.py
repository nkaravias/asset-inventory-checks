from .pubsub_publish_action import PubSubPublishAction
from .email_action import EmailAction
from .slack_message_action import SlackMessageAction


class ActionFactory:
    @staticmethod
    def create_action(check):
        # Determine the action type based on the properties of the check
        action_type = check.actionType

        if action_type == "PubSubPublish":
            return PubSubPublishAction(check)
        elif action_type == "Email":
            return EmailAction(check)
        elif action_type == "SlackMessage":
            return SlackMessageAction(check)
        else:
            raise ValueError("Unknown action type")

