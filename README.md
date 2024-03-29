# ansible-drift

[![Build Status](https://github.com/systemli/ansible-drift/workflows/Integration/badge.svg?branch=main)](https://github.com/systemli/ansible-drift/actions?query=workflow%3AIntegration)
[![Ansible Galaxy](http://img.shields.io/badge/ansible--galaxy-drift-blue.svg)](https://galaxy.ansible.com/systemli/drift)

ansible-drift will send mails showing your configration drift from a specified playbook.
The script can be run interactively or via cron and update your git repo if necessary.
Each host in hostlist will be checked separately.

## Role Variables

```
# a bash compatible list of hosts you want to check
drift_hostlist: "{{ groups['all']|sort|join(' ') }}"

# send mails to
drift_receiver: root

# run as
drift_user: ansible

# define playbook to be regularly executed
# drift_playbook:

# define a git branch to pull
# drift_branch: "origin main"
drift_branch: ""

```

## Download

Download latest release with `ansible-galaxy`

```
$ ansible-galaxy install systemli.drift
```

## Example Playbook

```
- hosts: servers
  roles:
    - systemli.drift
  vars:
    drift_playbook: /home/ansible/ansible/site.yml
```

Testing & Development
---------------------

Tests
-----

For developing and testing the role we use Github Actions, Molecule, and Vagrant. On the local environment you can easily test the role with

Run local tests with:

```
molecule test 
```

Requires Molecule, Vagrant and `python-vagrant` to be installed.For developing and testing the role we use Travis CI, Molecule and Vagrant. On the local environment you can easily test the role with



## License

GPL

## Author Information

https://www.systemli.org
