# -*- coding: utf-8 -*-

"""
Tests for the grafana_inviter.accounts module.
"""

import json
import pytest

from unittest.mock import ANY, call, patch, MagicMock
from grafana_inviter.accounts import AccountManager


def test_config_json():
    """Returns a test configuration
    """
    return {
        "ldap": {
            "url": "ldps://testserver",
            "user": "user",
            "password": "password",
            "query": {
                "group_base_dn": "OU=AC,OU=Employees,O=acme,C=global",
                "search_filter": "(&(o=SubUnit)(memberOf=CN=AnotherGroup,CN=GroupB,CN=Roles,O=acme,C=global))",
                "retrieve_attributes": ["uid", "mail", "name", "msDS-UserAccountDisabled", "memberOf"]
            }
        }
    }

LDAP_ACCOUNT_SEARCH_RESULT = [
    ("CN=John Doe,OU=AC,OU=Employees,O=acme,C=global", {
        "memberOf": [
            b"CN=TeamA,CN=GroupA,CN=Roles,O=acme,C=global",
            b"CN=AnotherGroup,CN=GroupB,CN=Roles,O=acme,C=global",
            b"CN=AcmeUsers,CN=acme,CN=Roles,O=acme,C=global",
            b"CN=Acme Employees,CN=Roles,O=acme,C=global"
        ],
        "name": [b"John Doe"],
        "msDS-UserAccountDisabled": [b"FALSE"],
        "uid": [b"jodoe"],
        "mail": [b"John.Doe@acme.com"]
    }),
    ("CN=Jane Doe,OU=AC,OU=Employees,O=acme,C=global", {
        "memberOf": [
            b"CN=TeamB,CN=GroupA,CN=Roles,O=acme,C=global",
            b"CN=AnotherGroup,CN=GroupB,CN=Roles,O=acme,C=global",
            b"CN=AcmeUsers,CN=acme,CN=Roles,O=acme,C=global",
            b"CN=Acme Employees,CN=Roles,O=acme,C=global"
        ],
        "name": [b"Jane Doe"],
        "msDS-UserAccountDisabled": [b"FALSE"],
        "uid": [b"jadoe"],
        "mail": [b"Jane.Doe@acme.com"]
    })
]


@patch("ldap.initialize")
def test_account_manager(mock_ldap_initialize):
    """Test account manager
    """
    # Given
    mock_ldap_connection = MagicMock()
    mock_ldap_initialize.return_value = mock_ldap_connection

    # When
    AccountManager(ldap_query_config=test_config_json()["ldap"]["query"],
                   ldap_user="user", ldap_password="password", ldap_url="ldps://testserver")

    # Then
    mock_ldap_initialize.assert_called_with("ldps://testserver")
    mock_ldap_connection.assert_has_calls([
        call.simple_bind_s("user", "password")
    ])


@patch("ldap.initialize")
def test_should_return_expected_accounts(mock_ldap_initialize):
    """Tests that accounts are returned from AccountManager.
    """
    # Given
    mock_ldap_connection = MagicMock()
    mock_ldap_initialize.return_value = mock_ldap_connection
    mock_ldap_connection.search_s.return_value = LDAP_ACCOUNT_SEARCH_RESULT

    manager = AccountManager(ldap_query_config=test_config_json()["ldap"]["query"],
                             ldap_user="user", ldap_password="password", ldap_url="ldps://testserver")

    # When
    accounts = manager.get_accounts()

    # Then
    mock_ldap_connection.assert_has_calls([
        call.search_s("OU=AC,OU=Employees,O=acme,C=global",
                      ANY,
                      "(&(o=SubUnit)(memberOf=CN=AnotherGroup,CN=GroupB,CN=Roles,O=acme,C=global))",
                      ["uid", "mail", "name", "msDS-UserAccountDisabled", "memberOf"])
    ])

    assert len(accounts) == 2
    assert any(account.name in ["Jane Doe", "John Doe"] for account in accounts)

    try:
        assert any(json.loads(str(account)) for account in accounts)
    except json.decoder.JSONDecodeError:
        pytest.fail("Expected a JSON encoded format.")
