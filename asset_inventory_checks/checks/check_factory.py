from .dataflow_machine_check import DataflowMachineCheck
from .service_account_key_check import ServiceAccountKeyCheck


class CheckFactory:
    @staticmethod
    def create_check(attributes):
        """
        Create a Check object based on the attributes provided.

        :param attributes: A dictionary of attributes from the Pub/Sub message.
        :return: A Check object.
        """
        check_type = attributes.get('check_type')
        print("I am inside the check factory")
        if check_type == "DataflowMachine":
            return DataflowMachineCheck(
                                        "DataflowMachine", "actionType")
        elif check_type == "ServiceAccountKey":
            return ServiceAccountKeyCheck(
                                          "ServiceAccountKey", "actionType")
        else:
            raise ValueError(f"Unknown check type: {check_type}")
