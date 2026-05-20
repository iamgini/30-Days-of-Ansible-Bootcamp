## Conditional Execution

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Conditional execution allows tasks to run only when specific conditions are met. This makes playbooks adaptable to different environments, operating systems, and states.

### Basic when Statement

```yaml
- name: Install Apache on RedHat
  yum:
    name: httpd
    state: present
  when: ansible_os_family == "RedHat"

- name: Install Apache on Debian
  apt:
    name: apache2
    state: present
  when: ansible_os_family == "Debian"
```

### Common Conditional Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Equal to | `when: ansible_distribution == "CentOS"` |
| `!=` | Not equal to | `when: ansible_distribution != "Ubuntu"` |
| `>` | Greater than | `when: ansible_memtotal_mb > 1024` |
| `<` | Less than | `when: ansible_processor_vcpus < 4` |
| `>=` | Greater or equal | `when: ansible_distribution_version >= "8"` |
| `<=` | Less or equal | `when: ansible_distribution_version <= "7"` |
| `in` | In list | `when: "'webserver' in group_names"` |
| `not in` | Not in list | `when: "'database' not in group_names"` |

### Boolean Conditions

```yaml
# Variable is defined
- name: Task runs if var is defined
  debug:
    msg: "Variable exists"
  when: my_variable is defined

# Variable is undefined
- name: Task runs if var is undefined
  debug:
    msg: "Variable doesn't exist"
  when: my_variable is not defined

# Boolean true/false
- name: Enable feature
  command: /usr/local/bin/enable_feature
  when: enable_feature | bool

# Variable is empty
- name: Check if empty
  debug:
    msg: "List is empty"
  when: my_list | length == 0
```

### Logical Operators

**AND condition:**
```yaml
- name: Install on production RedHat systems
  yum:
    name: monitoring-agent
    state: present
  when:
    - ansible_os_family == "RedHat"
    - "'production' in group_names"
```

**OR condition:**
```yaml
- name: Install on Ubuntu or Debian
  apt:
    name: package
    state: present
  when: ansible_distribution == "Ubuntu" or ansible_distribution == "Debian"
```

**Complex conditions:**
```yaml
- name: Complex condition
  debug:
    msg: "Condition met"
  when: >
    (ansible_distribution == "CentOS" and ansible_distribution_major_version == "8") or
    (ansible_distribution == "Ubuntu" and ansible_distribution_version >= "20.04")
```

### Conditionals with Facts

```yaml
# Based on OS
- name: RedHat specific task
  yum:
    name: httpd
  when: ansible_os_family == "RedHat"

# Based on memory
- name: Configure for high-memory systems
  template:
    src: high-memory.conf.j2
    dest: /etc/app/config.conf
  when: ansible_memtotal_mb > 16384

# Based on network
- name: Configure firewall
  firewalld:
    port: 8080/tcp
    permanent: yes
    state: enabled
  when: ansible_default_ipv4.address is defined
```

### Conditionals with Registered Variables

```yaml
- name: Check if file exists
  stat:
    path: /etc/app/config.conf
  register: config_file

- name: Copy default config if not exists
  copy:
    src: default-config.conf
    dest: /etc/app/config.conf
  when: not config_file.stat.exists

# Check command result
- name: Check if service is installed
  command: which nginx
  register: nginx_check
  ignore_errors: yes

- name: Install nginx if not present
  yum:
    name: nginx
    state: present
  when: nginx_check.rc != 0
```

### Conditionals in Loops

```yaml
- name: Create production users only
  user:
    name: "{{ item.name }}"
    state: present
  loop: "{{ users }}"
  when: item.env == "production"

# Multiple conditions in loop
- name: Install specific packages
  yum:
    name: "{{ item.package }}"
    state: present
  loop:
    - { package: 'httpd', os: 'RedHat', required: true }
    - { package: 'nginx', os: 'Debian', required: true }
    - { package: 'vim', os: 'all', required: false }
  when: 
    - item.required | bool
    - item.os == ansible_os_family or item.os == "all"
```

### Conditionals with Group Membership

```yaml
- name: Configure webservers
  template:
    src: web.conf.j2
    dest: /etc/web/web.conf
  when: "'webservers' in group_names"

- name: Install database tools on db servers
  yum:
    name: postgresql-client
    state: present
  when: inventory_hostname in groups['databases']
```

### Failed/Changed/Skipped Conditions

```yaml
- name: Attempt package installation
  yum:
    name: some-package
    state: present
  register: install_result
  ignore_errors: yes

- name: Use alternative if failed
  yum:
    name: alternative-package
    state: present
  when: install_result is failed

- name: Restart service if config changed
  service:
    name: myapp
    state: restarted
  when: config_update is changed
```

### Version Comparisons

```yaml
- name: Run on Ansible 2.9+
  debug:
    msg: "Running on modern Ansible"
  when: ansible_version.full is version('2.9', '>=')

- name: Check OS version
  yum:
    name: new-package
    state: present
  when: ansible_distribution_version is version('8.0', '>=')
```

### String Matching

```yaml
# Exact match
- name: Match exact hostname
  debug:
    msg: "This is web1"
  when: inventory_hostname == "web1.example.com"

# Regex match
- name: Match hostname pattern
  debug:
    msg: "This is a web server"
  when: inventory_hostname is regex("web.*\.example\.com")

# Contains
- name: Check if string contains
  debug:
    msg: "Contains 'prod'"
  when: "'prod' in inventory_hostname"

# Starts with
- name: Starts with check
  debug:
    msg: "Hostname starts with web"
  when: inventory_hostname is regex("^web")
```

### File/Path Conditions

```yaml
- name: Check if file exists
  stat:
    path: /etc/myapp/config
  register: config

- name: Tasks based on file state
  debug:
    msg: "File exists and is {{ 'directory' if config.stat.isdir else 'file' }}"
  when: config.stat.exists
```

### Practical Examples

**1. OS-specific package management:**
```yaml
- name: Install web server
  package:
    name: "{{ 'httpd' if ansible_os_family == 'RedHat' else 'apache2' }}"
    state: present
  when: ansible_os_family in ['RedHat', 'Debian']
```

**2. Environment-based configuration:**
```yaml
- name: Deploy production config
  template:
    src: prod.conf.j2
    dest: /etc/app/app.conf
  when: "'production' in group_names"

- name: Deploy development config
  template:
    src: dev.conf.j2
    dest: /etc/app/app.conf
  when: "'development' in group_names"
```

**3. Conditional service management:**
```yaml
- name: Check if service exists
  stat:
    path: /etc/systemd/system/myapp.service
  register: service_file

- name: Start service if exists
  service:
    name: myapp
    state: started
  when: service_file.stat.exists
```

**4. First-time setup:**
```yaml
- name: Check if initialized
  stat:
    path: /var/lib/app/.initialized
  register: init_status

- name: Run initialization
  command: /usr/local/bin/initialize.sh
  when: not init_status.stat.exists

- name: Create init marker
  file:
    path: /var/lib/app/.initialized
    state: touch
  when: not init_status.stat.exists
```

### assert Module

```yaml
- name: Validate requirements
  assert:
    that:
      - ansible_distribution == "CentOS"
      - ansible_distribution_major_version == "8"
      - ansible_memtotal_mb >= 2048
    fail_msg: "System does not meet requirements"
    success_msg: "System requirements validated"
```

### Best Practices

1. **Use facts for OS detection**: More reliable than hardcoding
2. **Group related conditions**: Use lists for AND, `or` for OR
3. **Document complex conditions**: Add comments
4. **Test both paths**: Ensure tasks work when condition is true/false
5. **Use `default()` filter**: Provide fallback values
6. **Avoid deep nesting**: Refactor complex conditions
7. **Use variables for readability**: Define condition once, reuse

### Example: Complete Conditional Playbook

```yaml
---
- name: Conditional deployment
  hosts: all
  become: yes
  tasks:
    - name: Set facts based on environment
      set_fact:
        is_production: "{{ 'production' in group_names }}"
        is_webserver: "{{ 'webservers' in group_names }}"
    
    - name: Install web server (RedHat)
      yum:
        name: httpd
        state: present
      when:
        - is_webserver | bool
        - ansible_os_family == "RedHat"
    
    - name: Install web server (Debian)
      apt:
        name: apache2
        state: present
      when:
        - is_webserver | bool
        - ansible_os_family == "Debian"
    
    - name: Configure production settings
      template:
        src: prod.conf.j2
        dest: /etc/app/app.conf
      when: is_production | bool
      notify: restart app
    
    - name: Enable monitoring in production
      service:
        name: monitoring-agent
        state: started
        enabled: yes
      when:
        - is_production | bool
        - ansible_memtotal_mb > 1024
  
  handlers:
    - name: restart app
      service:
        name: myapp
        state: restarted
```

### Running the Example

```bash
ansible-playbook site.yaml
```

Tasks will execute conditionally based on facts, variables, and group membership.
