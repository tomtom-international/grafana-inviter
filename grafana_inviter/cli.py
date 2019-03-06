# -*- coding: utf-8 -*-

"""Script for fetching users from LDAP and sending/generating invites for Grafana access.
"""

import argparse
from getpass import getpass
import sys
import anyconfig

from .accounts import AccountManager
from .grafana import Grafana


def parse_args(args):
    """Returns parsed commandline arguments.
    """

    parser = argparse.ArgumentParser(description="Script for generating/sending Grafana invite URLs. By default only invite URLs are generated.")
    parser.add_argument("--ldap-url", type=str, required=True, help="LDAP URL")
    parser.add_argument("--ldap-user", type=str, required=True, help="LDAP service account username")
    parser.add_argument("--ldap-password", type=str, help="LDAP service account password")
    parser.add_argument("--grafana-url", type=str, required=True, help="Grafana URL")
    parser.add_argument("--grafana-token", type=str, help="Grafana API token")
    parser.add_argument("--send-invite-mail", action="store_true", help="Send mail with Grafana invite URL.")
    parser.add_argument("--config", type=str, help="Location of configuration file")
    return parser.parse_args(args)


def main():
    """Main entrypoint
    """

    args = parse_args(sys.argv[1:])

    config = None
    if args.config:
        config = anyconfig.load(args.config)

    if not args.ldap_password and args.ldap_user:
        args.ldap_password = getpass("LDAP password: ")

    if not args.grafana_token:
        args.grafana_token = getpass("Grafana token: ")

    manager = AccountManager(config=config, username=args.ldap_user, password=args.ldap_password, ldap_server=args.ldap_url)
    accounts = manager.get_accounts()

    grafana = Grafana(grafana_server=args.grafana_url, grafana_token=args.grafana_token)

    for account in accounts:
        print("Sending invite to %s (%s)" % (account.name, account.mail))
        _, message = grafana.invite(account=account, send_mail=args.send_invite_mail)
        print(" > %s" % (message))

    grafana.populate_accounts_with_invite_links(accounts)
    print("Available invite URLs: %s" % [account.grafanaInviteLink for account in accounts if hasattr(account, "grafanaInviteLink")])

    return 0


if __name__ == "__main__":
    sys.exit(main())
