# -*- coding: utf-8 -*-

"""Module responsible for fetching accounts from LDAP.
"""

import json
import ldap3


# pylint: disable=too-few-public-methods
class AccountManager:
    """Returns accounts from LDAP
    """

    # pylint: disable=too-few-public-methods
    class Account:
        """Represents a user account filled with information obtained from LDAP.
        """

        def __init__(self, ldap_account, ldap_account_attributes):
            account = ldap_account["raw_attributes"]
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
        server = ldap3.Server(ldap_url)
        self.__connection = ldap3.Connection(server=server, user=ldap_user, password=ldap_password)
        self.__connection.bind()


    def get_accounts(self):
        """Connects to LDAP, searches for user accounts and generates a list of :class:`grafana_inviter.accounts.AccountManager.Account`

        Returns:
            [list] -- Returns a list of :class:`grafana_inviter.accounts.AccountManager.Account`
        """

        group_base_dn = self.__ldap_query_config["group_base_dn"]
        search_filter = self.__ldap_query_config["search_filter"]
        retrieve_attributes = self.__ldap_query_config["retrieve_attributes"]

        self.__connection.search(search_base=group_base_dn, search_filter=search_filter, search_scope=ldap3.SUBTREE, attributes=retrieve_attributes)
        group_members = self.__connection.response
        print(group_members)
        return [AccountManager.Account(member, retrieve_attributes) for member in group_members]
