# infra.aap_utilities.aap\_setup\_install

A role to install AAP 2.x, installing pre-requisites, unpacking the installation tarball and (optionally) writing the necessary inventory file.

## Requirements

* The installation package must have been extracted
* The necessary inventory must have been written

## Role Variables

The following input variables are available:

|Variable Name|Default Value|Required|Description|Example|
|---:|:---:|:---:|:---|:---:|
|`aap_setup_inst_setup_dir`|"`{{ aap_setup_prep_setup_dir }}`"|no|absolute path where to find the extracted installation tarball on the remote host, note that `aap_setup_prep_setup_dir` is a fact set by the role `aap_setup_prepare`|'/var/tmp/myinstaller'|
|`aap_setup_inst_inventory`|"`inventory`"|no|path to the inventory file/directory to be used for the installation, the path can be absolute or relative to the previous directory|'/etc/ansible/inventory'|
|`aap_setup_inst_extra_vars`|`{}`|no|dictionary of extra vars to use when calling setup.sh|see [defaults/main.yml](defaults/main.yml)|
|`aap_setup_inst_extra_vars_files`|`{}`|no|List of files to be applied as extra vars when calling setup.sh|see [defaults/main.yml](defaults/main.yml)|
|`controller_hostname/username/password/validate_certs`|none|see below|hostname and credentials of the installed controller, necessary to test previous installation|see the 'redhat\_cop.controller\_configuration' collection|
|`ah_hostname/username/password/validate_certs`|none|see below|hostname and credentials of the installed automation hub, necessary to test previous installation|see the 'redhat\_cop.ah\_configuration' collection|
|`aap_setup_inst_force`|false|no|a boolean deciding if the installation should proceed even if the controller and the automation hub are already installed|see [defaults/main.yml](defaults/main.yml)|

Note that the `controller_` and `ah_` variables are only required if the variable `aap_setup_inst_force` is _not_ true _and_ if the respective service is due to be installed.

## Dependencies

* `aap_setup_download`, in the same collection, can be used to download the tarball automatically.
* `aap_setup_prepare`, in the same collection, can be used to extract the tarball and write the inventory

## Example Playbook

```yaml
- name: download and install AAP from the bastion
  hosts: bastion
  gather_facts: false
  become: false
  tags: aap_installation
  roles:
    - infra.aap_utilities.aap_setup_download
    - infra.aap_utilities.aap_setup_prepare
    - infra.aap_utilities.aap_setup_install
```

Note that this only works without root access if the bastion host isn't part of the future cluster,
and if the RPM pre-requisites have been pre-installed.
Else change to `become: true`.

## Example Inventory Variables

```yaml
---
aap_setup_down_type: "setup-bundle"
aap_setup_rhel_version: 8

aap_setup_prep_inv_nodes:
  automationcontroller:
    - ansible-ctrl.example.com
  automationhub:
    - ansible-hub.example.com
  database:
    - database.example # if using an already existing DB, remove this and ensure that the following variables are filled with the valid details for your Controller and PAH
                       # databases: pg_host, pg_port, pg_database, ph_username, pg_password, automationhub_pg_host, automationhub_pg_port, automationhub_pg_database,
                       # automationhub_pg_username, automationhub_pg_password, automationhub_pg_sslmode
  execution_nodes:
    - execution-1.example
    - execution-2.example
  #servicescatalog_workers:
  #sso:

aap_setup_prep_inv_vars:
  automationcontroller: # denotes the automation controller nodes as hybrid nodes (both controller and execution)
    peers: execution_nodes
    node_type: hybrid

  execution_nodes:
    node_type: execution

  all:
    ansible_user: ansible
    ansible_become: true
    admin_password: changeme # admin password for Automation Controller UI
    pg_host: 'database.example'
    pg_port: '5432'

    pg_database: 'awx'
    pg_username: 'awx'
    pg_password: changeme
    pg_sslmode: 'prefer'  # set to 'verify-full' for client-side enforced SSL

    registry_url: 'registry.redhat.io'
    receptor_listener_port: 27199

    automationhub_admin_password: changeme # admin password for PAH UI
    automationhub_pg_host: 'database.example'
    automationhub_pg_port: '5432'

    automationhub_pg_database: 'automationhub'
    automationhub_pg_username: 'automationhub'
    automationhub_pg_password: changeme
    automationhub_pg_sslmode: 'prefer'
    automationhub_main_url: hub.example
    automationhub_require_content_approval: False
    automationhub_enable_unauthenticated_collection_access: True

    automationhub_ssl_validate_certs: False

    sso_console_admin_password: ''

aap_setup_prep_inv_secrets:
  all:
    registry_username: changeme
    registry_password: changeme
```

## License

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author Information

Eric Lavarde <elavarde@redhat.com>
