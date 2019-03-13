# -*- coding: utf-8 -*-

"""
Tests for the cli module.
"""

import argparse
import requests
import pytest
from unittest.mock import ANY, call, MagicMock, patch

from grafana_inviter.cli import configure, assemble, main, parse_args, validate


def test_config_json():
    """Returns a test configuration
    """
    return {
        "ldap": {
            "url": "ldaps://test-ldap",
            "user": "test-user",
            "password": "test-password",
            "query": {
                "group_base_dn": "OU=AC,OU=Employees,O=acme,C=global",
                "search_filter": "(&(o=SubUnit)(memberOf=CN=AnotherGroup,CN=GroupB,CN=Roles,O=acme,C=global))",
                "retrieve_attributes": ["uid", "mail", "name", "msDS-UserAccountDisabled", "memberOf"]
            }
        },
        "grafana": {
            "url": "https://test-grafana",
            "token": "test-token",
            "send_invite_mail": False
        }
    }


def test_should_raise_exception_if_config_argument_not_provided():
    """Validate that config argument is mandatory.
    """
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_args():
    """Validate that parse_args returns expected values.
    """

    # Given & When
    parser = parse_args(["--ldap-user", "user", "--ldap-password", "password", "--ask-ldap-password", "--ldap-url", "ldp",
                         "--grafana-url", "grafana", "--grafana-token", "token", "--ask-grafana-token",
                         "--send-invite-mail", "--config", "config.json"])

    # Then
    assert parser.ldap_user == "user"
    assert parser.ask_ldap_password
    assert parser.ldap_password == "password"
    assert parser.grafana_url == "grafana"
    assert parser.grafana_token == "token"
    assert parser.ask_grafana_token
    assert parser.send_invite_mail
    assert parser.config == "config.json"


@patch("anyconfig.load")
def test_configure_should_use_overwritten_argparse_values(mock_anyconfig_load):
    """Validate that argparse values take precedence over the configuration file.
    """

    # Given
    mock_anyconfig_load.return_value = test_config_json()

    dummy_args = parse_args(["--ldap-url", "ldaps://prod-ldap",
                             "--ldap-user", "prod-user", "--ldap-password", "prod-password",
                             "--grafana-url", "https://prod-grafana", "--grafana-token", "prod-token",
                             "--send-invite-mail",
                             "--config", "dummy_config.json"])

    # When
    config = configure(dummy_args)

    # Then
    assert config["ldap"]["url"] == "ldaps://prod-ldap"
    assert config["ldap"]["user"] == "prod-user"
    assert config["ldap"]["password"] == "prod-password"

    assert config["grafana"]["url"] == "https://prod-grafana"
    assert config["grafana"]["token"] == "prod-token"
    assert config["grafana"]["send_invite_mail"]


@patch("grafana_inviter.cli.getpass")
@patch("anyconfig.load")
def test_configure_should_use_interactively_asked_ldap_password_and_grafana_token(mock_anyconfig_load, mock_getpass):
    """Validate that configure will ask for LDAP password and Grafana token.
    """

    # Given
    mock_anyconfig_load.return_value = test_config_json()
    mock_getpass.side_effect = ["interactively-provided-ldap-password", "interactively-provided-grafana-token"]

    dummy_args = parse_args(["--ask-ldap-password", "--ask-grafana-token", "--config", "dummy_config.json"])

    # When
    config = configure(dummy_args)

    # Then
    mock_getpass.call_count == 2
    assert config["ldap"]["password"] == "interactively-provided-ldap-password"
    assert config["grafana"]["token"] == "interactively-provided-grafana-token"


@patch("anyconfig.loads")
@patch("anyconfig.validate")
def test_validate_should_raise_system_exit_if_schema_validation_fails(mock_anyconfig_validate, mock_anyconfig_loads):
    # Given
    mock_anyconfig_loads.return_value = MagicMock()
    mock_anyconfig_validate.return_value = (False, "Missing attribute 'password'")

    # When & Then
    with pytest.raises(SystemExit):
        validate(test_config_json())


@patch("grafana_inviter.cli.AccountManager")
@patch("grafana_inviter.cli.Grafana")
def test_assemble(mock_grafana_ctor, mock_account_manager_ctor):
    # Given
    mock_account_manager = MagicMock()
    mock_account_manager_ctor.return_value = mock_account_manager
    mock_account = MagicMock(name="John Doe", mail="John.Doe@acme.org")
    mock_account_manager.get_accounts.return_value = [mock_account]

    mock_grafana = MagicMock()
    mock_grafana_ctor.return_value = mock_grafana
    mock_grafana.invite.return_value = (True, "User invited")

    #  When
    assemble(test_config_json())

    # Then
    mock_account_manager_ctor.assert_called_with(ldap_query_config=test_config_json()["ldap"]["query"],
                                            ldap_user="test-user", ldap_password="test-password", ldap_url="ldaps://test-ldap")
    mock_grafana_ctor.assert_called_with(grafana_config=test_config_json()["grafana"])

    mock_grafana.invite.assert_called_with(account=mock_account, send_mail=False)

    mock_grafana.populate_accounts_with_invite_links.assert_called_with([mock_account])
