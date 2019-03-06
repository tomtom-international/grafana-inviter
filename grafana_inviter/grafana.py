# -*- coding: utf-8 -*-

"""Module responsible for generating a Grafana invite.
"""

from enum import Enum
import requests


class HttpMethod(Enum):
    """Enum for the various HTTP methods.
    """

    GET = 1
    POST = 2


class Grafana:
    """Simple class wrapping the Grafana HTTP API.
    """

    def __init__(self, grafana_server, grafana_token):
        """Constructor

        Arguments:
            grafana_server {str} -- Grafana URL.
            grafana_token {str} -- Admin token for authentication in Grafana.
        """

        self.__grafana_server = grafana_server
        self.__grafana_token = grafana_token


    def __query(self, method, api_endpoint, **kwargs):
        """Create a request query depending on the HTTP method and endpoiint.

        Arguments:
            method {HttpMethod} -- HTTP method.
            endpoint {str} -- Grafana API endpoint (eg. org/users).

        Returns:
            [requests.Response] -- Returns a requests.Response object.
        """

        requests_http_methods = {
            HttpMethod.GET: requests.get,
            HttpMethod.POST: requests.post
        }
        headers = {"Authorization": "Bearer %s" % self.__grafana_token}
        return requests_http_methods[method]("%s/api/%s" % (self.__grafana_server, api_endpoint), headers=headers, **kwargs)


    def invite(self, account, send_mail=False):
        """Generates an invite for given account in Grafana.

        Args:
            account {AccountManager.Account} -- Account to be used to generate invite for.

        Returns:
            [tuple(bool, str)] -- True if succeeded otherwise False including a message.
        """

        response = self.__query(HttpMethod.GET, "org/invites")
        invites = response.json()

        if any(invite["email"].lower() == account.mail.lower() for invite in invites):
            return (False, "User already invited")

        payload = {
            "name": account.name,
            "loginOrEmail": account.mail,
            "role": "Viewer",
            "sendEmail": send_mail,
            "orgId": 16
        }

        response = self.__query(HttpMethod.POST, "org/invites", json=payload)
        return (response.status_code == requests.codes.ok, response.json()['message'])


    def populate_accounts_with_invite_links(self, accounts):
        """Populates the accounts with a Grafana invite link in case an invitation is found.

        Arguments:
            accounts {list[grafana_inviter.AccountManager.Account]} -- Accounts we want to obtain the invite link for
        """

        response = self.__query(HttpMethod.GET, "org/invites")
        invites = response.json()
        accounts_copy = list(accounts)

        for invite in invites:
            # To avoid iterations over already found accounts we reverse the list (a copy) and
            # remove an account from the copied list each time we find a corresponding account in the invites.
            for account in reversed(accounts_copy):
                if account.mail == invite["email"]:
                    account.grafanaInviteLink = invite["url"]
                    accounts_copy.remove(account)
