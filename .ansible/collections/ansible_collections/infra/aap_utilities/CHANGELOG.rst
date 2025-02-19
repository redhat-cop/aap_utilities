==================================
infra.aap\_Utilities Release Notes
==================================

.. contents:: Topics

v2.5.2
======

Minor Changes
-------------

- Added ability to download the containerized installer.
- Added ability to install EDA Controller on OCP
- Tweaked how the installer to download is choosen, this should have no effective changes.

Bugfixes
--------

- Fixed an issue where where download would error trying to download a second version of the installer.

v2.5.1
======

Minor Changes
-------------

- Added support for providing OpenShift auth via api key for ocp install
- Changed isntances of ansible.builtin.yum module to dnf, this module is backwards comapatible, but the yum module has been removed.

v2.5.0
======

v2.4.0
======

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
