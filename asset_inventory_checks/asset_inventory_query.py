from datetime import datetime, timedelta
from google.cloud import asset_v1
from google.api_core.exceptions import GoogleAPICallError, RetryError


class AssetInventoryQuery:
    """
        asset_types=['dataflow.googleapis.com/Job']
        query = (
            "state = \"JOB_STATE_RUNNING\" "
            f"AND createTime < \"{date_string}\""
        )
        read_mask="name" or "" for everything
    """
    def __init__(self, scope, query_string, asset_types, read_mask=""):
        # Initialize with necessary configuration, credentials, etc.
        self.configuration = {}
        self.query_string = query_string
        self.asset_types = asset_types
        self.read_mask = read_mask
        self.scope = scope

    def perform_query(self):
        """
        Logic to perform the query to Google Cloud Asset Inventory
        """
        client = asset_v1.AssetServiceClient(transport="rest")
        #scope = f"organizations/{self.organization_id}"
 
        request = asset_v1.SearchAllResourcesRequest(
            scope=self.scope,
            query=self.query_string,
            asset_types=self.asset_types,
            read_mask=self.read_mask
        )
        # In case reauth is required
        response = None
        try:
            response = client.search_all_resources(request=request)
        except GoogleAPICallError as e:
            print(f"Error calling the API: {e}")
        except RetryError as e:
            print(f"Retry errors encountered: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return response