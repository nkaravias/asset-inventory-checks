from asset_inventory_checks.asset_inventory_query import AssetInventoryQuery
from .base_check import Check
from datetime import datetime, timedelta
from typing import Any

import re

class DataflowMachineCheck(Check):
    def __init__(self, check_type, expiry_days=30, expiring_soon_threshold=5):
        super().__init__(check_type, expiry_days, expiring_soon_threshold)
        # TODO where do we put this? Probably scheduler
        self.organization_id = "1012116149117"
        self.asset_types = ['dataflow.googleapis.com/Job']
        self.query = "state = \"JOB_STATE_RUNNING\" AND createTime < \"{}\"".format(
            (datetime.utcnow() - timedelta(days=expiry_days)).strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.read_mask = ""
        self.scope = f"organizations/{self.organization_id}"

    def process(self):
        # Get all active dataflow jobs that were created 30 days ago
        results = AssetInventoryQuery(self.scope, self.query, self.asset_types, self.read_mask).perform_query()

        if results:
            for result in results:
                print(result.name, result.create_time)
            self.expired_findings, self.expiring_soon_findings = self.organize_resources_by_expiry_status(results)

    def extract_app_code(self, resource: Any) -> str:
        if 'app_code' in resource.labels:
            return resource.labels['app_code']
        else:
            return 'unknown'