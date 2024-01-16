from asset_inventory_checks.asset_inventory_query import AssetInventoryQuery
from .base_check import Check


class DataflowMachineCheck(Check):
    def __init__(self, check_type, action_type):
        super().__init__(check_type, action_type)

    def process(self):
        query = AssetInventoryQuery()
        results = query.perform_query("0")
        # Process the results
        print("Processing DataflowMachineCheck with results:", results)
        # Further processing logic here
