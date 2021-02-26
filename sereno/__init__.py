"""
CLI and main
"""

import argparse
import os

import pkg_resources

from sereno.metrics import Metrics
from sereno.alerts import Alerts
from sereno.rules import Rules

_ROOT = os.path.abspath(os.path.dirname(__file__))
_DEFAULT_RULES_CONF = os.path.join(_ROOT, "conf", "rules.yaml")


def main(rules_conf_file, metrics_file, show_severity):
    """
    Main
    """
    metrics = Metrics(metrics_file).metrics
    rules = Rules(rules_conf_file).rules
    alerts = Alerts(metrics, rules)
    alerts.generate_alerts(show_severity)


def cli():
    """
    Command line interface
    """
    parser = argparse.ArgumentParser(description="Sereno: Rule-based Alerting")
    parser.add_argument(
        "-r",
        "--rules-config",
        help="Configuration file containing custom rules and severity levels",
        dest="rules_conf",
        default=_DEFAULT_RULES_CONF,
    )
    parser.add_argument(
        "-s",
        "--show-severity",
        help="Show severity levels in the alerts",
        dest="show_severity",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Display current version",
        action="version",
        version=pkg_resources.require("sereno")[0].version,
    )
    parser.add_argument("metrics_file", nargs=1)
    args = parser.parse_args()
    main(args.rules_conf, args.metrics_file[0], args.show_severity)
