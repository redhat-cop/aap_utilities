# aap\_setup\_download

A role to download the latest z-version of the AAP setup tarball for a given minor version (e.g. 2.1 at time of writing).

Shamelessly adapted from [Red Hat Ansible Automation Platform 2: Automating the Installer Download and publishing as a Content View in Satellite](https://www.redhat.com/en/blog/automating-installation-ansible-automation-platform-ansible-and-satellite).

## Requirements

You will need a Red Hat Ansible Automation Platform (AAP, hence the name) subscription.
Once this is a given, you will be able to create yourself an offline token at [https://access.redhat.com/management/api/](https://access.redhat.com/management/api/) (see [Getting started with Red Hat APIs](https://access.redhat.com/articles/3626371) for details).

## Role Variables

The following input variables are required:

* `aap_setup_down_offline_token` contains your offline token as described in the requirements.
It has no default value and _must_ be defined.
* `aap_setup_down_version` defines the minor version to download (e.g. `2.1`)
The default is the latest version available at time of writing.
* `aap_setup_down_dest_dir` is the directory to where you want to download the tarball.
It is by default the working directory `aap_setup_working_dir` also used by other roles of the collection, or ultimately `/var/tmp`.
* `aap_setup_down_type` can be either `setup` or `setup-bundle`, depending which flavour of the tarball you want to download.
* `aap_setup_rhel_version` defines the major RHEL version being used (currently 8 or 9). If you are gathering facts you possibly don't need to specify this as the role will attempt to work out the value required though you will if AAP will be installed on machines on a different OS than the installer will run on. Otherwise the default is 8.

The full path of the downloaded file is stored in the fact `aap_setup_down_installer_file` so that it can be used for extraction.

## Dependencies

None.

## Example Playbook

Combined with the role `aap_setup_prepare`, the following code will download and prepare the installation directory:

```yaml
- hosts: installationserver
  roles:
    - { role: redhat_cop.aap_utilities.aap_setup_download }
    - { role: redhat_cop.aap_utilities.aap_setup_prepare }
```

## License

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author Information

Eric Lavarde <elavarde@redhat.com>, Red Hat Consulting, Principal Architect
