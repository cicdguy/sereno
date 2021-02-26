"""
Metrics
"""

import json
from jsonschema import validate


class Metrics:
    """
    Metrics
    """
    def __init__(self, metrics_file):
        """
        Constructor
        """
        self.metrics_file = metrics_file
        self.schema = {
            "type": "object",
            "properties": {
                "server": {"type": "string"},
                "service": {"type": "string"},
                "component": {"type": "string"},
                "value": {"type": "number"},
                "timestamp": {"type": "number"},
                "active": {"type": "boolean"},
            },
            "required": [
                "server",
                "service",
                "component",
                "value",
                "timestamp",
                "active",
            ],
        }
        self.read()
        self.validate()

    def read(self):
        """
        Read metrics into list of dictionaries
        """
        with open(self.metrics_file, "r") as fil:
            self.metrics = json.load(fil)

    def validate(self):
        """
        Validate the structure of the metrics data
        """
        for metric in self.metrics:
            validate(metric, schema=self.schema)
