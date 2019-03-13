# -*- coding: utf-8 -*-

"""Module responsible for fetching accounts from LDAP.
"""

import json
import ldap


# pylint: disable=too-few-public-methods
class AccountManager:
    """Returns accounts from LDAP
    """

    # pylint: disable=too-few-public-methods
    class Account:
        """Represents a user account filled with information obtained from LDAP.
        """

        def __init__(self, ldap_account, ldap_account_attributes):
            account = ldap_account[1]
            for ldap_attribute in ldap_account_attributes:
                attribute_values = account[ldap_attribute]
                attribute_values_size = len(attribute_values)
                if attribute_values_size == 1:
                    attr_value = attribute_values[0].decode("utf-8")
                    setattr(self, ldap_attribute, attr_value)
                elif attribute_values_size > 1:
                    inner_attribute_list = []
                    for attribute_value in attribute_values:
                        inner_attribute_list.append(attribute_value.decode("utf-8"))
                    setattr(self, ldap_attribute, inner_attribute_list)


        def __repr__(self):
            return "%s" % json.dumps(self.__dict__)

    def __init__(self, ldap_query_config, ldap_user, ldap_password, ldap_url):
        self.__ldap_query_config = ldap_query_config
        self.__connection = ldap.initialize(ldap_url)
        self.__connection.simple_bind_s(ldap_user, ldap_password)


    def get_accounts(self):
        """Connects to LDAP, searches for user accounts and generates a list of :class:`grafana_inviter.accounts.AccountManager.Account`

        Returns:
            [list] -- Returns a list of :class:`grafana_inviter.accounts.AccountManager.Account`
        """

        group_base_dn = self.__ldap_query_config["group_base_dn"]
        search_filter = self.__ldap_query_config["search_filter"]
        retrieve_attributes = self.__ldap_query_config["retrieve_attributes"]

        # pylint: disable=no-member
        search_scope = ldap.SCOPE_SUBTREE

        group_members = self.__connection.search_s(group_base_dn, search_scope, search_filter, retrieve_attributes)
        return [AccountManager.Account(member, retrieve_attributes) for member in group_members]
