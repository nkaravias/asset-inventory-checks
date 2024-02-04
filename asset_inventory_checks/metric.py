from google.cloud import monitoring_v3
from datetime import datetime
import os


class Metric:
    def __init__(self, project_id):
        self.project_id = project_id
        self.client = monitoring_v3.MetricServiceClient()
        # Determine if running on Cloud Run and adjust namespace and labels accordingly
        if os.getenv("K_SERVICE"):
            self.namespace = "asset_inventory_check_service"
            self.revision = os.getenv("K_REVISION", "unknown_revision")
        else:
            # raise(ValueError("LOCAL"))
            self.namespace = "asset_inventory_check_service_local"
            self.revision = "local"

    def create(self, metric_type, value, labels=None):
        labels = labels or {}
        namespaced_metric_type = f"custom.googleapis.com/{self.namespace}/{metric_type}"
        series = monitoring_v3.TimeSeries()
        series.metric.type = namespaced_metric_type
        series.resource.type = 'global'
        series.metric.labels['revision'] = self.revision  # Include revision metadata
        series.metric.labels.update(labels)

        now = datetime.now()
        point = monitoring_v3.Point({
            "interval": {
                "end_time": {"seconds": int(now.timestamp()), "nanos": now.microsecond * 1000}
            },
            "value": {"double_value": value}
        })
        series.points.append(point)

        try:
            self.client.create_time_series(name=f"projects/{self.project_id}", time_series=[series])
            print(f"Metric '{namespaced_metric_type}' created with value {value} and labels {labels}.")
        except Exception as e:
            print(f"Failed to create metric '{namespaced_metric_type}': {e}")
