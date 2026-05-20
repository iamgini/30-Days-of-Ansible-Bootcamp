## Ansible Extra Variables

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### What are Extra Variables?

Extra variables (also called "extra vars") are variables passed to Ansible at runtime via the command line using the `-e` or `--extra-vars` flag. They have the **highest precedence** in Ansible's variable hierarchy, meaning they override all other variable definitions.

### Why Use Extra Variables?

- **Runtime flexibility**: Change playbook behavior without modifying files
- **CI/CD integration**: Pass different values for different environments
- **Override defaults**: Temporarily override inventory or playbook variables
- **Dynamic execution**: Specify targets, packages, or configurations at runtime

### Variable Precedence Hierarchy

From lowest to highest priority:
1. Role defaults (defined in roles)
2. Inventory variables (group_vars, host_vars)
3. Playbook vars_files
4. Playbook vars (defined in the playbook)
5. **Extra vars** (command line `-e`) ← **Highest Priority**

Extra vars always win!

### Passing Extra Variables

**1. Simple key=value format:**
```bash
ansible-playbook site.yml -e "package=httpd"
ansible-playbook site.yml -e "nodes=webservers"
```

**2. Multiple variables:**
```bash
ansible-playbook site.yml -e "package=httpd user=admin"
```

**3. JSON format:**
```bash
ansible-playbook site.yml -e '{"package":"httpd","state":"latest"}'
```

**4. YAML/JSON file:**
```bash
ansible-playbook site.yml -e "@vars.yml"
ansible-playbook site.yml -e "@vars.json"
```

### Example Playbook

```yaml
---
- name: Install package
  hosts: "{{ nodes | default('localhost') }}"
  become: yes
  vars:
    package: vim
  tasks:
    - name: Install {{ package }}
      yum:
        name: "{{ package }}"
        state: latest
```

### Running with Extra Variables

```bash
# Override the package variable
ansible-playbook site.yml -e "package=httpd"

# Specify nodes and package
ansible-playbook site.yml -e "nodes=webservers package=nginx"

# Use a variable file
ansible-playbook site.yml -e "@production-vars.yml"
```

### Common Use Cases

**1. Environment-specific deployments:**
```bash
ansible-playbook deploy.yml -e "@production.yml"
ansible-playbook deploy.yml -e "@staging.yml"
```

**2. Target selection:**
```bash
ansible-playbook maintenance.yml -e "target_hosts=database_servers"
```

**3. Version specification:**
```bash
ansible-playbook upgrade.yml -e "app_version=2.1.0"
```

**4. Feature flags:**
```bash
ansible-playbook site.yml -e "enable_monitoring=true"
```

### Best Practices

- Use extra vars for values that change between runs
- Provide sensible defaults in playbooks using `default()` filter
- Document required extra vars in playbook comments or README
- Use variable files (`@file.yml`) for multiple related variables
- Quote variables in YAML to avoid parsing issues: `"{{ variable }}"`

### Default Values

Protect against missing variables using the `default()` filter:

```yaml
hosts: "{{ target | default('localhost') }}"
```

This provides a fallback if the variable isn't supplied.
