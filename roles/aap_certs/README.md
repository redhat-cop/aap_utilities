# redhat\_cop.tower\_utilities.aap\_certs

Ansible role to install SSL certificates for AAP automation controller and/or automation hub.

Certificates are only installed if the underlying destination directory does already exist,
this allows to point the role at all servers in the cluster.

Note it is also possible to deploy the certificates at install time with the proper inventory variables.

## Requirements

The certificates must have been created with certificate and key.

## Role Variables

Available variables are listed below, along with default values defined (see [defaults](defaults/main.yml)).

Variables to point at the source certificates and keys for controller,
respective automation hub.
They are undefined by default which means that no certificate is installed:

```yaml
aap_certs_controller_ssl_cert: "{{ playbook_dir }}/tower.cert"
aap_certs_controller_ssl_key: "{{ playbook_dir }}/tower.key"
aap_certs_autohub_ssl_cert: "{{ playbook_dir }}/pulp.cert"
aap_certs_autohub_ssl_key: "{{ playbook_dir }}/pulp.key"
```

The content of the certificates and keys can also be set rather than specifying a file.
This is useful when you're using a secrets backend like HashiCorp Vault.
**Note that these are each mutually exclusive with the variables above.**

```yaml
aap_certs_controller_ssl_cert_content: "-----BEGIN CERTIFICATE----- xxxxxx -----END CERTIFICATE-----"
aap_certs_controller_ssl_key_content: "-----BEGIN PRIVATE KEY----- xxxxxx -----END PRIVATE KEY-----"
aap_certs_autohub_ssl_cert_content: "-----BEGIN CERTIFICATE----- xxxxxx -----END CERTIFICATE-----"
aap_certs_autohub_ssl_key_content: "-----BEGIN PRIVATE KEY----- xxxxxx -----END PRIVATE KEY-----"
```

The following variable defines if the old certificates/keys should be backed-up:

```yaml
aap_certs_create_backup: false
```

## Example Playbook

The following playbook and accompanying vars file containing the defined seed objects can be invoked in the following manner.

```sh
ansible-playbook playbook.yml -e @tower_vars.yml tower
```

```yaml
---
# Playbook to install Ansible Tower as a single node

- name: Install AAP certificates
  hosts: aap_servers
  become: true
  vars:
    aap_certs_controller_ssl_cert: "{{ playbook_dir }}/tower.cert"
    aap_certs_controller_ssl_key: "{{ playbook_dir }}/tower.key"
    aap_certs_autohub_ssl_cert: ""
    aap_certs_autohub_ssl_key: ""
  roles:
    - ansible-tower-install
```

## License

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author Information

Tom Page
