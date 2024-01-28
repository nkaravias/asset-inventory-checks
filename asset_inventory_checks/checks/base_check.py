from datetime import datetime, timedelta
from typing import Dict, List, Any
from asset_inventory_checks.actions.email_notification_action import EmailNotificationAction
from asset_inventory_checks.runtime_config_fetcher import RuntimeConfigFetcher
from asset_inventory_checks.logger_config import setup_logger

import os
import re



class Check:
    def __init__(self, check_type: str, expiry_days: int, expiring_soon_threshold: int):
        self.type = check_type
        #
        self.logger = setup_logger()
        self.logger.info("Initializing Check class")
        self.expiry_days = expiry_days
        self.expiring_soon_threshold = expiring_soon_threshold
        self.actions = []
        self.config_project_id = "rbsee-sandbox-asdf001"
        config_fetcher = RuntimeConfigFetcher(self.config_project_id, "platform")
        self.config_data = config_fetcher.get_config_text_value("appcode-inventory")
        self.logger.info(f"Configuration Data: {self.config_data}")
        #print(self.config_data)
  

    def process(self):
        raise NotImplementedError("Must override process in subclass")

    def act(self):
        raise NotImplementedError("Must override act in subclass")
    
    def extract_app_code(self, name: str) -> str:
        raise NotImplementedError("Must override extract_app_code in subclass")

    def add_to_map(self, map: Dict[str, Dict[str, List[str]]], app: str, expiry_date: datetime, resource_name: str) -> None:
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
    
    def organize_resources_by_expiry_status(self, resources: List[Any]) -> tuple:
        expired_resources_map = {}
        expiring_soon_resources_map = {}
        current_date = datetime.utcnow().date()

        for resource in resources:
            app = self.extract_app_code(resource)
            create_time = resource.create_time.date()
            expiry_date = create_time + timedelta(days=self.expiry_days)
            days_since_creation = (current_date - create_time).days
            days_until_expiry = (expiry_date - current_date).days

            if days_since_creation > self.expiry_days:
                self.add_to_map(expired_resources_map, app, expiry_date, resource.name)
            elif days_until_expiry <= self.expiring_soon_threshold:
                self.add_to_map(expiring_soon_resources_map, app, expiry_date, resource.name)

        return (
            self.sort_map_by_expiry_date(expired_resources_map),
            self.sort_map_by_expiry_date(expiring_soon_resources_map)
        )


    def create_email_action(self, appcode, subject, template_name, vars):
        # Extract the custodian email
        custodian_email = self.config_data.get("appcodes", {}).get(appcode, {}).get("custodian", None)

        # Validate custodian email
        if custodian_email is None or not self.is_valid_email(custodian_email):
            raise ValueError(f"Invalid or missing custodian email for appcode '{appcode}'")

        # Get sender from environment variable or use default
        sender = os.environ.get('EMAIL_SENDER', 'default_sender@example.com')
        if not self.is_valid_email(sender):
            sender = 'default_sender@example.com'

        action = EmailNotificationAction(subject, template_name, vars, sender, [custodian_email])
        self.actions.append(action)

    @staticmethod
    def is_valid_email(email):
        """ Check if the email is valid """
        pattern = r"^\S+@\S+\.\S+$"
        return re.match(pattern, email) is not None
