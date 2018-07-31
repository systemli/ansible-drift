# ansible-drift

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
# drift_branch: "origin master"
drift_branch: ""

```

## Download

Download latest release with `ansible-galaxy`

$ ansible-galaxy install systemli.drift

## Example Playbook

```
- hosts: servers
  roles:
    - systemli.drift
  vars:
    drift_playbook: /home/ansible/ansible/site.yml
```

## License

GPL

## Author Information

https://www.systemli.org
