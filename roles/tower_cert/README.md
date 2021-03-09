# redhat_cop.tower_utilities.tower_cert

Ansible role to install a new Ansible Tower Certificate. Note it is also possible to use the `install` role to deploy a certificate at install time using `tower_ssl_cert` and `tower_ssl_key`

## Requirements

None

## Role Variables

Available variables are listed below, along with default values defined (see defaults/main.yml)

```yaml
tower_ssl_cert: "{{ playbook_dir }}/tower.cert"
tower_ssl_key: "{{ playbook_dir }}/tower.key"
```

## Example Playbook

The following playbook and accompanying vars file containing the defined seed objects can be invoked in the following manner.

```sh
$ ansible-playbook playbook.yml -e @tower_vars.yml tower
```

```yaml
---
# Playbook to install Ansible Tower as a single node

- name: Install Ansible Tower Certificate
  hosts: tower
  become: true
  vars:
    tower_ssl_cert: /var/tmp/tower.cert
    tower_ssl_key: /var/tmp/tower.key
  roles:
    - ansible-tower-install
```

## License

MIT

## Author Information

Tom Page
