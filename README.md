# grafana-inviter

[![image](https://dev.azure.com/tomtomweb/GitHub-TomTom-International/_apis/build/status/tomtom-international.grafana-inviter?branchName=master)](https://dev.azure.com/tomtomweb/GitHub-TomTom-International/_build/latest?definitionId=2&branchName=master)
[![image](https://img.shields.io/pypi/v/grafana-inviter.svg)](https://pypi.org/project/grafana-inviter/)
[![image](https://img.shields.io/pypi/l/grafana-inviter.svg)](https://pypi.org/project/grafana-inviter/)
[![image](https://img.shields.io/pypi/pyversions/grafana-inviter.svg)](https://pypi.org/project/grafana-inviter/)

Inviting people to join a Grafana organization is usually done from the Grafana UI. For smaller groups this might be easy but for a larger set of people one
rather would like to not fiddle around in the UI and instead do it in an automated fashion.

This tool is intended to send invites to join a new Grafana organization to people obtained from LDAP.

## Installation

```bash
$ python setup.py install
```

or

```bash
$ pip install grafana-inviter
```

## Usage

* Copy the *example_config.json* configuration and adjust it to your needs
* Generate a Grafana API token with admin privileges (*https://<YOUR_GRAFANA_URL>/org/apikeys*)
* Ensure you have a LDAP service account user for searches created

```bash
$ grafana-inviter --grafana-token "<YOUR_GF_TOKEN_WITH>" --ldap-user <YOUR_SVC_ACCOUNT_USER> --config config.json --ask-ldap-password
LDAP password:
Sending invite to John Doe (John Doe@acme.org)
{'name': 'John Doe', 'loginOrEmail': 'John.Doe@acme.org', 'role': 'Viewer', 'sendEmail': False, 'orgId': 10}
 > User John.Doe@acme.org is already added to organization
Sending invite to Jane Doe (Jane.Doe@acme.org)
{'name': 'Jane Doe', 'loginOrEmail': 'Jane.Doe@acme.org', 'role': 'Viewer', 'sendEmail': False, 'orgId': 10}
 > Created invite for Jane.Doe@acme.org

Available invite URLs: ['https://<YOUR_GRAFANA_URL>/invite/Vv4Q8SYVyk7ULGpeWvjMXl0iuWLl67']
```
