from asset_inventory_checks.asset_inventory_query import AssetInventoryQuery
from asset_inventory_checks.actions.email_notification_action import EmailNotificationAction
from .base_check import Check
from datetime import datetime
from typing import Any

import re



class ServiceAccountKeyCheck(Check):
    def __init__(self, check_type: str, expiry_days: int = 5, expiring_soon_threshold: int = 4):
        super().__init__(check_type, expiry_days, expiring_soon_threshold)

        self.organization_id = "1012116149117"
        self.asset_types = ['iam.googleapis.com/ServiceAccountKey']
        self.query = "createTime < \"{}\"".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.read_mask = ""
        self.scope = f"organizations/{self.organization_id}"
        self.expiry_days = expiry_days
        self.expiring_soon_threshold = expiring_soon_threshold
        self.expired_findings = {}
        self.expiring_soon_findings = {}
        self.actions = []

    #def create_email_action(self, findings, subject, template_name, vars):
    def create_email_action(self, subject, template_name, vars):
        # Assuming 'vars' already contains the necessary findings and additional data
        recipients = ["recipient@example.com"]  # Define your recipients
        sender = "sender@example.com"           # Define the sender

        action = EmailNotificationAction(recipients, sender, subject, template_name, vars)
        self.actions.append(action)

    def process(self):
        results = AssetInventoryQuery(self.scope, self.query, self.asset_types, self.read_mask).perform_query()

        if results:
            for result in results:
                print(result.name, result.create_time)
            self.expired_findings, self.expiring_soon_findings = self.organize_resources_by_expiry_status(results)
            
        if self.expired_findings:
            vars_expired = {"expired_findings": self.expired_findings}
            #vars_expired.update({"additional_var": "additional value for expired"})
            self.create_email_action("Expired Keys Alert", "expired_template", vars_expired)

        
        if self.expiring_soon_findings:
            vars_expiring_soon = {"expiring_soon_findings": self.expiring_soon_findings}
            self.create_email_action("Keys Expiring Soon Alert", "expiring_soon_template", vars_expiring_soon)


        # Execute all actions
        for action in self.actions:
            action.execute()

    def extract_app_code(self, resource: Any) -> str:
        match = re.search(r'projects/(p|n)(.{4})-', resource.name)
        return match.group(2) if match else 'unknown'
