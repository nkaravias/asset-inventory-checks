from asset_inventory_checks.asset_inventory_query import AssetInventoryQuery
from .base_check import Check
from datetime import datetime, timedelta
import re

class DataflowMachineCheck(Check):
    def __init__(self, check_type, action_type
                ):
        super().__init__(check_type, action_type)
        # Construct the query
        # TODO where do we put this? Probably scheduler
        self.organization_id = "1012116149117"
        # Calculate the date 30 days ago
        thirty_days_ago = datetime.now() - timedelta(days=110)
        date_string = thirty_days_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.asset_types=['dataflow.googleapis.com/Job']
        self.query = (
            "state = \"JOB_STATE_RUNNING\" "
            f"AND createTime < \"{date_string}\""
        )
        self.read_mask=""
        self.scope=f"organizations/{self.organization_id}"

    def process(self):
        # Get all active dataflow jobs that were created 30 days ago
        results = AssetInventoryQuery(self.scope, self.query, self.asset_types, self.read_mask).perform_query()
        app_resources_map = self.organize_findings_by_app(results)
        # //TODO findings property should be added to the Check class
        self.findings = app_resources_map

    def organize_findings_by_app(self, resources):
        app_resources_map = {}
        for resource in resources:
            resource_name = resource.name  # Access the 'name' attribute of the ResourceSearchResult object
            #app = self.extract_app_from_name(resource_name)
            app= self.extract_app_code(resource)
            print(f"{resource_name} has appcode:{app} and is {resource}")
            if app not in app_resources_map:
                app_resources_map[app] = []
            app_resources_map[app].append(resource_name)
        return app_resources_map

    def extract_app_code(self, resource):
        if 'app_code' in resource.labels:
            return resource.labels['app_code']
        else:
            return 'unknown'