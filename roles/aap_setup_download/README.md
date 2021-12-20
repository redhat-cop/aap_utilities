aap\_setup\_download
==================

A role to download the latest z-version of the AAP setup tarball for a given minor version (e.g. 2.1 at time of writing).

Shamelessly adapted from [Red Hat Ansible Automation Platform 2: Automating the Installer Download and publishing as a Content View in Satellite](https://www.redhat.com/en/blog/automating-installation-ansible-automation-platform-ansible-and-satellite).

Requirements
------------

You will need a Red Hat Ansible Automation Platform (AAP, hence the name) subscription.
Once this is a given, you will be able to create yourself an offline token

Role Variables
--------------

The following input variables are required:

* `aap_setup_down_offline_token` contains your offline token as described in the requirements.
It has no default value and _must_ be defined. This token can be obtained at [Red Hat Access Management API](https://access.redhat.com/management/api).
* `aap_setup_down_version` defines the minor version to download (e.g. `2.1`), make sure you defines it as string and not as float!
The default is the latest version available at time of writing.
* `aap_setup_down_dest_dir` is the directory to where you want to download the tarball.
It is by default the working directory `aap_setup_working_dir` also used by other roles of the collection, or ultimately `/var/tmp`.
* `aap_setup_down_type` can be either `setup` or `setup-bundle`, depending which flavour of the tarball you want to download.

The full path of the downloaded file is stored in the fact `aap_setup_down_installer_file` so that it can be used for extraction.

Dependencies
------------

None.

Example Playbook
----------------

Combined with the role `aap_setup_prepare`, the following code will download and prepare the installation directory:


```yaml
- hosts: installationserver
  roles:
    - { role: redhat_cop.tower_utilities.aap_setup_download }
    - { role: redhat_cop.tower_utilities.aap_setup_prepare }
```

License
-------

MIT

Author Information
------------------

Eric Lavarde <elavarde@redhat.com>, Red Hat Consulting, Principal Architect
