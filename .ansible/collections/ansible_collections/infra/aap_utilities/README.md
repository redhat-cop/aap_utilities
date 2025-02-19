# Red Hat Communities of Practice Ansible Automation Platform Utilities Collection

[![pre-commit tests](https://github.com/redhat-cop/aap_utilities/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/redhat-cop/aap_utilities/actions/workflows/pre-commit.yml)
[![Galaxy Release](https://github.com/redhat-cop/aap_utilities/actions/workflows/release.yml/badge.svg)](https://github.com/redhat-cop/aap_utilities/actions/workflows/release.yml)

This ansible collection includes a number of roles which can be useful for installing and managing AWX or Ansible Automation Platform.
Using this collection, you'll be able to automate following tasks:

* RHEL based installs
  * prepare and install Automation controller and Private automation hub on RHEL
  * configure the OS to support Kerberos (if you plan to manage Windows hosts using AD credentials)
  * backup and restore Automation controller and Private automation hub
  * install a minimal Git repo over SSH, for demonstration and learning purposes
* OpenShift based installs
  * prepare and install Automation controller and Private automation hub on OpenShift

## Getting Help

We are on the Ansible Forums and Matrix, if you want to discuss something, ask for help, or participate in the community, please use the #infra-config-as-code tag on the fourm, or post to the chat in Matrix.

[Ansible Forums](https://forum.ansible.com/tag/infra-config-as-code)

[Matrix Chat Room](https://matrix.to/#/#aap_config_as_code:ansible.com)

## Requirements

The following collections are required to use this collection if you are using the Openshift specific roles.

| Name             | Minimum Version |
|------------------|:---------------:|
| ansible.posix    | 1.0.0           |
| kubernetes.core  | 2.2.0           |
| redhat.openshift | 2.0.1           |

> ⚠️ **IMPORTANT**
>
> To install this collection ensure that access to Automation Hub is configured or required collections are already installed.

The `aap_install_ocp` role requires the `kubernetes` (version 12.0.0 or later) Python module to be installed.

## Links to Ansible Automation Platform Collections

|                                      Collection Name                                         |                 Purpose                  |
|:--------------------------------------------------------------------------------------------:|:----------------------------------------:|
| [awx.awx/Ansible.controller repo](https://github.com/ansible/awx/tree/devel/awx_collection) |   Automation controller modules          |
|        [Ansible Hub Configuration](https://github.com/ansible/automation_hub_collection)     |       Automation hub configuration       |

## Links to other Validated Configuration Collections for Ansible Automation Platform

|                                      Collection Name                                       |                 Purpose                  |
|:------------------------------------------------------------------------------------------:|:----------------------------------------:|
| [Controller Configuration](https://github.com/redhat-cop/controller_configuration) |   Automation controller configuration    |
|             [EE Utilities](https://github.com/redhat-cop/ee_utilities)             | Execution Environment creation utilities |
|     [AAP installation Utilities](https://github.com/redhat-cop/aap_utilities)      |  Ansible Automation Platform Utilities   |
|   [AAP Configuration Template](https://github.com/redhat-cop/aap_configuration_template)   |  Configuration Template for this suite   |

## Included content

Click the `Content` button to see the list of content included in this collection.

## Installing this collection

You can install the redhat\_cop aap\_utilities collection with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install infra.aap_utilities
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: infra.aap_utilities
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```

## Using this collection

### See Also

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release and Upgrade Notes

Many roles and variables have been renamed to reflect the product renaming from Tower to controller/AAP.
Verify carefully your inventory variables and playbooks.

The previous OCP installation role has been suppressed due to the introduction of an operator.
In addition to the current OCP installation role, further (community) automation for AAP on OCP is available from the [GitOps catalogue](https://github.com/redhat-cop/gitops-catalog/tree/main/ansible-automation-platform).

## Releasing, Versioning and Deprecation

This collection follows [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

We plan to regularly release new minor or bugfix versions once new features or bugfixes have been implemented.

Releasing the current major version happens from the `devel` branch.

## Roadmap

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [AAP Utilities collection repository](https://github.com/redhat-cop/aap_utilities).
More information about contributing can be found in our [Contribution Guidelines.](https://github.com/redhat-cop/aap_utilities/blob/devel/.github/CONTRIBUTING.md)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](LICENSE) to see the full text.
