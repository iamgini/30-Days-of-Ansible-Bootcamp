## Ansible Magic Variables

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Magic variables are special variables automatically provided by Ansible that give you information about the playbook execution context, inventory, and other hosts. They're called "magic" because you don't define them - Ansible creates them automatically.

### Common Magic Variables

| Variable | Description |
|----------|-------------|
| `inventory_hostname` | Name of current host as defined in inventory |
| `inventory_hostname_short` | Short hostname (before first dot) |
| `group_names` | List of groups the current host belongs to |
| `groups` | Dictionary of all groups and their hosts |
| `hostvars` | Dictionary containing variables for all hosts |
| `play_hosts` | List of hosts in scope for current play |
| `ansible_play_hosts` | Same as play_hosts |
| `ansible_play_batch` | List of hosts in current batch |
| `ansible_version` | Ansible version information |
| `playbook_dir` | Directory containing the playbook |
| `role_path` | Path to current role |

### inventory_hostname

The name of the current host as specified in the inventory:

```yaml
- name: Show hostname
  debug:
    msg: "Current host: {{ inventory_hostname }}"
```

If your inventory has:
```ini
[webservers]
web1.example.com
web2.example.com
```

Then `inventory_hostname` would be `web1.example.com` or `web2.example.com`.

### group_names

List of all groups the current host belongs to:

```yaml
- name: Show groups
  debug:
    msg: "This host is in groups: {{ group_names }}"
```

Example output: `['webservers', 'production', 'us-east']`

**Conditional based on group:**
```yaml
- name: Install monitoring on production
  package:
    name: monitoring-agent
    state: present
  when: "'production' in group_names"
```

### groups

Dictionary of all inventory groups and their members:

```yaml
- name: Show all webservers
  debug:
    msg: "Webservers: {{ groups['webservers'] }}"

- name: Show all groups
  debug:
    msg: "{{ groups }}"
```

**Iterate over all hosts in a group:**
```yaml
- name: Configure backend servers
  template:
    src: haproxy.cfg.j2
    dest: /etc/haproxy/haproxy.cfg
```

**haproxy.cfg.j2:**
```jinja2
backend webservers
{% for host in groups['webservers'] %}
    server {{ host }} {{ hostvars[host]['ansible_default_ipv4']['address'] }}:80
{% endfor %}
```

### hostvars

Access variables from other hosts:

```yaml
- name: Get database IP from db server
  debug:
    msg: "DB IP: {{ hostvars['db1.example.com']['ansible_default_ipv4']['address'] }}"
```

**Common use case - building configuration files:**
```jinja2
# Database configuration
[database]
{% for host in groups['databases'] %}
host = {{ hostvars[host]['ansible_default_ipv4']['address'] }}
port = {{ hostvars[host]['db_port'] | default('5432') }}
{% endfor %}
```

### play_hosts

List of hosts that are in scope for the current play:

```yaml
- name: Show active hosts
  debug:
    msg: "Hosts in this play: {{ play_hosts }}"
```

**Useful for coordination:**
```yaml
- name: Check if I'm the last host
  debug:
    msg: "I'm the last one!"
  when: inventory_hostname == play_hosts[-1]
```

### ansible_version

Information about Ansible version:

```yaml
- name: Show Ansible version
  debug:
    msg: "Ansible {{ ansible_version.full }}"
    
- name: Require minimum version
  assert:
    that: ansible_version.full is version('2.9', '>=')
    msg: "Ansible 2.9 or higher required"
```

### playbook_dir

Directory containing the currently running playbook:

```yaml
- name: Use file relative to playbook
  copy:
    src: "{{ playbook_dir }}/files/config.conf"
    dest: /etc/app/config.conf
```

### role_path

Path to the current role (only available inside roles):

```yaml
- name: Include role-specific file
  include_vars: "{{ role_path }}/vars/custom.yml"
```

### Practical Examples

**1. Building a cluster configuration:**
```yaml
- name: Configure cluster nodes
  template:
    src: cluster.conf.j2
    dest: /etc/cluster/cluster.conf
```

**cluster.conf.j2:**
```jinja2
cluster_name: production
nodes:
{% for host in groups['cluster'] %}
  - hostname: {{ host }}
    ip: {{ hostvars[host]['ansible_default_ipv4']['address'] }}
    role: {{ hostvars[host]['cluster_role'] | default('member') }}
{% endfor %}
```

**2. Running task only on specific host:**
```yaml
- name: Initialize database (only on first db server)
  command: /usr/local/bin/init_db.sh
  when: inventory_hostname == groups['databases'][0]
```

**3. Coordinating across hosts:**
```yaml
- name: Wait for all web servers to be ready
  wait_for:
    host: "{{ hostvars[item]['ansible_default_ipv4']['address'] }}"
    port: 80
    timeout: 300
  loop: "{{ groups['webservers'] }}"
  delegate_to: localhost
```

**4. Group-based configuration:**
```yaml
- name: Set environment type
  set_fact:
    env_type: "{{ 'production' if 'prod' in group_names else 'development' }}"

- name: Apply production security
  include_tasks: security_hardening.yml
  when: env_type == 'production'
```

**5. Multi-tier application setup:**
```yaml
- name: Configure application servers with database info
  template:
    src: app.properties.j2
    dest: /etc/app/application.properties
```

**app.properties.j2:**
```jinja2
# Application Configuration
app.name={{ inventory_hostname_short }}
app.tier=application

# Database Connections
{% for db in groups['databases'] %}
db.host.{{ loop.index }}={{ hostvars[db]['ansible_default_ipv4']['address'] }}
db.port.{{ loop.index }}={{ hostvars[db]['db_port'] | default(5432) }}
{% endfor %}

# Load Balancer
lb.host={{ hostvars[groups['loadbalancers'][0]]['ansible_default_ipv4']['address'] }}
```

### Accessing Nested Variables

```yaml
# Access another host's fact
- name: Get web1 memory
  debug:
    msg: "{{ hostvars['web1.example.com']['ansible_memtotal_mb'] }}"

# Access another host's custom variable
- name: Get web1 app version
  debug:
    msg: "{{ hostvars['web1.example.com']['app_version'] }}"

# Loop through all hosts in a group
- name: Show all IPs in webservers group
  debug:
    msg: "{{ item }}: {{ hostvars[item]['ansible_default_ipv4']['address'] }}"
  loop: "{{ groups['webservers'] }}"
```

### Delegation with Magic Variables

```yaml
- name: Gather info from all hosts, report from localhost
  debug:
    msg: "{{ inventory_hostname }} has IP {{ ansible_default_ipv4.address }}"
  delegate_to: localhost
```

### Best Practices

1. **Use inventory_hostname**: More reliable than `ansible_hostname` fact
2. **Check group membership**: Use `'group' in group_names` for conditionals
3. **Validate hostvars access**: Use `default()` filter for safety
4. **Document magic variable usage**: Add comments explaining logic
5. **Test with --limit**: Ensure logic works with partial host sets
6. **Use groups carefully**: Remember groups are inventory-wide, not play-specific

### Common Patterns

**Pattern 1: Run once per group:**
```yaml
- name: Initialize shared resource
  command: /usr/local/bin/setup_shared.sh
  when: inventory_hostname == groups['webservers'][0]
  run_once: true
```

**Pattern 2: Serial coordination:**
```yaml
- name: Rolling update
  hosts: webservers
  serial: 1
  tasks:
    - name: Update node
      yum:
        name: myapp
        state: latest
    
    - name: Notify load balancer
      uri:
        url: "http://{{ hostvars[groups['loadbalancers'][0]]['ansible_default_ipv4']['address'] }}/api/reload"
        method: POST
```

**Pattern 3: Cross-group references:**
```yaml
- name: Configure app with cache servers
  template:
    src: app.conf.j2
    dest: /etc/app/app.conf
```

**Template:**
```jinja2
cache_servers:
{% for host in groups['cache'] %}
  - {{ hostvars[host]['ansible_default_ipv4']['address'] }}:6379
{% endfor %}
```

### Debugging Magic Variables

```bash
# Show all variables for a host
ansible hostname -m debug -a "var=hostvars[inventory_hostname]"

# Show groups
ansible hostname -m debug -a "var=groups"

# Show group membership
ansible hostname -m debug -a "var=group_names"
```

### Running the Example

```bash
ansible-playbook site.yaml
```

This will demonstrate various magic variables and their usage across your inventory.
