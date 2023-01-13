# aap\_setup\_install

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
    - redhat_cop.aap_utilities.aap_setup_download
    - redhat_cop.aap_utilities.aap_setup_prepare
    - redhat_cop.aap_utilities.aap_setup_install
```

Note that this only works without root access if the bastion host isn't part of the future cluster,
and if the RPM pre-requisites have been pre-installed.
Else change to `become: true`.

## License

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author Information

Eric Lavarde <elavarde@redhat.com>
