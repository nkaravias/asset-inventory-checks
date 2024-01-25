from asset_inventory_checks.asset_inventory_query import AssetInventoryQuery
from asset_inventory_checks.actions.email_notification_action import EmailNotificationAction
from .base_check import Check
from datetime import datetime, timedelta


class DataflowMachineCheck(Check):
    def __init__(self, check_type, expiry_days=30, expiring_soon_threshold=10):
        super().__init__(check_type, expiry_days, expiring_soon_threshold)
        # TODO where do we put this? Probably scheduler
        self.organization_id = "1012116149117"
        self.asset_types = ["dataflow.googleapis.com/Job"]
        self.query = 'state = "JOB_STATE_RUNNING" AND createTime < "{}"'.format(
            (datetime.utcnow() - timedelta(days=expiry_days)).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        )
        self.read_mask = ""
        self.scope = f"organizations/{self.organization_id}"
        self.expiry_days = expiry_days
        self.expiring_soon_threshold = expiring_soon_threshold
        self.expired_findings = {}
        self.expiring_soon_findings = {}
        self.actions = []

    def process(self):
        # Get all active dataflow jobs that were created 30 days ago
        results = AssetInventoryQuery(
            self.scope, self.query, self.asset_types, self.read_mask
        ).perform_query()

        if results:
            expired_findings, expiring_soon_findings = self.organize_resources_by_expiry_status(results)

            # Create actions for expired findings
            for app_code, findings in expired_findings.items():
                vars_expired = {"findings": findings}
                self.create_email_action(
                    app_code,
                    f"Expired Dataflow Jobs Alert for {app_code}",
                    "expired_dataflow_template",
                    vars_expired
                )

            # Create actions for expiring soon findings
            for app_code, findings in expiring_soon_findings.items():
                vars_expiring_soon = {"findings": findings}
                self.create_email_action(
                    app_code,
                    f"Dataflow Jobs expiring soon Alert for {app_code}",
                    "expiring_soon_dataflow_template",
                    vars_expiring_soon
                )
        # Execute all actions
        for action in self.actions:
            action.execute()

    # def extract_app_code(self, resource: Any) -> str:
    def extract_app_code(self, resource):
        if "app_code" in resource.labels:
            return resource.labels["app_code"]
        else:
            return "unknown"