# infra.aap\_utilities.git\_ssh\_setup

Creates a minimal Git server which can be used over SSH. It isn't meant as a full blown Git server,
but just for demonstration and learning purposes, and can be installed directly on the AAP servers.

## Requirements

The only pre-requisite is SSH itself, without which Ansible wouldn't work anyway.

## Role Variables

See the [defaults file](defaults/main.yml).

## Dependencies

None.

## Example Playbook

The following snippet, using the defaults, will create two Git repos under the git's user home folder,
which can be used (cloned and written) by the Ansible user:

```yaml
- hosts: controller.example.com
  roles:
    - infra.aap_utilities.git_ssh_setup
```

We've assumed that it will be created directly on the Controller server for demonstration purposes.

## License

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author Information

Create an [issue at GitHub](https://github.com/redhat-cop/aap_utilities/issues) if you want to contact us.
