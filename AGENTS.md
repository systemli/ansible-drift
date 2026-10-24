# AGENTS.md

Ansible role `systemli.drift` that installs ansible-drift, a script that mails configuration drift of hosts against a playbook.

## Layout

- `defaults/main.yml`: role variables (`drift_*`) with defaults; document them in the README
- `tasks/main.yml`: installs the script, user, SSH setup and systemd units
- `templates/`: `ansible-drift.j2` script and `systemd/` unit templates
- `callback_plugins/`: Ansible callback plugin used by the script
- `meta/`: Galaxy metadata
- `molecule/default/`: molecule scenario (Docker driver, Debian 13); CI generates its own `molecule/github` scenario that reuses `converge.yml`

## Checks

- `ansible-lint .` (config in `.ansible-lint`) and `yamllint .` (config in `.yamllint`) must pass
- `molecule test` needs Docker and `molecule-plugins[docker]`; CI tests Debian 12 and 13
- `ansible-lint` creates `.ansible/`; it is git ignored, never commit it

## Conventions

- Use fully qualified module names, quoted octal `mode` values and `true`/`false` booleans
- Give every task a `name`
- New or changed role variables need an entry in `defaults/main.yml` and the README
- GitHub Actions are pinned to commit SHAs with a `# vX.Y.Z` comment; Dependabot updates them

## Commits and PRs

- Write in English, use conventional commit titles (`feat:`, `fix:`, `chore:`, `ci:`; `!` for breaking changes)
- The PR title sets the release-drafter label (`enhancement`, `bug`, `chore`, `breaking`); a breaking change bumps the major version
- Open PRs as draft and fill in `.github/pull_request_template.md`: what changed and why, plus a breaking changes section if needed
- Do not list changed files or claim test results in the description; CI covers that
