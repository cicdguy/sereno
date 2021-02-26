"""
Rules and conditions
"""

import yaml
from rule_engine import Rule, RuleSyntaxError


class Rules:
    """
    Rules and conditions
    """
    def __init__(self, rules_conf_file):
        """
        Constructor
        """
        self.conf_file = rules_conf_file
        self.read_conf()
        self.read_severity_levels()
        self.read_rules()
        self.validate_rules()
        self.output_color_lookup()

    def read_conf(self):
        """
        Read the rules config
        """
        with open(self.conf_file, "r") as fil:
            self.conf = yaml.load(fil, Loader=yaml.SafeLoader)

    def read_severity_levels(self):
        """
        Read severity levels
        """
        self.severities = self.conf["severities"]

    def read_rules(self):
        """
        Read rules
        """
        self.rules = self.conf["rules"]

    def validate_rules(self):
        """
        Validate all rules' syntax
        """
        for rule in self.rules:
            if not Rule(rule["condition"]).is_valid(rule["condition"]):
                raise RuleSyntaxError(
                    message='Condition syntax invalid: {rule["condition"]}'
                )  # noqa: E501

    def output_color_lookup(self):
        """
        Match severity level color with rule
        """
        for rule in self.rules:
            rule["color"] = self.severities[rule["severity"]]["color"]
