# -*- coding: utf-8 -*-

"""Module that store the JSON configuration schema.
"""

def json_config_schema():
    """Returns the JSON configuration schema
    """
    return """
{
  "type": "object",
  "properties": {
    "ldap": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string"
        },
        "user": {
          "type": "string"
        },
        "password": {
          "type": "string"
        },
        "query": {
          "type": "object",
          "properties": {
            "group_base_dn": {
              "type": "string"
            },
            "search_filter": {
              "type": "string"
            },
            "retrieve_attributes": {
              "type": "array",
              "items": {
                "type": "string"
              }
            }
          },
          "required": [ "group_base_dn", "search_filter", "retrieve_attributes" ]
        }
      },
      "required": [ "url", "user", "password", "query" ]
    },
    "grafana": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string"
        },
        "token": {
          "type": "string"
        },
        "send_invite_mail": {
          "type": "boolean"
        },
        "orgId": {
          "type": "integer"
        }
      },
      "required": [ "url", "token", "orgId" ]
    }
  },
  "required": [ "ldap", "grafana" ]
}"""
