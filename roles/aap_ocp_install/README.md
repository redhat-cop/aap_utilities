# infra.aap_utilities.aap_ocp_install

## Summary

Installs Ansible Automation Platform (AAP) on OpenShift using the operator: connects to the OpenShift cluster, optionally creates the target namespace, installs the operator Subscription, then deploys your chosen components. Before any cluster changes, the role runs pre-flight checks and fails with a list of validation errors if something is wrong.

For operator channels below 2.5, the role creates standalone `AutomationController`, `AutomationHub`, and `EDA` custom resources. For channels 2.5 and later, define `aap_ocp_install_platform` and set **`aap_ocp_install_platform.component_deployment`** to **`unified`** (default) to apply one `AnsibleAutomationPlatform` CR, or to **`individual`** to create standalone component CRs first and then link them from the platform CR. Optional `aap_ocp_install_controller`, `aap_ocp_install_hub`, and `aap_ocp_install_eda` dictionaries can be omitted when you are not configuring that component.

## Requirements

- **Ansible:** 2.15.0 or later.
- **Python:** the `kubernetes` library (version 12.0.0 or later).
- **Operator channel naming:** use a channel string that includes a `major.minor` version (for example `stable-2.4` or `stable-2.5-cluster-scoped`) so the role can tell pre-2.5 installs from 2.5+ platform installs.

## Dependencies

Install these Ansible collections on the control node:

- `kubernetes.core`.
- `redhat.openshift`.

## Role variables

The tables below list user-facing variables and nested keys.

| Variable Name                                  | Required | Default Value | Description                                                                                                              |
| :--------------------------------------------- | :------: | :------------ | :----------------------------------------------------------------------------------------------------------------------- |
| `aap_ocp_install_namespace`                    | Yes      |               | Namespace for the operator Subscription and CSV; default namespace for components when their own `namespace` is not set. |
| `aap_ocp_install_create_namespace`             | No       | `true`        | Whether to create `aap_ocp_install_namespace`. Valid values: `true`, `false`.                                            |
| `aap_ocp_install_namespace_manifest_overrides` | No       |               | YAML mapping merged into the generated `Namespace` CR when `aap_ocp_install_create_namespace` is true.                   |
| `aap_ocp_install_connection`                   | Yes      |               | Connection settings; see [Connection keys](#connection-keys-aap_ocp_install_connection).                                 |
| `aap_ocp_install_operator`                     | Yes\*    |               | Operator install; see [Operator keys](#operator-keys-aap_ocp_install_operator).                                          |
| `aap_ocp_install_controller`                   | Yes\*    |               | Controller; see [Controller keys](#controller-keys-aap_ocp_install_controller).                                          |
| `aap_ocp_install_hub`                          | Yes\*    |               | Hub; see [Hub keys](#hub-keys-aap_ocp_install_hub).                                                                      |
| `aap_ocp_install_eda`                          | Yes\*    |               | EDA; see [EDA keys](#eda-keys-aap_ocp_install_eda).                                                                      |
| `aap_ocp_install_platform`                     | Yes\*    |               | AAP 2.5+ Platform; see [Platform keys](#platform-keys-aap_ocp_install_platform).                                         |
| `aap_ocp_install_lightspeed`                   | No       |               | AAP 2.5+ Lightspeed; see [Lightspeed keys](#lightspeed-keys-aap_ocp_install_lightspeed).                                 |

\* **Pre-2.5 (operator channel below 2.5):** When you limit the play with `--tags`, define the variable dictionary for each component you run (for example `--tags controller` requires `aap_ocp_install_controller`). If a component variable is omitted, that component is not installed. If `aap_ocp_install_operator` is omitted, the operator is not installed.

\* **AAP 2.5+ (operator channel 2.5 or later):** Set `aap_ocp_install_platform` and choose **`component_deployment`** (see [Platform keys](#platform-keys-aap_ocp_install_platform)). With **`unified`** (default), the role applies one `AnsibleAutomationPlatform` CR with embedded component specs; use the `platform` tag and component dictionaries for `install` and overrides only (no standalone component CRs from this role). With **`individual`**, set `install` on each component you want, use the same namespace as the platform for those components, and run **`controller`**, **`hub`**, **`eda`**, and **`platform`** together so standalone CRs exist before the Platform CR links them by name (see Red Hat documentation for AAP custom resources).

`aap_ocp_install_platform` and `aap_ocp_install_lightspeed` apply only when the operator channel resolves to AAP 2.5 or later.

### Connection keys (`aap_ocp_install_connection`)

| Key Name         | Required | Default | Description                                                     |
| :--------------- | :------: | :------ | :-------------------------------------------------------------- |
| `host`           | Yes      |         | OpenShift API URL.                                              |
| `username`       | Yes\*    |         | User name for cluster login.                                    |
| `password`       | Yes\*    |         | Password for cluster login.                                     |
| `api_key`        | Yes\*    |         | API token (do not set `username` / `password` when using this). |
| `validate_certs` | No       |         | Whether to verify TLS. Valid values: `true`, `false`.           |

\* Either `api_key`, or both `username` and `password`, must be set.

### Operator keys (`aap_ocp_install_operator`)

| Key Name                           | Required | Default     | Description                                                                                                                              |
| :--------------------------------- | :------: | :---------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| `channel`                          | Yes\*    |             | Catalog channel (for example `stable-2.5-cluster-scoped`).                                                                               |
| `approval`                         | No       | `automatic` | Whether catalog updates install without extra steps (`automatic`) or stop for your approval before the operator install runs (`manual`). |
| `starting_csv`                     | No       |             | Pin the starting `ClusterServiceVersion` if needed.                                                                                      |
| `operatorgroup_create`             | No       | `true`      | Whether to create the `OperatorGroup`.                                                                                                   |
| `operatorgroup_manifest_overrides` | No       |             | YAML mapping merged into the generated `OperatorGroup`.                                                                                  |
| `subscription_manifest_overrides`  | No       |             | YAML mapping merged into the generated `Subscription`.                                                                                   |

\* If the channel indicates AAP 2.5 or above, the 2.5+ platform installation path is used when `aap_ocp_install_platform` is defined.

### Controller keys (`aap_ocp_install_controller`)

| Key Name                         | Required | Default Value                             | Description                                                                                                                                                                                                                                                                                                          |
| :------------------------------- | :------: | :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `instance_name`                  | Yes      |                                           | Controller custom resource name (required when this component is installed pre-2.5 or in **individual** 2.5+).                                                                                                                                                                                                       |
| `namespace`                      | No       |                                           | Namespace for the controller CR; defaults to `aap_ocp_install_namespace`.                                                                                                                                                                                                                                            |
| `namespace_manifest_overrides`   | No       |                                           | YAML mapping merged into the generated `Namespace` when `namespace` is set.                                                                                                                                                                                                                                          |
| `admin_user`                     | No       | `admin`                                   | Admin account user name.                                                                                                                                                                                                                                                                                             |
| `replicas`                       | No       | `1`                                       | Number of replicas.                                                                                                                                                                                                                                                                                                  |
| `garbage_collect_secrets`        | No       | `false`                                   | Remove secrets when the instance is removed.                                                                                                                                                                                                                                                                         |
| `image_pull_policy`              | No       | `IfNotPresent`                            | Container image pull policy.                                                                                                                                                                                                                                                                                         |
| `create_preload_data`            | No       | `true`                                    | Preload default data on create.                                                                                                                                                                                                                                                                                      |
| `projects_persistence`           | No       | `false`                                   | When `true`, persist `/var/lib/projects` on a PVC. The controller defaults to **ReadWriteMany** access so every replica can use the same directory; use a StorageClass that supports it, or set `projects_storage_access_mode` (and related fields) through `controller_manifest_overrides` if your storage differs. |
| `projects_storage_size`          | No       | `8Gi`                                     | PVC capacity for the persistent projects volume when `projects_persistence` is `true`.                                                                                                                                                                                                                               |
| `controller_manifest_overrides`  | No       |                                           | YAML merged into the `AutomationController` CR (pre-2.5 or **individual** standalone CR only). On **unified** 2.5+, merged into `spec.controller` on the `AnsibleAutomationPlatform` CR; not merged into the platform CR in **individual** mode (adoption uses `name` only).                                         |
| `consolelink_manifest_overrides` | No       |                                           | YAML merged into the controller `ConsoleLink` (pre-2.5 only; not used when `aap_ocp_install_platform` is used on AAP 2.5+).                                                                                                                                                                                          |
| `create_link`                    | No       | `true`                                    | Whether to create the OpenShift console `ConsoleLink`.                                                                                                                                                                                                                                                               |
| `link_text`                      | No       | `Automation Controller (<INSTANCE_NAME>)` | Console link label.                                                                                                                                                                                                                                                                                                  |
| `install`                        | \*       | `false`                                   | On AAP 2.5+, whether the controller component is enabled on the platform.                                                                                                                                                                                                                                            |

\* Used for AAP 2.5 or later only.

> **Note (AAP 2.5+):** On **unified** deployment, `namespace`, `instance_name`, and `link_text` are not used for gateway-managed controller layout; `controller_manifest_overrides` still merges into `spec.controller` on the `AnsibleAutomationPlatform` CR. On **individual** deployment, `controller_manifest_overrides` applies only to the standalone `AutomationController` CR; the platform CR keeps adoption-style `spec.controller` (`name` / `disabled`). Use `aap_ocp_install_platform.platform_manifest_overrides` to patch the platform CR itself. Per-component `consolelink_manifest_overrides` applies only pre-2.5; with `aap_ocp_install_platform` on 2.5+, only `aap_ocp_install_platform.consolelink_manifest_overrides` applies for the platform console link.

### Hub keys (`aap_ocp_install_hub`)

| Key Name                         | Required | Default Value                      | Description                                                                                                                                                                                                     |
| :------------------------------- | :------: | :--------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `instance_name`                  | Yes      |                                    | Hub custom resource name.                                                                                                                                                                                       |
| `namespace`                      | No       |                                    | Namespace for the hub CR; defaults to `aap_ocp_install_namespace`.                                                                                                                                              |
| `namespace_manifest_overrides`   | No       |                                    | YAML mapping merged into the generated `Namespace` when `namespace` is set.                                                                                                                                     |
| `hub_manifest_overrides`         | No       |                                    | YAML merged into the `AutomationHub` CR (pre-2.5 or **individual** standalone CR only). On **unified** 2.5+, merged into `spec.hub` on the platform CR; not merged into the platform CR in **individual** mode. |
| `consolelink_manifest_overrides` | No       |                                    | YAML merged into the hub `ConsoleLink` (pre-2.5 only; not used when `aap_ocp_install_platform` is used on AAP 2.5+).                                                                                            |
| `storage_type`                   | \*       | `file`                             | `file`, `S3` (capital **S3**), or `azure`.                                                                                                                                                                      |
| `file_storage_storage_class`     | \*       |                                    | StorageClass for file-backed hub (when `storage_type` is `file`).                                                                                                                                               |
| `file_storage_size`              | \*       | `10Gi`                             | PVC size for file-backed hub.                                                                                                                                                                                   |
| `object_storage_s3_secret`       | \*       |                                    | Secret name for S3-backed hub.                                                                                                                                                                                  |
| `object_storage_azure_secret`    | \*       |                                    | Secret name for Azure-backed hub.                                                                                                                                                                               |
| `create_link`                    | No       | `true`                             | Whether to create the hub `ConsoleLink`.                                                                                                                                                                        |
| `link_text`                      | No       | `Automation Hub (<INSTANCE_NAME>)` | Console link label.                                                                                                                                                                                             |
| `install`                        | \*       | `false`                            | On AAP 2.5+, whether the hub component is enabled on the platform.                                                                                                                                              |

\* Used for AAP 2.5 or later only.

> **Note (AAP 2.5+):** On **unified** deployment, `namespace`, `instance_name`, and `link_text` are not used for gateway-managed hub; `hub_manifest_overrides` merges into `spec.hub`. On **individual** deployment, `instance_name` and namespace (must match the platform namespace) apply to the standalone hub CR and to `spec.hub.name` on the platform CR.

### EDA keys (`aap_ocp_install_eda`)

| Key Name                         | Required | Default Value                      | Description                                                                                                                                                                                           |
| :------------------------------- | :------: | :--------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `instance_name`                  | Yes      |                                    | EDA custom resource name.                                                                                                                                                                             |
| `namespace`                      | No       |                                    | Namespace for the EDA CR; defaults to `aap_ocp_install_namespace`.                                                                                                                                    |
| `namespace_manifest_overrides`   | No       |                                    | YAML mapping merged into the generated `Namespace` when `namespace` is set.                                                                                                                           |
| `eda_manifest_overrides`         | No       |                                    | YAML merged into the `EDA` CR (pre-2.5 or **individual** standalone CR only). On **unified** 2.5+, merged into `spec.eda` on the platform CR; not merged into the platform CR in **individual** mode. |
| `consolelink_manifest_overrides` | No       |                                    | YAML merged into the EDA `ConsoleLink` (pre-2.5 only; not used when `aap_ocp_install_platform` is used on AAP 2.5+).                                                                                  |
| `create_link`                    | No       | `true`                             | Whether to create the EDA `ConsoleLink`.                                                                                                                                                              |
| `link_text`                      | No       | `EDA Controller (<INSTANCE_NAME>)` | Console link label.                                                                                                                                                                                   |
| `install`                        | \*       | `false`                            | On AAP 2.5+, whether the EDA component is enabled on the platform.                                                                                                                                    |

\* Used for AAP 2.5 or later only.

> **Note (AAP 2.5+):** On **unified** deployment, `namespace`, `instance_name`, and `link_text` are not used for gateway-managed EDA; `eda_manifest_overrides` merges into `spec.eda`. On **individual** deployment, `instance_name` and namespace (must match the platform namespace) apply to the standalone EDA CR and to `spec.eda.name` on the platform CR.

### Platform keys (`aap_ocp_install_platform`)

| Key Name                         | Required | Default Value       | Description                                                                                                                                                                                                                                                                                                      |
| :------------------------------- | :------: | :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `instance_name`                  | Yes      |                     | Name of the `AnsibleAutomationPlatform` CR.                                                                                                                                                                                                                                                                      |
| `namespace`                      | No       |                     | Namespace for the platform CR; defaults to `aap_ocp_install_namespace`.                                                                                                                                                                                                                                          |
| `component_deployment`           | No       | `unified`           | **`unified`:** one `AnsibleAutomationPlatform` CR with embedded `spec.controller` / `spec.hub` / `spec.eda`. **`individual`:** create standalone component CRs for each component with `install: true`, then apply the platform CR with `spec.<component>.name` pointing at those CRs (same namespace required). |
| `namespace_manifest_overrides`   | No       |                     | YAML mapping merged into the generated platform `Namespace` when `namespace` is set.                                                                                                                                                                                                                             |
| `platform_manifest_overrides`    | No       |                     | YAML mapping merged into the `AnsibleAutomationPlatform` CR.                                                                                                                                                                                                                                                     |
| `consolelink_manifest_overrides` | No       |                     | YAML mapping merged into the platform `ConsoleLink`.                                                                                                                                                                                                                                                             |
| `create_link`                    | No       | `true`              | Whether to create the platform `ConsoleLink`.                                                                                                                                                                                                                                                                    |
| `link_text`                      | No       | `(<INSTANCE_NAME>)` | Console link label for the platform.                                                                                                                                                                                                                                                                             |

> **Note:** These keys apply only when installing AAP 2.5 or later. With **`unified`**, `namespace`, `instance_name`, and `link_text` on component dictionaries do not drive gateway layout; overrides still merge as described under [AAP 2.5+ manifest merge order](#aap-25-manifest-merge-order). With **`individual`**, each installed component's `instance_name` and effective namespace must match the standalone CRs and the platform namespace (operator requirement).

#### AAP 2.5+ manifest merge order

For the `AnsibleAutomationPlatform` CR, overrides are applied in this order:

1. Build the base `AnsibleAutomationPlatform` manifest (component enable/disable and defaults).
2. Merge `aap_ocp_install_platform.platform_manifest_overrides`.
3. **`unified` mode only:** when the corresponding component dictionary is defined, merge component overrides into `spec` subtrees:
   - `aap_ocp_install_controller.controller_manifest_overrides` into `spec.controller`
   - `aap_ocp_install_hub.hub_manifest_overrides` into `spec.hub`
   - `aap_ocp_install_eda.eda_manifest_overrides` into `spec.eda`

Later merges win on conflicting keys within the same subtree. The platform `Namespace` (when `namespace` is set) and platform `ConsoleLink` each use their own `*_manifest_overrides` keys on `aap_ocp_install_platform`, as listed in the platform table.

With **`individual`** `component_deployment`, step 3 is skipped: the platform CR keeps adoption-style `spec.<component>` (`name` / `disabled` only). Component `*_manifest_overrides` apply only when creating the standalone component CRs. To adjust the platform CR under **individual**, use `platform_manifest_overrides` (use sparingly; see `oc explain ansibleautomationplatform.spec`).

For **unified** installs, fields must match what the operator expects under `spec.controller`, `spec.hub`, and `spec.eda` (see `oc explain ansibleautomationplatform.spec.<component>`). Overrides may be supplied in either shape:

- **Platform shape (recommended):** keys that belong directly under `spec.<component>` (for example next to `replicas` and `disabled`).
- **Standalone-CR shape (compatibility):** the same fields under a top-level `spec` key in the override mapping. On the platform path, that inner `spec` mapping is merged into `spec.<component>` instead of producing an invalid nested `spec.<component>.spec`.

### Lightspeed keys (`aap_ocp_install_lightspeed`)

| Key Name  | Required | Default | Description                                                         |
| :-------- | :------: | :------ | :------------------------------------------------------------------ |
| `install` | No       | `false` | When `true`, enables Lightspeed on the platform CR (AAP 2.5+ only). |

## Tags

| Tag          | What runs                                                                                                                                                                                                                                                                          |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `always`     | Pre-validation, OpenShift authentication and connection check, optional top-level namespace creation, and finalization. Always evaluated when the role runs.                                                                                                                       |
| `operator`   | Operator `OperatorGroup` and `Subscription` when `aap_ocp_install_operator` is defined.                                                                                                                                                                                            |
| `platform`   | AAP 2.5+ only: create or update the `AnsibleAutomationPlatform` CR when `aap_ocp_install_platform` is defined and the channel resolves to 2.5+. When tagging this role, include this tag for a full 2.5+ platform apply.                                                           |
| `controller` | Pre-2.5: standalone `AutomationController` when `aap_ocp_install_controller` is defined. AAP 2.5+ **unified:** skipped (settings feed the platform CR). AAP 2.5+ **individual:** runs when `install` is true for the controller; creates the standalone CR before the platform CR. |
| `hub`        | Same pattern as `controller` for Automation Hub.                                                                                                                                                                                                                                   |
| `eda`        | Same pattern as `controller` for EDA.                                                                                                                                                                                                                                              |

**Console links:** Per-component `ConsoleLink` objects are created for controller, hub, and EDA only when you are **not** on an AAP 2.5+ platform install (`aap_ocp_install_platform` defined with channel 2.5+). On 2.5+ platform installs, only the platform `ConsoleLink` is managed (when `aap_ocp_install_platform.create_link` is true). Tag the corresponding component or `platform` so those steps run when you use selective tags.

## Example playbooks

Pre-2.5 (for example channel `stable-2.2`):

```yaml
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

AAP 2.5+ (single namespace: omit `aap_ocp_install_platform.namespace` to use `aap_ocp_install_namespace`):

```yaml
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
      instance_name: aaptest
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

You may set `aap_ocp_install_platform.namespace` to a different valid namespace than `aap_ocp_install_namespace` if your layout requires it; the simple case is one shared namespace.

## License

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author information

- Brant Evans
- Derek Waters
- Andrew Block
