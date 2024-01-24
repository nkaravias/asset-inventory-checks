from .base_action import Action
from google.cloud import pubsub_v1
import base64
import json


class EmailNotificationAction(Action):
    def __init__(self, subject, email_template, vars, sender, recipients):

        self.recipients = recipients
        self.sender = sender
        self.subject = subject
        self.email_template = email_template
        self.vars = vars

        # Print the creation event and parameters
        print(f"Creating EmailNotificationAction with parameters: \
               \nRecipients: {recipients} \
               \nSender: {sender} \
               \nSubject: {subject} \
               \nTemplateName: {email_template} \
               \nVars: {vars}")

    @property
    def email_payload(self):
        return {
            "emailPayload": {
                "destination": {
                    "to": self.recipients
                },
                "from": self.sender,
                "subject": self.subject,
                "templateName": self.email_template,
                "vars": self.vars
            }
        }

    def publish_to_pubsub(self, payload, attributes=None):
        encoded_payload = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
        publisher = pubsub_v1.PublisherClient(transport="rest")
        topic_name = 'projects/{project_id}/topics/{topic}'.format(
            project_id='nnnnnnnn',
            topic='ddddd',
        )

        try:
            publish_future = publisher.publish(topic_name, data=encoded_payload.encode("utf-8"), **(attributes or {}))
            return publish_future.result()
        except Exception as e:
            print(f"An error occurred while publishing to Pub/Sub: {e}")
            return None

    def execute(self):
        # Logic to send email notification based on findings and template
        print("The EmailNotificationAction is executing")
        #message_id = self.publish_to_pubsub(self.email_payload, {})
        #if message_id:
        #    print(f"Message published with ID: {message_id}")