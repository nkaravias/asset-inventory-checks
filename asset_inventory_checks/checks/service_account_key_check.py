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
        thirty_days_ago = datetime.now() - timedelta(days=1)
        date_string = thirty_days_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.asset_types=['iam.googleapis.com/ServiceAccountKey']
        self.query = (
            f"createTime < \"{date_string}\""
            #f"state = \"ACTIVE\" AND createTime < \"{date_string}\""
        )
        self.read_mask=""
        self.scope=f"organizations/{self.organization_id}"
        self.findings = {}

    def process(self):
        # Get all service account keys that were created 30 days ago
        results = AssetInventoryQuery(self.scope, self.query, self.asset_types, self.read_mask).perform_query()

        app_resources_map = self.organize_findings_by_app(results)
        self.findings = app_resources_map

    def organize_findings_by_app(self, resources):
        app_resources_map = {}
        for resource in resources:
            resource_name = resource.name  # Access the 'name' attribute of the ResourceSearchResult object
            print(resource.display_name)
            #print(resource)
            app = self.extract_app_from_name(resource_name)
            #print(f"{resource_name} has appcode:{app}")
            if app not in app_resources_map:
                app_resources_map[app] = []
            app_resources_map[app].append(resource_name)
        return app_resources_map
    # //TODO For keys we need to extract the appcode from somewhere else
    # because the name has the project number, not the project ID (which would include the app)
    def extract_app_from_name(self, name):
        match = re.search(r'projects/(p|n)(.{4})-', name)
        if match:
            # return the extracted appcode
            return match.group(2)
        else:
            # appcode couldn't be matched in the resource
            return 'unknown'