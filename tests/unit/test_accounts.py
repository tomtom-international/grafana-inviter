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
    {
        "raw_dn": b"CN=John Doe,OU=AC,OU=Employees,O=acme,C=global",
        "raw_attributes": {
            "memberOf": [
                b"CN=TeamA,vCN=GroupA,CN=Roles,O=acme,C=global",
                b"CN=AnotherGroup,CN=GroupB,CN=Roles,O=acme,C=global",
                b"CN=AcmeUsers,CN=acme,CN=Roles,O=acme,C=global",
                b"CN=Acme Employees,CN=Roles,O=acme,C=global"
            ],
            "name": [b"John Doe"],
            "msDS-UserAccountDisabled": [b"FALSE"],
            "uid": [b"jodoe"],
            "mail": [b"John.Doe@acme.com"]
        }
    },
    {
        "raw_dn": b"CN=Jane Doe,OU=AC,OU=Employees,O=acme,C=global",
        "raw_attributes": {
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
        }
    }
]


@patch("ldap3.Server")
@patch("ldap3.Connection")
def test_account_manager(mock_ldap_connection, mock_ldap_server):
    """Test account manager
    """
    # Given
    mock_ldap_server_instance = mock_ldap_server.return_value
    mock_ldap_connection_instance = mock_ldap_connection.return_value

    # When
    AccountManager(ldap_query_config=test_config_json()["ldap"]["query"],
                   ldap_user="user", ldap_password="password", ldap_url="ldps://testserver")

    # Then
    mock_ldap_server.assert_called_with("ldps://testserver")
    mock_ldap_connection.assert_called_with(server=mock_ldap_server_instance,
                                            user="user",
                                            password="password")
    mock_ldap_connection_instance.assert_has_calls([call.bind()])


@patch("ldap3.Server")
@patch("ldap3.Connection")
def test_should_return_expected_accounts(mock_ldap_connection, mock_ldap_server):
    """Tests that accounts are returned from AccountManager.
    """
    # Given
    mock_ldap_connection_instance = mock_ldap_connection.return_value
    mock_ldap_connection_instance.response = LDAP_ACCOUNT_SEARCH_RESULT

    manager = AccountManager(ldap_query_config=test_config_json()["ldap"]["query"],
                             ldap_user="user", ldap_password="password", ldap_url="ldps://testserver")

    # When
    accounts = manager.get_accounts()

    # Then
    mock_ldap_connection_instance.assert_has_calls([
        call.search(search_base="OU=AC,OU=Employees,O=acme,C=global",
                    search_filter="(&(o=SubUnit)(memberOf=CN=AnotherGroup,CN=GroupB,CN=Roles,O=acme,C=global))",
                    search_scope=ANY,
                    attributes=["uid", "mail", "name", "msDS-UserAccountDisabled", "memberOf"])
    ])

    assert len(accounts) == 2
    assert any(account.name in ["Jane Doe", "John Doe"] for account in accounts)

    try:
        assert any(json.loads(str(account)) for account in accounts)
    except json.decoder.JSONDecodeError:
        pytest.fail("Expected a JSON encoded format.")
