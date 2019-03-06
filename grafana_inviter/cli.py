# -*- coding: utf-8 -*-

"""Script for fetching users from LDAP and sending/generating invites for Grafana access.
"""

import argparse
from getpass import getpass
import sys
import anyconfig

from .accounts import AccountManager
from .grafana import Grafana
from .config_schema import json_config_schema


def parse_args(args):
    """Returns parsed commandline arguments.
    """

    parser = argparse.ArgumentParser(description="Script for generating/sending Grafana invite URLs. By default only invite URLs are generated.")
    parser.add_argument("--ldap-url", type=str, help="LDAP URL")
    parser.add_argument("--ldap-user", type=str, help="LDAP service account username")
    parser.add_argument("--ldap-password", type=str, help="LDAP service account password")
    parser.add_argument("--ask-ldap-password", action="store_true", help="Ask for the LDAP service account password")
    parser.add_argument("--grafana-url", type=str, help="Grafana URL")
    parser.add_argument("--grafana-token", type=str, help="Grafana API token")
    parser.add_argument("--ask-grafana-token", action="store_true", help="Ask for the Grafana API token")
    parser.add_argument("--send-invite-mail", action="store_true", help="Send mail with Grafana invite URL.")
    parser.add_argument("--config", required=True, type=str, help="Location of configuration file")
    return parser.parse_args(args)


def configure(args):
    """Load the configuration and alter it based on the passed argparse arguments which take presedence over the configuration file.
    """

    config = anyconfig.load(args.config)

    if args.ldap_url:
        config["ldap"]["url"] = args.ldap_url

    if args.ldap_user:
        config["ldap"]["user"] = args.ldap_user

    if args.ldap_password:
        config["ldap"]["password"] = args.ldap_password
    if args.ask_ldap_password:
        config["ldap"]["password"] = getpass("LDAP password: ")

    if args.grafana_url:
        config["grafana"]["url"] = args.grafana_url
    if args.grafana_token:
        config["grafana"]["token"] = args.grafana_token
    if args.ask_grafana_token:
        config["grafana"]["token"] = getpass("Grafana token: ")
    if args.send_invite_mail:
        config["grafana"]["send_invite_mail"] = True

    return config


def validate(config):
    """Validate the configuration
    """

    schema = anyconfig.loads(json_config_schema(), ac_parser="json")
    result, message = anyconfig.validate(config, schema)
    if not result:
        raise SystemExit(message)


def assemble(config):
    """Assembles all pieces together and sends invites to users.
    """

    manager = AccountManager(ldap_query_config=config["ldap"]["query"],
                             ldap_user=config["ldap"]["user"], ldap_password=config["ldap"]["password"],
                             ldap_url=config["ldap"]["url"])
    accounts = manager.get_accounts()

    grafana = Grafana(grafana_server=config["grafana"]["url"], grafana_token=config["grafana"]["token"])

    for account in accounts:
        print("Sending invite to %s (%s)" % (account.name, account.mail))
        _, message = grafana.invite(account=account, send_mail=config["grafana"]["send_invite_mail"])
        print(" > %s" % (message))

    grafana.populate_accounts_with_invite_links(accounts)
    print("Available invite URLs: %s" % [account.grafanaInviteLink for account in accounts if hasattr(account, "grafanaInviteLink")])

    return 0


def main():
    """Main entrypoint
    """

    args = parse_args(sys.argv[1:])
    config = configure(args)
    validate(config)
    assemble(config)


if __name__ == "__main__":
    sys.exit(main())
