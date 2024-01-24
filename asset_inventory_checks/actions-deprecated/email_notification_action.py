from .base_action import Action


class EmailNotificationAction(Action):
    def __init__(self, findings, email_template):
        self.findings = findings
        self.email_template = email_template

    def execute(self):
        # Logic to send email notification
        print("lala")