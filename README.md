# grafana-inviter

[![Azure DevOps builds](https://img.shields.io/azure-devops/build/tomtomweb/GitHub-TomTom-International/14.svg)](https://dev.azure.com/tomtomweb/GitHub-TomTom-International/_build/latest?definitionId=14&branchName=master)
[![Azure DevOps tests](https://img.shields.io/azure-devops/tests/tomtomweb/GitHub-TomTom-International/14.svg)](https://dev.azure.com/tomtomweb/GitHub-TomTom-International/_build/latest?definitionId=14&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/tomtomweb/GitHub-TomTom-International/14.svg)](https://dev.azure.com/tomtomweb/GitHub-TomTom-International/_build/latest?definitionId=14&branchName=master)

[![PyPI - Version](https://img.shields.io/pypi/v/grafana-inviter.svg)](https://pypi.org/project/grafana-inviter/)
[![PyPI - License](https://img.shields.io/pypi/l/grafana-inviter.svg)](https://pypi.org/project/grafana-inviter/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/grafana-inviter.svg)](https://pypi.org/project/grafana-inviter/)
[![PyPI - Format](https://img.shields.io/pypi/format/grafana-inviter.svg)](https://pypi.org/project/grafana-inviter/)
[![PyPI - Status](https://img.shields.io/pypi/status/grafana-inviter.svg)](https://pypi.org/project/grafana-inviter/)
[![PyUp - Updates](https://pyup.io/repos/github/tomtom-international/grafana-inviter/shield.svg)](https://pyup.io/repos/github/tomtom-international/grafana-inviter/)

Inviting people to join a Grafana organization is usually done from the Grafana UI. For smaller groups this might be easy but for a larger set of people one
rather would like to not fiddle around in the UI and instead do it in an automated fashion.

This tool is intended to send invites to join a new Grafana organization to people obtained from LDAP.

## Features

* Fetch users from LDAP and generate Grafana invites links
* Send invite links to users

## Quickstart

```bash
pip install grafana-inviter
```

* Copy the *example_config.json* configuration and adjust it to your needs
* Generate a Grafana API token with admin privileges (*https://<YOUR_GRAFANA_URL>/org/apikeys*)
* Ensure you have a LDAP service account user for searches created

```bash
grafana-inviter --grafana-token "<YOUR_GF_TOKEN_WITH>" --ldap-user <YOUR_SVC_ACCOUNT_USER> --config config.json --ask-ldap-password
LDAP password:
Sending invite to John Doe (John Doe@acme.org)
{'name': 'John Doe', 'loginOrEmail': 'John.Doe@acme.org', 'role': 'Viewer', 'sendEmail': False, 'orgId': 10}
 > User John.Doe@acme.org is already added to organization
Sending invite to Jane Doe (Jane.Doe@acme.org)
{'name': 'Jane Doe', 'loginOrEmail': 'Jane.Doe@acme.org', 'role': 'Viewer', 'sendEmail': False, 'orgId': 10}
 > Created invite for Jane.Doe@acme.org

Available invite URLs: ['https://<YOUR_GRAFANA_URL>/invite/Vv4Q8SYVyk7ULGpeWvjMXl0iuWLl67']
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [tomtom-international/cookiecutter-python](https://github.com/tomtom-international/cookiecutter-python) project template.
