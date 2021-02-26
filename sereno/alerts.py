"""
Alerts
"""

from rich.console import Console
from rule_engine import Rule, Context

from sereno.utils import (
    _get_unique_values_for_given_key,
    _get_items_for_given_values_list,
)


class Alerts:
    """
    Alerts
    """
    def __init__(self, metrics, rules):
        """
        Constructor
        """
        self.metrics = metrics
        self.rules = rules
        self.stream = Console()
        self.get_unique_services()
        self.get_servers_per_service()
        self.get_unique_timestamps()

    def print_alert(self, rule, metric, show_severity):
        """
        Print alert to console
        """
        m = metric  # For brevity # pylint: disable=C0103
        severity_level = ""
        if show_severity:
            severity_level = rule["severity"] + " "
        alert_format = f"{severity_level}ALERT timestamp: {m['timestamp']}, component: {m['component']}, value: {m['value']}, server: {m['server']}, service: {m['service']}"  # noqa: E501  # pylint: disable=C0301
        if rule["majority"]:
            alert_format = f"{severity_level}ALERT timestamp: {m['timestamp']}, component: {m['component']}, value: {m['value']}, service: {m['service']}, threshold: {rule['threshold']}"  # noqa: E501  # pylint: disable=C0301
        self.stream.print(alert_format, style=rule["color"])

    def generate_alerts(self, show_severity=False):
        """
        Generate alerts based on rules
        """
        context = Context(default_value=None)
        for rule in self.rules:  # pylint: disable=R1702
            condition = Rule(rule["condition"], context=context)
            matches = condition.filter(self.metrics)
            matches_dict = [i for i in matches]  # pylint: disable=R1721
            if not rule["majority"]:
                for match in matches_dict:
                    self.print_alert(rule, match, show_severity)
            else:
                for service in self.services:
                    for timestamp in self.timestamps:
                        filtered_matches = [
                            i
                            for i in matches_dict
                            if i["service"] == service and i["timestamp"] == timestamp  # noqa: E501  # pylint: disable=C0301
                        ]
                        if len(filtered_matches) / self.servers[service]["count"] > 0.5:  # noqa: E501  # pylint: disable=C0301
                            for selected in filtered_matches:
                                self.print_alert(rule, selected, show_severity)

    def get_unique_services(self):
        """
        Get names of all unique clustered services
        """
        self.services = _get_unique_values_for_given_key(self.metrics, "service")  # noqa: E501

    def get_servers_per_service(self):
        """
        Get a dictionary of services and
        their respective servers and counts
        """
        self.servers = _get_items_for_given_values_list(
            self.metrics, self.services, "service", "server"
        )

    def get_unique_timestamps(self):
        """
        Get unique timestamps from metrics
        """
        self.timestamps = _get_unique_values_for_given_key(self.metrics, "timestamp")  # noqa: E501
