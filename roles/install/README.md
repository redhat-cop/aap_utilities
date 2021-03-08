# redhat_cop.tower_utilities.install

Ansible role to prep to install Ansible Tower and Ansible automation hub.

## Requirements

None

## Role Variables

Available variables are listed below, along with default values defined (see defaults/main.yml) and the pre_tasks role which runs as a dependency of this role.

```yaml
tower_working_location: "/root/"
tower_force_setup: true

# Tower variables
tower_admin_password: "password"

# Postgresql variables
tower_pg_database: "awx"
tower_pg_username: "awx"
tower_pg_password: "password"

# RabbitMQ variables
tower_rabbitmq_username: tower
tower_rabbitmq_password: "password"
tower_rabbitmq_cookie: "cookiemonster"
tower_rabbitmq_port: 5672
tower_rabbitmq_vhost: tower
tower_rabbitmq_use_long_name: false

tower_releases_url: https://releases.ansible.com/ansible-tower/setup
tower_setup_file: ansible-tower-setup-{{ tower_release_version }}.tar.gz

tower_hosts:
  - "localhost ansible_connection=local"

tower_database_host: ""
tower_database_port: ""

# as long as the host name is empty, Automation Hub will NOT be installed
tower_ah_hosts: []

# the default configures an AH using the default database with similar defaults
# as Tower
tower_ah_admin_password: "{{ tower_admin_password }}"
# if tower_database_host isn't defined or is empty,
# the host where the installation takes place is deemed to host the DB
tower_ah_pg_host: "{{ tower_database_host | default(ansible_host | default(inventory_hostname), true) }}"
tower_ah_pg_port: "{{ tower_database_port }}"
tower_ah_pg_database: 'automationhub'  # it is NOT supported to use the same name as for Tower!
tower_ah_pg_username: "{{ tower_pg_username }}"
tower_ah_pg_password: "{{ tower_pg_password }}"
tower_ah_pg_sslmode: prefer

tower_ssh_connection_vars: ''

# Set isolated groups for isolated nodes if required
isolated_groups:
  - name: dmz1
    hostnames:
    - isolatednode0.dmz1.example.com
  - name: dmz2
    hostnames:
    - isolatednode0.dmz2.example.com
    - isolatednode1.dmz2.example.com

```

## tower_ssh_connection_vars

Connection vars can be set in the inventory file through a list of vars.

```yaml
tower_ssh_connection_vars:
  - name: ansible_connection
    value: ssh
  - name: ansible_user
    value: vagrant
  - name: ansible_ssh_pass
    value: vagrant
  - name: ansible_ssh_private_key_file
    value: /path/to/file
  - name: ansible_become
    value: true
```

## Example Playbook

The following playbook and accompanying vars file containing the defined seed objects can be invoked in the following manner.

```sh
$ ansible-playbook playbook.yml -e @tower_vars.yml tower
```

```yaml
---
# Playbook to install Ansible Tower as a single node

- name: Install Ansible Tower
  hosts: tower
  become: true
  vars:
    tower_releases_url: https://releases.ansible.com/ansible-tower/setup-bundle
    tower_release_version: bundle-3.8.1-1
  roles:
    - redhat_cop.tower_utilities.install
```


```yaml
---
# Playbook to install Ansible Automation Hub only

- name: Install Automation Hub
  hosts: tower
  become: true
  vars:
    tower_hosts: []
    tower_ah_hosts:
      - "localhost ansible_connection=local"
  roles:
    - redhat_cop.tower_utilities.install
```

```yaml
---
# Playbook to install Ansible Tower as a cluster

- name: Setup Ansible Tower
  hosts: localhost
  become: true
  vars:
    tower_hosts:
      - "clusternode[1:3].example.com"
    tower_database_host: "dbnode.example.com"
    tower_database_port: "5432"
  roles:
    - redhat_cop.tower_utilities.install
```

## License

MIT

## Author Information

Tom Page
