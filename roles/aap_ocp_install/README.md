# aap_ocp_install

A role to install Ansible Automation Platform (AAP) 2.x on OpenShift using the operator.

## Requirements

This role requires the `kubernetes` (version 12.0.0 or later) Python module.
In addition the kubernetes.core and redhat.openshift Ansible collections are required.

## Role Variables

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

| Variable Name              | Required | Default Value | Description                                                            |
|----------------------------|:--------:|---------------|------------------------------------------------------------------------|
| aap_ocp_install_namespace  | Yes      | None          | Namespace to create operator, controller, and hub in                   |
| aap_ocp_install_connection | Yes      | None          | Dictionary containing keys defined in the `connection variables table` |
| aap_ocp_install_operator   | Yes*     | None          | Dictionary containing keys defined in the `operator variables table`   |
| aap_ocp_install_controller | Yes*     | None          | Dictionary containing keys defined in the `controller variables table` |
| aap_ocp_install_hub        | Yes*     | None          | Dictionary containing keys defined in the `hub variables table`        |

\* Variable and required keys must be defined when the type of tag is specified (e.g. `--tags controller` requires the aap_ocp_install_controller variable be defined).
If the variable is omitted the corresponding component will not be installed (e.g. if only aap_ocp_install_hub variable is defined then the operator and controller installation will be skipped)

### aap_ocp_install_connection keys

| Key Name       | Required | Default Value | Description                                                  |
|----------------|:--------:|---------------|--------------------------------------------------------------|
| host           | Yes      | None          | OCP cluster to create the AAP objects in                     |
| username       | Yes      | None          | Username to use for authenticating with OCP                  |
| password       | Yes      | None          | Password to use for authenticating with OCP                  |
| validate_certs |          | None          | Validate SSL certificates. Valid values are: `true`, `false` |

### aap_ocp_install_operator keys

| Key Name | Required | Default Value | Description                                                         |
|----------|:--------:|---------------|---------------------------------------------------------------------|
| channel  | Yes      | None          | Channel to subscribe (e.g. stable-2.2 or stable-2.2-cluster-scoped) |
| approval |          | Automatic     | Update approval method. Valid values are Automatic or Manual.       |

> ℹ️ **NOTE**
>
> When `approval` is set to `Manual` the operator will be installed with `Automatic` approval and then after installation the approval will be updated to Manual.

### aap_ocp_install_controller keys

| Key Name                     | Required | Default Value                           | Description                                                                                                            |
|------------------------------|:--------:|-----------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| instance_name                | Yes      | None                                    | Name of the controller instance to create                                                                              |
| namespace                    |          | None                                    | Name of the namespace to create the controller instance in. If not specified `aap_ocp_install_namespace` will be used. |
| admin_user                   |          | admin                                   | Username to use for the admin account                                                                                  |
| replicas                     |          | 1                                       | How many replicas to create.                                                                                           |
| garbage_collect_secrets      |          | false                                   | Whether or not to remove secrets upon instance removal                                                                 |
| image_pull_policy            |          | IfNotPresent                            | The image pull policy                                                                                                  |
| create_preload_data          |          | true                                    | Whether or not to preload data upon instance creation                                                                  |
| projects_persistence         |          | false                                   | Whether or not the /var/lib/projects directory will be persistent                                                      |
| projects_storage_size        |          | 8Gi                                     | Size of /var/lib/projects persistent volume claim (PVC)                                                                |
| link_text                    |          | Automation Controller (<INSTANCE_NAME>) | Text used for creating the OCP application link                                                                        |

| ### aap_ocp_install_hub keys |### aap_ocp_install_hub keys

| Key Name      | Required | Default Value                    | Description                                     |
|---------------|:--------:|----------------------------------|-------------------------------------------------|
| instance_name | Yes      | None                             | Name of the hub instance to create              |
| link_text     |          | Automation Hub (<INSTANCE_NAME>) | Text used for creating the OCP application link |

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

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author Information

Brant Evans
