# aap_password_rotate

Rotates PostgreSQL database passwords and admin user passwords across all Ansible Automation Platform 2.7 components: Controller, Gateway, Event-Driven Ansible (EDA), and Automation Hub.

Supports both **podman** (containerised installer) and **operator** (Kubernetes/OpenShift) deployments, with both **installer-managed** and **external** databases.

> This role complements the `aap_secret_rotate` role, which handles SECRET_KEY (encryption key) rotation. These are two separate operations: password rotation changes authentication credentials, while secret rotation changes the keys used to encrypt database fields.

## Requirements

- Ansible >= 2.15
- AAP 2.7 (tested on 2.7.2 and 2.7.4)
- For podman: SSH access to the AAP host with podman permissions
- For operator: `kubectl` or `oc` with cluster-admin or namespace-scoped permissions
- For external DB: no special requirements (the role pauses or runs a user-provided hook)

## What Gets Rotated

### Database Passwords

| Component | DB User | Inventory Variable |
| --- | --- | --- |
| Controller | `awx` | `controller_pg_password` |
| Gateway | `gateway` | `gateway_pg_password` |
| EDA | `eda` | `eda_pg_password` |
| Hub | `pulp` | `hub_pg_password` |
| PostgreSQL superuser | `postgres` | `postgresql_admin_password` |

### Admin User Passwords

| Component | Method |
| --- | --- |
| Gateway | Django shell via `aap-gateway-manage shell` (`get_user_model().set_password`) |
| Controller | Django shell via `awx-manage shell` (`get_user_model().set_password`) |
| Hub | `pulpcore-manager reset-admin-password --password <pw>` |
| EDA | `aap-eda-manage update_password --username admin --password <pw>` |

> **Note:** Gateway and Controller use the Django ORM directly instead of the
> interactive `changepassword` command, which requires a TTY that is not
> available inside `podman exec` or `kubectl exec` contexts.

## How It Works

### Podman (via installer, recommended)

Per [KCS 7145426](https://access.redhat.com/solutions/7145426), the containerised installer natively supports password rotation:

1. If rotating the postgres superuser: `ALTER ROLE postgres` first
2. Update the inventory file with new `*_pg_password` values
3. Re-run the installer (handles ALTER ROLE for component users, updates podman secrets, restarts containers)
4. Rotate admin passwords via management commands

### Podman (manual, for external DB)

When the installer cannot reach the external database:

1. `ALTER ROLE` for each component DB user directly on the external PostgreSQL
2. Update podman secrets
3. Restart component containers
4. Rotate admin passwords via management commands

### Operator

1. `ALTER ROLE` for each component via exec into the PG pod (internal DB), or pause/hook for user action (external DB)
2. Patch Kubernetes `postgres-configuration` Secrets with new passwords
3. Rollout restart all component Deployments
4. Rotate admin passwords via exec into component pods
5. Patch `admin-password` Secrets to keep them in sync (per KCS 7144197)

## Usage

### Dry run (safe, read-only)

```yaml
- name: Dry run password rotation
  hosts: aap
  roles:
    - role: infra.aap_utilities.aap_password_rotate
      aap_password_rotate_dry_run: true
```

### Full rotation, podman (DB + admin passwords)

```yaml
- name: Rotate all passwords
  hosts: aap
  roles:
    - role: infra.aap_utilities.aap_password_rotate
      aap_password_rotate_deployment_type: podman
      aap_password_rotate_scope:
        - db
        - admin
      aap_password_rotate_include_postgres_admin: true
      aap_password_rotate_podman_use_installer: true
```

### DB passwords only, operator

```yaml
- name: Rotate DB passwords
  hosts: localhost
  connection: local
  roles:
    - role: infra.aap_utilities.aap_password_rotate
      aap_password_rotate_deployment_type: operator
      aap_password_rotate_namespace: my-aap
      aap_password_rotate_cr_name: my-aap
      aap_password_rotate_scope:
        - db
```

### Custom passwords

```yaml
- name: Rotate with specific passwords
  hosts: aap
  roles:
    - role: infra.aap_utilities.aap_password_rotate
      aap_password_rotate_deployment_type: podman
      aap_password_rotate_controller_pg_password: "MyNewCtrlPw-2026!"
      aap_password_rotate_gateway_pg_password: "MyNewGwPw-2026!"
      aap_password_rotate_eda_pg_password: "MyNewEdaPw-2026!"
      aap_password_rotate_hub_pg_password: "MyNewHubPw-2026!"
```

### External database (interactive)

When `external_db: true`, the role generates new passwords, writes `ALTER ROLE` SQL
to a helper file, and pauses for you to apply the SQL on your external database.
After you confirm, the role patches application secrets and restarts services.

```yaml
- name: Rotate with external DB (interactive pause)
  hosts: localhost
  connection: local
  roles:
    - role: infra.aap_utilities.aap_password_rotate
      aap_password_rotate_deployment_type: operator
      aap_password_rotate_namespace: my-aap
      aap_password_rotate_cr_name: my-aap
      aap_password_rotate_external_db: true
```

### External database (custom hook)

If you want to automate the external DB password change, provide your own tasks
file via `aap_password_rotate_external_db_tasks`. The role calls `include_tasks`
on it instead of pausing. Your tasks file receives these variables:

| Variable | Type | Description |
| --- | --- | --- |
| `aap_password_rotate_components` | list | Components being rotated (e.g. `[controller, hub, eda, gateway]`) |
| `__pw_db_users` | dict | Component to DB username (e.g. `{controller: automationcontroller}`) |
| `__pw_db_passwords` | dict | Component to new password |
| `__pw_postgres_admin_password` | str | New postgres superuser password (when `include_postgres_admin: true`) |

Example hook for AWS RDS:

```yaml
# my_rds_password_rotate.yml
- name: Update RDS password for each component
  amazon.aws.rds_instance:
    db_instance_identifier: "aap-{{ item }}"
    master_user_password: "{{ __pw_db_passwords[item] }}"
  loop: "{{ aap_password_rotate_components }}"
  no_log: true
```

Example hook using `psql` on a bastion host:

```yaml
# my_bastion_alter_role.yml
- name: ALTER ROLE via psql on bastion
  ansible.builtin.command:
    cmd: >-
      psql -h {{ my_pg_host }} -U postgres -c
      "ALTER ROLE {{ __pw_db_users[item] }} WITH PASSWORD '{{ __pw_db_passwords[item] }}';"
  loop: "{{ aap_password_rotate_components }}"
  delegate_to: bastion
  no_log: true
```

Playbook using the hook:

```yaml
- name: Rotate with external DB (automated via hook)
  hosts: localhost
  connection: local
  roles:
    - role: infra.aap_utilities.aap_password_rotate
      aap_password_rotate_deployment_type: operator
      aap_password_rotate_namespace: my-aap
      aap_password_rotate_cr_name: my-aap
      aap_password_rotate_external_db: true
      aap_password_rotate_external_db_tasks: "{{ playbook_dir }}/my_rds_password_rotate.yml"
```

## Role Variables

See [`defaults/main.yml`](defaults/main.yml) for all configurable variables and [`meta/argument_specs.yml`](meta/argument_specs.yml) for full documentation.

## Verification

After rotation, the role automatically verifies:

1. Gateway ping responds (HTTP 200)
2. Admin authentication works with the new password
3. Controller, Hub, and EDA APIs respond
4. DB connectivity with new passwords (podman only)

## Related

- `aap_secret_rotate`: Rotates SECRET_KEY (encryption keys) across AAP components
- [KCS 7145426](https://access.redhat.com/solutions/7145426): How to rotate PostgreSQL database passwords in AAP 2.7 Containerized
- [KCS 7100528](https://access.redhat.com/solutions/7100528): How to change PostgreSQL Database password of gateway
- [KCS 6746191](https://access.redhat.com/solutions/6746191): How to change Admin and PostgreSQL Database Passwords (AAP 2.4 and earlier)
- [KCS 7130353](https://access.redhat.com/solutions/7130353): How to change Automation Gateway Admin Password on AAP 2.5
- [KCS 7144197](https://access.redhat.com/solutions/7144197): How to find auto-generated passwords in AAP

## License

GPL-3.0-or-later

## Author

Alexey Masolov (@amasolov), Red Hat
