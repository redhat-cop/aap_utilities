==================================
infra.aap\_utilities Release Notes
==================================

.. contents:: Topics

v3.2.0
======

Minor Changes
-------------

- Added the ability to run a backup on containerized deployment.
- README - Standardized collection links tables, added changelog link, converted LICENSE to absolute URL, and added Support section for certification review.
- meta/runtime.yml - Updated minimum ansible-core version from 2.15 to 2.16.

v3.1.0
======

Minor Changes
-------------

- aap_ocp_install - add optional manifest overrides for AAP 2.5+ (platform namespace, ConsoleLink, whole CR, and controller/hub/EDA spec subtrees)
- collection build - exclude ``.ansible`` and ``.venv`` from the built artifact (galaxy build / importer)

v3.0.0
======

Minor Changes
-------------

- Add analyse_receptor_stdout.py script and documentation to identify lingering tasks and hosts
- Add consistently prefix to name of tasks in non-main tasks files as per good practices
- Add no_log to sensitive tasks handling tokens, passwords, and certificates across aap_setup_download, aap_setup_install, aap_ocp_install, and aap_certs roles.
- Adding a role to manage containerized services for AAP 2.5+
- Adds task to validate connection to OpenShift before proceeding
- CI workflows - fix issue-remove-inactive user object comparison and stray quote in issue-labeled comment.
- CONTRIBUTING.md - fix grammar and typos.
- Change regex_search to match test in pre-validate tasks
- Fix ansible-core 2.19 deprecation warnings for OCP install role
- Modify URL used to validate installation
- Satisfy ansible-core 2.19+ strictness on types for until loop waiting on empty list
- Standardize when and until keys in OCP install role
- analyse_receptor_stdout.py - improve error handling with JSON parse guards, safe event_data access, explicit encoding, and proper exit codes.
- changelogs/config.yaml - fix title capitalization to match FQCN.
- galaxy.yml - add dev-only files to build_ignore to reduce collection artifact size.
- overcome Git security feature since 2.35.2 refusing to clone Git repositories from other users

Breaking Changes / Porting Guide
--------------------------------

- The default installation is now containerized of AAP 2.6 on RHEL 10, instead of RPM of AAP 2.5 on RHEL 8

Bugfixes
--------

- Fixed readme because containerized-setup isn't a valid download type
- README.md - fix broken Galaxy Release badge link and forum typo.
- aap_manage_containerized_services - fix broken FQCN module names, corrupted Jinja2 expressions, invalid group names, and typos across all task files.
- aap_manage_containerized_services - fix double underscore in include_tasks filename preventing role execution.
- aap_ocp_install - default __aap_ocp_install_25_install to false when operator channel is not defined.
- aap_ocp_install - fix platform link_text validation asserting the wrong variable (controller instead of platform).
- aap_ocp_install - guard operator channel version parsing to prevent failures when aap_ocp_install_operator is undefined.
- aap_remove - kill lingering processes owned by service users before attempting user removal, preventing ``userdel: user is currently used by process`` failures (https://github.com/redhat-cop/aap_utilities/issues/254).
- aap_setup_download - fix installer filename filtering to precisely match the requested type (``setup`` vs ``setup-bundle``), preventing type cross-contamination and ensuring all available versions are returned (https://github.com/redhat-cop/aap_utilities/issues/328).
- aap_setup_install - fix containerized wait tasks failing with ``CERTIFICATE_VERIFY_FAILED`` by defaulting ``validate_certs`` to ``false`` instead of ``omit``, matching the pre-check tasks (https://github.com/redhat-cop/aap_utilities/issues/319).
- aap_setup_install - fix wrong registered variable names (__aap_setup_inst_ctl_ah, __aap_setup_inst_ctl_eda) causing undefined variable errors for hub/EDA install decisions on AAP < 2.5.
- aap_setup_install - handle both dict and list types for ``aap_setup_prep_inv_nodes`` hostname variables, fixing ``'list object' has no attribute 'keys'`` errors when inventory nodes are provided as a list (https://github.com/redhat-cop/aap_utilities/issues/327).
- galaxy.yml - fix double slash in issues URL.
- git_ssh_setup - add missing become on all system-level tasks.
- increased the limit of images from 25 to 100 on the API request to ensure that latest version will be pulled
- init bare Git repos without becoming another user to avoid non-root issues
- kerberos - add missing become on krb5.conf template task.
- kerberos - fix deprecated spelling and update collection name from redhat_cop to infra.
- markdownlint - fix rule ID typo MD0046 to MD046.

v2.8.0
======

Minor Changes
-------------

- aap_ocp_install - Add option to disable ConsoleLink CR creation

v2.7.0
======

Minor Changes
-------------

- aap_ocp_install - Enhanced support for manual approval of OLM operators.

v2.6.1
======

Bugfixes
--------

- aap_ocp_install - Expose route variables
- aap_ocp_install - PAH install used wrong variable name for manifest overrides
- aap_ocp_install - PAH not able to be installed in separate namespace when installing AAP 2.4 and below

v2.6.0
======

Minor Changes
-------------

- Added support to allow installation of AAP 2.5 using the new platform operator method
- Added support to install latest AAP 2.5 version
- aap_backup - Updated tasks and default to parametrize async and poll to respect long running backup for AAP2.4+ with private automation hub

Bugfixes
--------

- Fixed inventory not rendering properly due to another recent change.

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
