# -*- coding: utf-8 -*-

"""
Tests for the cli module.
"""

import requests
import pytest
from unittest.mock import ANY, call, MagicMock, patch

from grafana_inviter.cli import main, parse_args


def test_should_raise_exception_if_no_argument_provided():
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_args():
    parser = parse_args(["--ldap-user", "user", "--ldap-password", "password", "--ldap-url", "ldp",
                         "--grafana-url", "grafana", "--grafana-token", "token",
                         "--send-invite-mail", "--config", "config.json"])
    assert parser.ldap_user == "user"
    assert parser.ldap_password == "password"
    assert parser.grafana_url == "grafana"
    assert parser.grafana_token == "token"
    assert parser.send_invite_mail
    assert parser.config == "config.json"


@patch("grafana_inviter.cli.parse_args")
@patch("anyconfig.load")
@patch("grafana_inviter.cli.getpass")
@patch("grafana_inviter.cli.AccountManager")
@patch("grafana_inviter.cli.Grafana")
def test_main(mock_grafana, mock_account_manager, mock_getpass, mock_anyconfig_load, mock_parse_args):
    # Given
    mock_parser = MagicMock(ldap_user="ldap_user", ldap_password="password", ldap_url="ldap-server",
                            grafana_url="grafana-server", grafana_token="token")
    mock_parse_args.return_value = mock_parser
    mock_parse_args.config.return_value = "config.json"
    mock_config = MagicMock()
    mock_anyconfig_load.return_value = mock_config



    #  When
    main()

    # Then
    mock_account_manager.assert_called_with(config=mock_config, username="ldap_user", password="password", ldap_server="ldap-server")
    mock_grafana.assert_called_with(grafana_server="grafana-server", grafana_token="token")
