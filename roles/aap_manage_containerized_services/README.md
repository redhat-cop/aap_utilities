# infra.aap_utilities.aap\_manage\_containerized\_services

An Ansible role to manage the service comprising the containerized version of AAP.

## Requirements

A valid inventory file for the instance being managed.

## Role Variables

There is only one input variable required for this role.

`svc_action`: stop | start | restart | status

- _The default value for `svc_action` (set in `defaults/main.yml`) is `status`. Unless a different value is specified, the role will display the status of all services running in a given AAP instance._

## Tags

Each service is assigned a tag to enable manipulation of individual services rather than the entire instance. The available tags are: `postgres`, `receptor`, `redisunix`, `redistcp`, `hub`, `controller`, `eda`, and `gateway`.

## Dependencies

None

## Example Playbook

```yaml
- name: Manage the AAP instance's services
  hosts: all
  become: false
  gather_facts: false

  roles:
    - role: infra.aap_utilities.aap_manage_containerized_services
      # Valid values for the variable below are: "status", "start", "stop", and "restart".
      # The default operation (value of the variable) is "status".
      svc_action: <action>
...
```

## How To Use

Create a playbook using the example above as a guide, and execute it as normal. To avoid unnecessary output from skipped hosts, use "`ANSIBLE_DISPLAY_SKIPPED_HOSTS=false`" with the `ansible-playbook` command:

```text
ANSIBLE_DISPLAY_SKIPPED_HOSTS=false ansible-playbook -i <path_to_inventory> example_playbook.yml -e "svc_action=<action>"
```

## License

[GPLv3+0](https://github.com/redhat-cop/aap_utilities#licensing)

## Author Information

Kevin Gregory, Red Hat Consulting, Senior Consultant
