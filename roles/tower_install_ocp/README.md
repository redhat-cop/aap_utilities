# ansible-tower-install

Ansible role to install Ansible Tower on OCP.

## Requirements

python >= 2.7

---PYTHON MODULES---
openshift
kubernetes
PyYAML >= 3.11
requests-oauthlib

## Role Variables

```yaml

#Directory from which Tower installation will launch
tower_working_location: "/root/"

# Location of tower version to install
tower_releases_url: https://releases.ansible.com/ansible-tower/setup_openshift/
tower_setup_file: ansible-tower-openshift-setup-{{ tower_release_version }}.tar.gz

# This will create or update a default admin (superuser) account in Tower
admin_user: admin
admin_password: 'mypassword'

# Tower Secret key
# It's *very* important that this stay the same between upgrades or you will lose
# the ability to decrypt your credentials
secret_key: 'mysecretkey'

# Database Settings
# =================

# Set pg_hostname if you have an external postgres server, otherwise
# a new postgres service will be created
# pg_hostname=postgresql

# If using an external database, provide your existing credentials.
# If you choose to use the provided containerized Postgres depolyment, these
# values will be used when provisioning the database.
pg_username: 'awx'
pg_password: 'awx'
pg_database: 'tower'
pg_port: 5432
pg_sslmode: 'prefer'  # set to 'verify-full' for client-side enforced SSL

# Note: The user running this installer will need cluster-admin privileges.
# Tower's job execution container requires running in privileged mode,
# and a service account must be created for auto peer-discovery to work.

# Deploy into Openshift
# =====================

openshift_host: https://openshift.example.com
openshift_skip_tls_verify: false
openshift_project: tower
openshift_user: admin
openshift_password: password
# If you don't want to hardcode a password here, just do:
# ./setup_openshift.sh -e openshift_token=$TOKEN

# Skip this section if you BYO database. This is only used when you want the
# installer to deploy a containerized Postgres deployment inside of your
# OpenShift cluster. This is only recommended if you have experience storing and
# managing persistent data in containerized environments.
#
#
# Name of a PVC you've already provisioned for database:
openshift_pg_pvc_name: postgresql
# Openshift Persistant Volume Claim Size
pvc_claim_size: 10Gi

```

## Example Playbook

The following playbook and accompanying vars file containing the defined seed objects can be invoked in the following manner.

```sh
$ ansible-playbook playbook.yml -e @tower_vars.yml
```

```yaml
---
# Playbook to install Ansible Tower as a single node

- name: Install Ansible Tower on OCP
  hosts: localhost
  become: true
  vars:
    tower_tower_release_version: 3.7.2-1.tar.gz
  roles:
    - tower_install_ocp
```

## License

MIT

## Author Information

Chris Renwick

