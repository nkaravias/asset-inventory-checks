from .pubsub_publish_action import PubSubPublishAction
from .email_action import EmailAction
from .slack_message_action import SlackMessageAction


class ActionFactory:
    @staticmethod
    def create_action(action_type):
        if action_type == "PubSubPublish":
            return PubSubPublishAction("PubSubPublish")
        elif action_type == "Email":
            return EmailAction("Email")
        elif action_type == "SlackMessage":
            return SlackMessageAction("SlackMessage")
        else:
            raise ValueError("Unknown action type")
