# aap_ocp_install

A role to install Ansible Automation Platform (AAP) 2.x on OpenShift using the operator.

## Requirements

This role requires the `kubernetes` (version 12.0.0 or later) Python module.
In addition the kubernetes.core and redhat.openshift Ansible collections are required.

## Role Variables

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

| Variable Name              | Default Value | Required | Description                                                            |
|----------------------------|:-------------:|:--------:|------------------------------------------------------------------------|
| aap_ocp_install_namespace  | None          |          |                                                                        |
| aap_ocp_install_connection | None          | Yes      | Dictionary containing keys defined in the `connection variables table` |
| aap_ocp_install_operator   | None          | Yes*     | Dictionary containing keys defined in the `operator variables table`   |
| aap_ocp_install_controller | None          | Yes*     | Dictionary containing keys defined in the `controller variables table` |
| aap_ocp_install_hub        | None          | Yes*     | Dictionary containing keys defined in the `hub variables table`        |

\* Variable and required keys must be defined when no tags are specified or the type of tag is specified (e.g. `--tags controller` requires the aap_ocp_install_controller variable be defined.)

### aap_ocp_install_connection keys

| Key Name       | Default Value | Required | Description                                                  |
|----------------|:-------------:|:--------:|--------------------------------------------------------------|
| host           | None          | Yes      | OCP cluster to create the AAP objects in                     |
| username       | None          | Yes      | Username to use for authenticating with OCP                  |
| password       | None          | Yes      | Password to use for authenticating with OCP                  |
| validate_certs | None          |          | Validate SSL certificates. Valid values are: `true`, `false` |

### aap_ocp_install_operator keys

| Key Name | Default Value | Required | Description                                                   |
|----------|:-------------:|:--------:|---------------------------------------------------------------|
| channel  | None          | Yes      | Channel to subscribe (e.g. stable-2.2)                        |
| approval | Automatic     |          | Update approval method. Valid values are Automatic or Manual. |

> ℹ️ **NOTE**
>
> When `approval` is set to `Manual` the operator will be installed with `Automatic` approval and then after installation the approval will be updated to Manual.

### aap_ocp_install_controller keys

| Key Name      | Default Value | Required | Description                                     |
|---------------|:-------------:|:--------:|-------------------------------------------------|
| instance_name | None          | Yes      | Name of the controller instance to create       |
| replicas      | None          |          | How many replicas to create. Default: 1         |
| link_text     | None          |          | Text used for creating the OCP application link |

### aap_ocp_install_hub keys

| Key Name      | Default Value | Required | Description                                     |
|---------------|:-------------:|:--------:|-------------------------------------------------|
| instance_name | None          | Yes      | Name of the hub instance to create              |
| link_text     | None          |          | Text used for creating the OCP application link |

## Dependencies

This role depends on the redhat.openshift and kubernetes.core collections.

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yml
---
- name: Install AAP on OCP playbook
  hosts: localhost
  gather_facts: false

  vars:
    aap_ocp_install_ocp_connection:
      host: "https://api.crc.testing:6443"
      username: kubeadmin
      password: <PASSWORD>
      validate_certs: false
    aap_ocp_install_namespace: aap-test
    aap_ocp_install_operator:
      channel: "stable-2.2"
    aap_ocp_install_controller:
      instance_name: automationcontroller
    aap_ocp_install_hub:
      instance_name: automationhub

  roles:
    - redhat_cop.aap_utilities.aap_ocp_install
...
```

## License

MIT

## Author Information

Brant Evans
