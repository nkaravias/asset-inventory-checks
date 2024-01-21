from asset_inventory_checks.asset_inventory_query import AssetInventoryQuery
from .base_check import Check
from datetime import datetime
import re


class ServiceAccountKeyCheck(Check):
    def __init__(self, check_type: str, action_type: str, expiry_days: int = 5, expiring_soon_threshold: int = 4):
        super().__init__(check_type, action_type, expiry_days, expiring_soon_threshold)

        self.organization_id = "1012116149117"
        self.asset_types = ['iam.googleapis.com/ServiceAccountKey']
        self.query = "createTime < \"{}\"".format(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.read_mask = ""
        self.scope = f"organizations/{self.organization_id}"
        self.expiry_days = expiry_days
        self.expiring_soon_threshold = expiring_soon_threshold
        self.expired_findings = {}
        self.expiring_soon_findings = {}

    def process(self):
        results = AssetInventoryQuery(self.scope, self.query, self.asset_types, self.read_mask).perform_query()

        if results:
            for result in results:
                print(result.name, result.create_time)
            self.expired_findings, self.expiring_soon_findings = self.organize_resources_by_expiry_status(results)

    def extract_app_code(self, name: str) -> str:
        match = re.search(r'projects/(p|n)(.{4})-', name)
        return match.group(2) if match else 'unknown'
