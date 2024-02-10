from .base_action import Action
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json

class SlackMessageAction(Action):
    def __init__(self, findings, slack_channel_name, token, message_type="NORMAL", bot_name="Bot"):
        super().__init__()
        self.findings = findings
        self.slack_channel_name = slack_channel_name
        self.token = token
        self.message_type = message_type
        self.bot_name = bot_name

    def execute(self):
        client = WebClient(token=self.token)
        color = "#FFFF00" if self.message_type == "NORMAL" else "#FF0000"  # Yellow for normal, red for warning
        icon_emoji = ":information_source:" if self.message_type == "NORMAL" else ":warning:"

        try:
            # Send parent message to start the thread
            parent_message_response = client.chat_postMessage(
                channel=self.slack_channel_name,
                text="These are the findings:",  # Fallback text for notifications
                username=self.bot_name,
                icon_emoji=icon_emoji
            )
            thread_ts = parent_message_response["ts"]  # Capture the timestamp to use as thread_ts for replies

            # Construct the blocks for the detailed findings
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{icon_emoji} Detailed Findings:*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"```{json.dumps(self.findings, indent=4)}```"  # Pretty print findings
                    }
                }
            ]

            # Post the detailed findings as a reply in the thread
            client.chat_postMessage(
                channel=self.slack_channel_name,
                text="Detailed findings are attached.",  # Fallback text for notifications
                blocks=blocks,
                thread_ts=thread_ts,  # Reply in the thread
                username=self.bot_name
            )

            self.logger.info(f"Message sent to {self.slack_channel_name} in a thread")
        except SlackApiError as e:
            self.logger.error(f"Error sending message to Slack: {e.response['error']}")
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while sending message to Slack: {e}")
