from .base_action import Action
import json

class EmailNotificationAction(Action):
    #def __init__(self, findings, email_template):
    def __init__(self, recipients, sender, subject, email_template, vars):

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


    def execute(self):
        # Logic to send email notification based on findings and template
        print("EMAIL NOTIFIER IS EXECUTING")
        # Use the email_payload property
        email_payload = self.email_payload
        print(f"This is the payload for {self.subject}: {self.email_payload}")

#        # Encode payload in base64
#        encoded_payload = base64.b64encode(json.dumps(email_payload).encode("utf-8")).decode("utf-8")
#
#        # Publish to Pub/Sub topic
#        publisher = pubsub_v1.PublisherClient()
#        topic_name = 'projects/{project_id}/topics/{topic}'.format(
#            project_id='your-project-id',  # Replace with your project ID
#            topic='your-topic-name',       # Replace with your topic name
#        )
#        publisher.publish(topic_name, encoded_payload.encode("utf-8"))
