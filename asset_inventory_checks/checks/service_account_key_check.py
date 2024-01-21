from asset_inventory_checks.asset_inventory_query import AssetInventoryQuery
from .base_check import Check
from datetime import datetime, timedelta
import re


class ServiceAccountKeyCheck(Check):
    def __init__(self, check_type, action_type
                ):
        super().__init__(check_type, action_type)
        # Construct the query
        # TODO where do we put this? Probably scheduler
        self.organization_id = "1012116149117"
        # Calculate the date 30 days ago
        thirty_days_ago = datetime.now() - timedelta(days=0)
        date_string = thirty_days_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.asset_types = ['iam.googleapis.com/ServiceAccountKey']
        self.query = (
            f"createTime < \"{date_string}\""
            # f"state = \"ACTIVE\" AND createTime < \"{date_string}\""
        )
        self.read_mask = ""
        self.scope = f"organizations/{self.organization_id}"
        self.findings = {}

    def process(self):
        # Get all service account keys that were created 30 days ago
        results = AssetInventoryQuery(self.scope, self.query,
                                      self.asset_types, self.read_mask).perform_query()

        app_resources_map = self.organize_findings_by_app(results)
        expired_keys_map = self.organize_expired_keys_by_app_and_date(results)
        #self.findings = app_resources_map
        print(expired_keys_map)
        self.findings = app_resources_map

    def organize_findings_by_app(self, resources):
        app_resources_map = {}
        for resource in resources:
            resource_name = resource.name
            print(resource.display_name)
            # print(resource)
            app = self.extract_app_from_name(resource_name)
            # print(f"{resource_name} has appcode:{app}")
            if app not in app_resources_map:
                app_resources_map[app] = []
            app_resources_map[app].append(resource_name)
        return app_resources_map
    # //TODO For keys we need to extract the appcode from somewhere else
    # because the name has the project number, not the project ID
    # (which would include the app)

    def extract_app_from_name(self, name):
        match = re.search(r'projects/(p|n)(.{4})-', name)
        if match:
            # return the extracted appcode
            return match.group(2)
        else:
            # appcode couldn't be matched in the resource
            return 'unknown'

    def organize_expired_keys_by_app_and_date(self, resources):
        expired_keys_map = {}
        current_date = datetime.now().date()

        for resource in resources:
            app = self.extract_app_from_name(resource.name)
            create_time = resource.create_time
            expiry_date = (create_time + timedelta(days=2)).date()
            days_overdue = (current_date - expiry_date).days

            # Check if key is expired and by how many days
            if days_overdue > 0:
                if app not in expired_keys_map:
                    expired_keys_map[app] = {}
                if expiry_date not in expired_keys_map[app]:
                    expired_keys_map[app][expiry_date] = {"assets": [], "days_overdue": days_overdue}

                expired_keys_map[app][expiry_date]["assets"].append(resource.name)

        # Sort and transform the map for the desired output format
        return {
            app: sorted(
                [{"expiry_date": str(expiry_date), "assets": info["assets"], "days_overdue": info["days_overdue"]}
                 for expiry_date, info in dates.items()],
                key=lambda x: x["expiry_date"]
            )
            for app, dates in expired_keys_map.items()
        }