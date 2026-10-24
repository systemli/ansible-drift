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

## Supported Platforms

Debian 13 (trixie) and Debian 12 (bookworm). Both are tested in CI.

## Testing & Development

The role is tested with GitHub Actions and Molecule using the Docker driver. To test locally, install Docker, `molecule`, `molecule-plugins[docker]` and `ansible-lint`, then run:

```
molecule test
```

Use `molecule converge` and `molecule login` to iterate on a running container.

## License

GPL

## Author Information

https://www.systemli.org
