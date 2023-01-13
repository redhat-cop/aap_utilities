# Red Hat Communities of Practice Ansible Automation Platform Utilities Collection

![pre-commit tests](https://github.com/redhat-cop/aap_utilities/actions/workflows/pre-commit.yml/badge.svg)
![Galaxy Release](https://github.com/redhat-cop/aap_utilities/workflows/galaxy-release/badge.svg)
<!-- Further CI badges go here as above -->

This ansible collection includes a number of roles which can be useful for installing and managing AWX or Ansible Automation Platform.
Using this collection, you'll be able to automate following tasks:

* RHEL based installs
  * prepare and install Automation controller and Private automation hub on RHEL
  * configure the OS to support Kerberos (if you plan to manage Windows hosts using AD credentials)
  * backup and restore Automation controller and Private automation hub
  * install a minimal Git repo over SSH, for demonstration and learning purposes
* OpenShift based installs
  * prepare and install Automation controller and Private automation hub on OpenShift

## Requirements

The following collections are required to use this collection.

| Name             | Minimum Version |
|------------------|:---------------:|
| ansible.posix    | 1.0.0           |
| kubernetes.core  | 2.2.0           |
| redhat.openshift | 2.0.1           |

> ⚠️ **IMPORTANT**
>
> To install this collection ensure that access to Automation Hub is configured or required collections are already installed.

The `aap_install_ocp` role requires the `kubernetes` (version 12.0.0 or later) Python module to be installed.

## Redhat Communities of Practice Configuration Collections Suite

|Collection Name|Purpose|
|:---:|:---:|
|[Controller Configuration](https://galaxy.ansible.com/redhat_cop/controller_configuration)|Automation controller configuration|
|[Hub Configuration](https://galaxy.ansible.com/redhat_cop/ah_configuration)|Automation hub configuration|
|[EE Utilities](https://galaxy.ansible.com/redhat_cop/ee_utilities)|Execution Environment creation utilities|
|[AAP installation Utilities](https://galaxy.ansible.com/redhat_cop/aap_utilities)|Ansible Automation Platform Utilities|
|[AAP Configuration Template](https://github.com/redhat-cop/aap_configuration_template)|Configuration Template for this suite|

## Included content

Click the `Content` button to see the list of content included in this collection.

## Installing this collection

You can install the redhat\_cop aap\_utilities collection with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install redhat_cop.aap_utilities
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: redhat_cop.aap_utilities
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

## Roadmap

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [AAP Utilities collection repository](https://github.com/redhat-cop/aap_utilities).
More information about contributing can be found in our [Contribution Guidelines.](https://github.com/redhat-cop/aap_utilities/blob/devel/.github/CONTRIBUTING.md)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
