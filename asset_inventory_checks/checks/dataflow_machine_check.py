from ..asset_inventory_query import AssetInventoryQuery
from .base_check import Check


class DataflowMachineCheck(Check):
    def __init__(self, status, check_type, action_type, configuration,
                 query_params):
        super().__init__(status, check_type, action_type)
        self.configuration = configuration
        self.query_params = query_params

    def process(self):
        query = AssetInventoryQuery(self.configuration)
        results = query.perform_query(self.query_params)
        # Process the results
        print("Processing DataflowMachineCheck with results:", results)
        # Further processing logic here
