=================================
infra.aap_Utilities Release Notes
=================================

.. contents:: Topics


v2.3.0
======

Minor Changes
-------------

- galaxy.yml added to enable install from source

Deprecated Features
-------------------

- The kerberos role is now depreciated as it is not compatible with Execution Environments.

Bugfixes
--------

- Availability checks will use credentials from either aap_setup_prep_inv_secrets or aap_setup_prep_inv_vars
- Use correct variable name for OCP connection details

v2.2.4
======

Minor Changes
-------------

- Added ability to add extra vars files in aap_setup_install role.
- Bumped the default aap version to 2.3

Bugfixes
--------

- Fix hostnames for install check
- Fixed tag in aap_remove role for automation hub.
- Update license information in each role.

v2.2.3
======

Breaking Changes / Porting Guide
--------------------------------

- removed the warn on the builtin command role as module feature depreciated in recent ansible release.
