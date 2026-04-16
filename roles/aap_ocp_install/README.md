# infra.aap_utilities.aap_ocp_install

A role to install Ansible Automation Platform (AAP) 2.x on OpenShift using the operator.

## Requirements

- **Ansible:** 2.15.0 or later.
- **Python:** the `kubernetes` module (version 12.0.0 or later).
- **Ansible collections:** `kubernetes.core` and `redhat.openshift`.

## Tags

This role defines the following tags:

| Tag | Purpose |
| --- | ------- |
| `always` | OpenShift initialization and finalization (authentication, validation, namespace setup where applicable, and finalization). Runs whenever the role runs. |
| `operator` | Install the AAP operator when `aap_ocp_install_operator` is defined. |
| `platform` | AAP 2.5+ only: build and apply the `AnsibleAutomationPlatform` CR when `aap_ocp_install_platform` is defined and the operator channel resolves to 2.5 or later. |
| `controller` | Pre-2.5 only: standalone Automation Controller install when `aap_ocp_install_controller` is defined and the channel is below 2.5. On 2.5+, this path is skipped; use `platform` and `aap_ocp_install_platform` plus optional controller overrides. |
| `hub` | Pre-2.5 only: standalone Hub install. On 2.5+, skipped in favor of the platform path; see `platform` and hub overrides. |
| `eda` | Pre-2.5 only: standalone EDA install. On 2.5+, skipped in favor of the platform path; see `platform` and EDA overrides. |

## Role Variables

The tables below document user-facing variables and nested keys.

| Variable Name                                  | Required   | Default Value   | Description                                                                                                |
| ---------------------------------------------- | :--------: | --------------- | ----------------------------------------------------------------------------------------------             |
| aap_ocp_install_namespace                      | Yes        |                 | Namespace to create operator, controller, and hub in                                                       |
| aap_ocp_install_create_namespace               | No         | true            | Create the Namespace for the operator, controller and hub. Valid values are: `true`, `false`               |
| aap_ocp_install_namespace_manifest_overrides   | No         |                 | YAML mapping merged into the generated default `Namespace` when `aap_ocp_install_create_namespace` is true |
| aap_ocp_install_connection                     | Yes        |                 | Dictionary containing keys defined in the `connection variables table`                                     |
| aap_ocp_install_operator                       | Yes*       |                 | Dictionary containing keys defined in the `operator variables table`                                       |
| aap_ocp_install_controller                     | Yes*       |                 | Dictionary containing keys defined in the `controller variables table`                                     |
| aap_ocp_install_hub                            | Yes*       |                 | Dictionary containing keys defined in the `hub variables table`                                            |
| aap_ocp_install_eda                            | Yes*       |                 | Dictionary containing keys defined in the `eda variables table`                                            |
| aap_ocp_install_platform                       | Yes*       |                 | Dictionary containing keys defined in the `platform variables table`                                       |
| aap_ocp_install_lightspeed                     | No         |                 | Dictionary containing keys defined in the `lightspeed variables table`                                     |

\* **Pre-2.5 (operator channel below 2.5):** When you limit the play with `--tags`, define the variable dictionary for each component you run (for example `--tags controller` requires `aap_ocp_install_controller`). If a component's variable is omitted, that component is not installed. If `aap_ocp_install_operator` is omitted, the operator is not installed.

\* **AAP 2.5+ (operator channel 2.5 or later):** The unified install runs under the `platform` tag. The `controller`, `hub`, and `eda` tags do **not** run the standalone component installers; set `aap_ocp_install_platform` and use `aap_ocp_install_controller`, `aap_ocp_install_hub`, and `aap_ocp_install_eda` for `install` flags and manifest overrides as documented below.

`aap_ocp_install_platform` and `aap_ocp_install_lightspeed` apply only when installing AAP 2.5 or later.

### aap_ocp_install_connection keys

| Key Name       | Required | Default Value | Description                                                  |
|----------------|:--------:|---------------|--------------------------------------------------------------|
| host           |   Yes    |               | OCP cluster to create the AAP objects in                     |
| username       |   Yes*   |               | Username to use for authenticating with OCP                  |
| password       |   Yes*   |               | Password to use for authenticating with OCP                  |
| api_key        |   Yes*   |               | OCP API Token                                                |
| validate_certs |          |               | Validate SSL certificates. Valid values are: `true`, `false` |

\* Either `api_key` or `username` and `password` can be specified.

### aap_ocp_install_operator keys

| Key Name                         | Required | Default Value | Description                                                                    |
|----------------------------------|:--------:|---------------|--------------------------------------------------------------------------------|
| channel                          |   Yes*   |               | Channel to subscribe (e.g. stable-2.5 or stable-2.5-cluster-scoped)            |
| approval                         |          | Automatic     | Update approval method. Valid values are Automatic or Manual.                  |
| starting_csv                     |          |               | Set the starting ClusterServiceVersion (e.g. aap-operator.v2.5.0-0.1728520175) |
| operatorgroup_create             |          | true          | Create the `OperatorGroup` for the Operator                                    |
| operatorgroup_manifest_overrides |          |               | YAML Manifest to override the generated `OperatorGroup` resource               |
| subscription_manifest_overrides  |          |               | YAML Manifest to override the generated `Subscription` resource                |

\* If the channel indicates version 2.5 or above of AAP, then the AAP operator platform installation method will be used.

### aap_ocp_install_controller keys

| Key Name                         | Required   | Default Value                             | Description                                                                                                                             |
| -------------------------------- | :--------: | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------                |
| instance_name                    | Yes        |                                           | Name of the controller instance to create                                                                                               |
| namespace                        |            |                                           | Name of the namespace to create the controller instance in. If not specified `aap_ocp_install_namespace` will be used.                  |
| namespace_manifest_overrides     |            |                                           | YAML Manifest to override the generated `Namespace` resource for the controller if the `namespace` key is defined                       |
| admin_user                       |            | admin                                     | Username to use for the admin account                                                                                                   |
| replicas                         |            | 1                                         | How many replicas to create.                                                                                                            |
| garbage_collect_secrets          |            | false                                     | Whether or not to remove secrets upon instance removal                                                                                  |
| image_pull_policy                |            | IfNotPresent                              | The image pull policy                                                                                                                   |
| create_preload_data              |            | true                                      | Whether or not to preload data upon instance creation                                                                                   |
| projects_persistence             |            | false                                     | Whether or not the /var/lib/projects directory will be persistent                                                                       |
| projects_storage_size            |            | 8Gi                                       | Size of /var/lib/projects persistent volume claim (PVC)                                                                                 |
| controller_manifest_overrides    |            |                                           | YAML mapping merged into the `AutomationController` CR (pre-2.5) or into `spec.controller` on the `AnsibleAutomationPlatform` CR (2.5+) |
| consolelink_manifest_overrides   |            |                                           | YAML mapping merged into the generated `ConsoleLink` for the controller (pre-2.5 only; not used on the platform install path)           |
| create_link                      |            | true                                      | Create an OCP console application link (i.e. apply ConsoleLink CR)                                                                      |
| link_text                        |            | Automation Controller (<INSTANCE_NAME>)   | Text used when creating the OCP console application link                                                                                |
| install                          | *          | false                                     | Whether or not to install the Controller platform component in AAP 2.5 or later                                                         |

\* These settings are only used for installing AAP 2.5 or later.

> ℹ️ **NOTE**
>
> The namespace, instance_name and link_text values will be ignored when using the platform installation method. On AAP 2.5+, `controller_manifest_overrides` is merged into `spec.controller` on the `AnsibleAutomationPlatform` CR. Per-component `consolelink_manifest_overrides` is only used on the pre-2.5 install path; on 2.5+ use `aap_ocp_install_platform.consolelink_manifest_overrides` for the platform ConsoleLink.

### aap_ocp_install_hub keys

| Key Name                         | Required   | Default Value                      | Description                                                                                                               |
| -------------------------------- | :--------: | ---------------------------------- | -----------------------------------------------------------------------------------------------------------------         |
| instance_name                    | Yes        |                                    | Name of the hub instance to create                                                                                        |
| namespace                        |            |                                    | Name of the namespace to create the hub instance in. If not specified `aap_ocp_install_namespace` will be used.           |
| namespace_manifest_overrides     |            |                                    | YAML Manifest to override the generated `Namespace` resource for the hub if the `namespace` key is defined                |
| hub_manifest_overrides           |            |                                    | YAML mapping merged into the `AutomationHub` CR (pre-2.5) or into `spec.hub` on the `AnsibleAutomationPlatform` CR (2.5+) |
| consolelink_manifest_overrides   |            |                                    | YAML mapping merged into the generated `ConsoleLink` for the hub (pre-2.5 only; not used on the platform install path)    |
| storage_type                     | *          | file                               | Hub storage type: `file`, `S3` (capital **S3**), or `azure`                                                               |
| file_storage_storage_class       | *          |                                    | OpenShift StorageClass to use for file storage type for hub                                                               |
| file_storage_size                | *          | 10Gi                               | Storage size for file storage type for hub                                                                                |
| object_storage_s3_secret         | *          |                                    | Name of an OpenShift Secret used to access S3 storage for hub                                                             |
| object_storage_azure_secret      | *          |                                    | Name of an OpenShift Secret used to access Azure storage for hub                                                          |
| create_link                      |            | true                               | Create an OCP console application link (i.e. apply ConsoleLink CR)                                                        |
| link_text                        |            | Automation Hub (<INSTANCE_NAME>)   | Text used for creating the OCP application link                                                                           |
| install                          | *          | false                              | Whether or not to install the Hub platform component in AAP 2.5 or later                                                  |

\* These settings are only used for installing AAP 2.5 or later.

> ℹ️ **NOTE**
>
> The namespace, instance_name and link_text values will be ignored when using the platform installation method. On AAP 2.5+, `hub_manifest_overrides` is merged into `spec.hub` on the `AnsibleAutomationPlatform` CR.

### aap_ocp_install_eda keys

| Key Name                         | Required   | Default Value                      | Description                                                                                                        |
| -------------------------------- | :--------: | ---------------------------------- | -----------------------------------------------------------------------------------------------------------------  |
| instance_name                    | Yes        |                                    | Name of the EDA instance to create                                                                                 |
| namespace                        |            |                                    | Name of the namespace to create the EDA instance in. If not specified `aap_ocp_install_namespace` will be used.    |
| namespace_manifest_overrides     |            |                                    | YAML Manifest to override the generated `Namespace` resource for the EDA if the `namespace` key is defined         |
| eda_manifest_overrides           |            |                                    | YAML mapping merged into the `EDA` CR (pre-2.5) or into `spec.eda` on the `AnsibleAutomationPlatform` CR (2.5+)    |
| consolelink_manifest_overrides   |            |                                    | YAML mapping merged into the generated `ConsoleLink` for EDA (pre-2.5 only; not used on the platform install path) |
| create_link                      |            | true                               | Create an OCP console application link (i.e. apply ConsoleLink CR)                                                 |
| link_text                        |            | EDA Controller (<INSTANCE_NAME>)   | Text used for creating the OCP application link                                                                    |
| install                          | *          | false                              | Whether or not to install the EDA platform component in AAP 2.5 or later                                           |

\* These settings are only used for installing AAP 2.5 or later.

> ℹ️ **NOTE**
>
> The namespace, instance_name and link_text values will be ignored when using the platform installation method. On AAP 2.5+, `eda_manifest_overrides` is merged into `spec.eda` on the `AnsibleAutomationPlatform` CR.

### aap_ocp_install_platform keys

| Key Name                         | Required   | Default Value       | Description                                                                                                                |
| -------------------------------- | :--------: | ------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| instance_name                    | Yes        |                     | Name of the AAP Platform instance to create                                                                                |
| namespace                        |            |                     | Name of the namespace to create the AAP platform instance in. If not specified `aap_ocp_install_namespace` will be used.   |
| namespace_manifest_overrides     |            |                     | YAML mapping merged into the generated `Namespace` resource when `namespace` is set                                        |
| platform_manifest_overrides      |            |                     | YAML mapping deep-merged into the generated `AnsibleAutomationPlatform` CR (after rendering the template)                  |
| consolelink_manifest_overrides   |            |                     | YAML mapping merged into the generated platform `ConsoleLink` resource                                                     |
| create_link                      |            | true                | Create an OCP console application link (i.e. apply ConsoleLink CR)                                                         |
| link_text                        |            | (<INSTANCE_NAME>)   | Text used for creating the platform OCP application link                                                                   |

> ℹ️ **NOTE**
>
> These settings are only used when installing AAP 2.5 or later. Namespace, instance_name and link_text values for individual components (hub, controller, eda) are ignored when using the platform installation method; optional `controller_manifest_overrides`, `hub_manifest_overrides`, and `eda_manifest_overrides` on those component dictionaries are still merged into the unified CR (see **AAP 2.5+ manifest merge order** below).

#### AAP 2.5+ manifest merge order

For the `AnsibleAutomationPlatform` CR, overrides are applied in this order:

1. Render the `AnsibleAutomationPlatform` manifest from the role template.
2. Deep-merge `aap_ocp_install_platform.platform_manifest_overrides` (optional cross-cutting patch).
3. Deep-merge component-specific mappings into `spec` subtrees when the corresponding variable dictionary is defined:
   - `aap_ocp_install_controller.controller_manifest_overrides` into `spec.controller`
   - `aap_ocp_install_hub.hub_manifest_overrides` into `spec.hub`
   - `aap_ocp_install_eda.eda_manifest_overrides` into `spec.eda`

Later steps win on conflicting keys within the same subtree. The platform `Namespace` (when `namespace` is set) and platform `ConsoleLink` each support their own `*_manifest_overrides` keys on `aap_ocp_install_platform` as described in the table above.

For the unified `AnsibleAutomationPlatform` CR, component settings must appear under `spec.controller`, `spec.hub`, and `spec.eda` at the same nesting level the operator expects (see `oc explain ansibleautomationplatform.spec.<component>`). You may supply overrides in either form:

- **Platform shape (recommended):** keys that belong directly under `spec.<component>` (for example `postgres_configuration_secret` next to `replicas` and `disabled`).
- **Standalone-CR shape (compatibility):** the same fields nested under a top-level `spec` key in the override mapping, as used when merging into a standalone `AutomationController` / `AutomationHub` / EDA CR. On the platform install path, that inner `spec` mapping is merged into `spec.<component>` instead of creating an invalid nested `spec.<component>.spec`.

### aap_ocp_install_lightspeed keys

| Key Name | Required | Default Value | Description                                                  |
|----------|:--------:|---------------|--------------------------------------------------------------|
| install  | No       | false         | Whether or not to install the platform Lightspeed components |

> ℹ️ **NOTE**
>
> These settings are only used when installing AAP 2.5 or later.

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
```

## License

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author Information

- Brant Evans
- Derek Waters
- Andrew Block
