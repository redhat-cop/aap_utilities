=================================
infra.aap_Utilities Release Notes
=================================

.. contents:: Topics


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
