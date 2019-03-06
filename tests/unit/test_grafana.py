# -*- coding: utf-8 -*-

"""
Tests for the invite module.
"""

import json
import requests
from unittest.mock import ANY, call, MagicMock, patch

from grafana_inviter.grafana import Grafana


@patch("requests.get")
@patch("requests.post")
def test_should_generate_successful_invite(mock_requests_post, mock_requests_get):
    """
    """
    # Given
    mock_account = MagicMock()
    mock_account.name = "John Doe"
    mock_account.mail = "john.doe@acme.org"

    mock_requests_post_response = MagicMock(status_code=requests.codes.ok)
    mock_requests_post_response.json.return_value = { "message": "" }
    mock_requests_post.return_value = mock_requests_post_response

    # When
    grafana = Grafana("http://grafana", "my-token")
    result, message = grafana.invite(mock_account)

    # Then
    mock_requests_post.assert_called_with(
        "http://grafana/api/org/invites",
        headers={"Authorization": "Bearer my-token"},
        json={"name": "John Doe", "loginOrEmail": "john.doe@acme.org", "role": "Viewer", "sendEmail": False, "orgId": 16 })

    assert result == True
    assert message == ""


@patch("requests.get")
@patch("requests.post")
def test_should_return_false_if_request_failed(mock_requests_post, mock_requests_get):
    """Test that returned tuple in case of an request error is properly set.
    """

    # Given
    mock_account = MagicMock()
    mock_requests_post_response = MagicMock(status_code=requests.codes.bad_request,
                                       side_effect=requests.exceptions.HTTPError())
    mock_requests_post_response.json.return_value = { "message": "Some error" }
    mock_requests_post.return_value = mock_requests_post_response

    # When
    grafana = Grafana("http://grafana", "my-token")
    result, message = grafana.invite(mock_account)

    # Then
    assert not result
    assert message == "Some error"


@patch("requests.get")
@patch("requests.post")
def test_should_not_send_invite_post_request_if_user_was_already_invited(mock_requests_post, mock_requests_get):
    """Test that a user is not invited again if it was already invited.
    """

    # Given
    mock_account = MagicMock(mail="Jane.Doe@acme.org")
    mock_requests_get_response = MagicMock(status_code=requests.codes.ok)
    mock_requests_get_response.json.return_value = [{
                                        "id": 123, "orgId": 12,
                                        "name": "Jane Doe", "email": "Jane.Doe@acme.org",
                                        "role": "Viewer",
                                        "invitedByLogin": "", "invitedByEmail": "", "invitedByName": "",
                                        "code": "ksXr3Cw1Uis3w6fNiaNYXMKeMYD0Zb",
                                        "status": "InvitePending",
                                        "url": "https://grafana/invite/ksXr3Cw1Uis3w6fNiaNYXMKeMYD0Zb",
                                        "emailSent": False,
                                        "emailSentOn": "2019-02-28T09:52:35Z",
                                        "createdOn":"2019-02-28T09:52:35Z"
                                        },
                                        {
                                        "id": 124, "orgId": 12,
                                        "name": "Johmn Doe", "email": "John.Doe@acme.org",
                                        "role": "Viewer",
                                        "invitedByLogin": "", "invitedByEmail": "", "invitedByName": "",
                                        "code": "ksXr3Cw1Uis3w6fNiaNYXMKeMYD0Zf",
                                        "status": "InvitePending",
                                        "url": "https://grafana/invite/ksXr3Cw1Uis3w6fNiaNYXMKeMYD0Zf",
                                        "emailSent": False,
                                        "emailSentOn": "2019-02-28T09:52:35Z",
                                        "createdOn":"2019-02-28T09:52:35Z"
                                        }]
    mock_requests_get.return_value = mock_requests_get_response#

    # When
    grafana = Grafana("http://grafana", "my-token")
    result, message = grafana.invite(mock_account)

    # Then
    assert not result
    assert "User already invited" in message


@patch("requests.get")
def test_should_populate_invite_link_to_account(mock_requests_get):
    """[summary]
    """

    # Given
    mock_accounts = [MagicMock(mail="John.Doe@acme.org"), MagicMock(mail="Jane.Doe@acme.org")]

    mock_requests_get_response = MagicMock(status_code=requests.codes.ok)
    mock_requests_get_response.json.return_value = [{
                                        "id": 123, "orgId": 12,
                                        "name": "John Doe", "email": "John.Doe@acme.org",
                                        "role": "Viewer",
                                        "invitedByLogin": "", "invitedByEmail": "", "invitedByName": "",
                                        "code": "ksXr3Cw1Uis3w6fNiaNYXMKeMYD0Zh",
                                        "status": "InvitePending",
                                        "url": "https://grafana/invite/ksXr3Cw1Uis3w6fNiaNYXMKeMYD0Zh",
                                        "emailSent": False,
                                        "emailSentOn": "2019-02-28T09:52:35Z",
                                        "createdOn":"2019-02-28T09:52:35Z"
                                        }]
    mock_requests_get.return_value = mock_requests_get_response

    # When
    grafana = Grafana("http://grafana", "my-token")
    grafana.populate_accounts_with_invite_links(mock_accounts)

    # Then
    account_with_invite = [mock_account for mock_account in mock_accounts if mock_account.mail == "John.Doe@acme.org"]
    assert len(account_with_invite) == 1
    assert hasattr(account_with_invite[0], "grafanaInviteLink")
