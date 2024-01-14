from .dataflow_machine_check import DataflowMachineCheck
from .service_account_key_check import ServiceAccountKeyCheck


class CheckFactory:
    @staticmethod
    def create_check(check_type):
        if check_type == "DataflowMachine":
            return DataflowMachineCheck("status",
                                        "DataflowMachine", "actionType")
        elif check_type == "ServiceAccountKey":
            return ServiceAccountKeyCheck("status",
                                          "ServiceAccountKey", "actionType")
        else:
            raise ValueError("Unknown check type")
