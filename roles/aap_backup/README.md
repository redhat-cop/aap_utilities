# infra.aap\_utilities.backup

Ansible role to backup Ansible Automation Platform.

## Requirements

None

## Role Variables

Available variables are listed below, along with default values defined (see defaults/main.yml)

```yaml
aap_setup_prep_setup_dir:  # Must be set, though if the aap_setup_prepare role has been run prior, a fact will be set.
aap_backup_dest: "/root"
aap_backup_async: 10000
aap_backup_poll: 20
```

## Example Playbook

The following playbook and accompanying vars file containing the defined seed objects can be invoked in the following manner.

```sh
ansible-playbook playbook.yml -e @aap_vars.yml controller
```

```yaml
---
# Playbook to backup Automation controller

- name: Backup Automation controller
  hosts: localhost
  become: true
  vars:
    aap_setup_prep_setup_dir: /root/ansible-automation-platform-installer/
    aap_backup_dest: /aap_backups/
  roles:
    - infra.aap_utilities.aap_backup
```

## License

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author Information

Sean Sullivan
