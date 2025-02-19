# infra.aap\_utilities.aap\_restore

Ansible role to restore a backup of Ansible Automation Platform.

## Requirements

None

## Role Variables

Available variables are listed below, along with default values defined (see defaults/main.yml)

```yaml
# Role Vars
aap_setup_working_dir:  # Must be set, though if the aap_setup_prepare role has been run prior, a fact will be set.
aap_restore_location: "{{ aap_setup_working_dir }}/{{ aap_restore_file }}"
```

## Example Playbook

The following playbook and accompanying vars file containing the defined seed objects can be invoked in the following manner.

```sh
ansible-playbook playbook.yml -e @aap_vars.yml
```

```yaml
---
- name: Restore AAP
  hosts: localhost
  become: true
  vars:
    aap_setup_working_dir: /root/ansible-automation-platform-installer/
    aap_restore_location: "{{playbook_dir}}/aap-backup-latest.tar.gz"
  roles:
    - infra.aap_utilities.aap_restore
```

## License

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author Information

Sean Sullivan
