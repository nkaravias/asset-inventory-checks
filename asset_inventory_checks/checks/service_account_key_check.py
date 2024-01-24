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


    def process(self):
        results = AssetInventoryQuery(self.scope, self.query, self.asset_types, self.read_mask).perform_query()


        if results:
            expired_findings, expiring_soon_findings = self.organize_resources_by_expiry_status(results)

            # Create actions for expired findings
            for app_code, findings in expired_findings.items():
                vars_expired = {"findings": findings}
                self.create_email_action(
                    f"Expired Keys Alert for {app_code}",
                    "expired_template",
                    vars_expired,
                    "sender@example.com",
                    ["expired@example.com"]
                )

            # Create actions for expiring soon findings
            for app_code, findings in expiring_soon_findings.items():
                vars_expiring_soon = {"findings": findings}
                self.create_email_action(
                    f"Keys Expiring Soon Alert for {app_code}",
                    "expiring_soon_template",
                    vars_expiring_soon,
                    "sender@example.com",
                    ["recipient@example.com"]
                )

        # Execute all actions
        for action in self.actions:
            action.execute()

    def extract_app_code(self, resource: Any) -> str:
        match = re.search(r'projects/(p|n)(.{4})-', resource.name)
        return match.group(2) if match else 'unknown'
