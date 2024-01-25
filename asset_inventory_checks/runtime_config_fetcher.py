from google.cloud import runtimeconfig
import json

class RuntimeConfigFetcher:
    def __init__(self, project_id, config_name):
        self.project_id = project_id
        self.config_name = config_name
        self.client = runtimeconfig.Client(project=project_id)

    def get_config_text_value(self, variable_name):
        config = self.client.config(self.config_name)
        #variable = config.variable(variable_name)
        variable = config.get_variable(variable_name)
        variable.reload()
        if variable.exists():
            #value = variable.value.decode('UTF-8')
            value = variable.text
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            print(f"Error decoding JSON for Runtime Config variable: {variable_name}")
            return {}
