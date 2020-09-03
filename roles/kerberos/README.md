# redhat_cop.tower_utilities.kerberos

Ansible role to setup kerberos on a server.

## Requirements

This role is setup to authenticate to a windows domain server with kerberos and all required packages to run windows winrm for remote windows management with ansible

## Role Variables

All Kerberos variables are eligble to be set. However a few are set by default. If you wish to change them, you can specifiy the variable in your inventory file. They are the following:

```yaml
#defaults for Kerberos
krb_dns_lookup_realm: "true"
krb_dns_lookup_kdc: "true"
krb_ticket_lifetime: "24h"
krb_renew_lifetime: "7d"
krb_forwardable: "true"
krb_rdns : "false"

#Domain name
krb_realm_name=YOURDOMAIN.LCL
#hostname of Domain Server
krb_kdc_hostname=yourdomainctl
krb_admin_hostname=yourdomainctl
```

## Dependencies

There are no dependencies requred for this role

The dependencies for Linux, are all installed by this role.

For Windows 2k12 and 2k16 the powershell script in files needs to be run in through a privledged Powershell.

For Windows 2k8 the folllowing is required for some ansible modules to work:
Server 2008 R2 Service pack 1
Powershell v4. via Windows Management Framework 4.0 build 6.1
To check what version of powershell is installed, run the following in powershell:
$PSVersionTable.PSVersion

A technet guide on upgrading to 4 is here:
https://social.technet.microsoft.com/wiki/contents/articles/20623.step-by-step-upgrading-the-powershell-version-4-on-2008-r2.aspx

## Example Playbook

The following playbook and accompanying vars file containing the defined seed objects can be invoked in the following manner. This is role is meant to be used by other roles for setup.

### Playbook File
```yaml
---
- hosts: towers
  remote_user: root
  any_errors_fatal: true
  gather_facts: False
  roles:
    - win_rm_kerb_role
```

### Example Inventory File

```yaml
---
[towers]
192.168.100.129

[all:vars]
ansible_connection=ssh
ansible_ssh_user=root

#Domain name
krb_realm_name=REDHAT.LCL
#hostname of Domain Server
krb_kdc_hostname=redhatdomainctl
krb_admin_hostname=redhatdomainctl
```

## License

MIT

## Author Information

[Sean Sullivan](https://github.com/Wilk42)
