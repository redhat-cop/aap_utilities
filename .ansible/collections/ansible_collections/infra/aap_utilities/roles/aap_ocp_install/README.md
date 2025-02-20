# infra.aap_utilities.aap_ocp_install

A role to install Ansible Automation Platform (AAP) 2.x on OpenShift using the operator.

## Requirements

This role requires the `kubernetes` (version 12.0.0 or later) Python module.
In addition the kubernetes.core and redhat.openshift Ansible collections are required.

## Role Variables

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

| Variable Name                                | Required | Default Value | Description                                                                                  |
|----------------------------------------------|:--------:|---------------|----------------------------------------------------------------------------------------------|
| aap_ocp_install_namespace                    | Yes      | None          | Namespace to create operator, controller, and hub in                                         |
| aap_ocp_install_create_namespace             | No       | None          | Create the Namespace for the operator, controller and hub. Valid values are: `true`, `false` |
| aap_ocp_install_namespace_manifest_overrides | No       | None          | Namespace to create operator, controller, and hub in                                         |
| aap_ocp_install_connection                   | Yes      | None          | Dictionary containing keys defined in the `connection variables table`                       |
| aap_ocp_install_operator                     | Yes*     | None          | YAML Manifest to override the generated operator `Namespace` resource                        |
| aap_ocp_install_controller                   | Yes*     | None          | Dictionary containing keys defined in the `controller variables table`                       |
| aap_ocp_install_hub                          | Yes*     | None          | Dictionary containing keys defined in the `hub variables table`                              |
| aap_ocp_install_eda                          | Yes*     | None          | Dictionary containing keys defined in the `eda variables table`                              |
| aap_ocp_install_platform                     | Yes*     | None          | Dictionary containing keys defined in the `platform variables table`                         |
| aap_ocp_install_lightspeed                   | No       | None          | Dictionary containing keys defined in the `lightspeed variables table`                       |

\* Variable and required keys must be defined when the type of tag is specified (e.g. `--tags controller` requires the aap_ocp_install_controller variable be defined).
If the variable is omitted the corresponding component will not be installed (e.g. if only aap_ocp_install_hub variable is defined then the operator and controller installation will be skipped)

The aap_ocp_install_platform and aap_ocp_install_lightspeed Dictionaries are only used when installing AAP 2.5 or later.

### aap_ocp_install_connection keys

| Key Name       | Required | Default Value | Description                                                  |
|----------------|:--------:|---------------|--------------------------------------------------------------|
| host           | Yes      | None          | OCP cluster to create the AAP objects in                     |
| username       | Yes*     | None          | Username to use for authenticating with OCP                  |
| password       | Yes*     | None          | Password to use for authenticating with OCP                  |
| api_key        | Yes*     | None          | OCP API Token                                                |
| validate_certs |          | None          | Validate SSL certificates. Valid values are: `true`, `false` |

\* Either `api_key` or `username` and `password` can be specified.

### aap_ocp_install_operator keys

| Key Name                         | Required  | Default Value | Description                                                         |
|----------------------------------|:---------:|---------------|---------------------------------------------------------------------|
| channel                          | Yes*      | None          | Channel to subscribe (e.g. stable-2.2 or stable-2.2-cluster-scoped) |
| approval                         |           | Automatic     | Update approval method. Valid values are Automatic or Manual.       |
| operatorgroup_create             |           | true          | Create the `OperatorGroup` for the Operator                         |
| operatorgroup_manifest_overrides |           |               | YAML Manifest to override the generated `OperatorGroup` resource    |
| subscription_manifest_overrides  |           |               | YAML Manifest to override the generated `Subscription` resource     |

\* If the channel indicates version 2.5 or above of AAP, then the new AAP operator platform installation method will be used.

> ℹ️ **NOTE**
>
> When `approval` is set to `Manual` the operator will be installed with `Automatic` approval and then after installation the approval will be updated to Manual.

### aap_ocp_install_controller keys

| Key Name                       | Required | Default Value                           | Description                                                                                                            |
|--------------------------------|:--------:|-----------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| instance_name                  | Yes      | None                                    | Name of the controller instance to create                                                                              |
| namespace                      |          | None                                    | Name of the namespace to create the controller instance in. If not specified `aap_ocp_install_namespace` will be used. |
| namespace_manifest_overrides   |          | None                                    | YAML Manifest to override the generated `Namespace` resource for the controller if the `namespace` key is defined |
| admin_user                     |          | admin                                   | Username to use for the admin account                                                                                  |
| replicas                       |          | 1                                       | How many replicas to create.                                                                                           |
| garbage_collect_secrets        |          | false                                   | Whether or not to remove secrets upon instance removal                                                                 |
| image_pull_policy              |          | IfNotPresent                            | The image pull policy                                                                                                  |
| create_preload_data            |          | true                                    | Whether or not to preload data upon instance creation                                                                  |
| projects_persistence           |          | false                                   | Whether or not the /var/lib/projects directory will be persistent                                                      |
| projects_storage_size          |          | 8Gi                                     | Size of /var/lib/projects persistent volume claim (PVC)                                                                |
| link_text                      |          | Automation Controller (<INSTANCE_NAME>) | Text used for creating the OCP application link                                                                        |
| controller_manifest_overrides  |          | None                           | YAML Manifest to override the generated `AutomationController` resource link                                                                        |
| consolelink_manifest_overrides |          | None                           | YAML Manifest to override the generated `ConsoleLink` resource                                                                         |
| install                        | *        | false                                   | Whether or not to install the Controller platform component in AAP 2.5 or later    |

\* These settings are only used for installing AAP 2.5 or later.

> ℹ️ **NOTE**
>
> The namespace, instance_name and link_text values will be ignored when using the platform installation method.

### aap_ocp_install_hub keys

| Key Name                           | Required | Default Value                    | Description                                                       |
|------------------------------------|:--------:|----------------------------------|-------------------------------------------------------------------|
| instance_name                      | Yes      | None                             | Name of the hub instance to create                                |
| namespace                          |          | None                             | Name of the namespace to create the hub instance in. If not specified `aap_ocp_install_namespace` will be used. |
| namespace_manifest_overrides       |          | None                             | YAML Manifest to override the generated `Namespace` resource for the hub if the `namespace` key is defined |
| link_text                          |          | Automation Hub (<INSTANCE_NAME>) | Text used for creating the OCP application link                   |
| hub_manifest_overrides             |          | None                             | YAML Manifest to override the generated `AutomationHub` resource  |
| consolelink_manifest_overrides     |          | None                             | YAML Manifest to override the generated `ConsoleLink` resource    |
| storage_type                       | *        | file                             | Hub storage type (file, S3 or azure)                              |
| file_storage_storage_class         | *        | None                             | OpenShift StorageClass to use for file storage type for hub       |
| file_storage_size                  | *        | 10Gi                             | Storage size for file storage type for hub                        |
| object_storage_s3_secret           | *        | None                             | Name of an OpenShift Secret used to access S3 storage for hub     |
| object_storage_azure_secret        | *        | None                             | Name of an OpenShift Secret used to access Azure storage for hub  |
| install                            | *        | false                            | Whether or not to install the Hub platform component in AAP 2.5 or later    |

\* These settings are only used for installing AAP 2.5 or later.

> ℹ️ **NOTE**
>
> The namespace, instance_name and link_text values will be ignored when using the platform installation method.

### aap_ocp_install_eda keys

| Key Name      | Required | Default Value                    | Description                                     |
|------------------------------------|:--------:|----------------------------------|-------------------------------------------------|
| instance_name                      | Yes      | None                             | Name of the EDA instance to create              |
| namespace                          |          | None                             | Name of the namespace to create the EDA instance in. If not specified `aap_ocp_install_namespace` will be used. |
| namespace_manifest_overrides       |          | None                             | YAML Manifest to override the generated `Namespace` resource for the EDA if the `namespace` key is defined |
| link_text                          |          | EDA Controller (<INSTANCE_NAME>) | Text used for creating the OCP application link |
| eda_manifest_overrides             |          | None                             | YAML Manifest to override the generated `EDA` resource  |
| consolelink_manifest_overrides     |          | None                             | YAML Manifest to override the generated `ConsoleLink` resource    |
| install                            | *        | false                            | Whether or not to install the EDA platform component in AAP 2.5 or later    |

\* These settings are only used for installing AAP 2.5 or later.

> ℹ️ **NOTE**
>
> The namespace, instance_name and link_text values will be ignored when using the platform installation method.

### aap_ocp_install_platform keys

| Key Name      | Required | Default Value                    | Description                                     |
|---------------|:--------:|----------------------------------|-------------------------------------------------|
| instance_name | Yes      | None                             | Name of the AAP Platform instance to create     |
| namespace     |          | None                             | Name of the namespace to create the AAP platform instance in. If not specified `aap_ocp_install_namespace` will be used. |
| link_text     |          | (<INSTANCE_NAME>)                | Text used for creating the platform OCP application link |

> ℹ️ **NOTE**
>
> These settings are only used when installing AAP 2.5 or later. namespace, instance_name and link_text values for individual components (hub, controller, eda) will be ignored when using the platform installation method.

### aap_ocp_install_lightspeed keys

| Key Name      | Required | Default Value                    | Description                                     |
|---------------|:--------:|----------------------------------|-------------------------------------------------|
| install       | No       | false                            | Whether or not to install the platform Lightspeed components  |

> ℹ️ **NOTE**
>
> These settings are only used when installing AAP 2.5 or later.

## Dependencies

This role depends on the redhat.openshift and kubernetes.core collections.

## Example Playbook

The following playbook will install AAP versions 2.4 and earlier:

```yml
---
- name: Install AAP on OCP playbook
  hosts: localhost
  gather_facts: false

  vars:
    aap_ocp_install_connection:
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
    aap_ocp_install_eda:
      instance_name: edacontroller

  roles:
    - infra.aap_utilities.aap_ocp_install
...
```

The following playbook will install AAP versions 2.5 and later:

```yml
---
- name: Install AAP on OCP playbook 2.5+
  hosts: localhost
  gather_facts: false

  vars:
    aap_ocp_install_connection:
      host: "https://api.crc.testing:6443"
      username: kubeadmin
      password: <PASSWORD>
      validate_certs: false
    aap_ocp_install_namespace: aap-test
    aap_ocp_install_operator:
      channel: "stable-2.5-cluster-scoped"
    aap_ocp_install_platform:
      instance_name: automationcontroller
      namespace: aap-platform
    aap_ocp_install_controller:
      install: true
    aap_ocp_install_eda:
      install: true
    aap_ocp_install_hub:
      install: true
      storage_type: file
      file_storage_storage_class: my-filestore-rwx
      file_storage_size: 30Gi

  roles:
    - infra.aap_utilities.aap_ocp_install
...
```

## License

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author Information

* Brant Evans
* Derek Waters
* Andrew Block
