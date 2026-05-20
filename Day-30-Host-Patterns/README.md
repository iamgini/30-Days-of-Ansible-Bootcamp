## Host Patterns

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Host patterns let you specify which hosts or groups from your inventory should be targeted by a play or ad-hoc command. Mastering patterns allows precise control over automation scope.

### Basic Patterns

**All hosts:**
```yaml
- hosts: all
```

**Single host:**
```yaml
- hosts: web1.example.com
```

**Single group:**
```yaml
- hosts: webservers
```

**Multiple groups:**
```yaml
- hosts: webservers,databases
```

### Wildcards

**Asterisk (*) matches any characters:**
```yaml
- hosts: *.example.com           # All hosts in example.com domain
- hosts: web*.example.com        # web1, web2, webserver, etc.
- hosts: 192.168.1.*             # All hosts in subnet
```

**Question mark (?) matches single character:**
```yaml
- hosts: web?.example.com        # web1, web2, web3, etc. (not web10)
```

**Character ranges:**
```yaml
- hosts: web[1-5].example.com    # web1 through web5
- hosts: web[a-c].example.com    # weba, webb, webc
```

### Boolean Operations

**AND (intersection - colon or &):**
```yaml
- hosts: webservers:&production  # Hosts in BOTH groups
- hosts: webservers:&us_east     # Web servers in US East
```

**OR (union - comma or :):**
```yaml
- hosts: webservers:databases    # Hosts in EITHER group
- hosts: webservers,databases    # Same as above
```

**NOT (exclusion - exclamation mark):**
```yaml
- hosts: webservers:!staging     # Web servers NOT in staging
- hosts: all:!databases          # All hosts except databases
```

### Complex Patterns

**Combine operations:**
```yaml
# Production web servers not in maintenance
- hosts: webservers:&production:!maintenance

# US East web or database servers
- hosts: (webservers:databases):&us_east

# All production servers except databases
- hosts: production:!databases
```

### Regex Patterns

Use `~` prefix for regex:

```yaml
- hosts: ~web[0-9]+\.example\.com     # web1, web2, web10, etc.
- hosts: ~(web|app).*\.example\.com   # Hosts starting with web or app
```

### Inventory-Based Patterns

**Sample inventory:**
```ini
[webservers]
web1.example.com
web2.example.com
web3.example.com

[databases]
db1.example.com
db2.example.com

[us_east]
web1.example.com
db1.example.com

[us_west]
web2.example.com
db2.example.com

[production]
web1.example.com
web2.example.com
db1.example.com

[staging]
web3.example.com
db2.example.com
```

**Pattern examples:**
```yaml
# Only production web servers in US East
- hosts: webservers:&production:&us_east
# Result: web1.example.com

# All databases not in production
- hosts: databases:!production
# Result: db2.example.com

# Web or database servers in US West
- hosts: (webservers:databases):&us_west
# Result: web2.example.com, db2.example.com
```

### Command Line Usage

**Ad-hoc commands:**
```bash
# Single group
ansible webservers -m ping

# Multiple groups
ansible webservers:databases -m ping

# Pattern with exclusion
ansible all:!staging -m shell -a "uptime"

# Intersection
ansible webservers:&production -m service -a "name=httpd state=restarted"

# Complex pattern
ansible "webservers:&production:!maintenance" -m ping
```

**Playbook with --limit:**
```bash
# Run playbook on subset of hosts
ansible-playbook site.yml --limit webservers

# Run on specific host
ansible-playbook site.yml --limit web1.example.com

# Run on pattern
ansible-playbook site.yml --limit "webservers:&us_east"

# Exclude hosts
ansible-playbook site.yml --limit "all:!staging"
```

### Index-Based Selection

**First host in group:**
```yaml
- hosts: webservers[0]
```

**Specific index:**
```yaml
- hosts: webservers[2]      # Third server (0-indexed)
```

**Range:**
```yaml
- hosts: webservers[0:2]    # First three servers
- hosts: webservers[2:]     # Third server onwards
- hosts: webservers[:3]     # First four servers
```

**Last server:**
```yaml
- hosts: webservers[-1]
```

### Practical Examples

**1. Maintenance on specific environment:**
```yaml
---
- name: Update staging web servers
  hosts: webservers:&staging
  become: yes
  tasks:
    - name: Update packages
      yum:
        name: '*'
        state: latest
```

**2. Deploy to production, excluding maintenance:**
```yaml
---
- name: Deploy to active production servers
  hosts: production:!maintenance
  tasks:
    - name: Deploy application
      copy:
        src: app.jar
        dest: /opt/app/
```

**3. Regional deployment:**
```yaml
---
- name: Update US East data centers
  hosts: all:&us_east
  tasks:
    - name: Configure regional settings
      template:
        src: config.j2
        dest: /etc/app/config.conf
```

**4. Canary deployment (first server only):**
```yaml
---
- name: Canary deployment
  hosts: webservers[0]
  tasks:
    - name: Deploy to canary
      copy:
        src: app-v2.jar
        dest: /opt/app/

- name: Full deployment after canary success
  hosts: webservers[1:]
  tasks:
    - name: Deploy to remaining servers
      copy:
        src: app-v2.jar
        dest: /opt/app/
```

**5. Multi-tier application:**
```yaml
---
- name: Configure frontend
  hosts: (webservers:loadbalancers):&production
  tasks:
    - name: Configure frontend tier
      # Tasks here

- name: Configure backend
  hosts: (appservers:databases):&production
  tasks:
    - name: Configure backend tier
      # Tasks here
```

### Dynamic Patterns with Variables

```yaml
---
- name: Deploy to specific environment
  hosts: "{{ target_env }}"
  tasks:
    - name: Deploy
      # Tasks here
```

**Run with:**
```bash
ansible-playbook site.yml -e "target_env=webservers:&production"
```

### Using --limit Creatively

**List matching hosts:**
```bash
# See which hosts match a pattern
ansible-playbook site.yml --list-hosts --limit "webservers:&production"
```

**Step-by-step deployment:**
```bash
# Deploy to one server at a time
ansible-playbook site.yml --limit web1.example.com
ansible-playbook site.yml --limit web2.example.com
```

**Retry failed hosts:**
```bash
# Run playbook
ansible-playbook site.yml

# Retry only failed hosts (Ansible creates retry file)
ansible-playbook site.yml --limit @/path/to/site.retry
```

### Best Practices

1. **Use meaningful group names**: `production` not `group1`
2. **Organize inventory logically**: By environment, location, function
3. **Test patterns first**: Use `--list-hosts` to verify
4. **Document complex patterns**: Add comments explaining logic
5. **Use variables for dynamic targeting**: Make playbooks flexible
6. **Leverage multiple group memberships**: Intersect groups for precision
7. **Quote complex patterns**: Prevent shell interpretation

### Common Patterns Reference

```yaml
# All hosts
hosts: all

# Single host
hosts: hostname.example.com

# Single group
hosts: webservers

# Multiple groups (OR)
hosts: webservers:databases

# Group intersection (AND)
hosts: webservers:&production

# Group exclusion (NOT)
hosts: all:!staging

# Wildcard
hosts: web*.example.com

# Range
hosts: web[1-5].example.com

# Complex combination
hosts: (webservers:appservers):&production:!maintenance

# First host in group
hosts: webservers[0]

# Regex
hosts: ~web\d+\.example\.com
```

### Testing Patterns

**List hosts matching pattern:**
```bash
ansible-playbook site.yml --list-hosts
ansible all --list-hosts
ansible "webservers:&production" --list-hosts
```

**Verify pattern before execution:**
```bash
# Check mode (dry run)
ansible-playbook site.yml --check --diff

# What hosts would be affected?
ansible-playbook site.yml --list-hosts --limit "pattern"
```

### Complete Example

**Playbook with multiple plays and patterns:**
```yaml
---
# Update all production servers except those in maintenance
- name: System updates
  hosts: production:!maintenance
  become: yes
  tasks:
    - name: Update packages
      yum:
        name: '*'
        state: latest

# Configure only web servers in US East
- name: Regional web server configuration
  hosts: webservers:&us_east
  tasks:
    - name: Deploy regional config
      template:
        src: us-east-config.j2
        dest: /etc/app/config.conf

# Database maintenance - one at a time
- name: Database optimization
  hosts: databases:&production
  serial: 1
  tasks:
    - name: Optimize database
      command: /usr/local/bin/optimize_db.sh

# Canary deployment - test on one server first
- name: Canary deployment
  hosts: webservers[0]
  tasks:
    - name: Deploy to canary
      copy:
        src: app-v2.jar
        dest: /opt/app/

# Full deployment to remaining servers
- name: Full deployment
  hosts: webservers[1:]:&production
  serial: 25%
  tasks:
    - name: Deploy to production
      copy:
        src: app-v2.jar
        dest: /opt/app/
```

### Running Examples

```bash
# Run entire playbook
ansible-playbook site.yaml

# Target specific pattern
ansible-playbook site.yaml --limit "webservers:&production"

# Exclude hosts
ansible-playbook site.yaml --limit "all:!staging"

# Single host
ansible-playbook site.yaml --limit web1.example.com

# List what would be targeted
ansible-playbook site.yaml --list-hosts
```

### Summary

Host patterns provide:
- ✅ Precise host targeting
- ✅ Flexible group combinations
- ✅ Dynamic scope control
- ✅ Safe deployment strategies
- ✅ Environment isolation
- ✅ Regional deployments
- ✅ Canary and rolling updates

Congratulations on completing the 30-day Ansible Bootcamp! You now have comprehensive knowledge of Ansible automation from basics to advanced topics.
