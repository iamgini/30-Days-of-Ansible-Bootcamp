## Ansible Custom Facts

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Custom facts (also called local facts) allow you to define your own facts on managed nodes that Ansible can discover and use. These facts persist across playbook runs and can provide application-specific or environment-specific information.

### What are Custom Facts?

Custom facts are user-defined facts stored on the managed node in `/etc/ansible/facts.d/`. Ansible automatically discovers and loads these facts during the gather_facts phase.

### Creating Custom Facts

Custom facts must be:
- Located in `/etc/ansible/facts.d/` directory on the managed node
- Have a `.fact` extension
- Be in INI, JSON, or executable format
- Return valid JSON (for executable scripts)

### INI Format

**File: /etc/ansible/facts.d/custom.fact**
```ini
[general]
app_name=MyApplication
app_version=2.1.0
environment=production

[database]
db_host=db.example.com
db_port=5432
db_name=myapp_db
```

**Accessing in playbook:**
```yaml
- name: Show custom facts
  debug:
    msg: "App: {{ ansible_local.custom.general.app_name }} v{{ ansible_local.custom.general.app_version }}"
```

### JSON Format

**File: /etc/ansible/facts.d/app_config.fact**
```json
{
  "application": {
    "name": "MyApp",
    "version": "2.1.0",
    "port": 8080
  },
  "features": {
    "caching": true,
    "monitoring": true
  }
}
```

**Accessing in playbook:**
```yaml
- name: Show app port
  debug:
    msg: "Application port: {{ ansible_local.app_config.application.port }}"
```

### Executable Scripts

Custom facts can be executable scripts that output JSON:

**File: /etc/ansible/facts.d/system_info.fact** (executable)
```bash
#!/bin/bash
cat <<EOF
{
  "disk_usage": "$(df -h / | awk 'NR==2 {print $5}')",
  "active_users": $(who | wc -l),
  "last_boot": "$(uptime -s)"
}
EOF
```

**Make it executable:**
```bash
chmod +x /etc/ansible/facts.d/system_info.fact
```

**Accessing:**
```yaml
- name: Show disk usage
  debug:
    msg: "Disk usage: {{ ansible_local.system_info.disk_usage }}"
```

### Python Script Example

**File: /etc/ansible/facts.d/app_status.fact**
```python
#!/usr/bin/env python3
import json
import subprocess

def get_app_status():
    try:
        result = subprocess.run(['systemctl', 'is-active', 'myapp'], 
                              capture_output=True, text=True)
        active = result.stdout.strip() == 'active'
    except:
        active = False
    
    return {
        'app_running': active,
        'app_name': 'myapp',
        'check_time': subprocess.run(['date', '+%Y-%m-%d %H:%M:%S'],
                                    capture_output=True, text=True).stdout.strip()
    }

if __name__ == '__main__':
    print(json.dumps(get_app_status()))
```

### Creating Custom Facts with Ansible

**Deploy custom facts from playbook:**
```yaml
---
- name: Setup custom facts
  hosts: all
  become: yes
  tasks:
    - name: Create facts.d directory
      file:
        path: /etc/ansible/facts.d
        state: directory
        mode: '0755'
    
    - name: Deploy custom fact file
      copy:
        content: |
          [general]
          app_name=MyApp
          environment={{ env_name }}
          deployment_date={{ ansible_date_time.date }}
        dest: /etc/ansible/facts.d/app.fact
        mode: '0644'
    
    - name: Reload facts
      setup:
        filter: ansible_local
```

### Accessing Custom Facts

Custom facts are available under `ansible_local` namespace:

```yaml
# Structure: ansible_local.<filename_without_extension>.<section>.<key>

- name: Access INI fact
  debug:
    msg: "{{ ansible_local.custom.general.app_name }}"

- name: Access JSON fact
  debug:
    msg: "{{ ansible_local.app_config.application.name }}"

- name: Access all custom facts
  debug:
    var: ansible_local
```

### Use Cases

**1. Application configuration:**
```ini
# /etc/ansible/facts.d/webapp.fact
[config]
version=2.1.0
port=8080
ssl_enabled=true
max_connections=1000
```

**2. Environment identification:**
```json
{
  "environment": "production",
  "datacenter": "us-east-1",
  "tier": "frontend",
  "maintenance_window": "Sunday 02:00-04:00"
}
```

**3. Dynamic status information:**
```bash
#!/bin/bash
# /etc/ansible/facts.d/metrics.fact
echo "{
  \"cpu_load\": \"$(uptime | awk -F'load average:' '{ print $2 }')\",
  \"free_memory_mb\": $(free -m | awk 'NR==2{print $4}'),
  \"disk_free_pct\": \"$(df -h / | awk 'NR==2{print $4}')\"
}"
```

**4. Installed software versions:**
```python
#!/usr/bin/env python3
# /etc/ansible/facts.d/versions.fact
import json
import subprocess

def get_version(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return "not_installed"

facts = {
    "nginx": get_version("nginx -v 2>&1 | awk '{print $3}'"),
    "python": get_version("python3 --version | awk '{print $2}'"),
    "node": get_version("node --version")
}

print(json.dumps(facts))
```

### Using Custom Facts in Playbooks

**Conditional tasks:**
```yaml
- name: Enable monitoring
  service:
    name: monitoring-agent
    state: started
  when: ansible_local.app_config.features.monitoring == true
```

**Template configuration:**
```yaml
- name: Configure application
  template:
    src: app.conf.j2
    dest: /etc/app/app.conf
```

**app.conf.j2:**
```jinja2
[app]
name = {{ ansible_local.webapp.config.version }}
port = {{ ansible_local.webapp.config.port }}
ssl = {{ ansible_local.webapp.config.ssl_enabled }}
```

### Refreshing Custom Facts

Facts are gathered once per play. To reload after creating/modifying:

```yaml
- name: Update custom fact
  copy:
    content: |
      {"version": "3.0.0"}
    dest: /etc/ansible/facts.d/app.fact

- name: Reload facts
  setup:
    filter: ansible_local
    
- name: Use updated fact
  debug:
    msg: "New version: {{ ansible_local.app.version }}"
```

### Best Practices

1. **Use descriptive filenames**: `app_config.fact` instead of `custom.fact`
2. **Validate JSON**: Ensure executable scripts output valid JSON
3. **Handle errors**: Scripts should handle failures gracefully
4. **Keep it lightweight**: Don't run expensive operations
5. **Document format**: Add comments in INI files
6. **Version your facts**: Include version info in custom facts
7. **Test executables**: Verify scripts work independently
8. **Set permissions**: Ensure facts are readable by Ansible

### Debugging Custom Facts

**View all local facts:**
```bash
ansible hostname -m setup -a "filter=ansible_local"
```

**Test fact script manually:**
```bash
# SSH to managed node
/etc/ansible/facts.d/my_script.fact

# Should output valid JSON
```

**Troubleshooting:**
- Check file permissions (must be readable)
- Verify JSON syntax (use `jq` or `python -m json.tool`)
- Ensure executables have proper shebang
- Check directory exists: `/etc/ansible/facts.d/`

### Complete Example

**Playbook:**
```yaml
---
- name: Custom Facts Demo
  hosts: nodes
  become: yes
  tasks:
    - name: Create facts directory
      file:
        path: /etc/ansible/facts.d
        state: directory
        
    - name: Deploy custom fact
      copy:
        content: |
          [application]
          name=WebApp
          version=1.0.0
          environment=production
        dest: /etc/ansible/facts.d/myapp.fact
        
    - name: Refresh facts
      setup:
        filter: ansible_local
        
    - name: Display custom facts
      debug:
        msg: "Running {{ ansible_local.myapp.application.name }} v{{ ansible_local.myapp.application.version }} in {{ ansible_local.myapp.application.environment }}"
```

### Running the Example

```bash
ansible-playbook site.yaml
```

This will create, deploy, and display custom facts on your managed nodes.
