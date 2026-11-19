# aap_secret_rotate

Rotate database encryption secret keys across all Ansible Automation Platform 2.7 components. Supports both **podman** (containerised installer) and **operator** (Kubernetes/OpenShift) deployments.

## Components

| Component | Management Command | Key Source |
| --- | --- | --- |
| Controller | `awx-manage regenerate_secret_key --use-custom-key` | `TOWER_SECRET_KEY` env var |
| Gateway | `aap-gateway-manage rotate_secret_key --use-custom-key` | `GATEWAY_SECRET_KEY` env var |
| EDA | `aap-eda-manage rotate_db_encryption_key --use-custom-key` | `EDA_DB_ROTATION_KEY` env var |
| Hub | `pulpcore-manager rotate-db-key` | Multi-key file (Fernet) |

## Prerequisites

1. **Database backup**: Always back up the AAP database before rotating keys. This role does **not** perform database backups. Use the AAP installer's `backup.yml` playbook (podman) or the `AnsibleAutomationPlatformBackup` CR (operator).

2. **Podman deployments**: SSH access to the AAP host with permissions to manage podman containers and secrets.

3. **Operator deployments**: `kubectl` or `oc` (or any compatible CLI) configured with access to the AAP namespace. The role auto-detects which binary is available. Required permissions:
   - `Secret`: get, list, create, update, patch
   - `Job`: create, get, list, delete
   - `Deployment`: get, list
   - `AnsibleAutomationPlatform` CR: get, patch
   - `ExternalSecret` (if ESO-managed): get, list, patch
   - `Application` (if ArgoCD-managed): get, list, patch

## Variables

### General

| Variable | Default | Description |
| --- | --- | --- |
| `aap_secret_rotate_components` | `[controller, hub, eda, gateway]` | Components to rotate, in order. Gateway should be last (session invalidation). |
| `aap_secret_rotate_deployment_type` | `""` (auto-detect) | `podman` or `operator`. Auto-detected if empty. |
| `aap_secret_rotate_dry_run` | `false` | Report what would change without writing. Components that support native `--dry-run` (Gateway, EDA) will use it. |
| `aap_secret_rotate_backup_dir` | `{{ playbook_dir }}/secret_backups/{{ date }}` | Directory on the control node for key backups. |

### Custom Keys

If left empty, a new Fernet-compatible key is auto-generated per component.

| Variable | Default | Description |
| --- | --- | --- |
| `aap_secret_rotate_controller_key` | `""` | Custom key for Controller |
| `aap_secret_rotate_gateway_key` | `""` | Custom key for Gateway |
| `aap_secret_rotate_eda_key` | `""` | Custom key for EDA |
| `aap_secret_rotate_hub_key` | `""` | Custom key for Hub |

### Operator-specific

| Variable | Default | Description |
| --- | --- | --- |
| `aap_secret_rotate_namespace` | `aap` | Kubernetes namespace containing the AAP workloads |
| `aap_secret_rotate_operator_namespace` | `""` (same as workload NS) | Namespace where AAP component operator Deployments run. Set when operators are installed separately (for example `aap-operators`) from the workloads. |
| `aap_secret_rotate_cr_name` | `aap` | Name of the `AnsibleAutomationPlatform` CR |
| `aap_secret_rotate_idle_timeout` | `300` | Seconds to wait for pods to terminate after idling |
| `aap_secret_rotate_rollout_timeout` | `300` | Seconds to wait for pods to become ready after un-idling |
| `aap_secret_rotate_kubectl_binary` | `""` (auto-detect) | Path to kubectl-compatible CLI. Auto-detected: tries `kubectl`, falls back to `oc`. |

### External Secrets Operator (ESO)

| Variable | Default | Description |
| --- | --- | --- |
| `aap_secret_rotate_eso_managed` | `""` (auto-detect) | Whether secrets are managed by ESO. Auto-detected by looking for `ExternalSecret` resources in the AAP namespace. |
| `aap_secret_rotate_eso_resume_after` | `false` | Resume ESO reconciliation after rotation. If `false`, ExternalSecrets stay paused until the external store is updated manually. |

### ArgoCD / GitOps

| Variable | Default | Description |
| --- | --- | --- |
| `aap_secret_rotate_argocd_managed` | `""` (auto-detect) | Whether the deployment is managed by ArgoCD. Auto-detected by looking for an Application targeting the AAP namespace. |
| `aap_secret_rotate_argocd_app_name` | `""` (auto-detect) | ArgoCD Application name. Auto-detected if empty. |
| `aap_secret_rotate_argocd_app_namespace` | `""` (auto-detect) | Namespace where the ArgoCD Application CR lives. Auto-detected by cluster-wide search. Override if RBAC restricts cluster-wide Application listing. |
| `aap_secret_rotate_argocd_resume_after` | `false` | Resume ArgoCD auto-sync after rotation. If `false`, the Application stays suspended until the Git repo is updated. |

### Podman-specific

| Variable | Default | Description |
| --- | --- | --- |
| `aap_secret_rotate_controller_container` | `automation-controller-task` | Controller container name |
| `aap_secret_rotate_gateway_container` | `automation-gateway` | Gateway container name |
| `aap_secret_rotate_eda_container` | `automation-eda-api` | EDA container name |
| `aap_secret_rotate_hub_container` | `automation-hub-api` | Hub container name |

## Usage

### Dry Run (recommended first step)

```yaml
- name: AAP Secret Key Rotation (dry run)
  hosts: aap
  roles:
    - role: infra.aap_utilities.aap_secret_rotate
      aap_secret_rotate_dry_run: true
```

### Full Rotation (podman)

```yaml
- name: AAP Secret Key Rotation
  hosts: aap
  become: true
  roles:
    - role: infra.aap_utilities.aap_secret_rotate
      aap_secret_rotate_deployment_type: podman
```

### Full Rotation (operator on any Kubernetes)

```yaml
- name: AAP Secret Key Rotation
  hosts: localhost
  connection: local
  roles:
    - role: infra.aap_utilities.aap_secret_rotate
      aap_secret_rotate_deployment_type: operator
      aap_secret_rotate_namespace: my-aap
      aap_secret_rotate_cr_name: my-aap
```

When AAP operators run in a different namespace from the workloads:

```yaml
- name: AAP Secret Key Rotation (split operator namespace)
  hosts: localhost
  connection: local
  roles:
    - role: infra.aap_utilities.aap_secret_rotate
      aap_secret_rotate_deployment_type: operator
      aap_secret_rotate_namespace: aap
      aap_secret_rotate_operator_namespace: aap-operators
```

### Operator with ESO and ArgoCD (enterprise GitOps)

```yaml
- name: AAP Secret Key Rotation (GitOps environment)
  hosts: localhost
  connection: local
  roles:
    - role: infra.aap_utilities.aap_secret_rotate
      aap_secret_rotate_deployment_type: operator
      aap_secret_rotate_namespace: aap-prod
      aap_secret_rotate_cr_name: aap
      # ESO and ArgoCD (including the Application namespace) are
      # auto-detected; override only if cluster-wide listing is restricted:
      # aap_secret_rotate_eso_managed: true
      # aap_secret_rotate_argocd_managed: true
      # aap_secret_rotate_argocd_app_name: aap-prod
      # aap_secret_rotate_argocd_app_namespace: argocd
```

After the playbook completes, you will see action-required messages telling you to:

1. Update the new key values in your external secret store (Vault, AWS SM, etc.)
2. Update your Git repository with the new secret references (SealedSecrets, SOPS, etc.)
3. Resume ESO reconciliation and ArgoCD auto-sync

### Single Component

```yaml
- name: Rotate Controller key only
  hosts: aap
  become: true
  roles:
    - role: infra.aap_utilities.aap_secret_rotate
      aap_secret_rotate_components:
        - controller
```

## How It Works

### Lifecycle

1. **Preflight**: Detect deployment type, validate components, detect ESO/ArgoCD
2. **Backup**: Read and save current keys to the control node
3. **Generate**: Create new Fernet-compatible keys (or use provided custom keys)
4. **Pause GitOps** (operator only): Suspend ArgoCD auto-sync, pause ESO reconciliation
5. **Idle/Stop**: For operator, idle the entire platform. For podman, stop containers per component.
6. **Rotate**: Run each component's management command with the new key
7. **Write**: Update the secret storage (podman secret or K8s Secret) with the new key
8. **Un-idle/Start**: Bring services back up
9. **Resume GitOps** (optional): Resume ESO/ArgoCD if configured
10. **Verify**: Check platform health, display post-rotation action items

### Hub's Multi-Key File

Hub uses a different mechanism from the other components. Its `DB_ENCRYPTION_KEY` is a Fernet symmetric key stored in a file that supports multiple keys (one per line). The first key encrypts new data, all keys can decrypt existing data.

The rotation process:

1. Write multi-key file: new key on line 1, old key on line 2
2. Run `pulpcore-manager rotate-db-key` to re-encrypt all data with the new key
3. Write final file with only the new key

### Operator Deployment Flow

For operator deployments, the role idles the entire `AnsibleAutomationPlatform` CR once (sets `spec.idle_aap: true`), runs rotation Jobs for each component, patches the K8s Secrets, then un-idles. This avoids multiple scale-down/up cycles.

### Enterprise GitOps (ESO + ArgoCD)

Many enterprise customers manage AAP operator deployments using a GitOps pattern:

- **External Secrets Operator (ESO)** syncs secret values from an external store (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, etc.) into Kubernetes Secrets.
- **ArgoCD** manages the AAP CR and namespace resources declaratively from a Git repository.

The role handles this by:

1. **Auto-detecting** ESO-managed secrets (looks for `ExternalSecret` resources) and ArgoCD-managed Applications (looks for `Application` resources targeting the AAP namespace) during preflight.
2. **Pausing ESO reconciliation** by annotating `ExternalSecret` resources with `reconcile.external-secrets.io/disabled: "true"`, preventing ESO from overwriting the rotated key values.
3. **Suspending ArgoCD auto-sync** by removing `spec.syncPolicy.automated` from the Application, preventing ArgoCD from reverting the `idle_aap` patch or secret changes.
4. **Displaying clear action items** after rotation, telling the operator exactly what needs updating in the external secret store and Git repo.
5. **Optionally resuming** ESO and ArgoCD if `aap_secret_rotate_eso_resume_after` or `aap_secret_rotate_argocd_resume_after` are set to `true`. By default both stay paused, which is the safe option: it ensures the operator updates the source of truth before the controllers resume.

### Podman Deployment Flow

For podman deployments, each component's containers are stopped individually, the management command is executed in the container, the podman secret is replaced, and containers are restarted.

## Supported Versions

- AAP 2.7 (all components)
- EDA rotation also available in AAP 2.6.20260715+

## Backups

Current key values are saved to `{{ aap_secret_rotate_backup_dir }}/aap_secret_keys.bak` on the control node before any rotation occurs. Store this file securely; it contains the keys needed to decrypt the database if rollback is necessary.

## Licence

GPL-3.0-or-later
