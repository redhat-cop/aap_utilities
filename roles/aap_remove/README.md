# redhat_cop.aap_utilities.aap_remove

Ansible role to remove instances of AAP.

## Requirements

None

## Role Variables

Available variables are listed below, along with default values defined (see defaults/main.yml)

```yaml
# Role Vars
aap_remove_controller: false
aap_remove_ah: false
```

The above are used to determine whether to remove Controller or Automation Hub from the node.
We recommend setting a host vars or simply using separate plays for each host which determines which of these vars to set true.
An example is below.

## Example Playbook

```yaml
---
# Playbook to install AAP2

- name: Remove Ansible Controller
  hosts: controller
  vars:
    aap_remove_controller: true
  roles:
    - redhat_cop.aap_utilities.aap_remove

- name: Remove Ansible Automation Hub
  hosts: ah
  vars:
    aap_remove_ah: true
  roles:
    - redhat_cop.aap_utilities.aap_remove
```

## License

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author Information

Tom Page
