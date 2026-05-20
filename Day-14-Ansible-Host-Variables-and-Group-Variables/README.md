## Ansible Host Variables and Group Variables

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Host variables and group variables provide a structured way to organize variables for different hosts and groups in your inventory. This approach scales better than inline variables and makes your playbooks cleaner and more maintainable.

### Directory Structure

Ansible automatically loads variables from two special directories:

```
project/
├── ansible.cfg
├── inventory
├── site.yml
├── group_vars/
│   ├── all              # Variables for all hosts
│   ├── webservers       # Variables for webservers group
│   └── databases        # Variables for databases group
└── host_vars/
    ├── node1.example.com    # Variables specific to node1
    └── node2.example.com    # Variables specific to node2
```

### Group Variables (group_vars/)

Variables in `group_vars/` apply to all hosts in a specific inventory group.

**inventory:**
```ini
[webservers]
node1.example.com
node2.example.com

[databases]
db1.example.com
```

**group_vars/webservers:**
```yaml
web_package: httpd
web_service: httpd
web_port: 80
```

**group_vars/databases:**
```yaml
db_package: postgresql
db_service: postgresql
db_port: 5432
```

**group_vars/all:**
```yaml
# Variables for ALL hosts
firewall_package: firewalld
firewall_service: firewalld
```

### Host Variables (host_vars/)

Variables in `host_vars/` apply to a specific host and **override** group variables.

**host_vars/node1.example.com:**
```yaml
ansible_user: admin
web_package: nginx    # Overrides group_vars setting
web_service: nginx
custom_port: 8080
```

**host_vars/node2.example.com:**
```yaml
ansible_user: devops
# Will use web_package from group_vars
```

### Variable Precedence

When the same variable is defined in multiple places, Ansible uses this order (highest priority wins):

1. **Host vars** (host_vars/hostname) ← Highest priority
2. **Group vars** (group_vars/groupname)
3. **Group vars/all** (group_vars/all)
4. Playbook vars
5. Role defaults ← Lowest priority

### Example Playbook

**site.yml:**
```yaml
---
- name: Install and configure httpd
  hosts: webservers
  become: yes
  tasks:
    - name: Install {{ web_package }}
      yum:
        name: "{{ web_package }}"
        state: latest
        
    - name: Start {{ web_service }}
      service:
        name: "{{ web_service }}"
        state: started
```

**Running the playbook:**
```bash
ansible-playbook site.yml
```

In this example:
- `node1` will install **nginx** (from host_vars)
- `node2` will install **httpd** (from group_vars)

### Special Variables

You can also define connection variables in host_vars:

```yaml
# host_vars/node1
ansible_host: 192.168.1.10        # Actual IP address
ansible_user: admin               # SSH user
ansible_port: 2222               # SSH port
ansible_ssh_private_key_file: ~/.ssh/custom_key
ansible_become: yes              # Enable privilege escalation
ansible_become_method: sudo      # Escalation method
```

### File Naming Conventions

Both directories support multiple naming conventions:

**Single file per host/group:**
```
group_vars/webservers
host_vars/node1.example.com
```

**Directory with multiple files:**
```
group_vars/webservers/
  ├── vars.yml
  ├── vault.yml
host_vars/node1.example.com/
  ├── vars.yml
  ├── vault.yml
```

### Best Practices

1. **Organize by function**: Group related variables together
2. **Use group_vars/all** for common variables across all hosts
3. **Use host_vars sparingly**: Only for host-specific overrides
4. **Document variables**: Add comments explaining purpose
5. **Encrypt sensitive data**: Use Ansible Vault (Day 20-21)
6. **Keep it DRY**: Don't repeat variables; use group_vars
7. **Meaningful names**: Use descriptive group and host names

### Common Use Cases

**1. Environment-specific configuration:**
```
group_vars/production
group_vars/staging
group_vars/development
```

**2. Role-based variables:**
```
group_vars/webservers
group_vars/database_servers
group_vars/load_balancers
```

**3. Location-based variables:**
```
group_vars/us_east
group_vars/eu_west
```

**4. Host-specific customizations:**
```
host_vars/special_node    # Node with different configuration
```

### Debugging Variables

To see which variables are applied to a host:

```bash
# Show all variables for a host
ansible -m debug -a "var=hostvars[inventory_hostname]" hostname

# Show specific variable
ansible -m debug -a "var=web_package" hostname
```

### Running the Example

```bash
# Install packages on all nodes in the inventory
ansible-playbook site.yml -e "nodes=all"

# Target specific group
ansible-playbook site.yml -e "nodes=webservers"
```

The variables from group_vars and host_vars will be automatically loaded based on each host's group membership and hostname.
