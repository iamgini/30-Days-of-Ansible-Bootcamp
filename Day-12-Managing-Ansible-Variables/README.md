## Managing Ansible Variables

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Variable Basics

Variables in Ansible make your playbooks flexible and reusable. Instead of hardcoding values, you can use variables to adapt playbooks for different environments, packages, or configurations.

**Variable Naming Rules:**

| Valid Variable Names | Invalid Names |
| -------------------- | ------------- |
| file_name            | file name     |
| new_server           | new.server    |
| webserver_1          | 1st webserver |
| router_ip_101        | router-ip-$1  |

- Must start with a letter
- Can contain letters, numbers, and underscores
- Cannot contain spaces, dots, or special characters
- Cannot start with numbers

### Defining Variables

You can define variables at different scopes in Ansible:

**1. Play Scope (inline in playbook):**
```yaml
---
- name: Example playbook
  hosts: webservers
  vars:
    web_package: httpd
    web_service: httpd
  tasks:
    - name: Install {{ web_package }}
      yum:
        name: "{{ web_package }}"
```

**2. External Variable Files:**
```yaml
---
- name: Example playbook
  hosts: webservers
  vars_files:
    - vars.yaml
  tasks:
    - name: Install {{ web_package }}
      yum:
        name: "{{ web_package }}"
```

**3. Command Line (extra vars):**
```bash
ansible-playbook site.yml -e "nodes=webservers"
```

### Using Variables in Tasks

Variables are referenced using Jinja2 syntax `{{ variable_name }}`:

```yaml
- name: Install {{ web_package }}
  yum:
    name: "{{ web_package }}"
    state: latest
```

**Important:** Always quote strings that start with variables:
```yaml
name: "{{ web_package }}"  # Correct
name: {{ web_package }}    # May cause YAML parsing errors
```

### Example Playbook

This example demonstrates using external variable files:

**vars.yaml:**
```yaml
web_package: httpd
web_service: httpd
firewall_package: firewalld
firewall_service: firewalld
```

**site.yml:**
```yaml
---
- name: Install and configure httpd
  hosts: "{{ nodes }}"
  become: yes
  vars_files:
    - vars.yaml
  tasks:
    - name: Install {{ web_package }} & {{ firewall_package }}
      yum:
        name: 
          - "{{ web_package }}"
          - "{{ firewall_package }}"
        state: latest
        
    - name: Enable and Start {{ web_service }}
      service:
        name: "{{ web_service }}"
        enabled: true
        state: started
```

### Running the Playbook

```bash
# Using extra variable for nodes
ansible-playbook site.yml -e "nodes=webservers"

# Or specify specific host
ansible-playbook site.yml -e "nodes=node1.example.com"
```

### Variable Precedence

Ansible has a specific order for variable precedence (from lowest to highest):
1. Role defaults
2. Inventory variables
3. Playbook vars_files
4. Playbook vars
5. Extra vars (-e on command line) - **highest priority**

### Best Practices

- Use descriptive variable names
- Group related variables in separate files
- Document variable purposes in comments
- Use defaults for optional variables
- Store sensitive data in Ansible Vault (covered in Day 20-21)
