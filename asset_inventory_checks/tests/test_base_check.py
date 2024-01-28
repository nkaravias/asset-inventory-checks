import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from asset_inventory_checks.checks.base_check import Check

"""
* The mock_runtime_config_fetcher fixture mocks the RuntimeConfigFetcher to return a predetermined configuration. This is important since the Check class constructor uses this fetcher.
* The check_instance fixture provides an instance of Check for testing.
* test_init checks the initialization of the Check instance.
* test_is_valid_email tests the static method for email validation.
* test_create_email_action ensures that the create_email_action method correctly initializes an EmailNotificationAction.
* test_add_to_map and test_sort_map_by_expiry_date test specific utility methods in Check.
"""

class TestCheck:
    @pytest.fixture
    def mock_runtime_config_fetcher(self, mocker):
        mocker.patch('asset_inventory_checks.runtime_config_fetcher.RuntimeConfigFetcher.get_config_text_value', return_value={"appcodes": {"test": {"custodian": "test@example.com"}}})

    @pytest.fixture
    def check_instance(self, mock_runtime_config_fetcher):
        return Check('TestCheck', 5, 2)

    def test_init(self, check_instance):
        assert check_instance.type == 'TestCheck'
        assert check_instance.expiry_days == 5
        assert check_instance.expiring_soon_threshold == 2
        assert check_instance.config_data == {"appcodes": {"test": {"custodian": "test@example.com"}}}

    def test_is_valid_email(self):
        assert Check.is_valid_email('test@example.com')
        assert not Check.is_valid_email('invalid-email')
    
    @patch('asset_inventory_checks.checks.base_check.EmailNotificationAction')
    def test_create_email_action(self, mock_email_action, check_instance):
        check_instance.create_email_action('test', 'Subject', 'template', {'var': 'value'})
        mock_email_action.assert_called_with('Subject', 'template', {'var': 'value'}, 'default_sender@example.com', ['test@example.com'])
    
    def test_add_to_map(self, check_instance):
        test_map = {}
        check_instance.add_to_map(test_map, 'app', '2023-01-01', 'resource_name')
        assert test_map == {'app': {'2023-01-01': ['resource_name']}}

    def test_sort_map_by_expiry_date(self, check_instance):
        test_map = {'app': {'2023-01-01': ['resource1'], '2023-01-02': ['resource2']}}
        sorted_map = check_instance.sort_map_by_expiry_date(test_map)
        assert sorted_map == {'app': [{'expiry_date': '2023-01-01', 'assets': ['resource1']}, {'expiry_date': '2023-01-02', 'assets': ['resource2']}]}

"""
* The check_instance fixture creates an instance of the Check class.
* create_mock_resource is a helper function that creates a mock resource with a specified create_time.
* In the test_organize_resources_by_expiry_status method, we create mock resources representing different scenarios (expired, expiring soon, and not expiring).
* We then call the organize_resources_by_expiry_status() method with these resources and verify the output maps.
* The assertions check if the resources are categorized correctly based on their creation time.
"""


class TestCheckOrganizeResources:
    class DummyCheck(Check):
        def extract_app_code(self, name):
            return 'app'

    @pytest.fixture
    def check_instance(self):
        return self.DummyCheck('TestCheck', 5, 2)

    def create_mock_resource(self, days_ago):
        mock_resource = MagicMock()
        mock_resource.create_time.date.return_value = datetime.utcnow().date() - timedelta(days=days_ago)
        return mock_resource

    def test_organize_resources_by_expiry_status(self, check_instance, mocker):
        # Mock the extract_app_code method
        mocker.patch.object(Check, 'extract_app_code', return_value='app')

        # Create mock resources
        resource_expired = self.create_mock_resource(10)  # Created 10 days ago
        resource_expiring_soon = self.create_mock_resource(3)  # Created 3 days ago
        resource_not_expiring = self.create_mock_resource(1)  # Created 1 day ago

        resources = [resource_expired, resource_expiring_soon, resource_not_expiring]

        # Call the method
        expired_resources_map, expiring_soon_resources_map = check_instance.organize_resources_by_expiry_status(resources)

        # Assertions for expired resources
        assert 'app' in expired_resources_map
        assert len(expired_resources_map['app']) == 1  # 1 date with expired resources
        assert resource_expired.name in [res for date_info in expired_resources_map['app'] for res in date_info['assets']]

        # Assertions for expiring soon resources
        assert 'app' in expiring_soon_resources_map
        assert len(expiring_soon_resources_map['app']) == 1  # 1 date with expiring soon resources
        assert resource_expiring_soon.name in [res for date_info in expiring_soon_resources_map['app'] for res in date_info['assets']]