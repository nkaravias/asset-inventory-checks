from asset_inventory_checks.asset_inventory_query import AssetInventoryQuery
from .base_check import Check
from datetime import datetime, timedelta
import re


class ServiceAccountKeyCheck(Check):
    def __init__(self, check_type, action_type, expiry_days=5, expiring_soon_threshold=4):
        super().__init__(check_type, action_type)
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
        results = AssetInventoryQuery(self.scope, self.query,
                                      self.asset_types, self.read_mask).perform_query()

        if results:
            for result in results:
                print(result.name, result.create_time)
            self.expired_findings, self.expiring_soon_findings = self.organize_keys_by_expiry_status(results)

    def organize_keys_by_expiry_status(self, resources):
        expired_keys_map = {}
        expiring_soon_keys_map = {}
        current_date = datetime.utcnow().date()

        for resource in resources:
            app = self.extract_app_code(resource.name)
            create_time = resource.create_time.date()
            expiry_date = create_time + timedelta(days=self.expiry_days)
            days_since_creation = (current_date - create_time).days
            days_until_expiry = (expiry_date - current_date).days

            if days_since_creation > self.expiry_days:  # Key is expired
                self.add_to_map(expired_keys_map, app, expiry_date, resource.name)
            elif days_until_expiry <= self.expiring_soon_threshold:  # Key will expire soon
                self.add_to_map(expiring_soon_keys_map, app, expiry_date, resource.name)

        return (
            self.sort_map_by_expiry_date(expired_keys_map),
            self.sort_map_by_expiry_date(expiring_soon_keys_map)
        )

    def add_to_map(self, map, app, expiry_date, resource_name):
        if app not in map:
            map[app] = {}
        if expiry_date not in map[app]:
            map[app][expiry_date] = []
        map[app][expiry_date].append(resource_name)

    def sort_map_by_expiry_date(self, map):
        return {
            app: sorted(
                [{"expiry_date": str(expiry_date), "assets": assets}
                 for expiry_date, assets in dates.items()],
                key=lambda x: x["expiry_date"]
            )
            for app, dates in map.items()
        }

    def extract_app_code(self, name):
        match = re.search(r'projects/(p|n)(.{4})-', name)
        return match.group(2) if match else 'unknown'
