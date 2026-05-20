## Jinja2 Templates

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Jinja2 is a powerful templating engine used by Ansible to generate dynamic configuration files, scripts, and web pages. It allows you to use variables, loops, conditionals, and filters to create flexible templates.

### Basic Template Syntax

**Template file (config.j2):**
```jinja2
# Application Configuration
app_name = {{ app_name }}
app_port = {{ app_port }}
debug_mode = {{ debug_mode | default('false') }}
```

**Playbook:**
```yaml
- name: Deploy configuration
  template:
    src: config.j2
    dest: /etc/app/config.conf
  vars:
    app_name: "MyApp"
    app_port: 8080
    debug_mode: "true"
```

### Variable Substitution

**Simple variables:**
```jinja2
Hostname: {{ ansible_hostname }}
IP Address: {{ ansible_default_ipv4.address }}
OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
```

**Dictionary access:**
```jinja2
{# Dot notation #}
Database Host: {{ database.host }}
Database Port: {{ database.port }}

{# Bracket notation #}
Database Host: {{ database['host'] }}
Database Port: {{ database['port'] }}
```

**List access:**
```jinja2
First server: {{ servers[0] }}
Second server: {{ servers[1] }}
```

### Comments

```jinja2
{# This is a comment - won't appear in output #}

{# 
Multi-line comment
Anything here is ignored
#}
```

### Conditionals

**If statement:**
```jinja2
{% if ansible_os_family == "RedHat" %}
# RedHat-based system
package_manager = yum
{% elif ansible_os_family == "Debian" %}
# Debian-based system
package_manager = apt
{% else %}
# Other system
package_manager = unknown
{% endif %}
```

**Inline conditional (ternary operator):**
```jinja2
Environment = {{ 'production' if is_prod else 'development' }}
Debug = {{ 'enabled' if debug_mode | bool else 'disabled' }}
```

**Check if variable is defined:**
```jinja2
{% if db_password is defined %}
Database Password = {{ db_password }}
{% else %}
# No database password configured
{% endif %}
```

### Loops

**Simple loop:**
```jinja2
# Installed Packages:
{% for package in packages %}
- {{ package }}
{% endfor %}
```

**Loop with index:**
```jinja2
{% for server in servers %}
Server {{ loop.index }}: {{ server }}
{% endfor %}
```

**Loop over dictionary:**
```jinja2
{% for key, value in database_config.items() %}
{{ key }} = {{ value }}
{% endfor %}
```

**Loop variables:**
- `loop.index` - Current iteration (1-indexed)
- `loop.index0` - Current iteration (0-indexed)
- `loop.first` - True on first iteration
- `loop.last` - True on last iteration
- `loop.length` - Total iterations

**Example with loop variables:**
```jinja2
{% for user in users %}
User {{ loop.index }}/{{ loop.length }}: {{ user.name }}
  {% if loop.first %}
  # First user - admin privileges
  {% endif %}
  {% if loop.last %}
  # Last user
  {% endif %}
{% endfor %}
```

### Filters

Filters transform variable values:

**String filters:**
```jinja2
Uppercase: {{ name | upper }}
Lowercase: {{ name | lower }}
Capitalize: {{ name | capitalize }}
Title Case: {{ name | title }}
Replace: {{ text | replace('old', 'new') }}
```

**Default values:**
```jinja2
Port: {{ port | default('8080') }}
Host: {{ host | default('localhost') }}
```

**Number filters:**
```jinja2
Rounded: {{ 3.14159 | round(2) }}
Absolute: {{ -42 | abs }}
Integer: {{ "42" | int }}
Float: {{ "3.14" | float }}
```

**List filters:**
```jinja2
First item: {{ my_list | first }}
Last item: {{ my_list | last }}
Length: {{ my_list | length }}
Join: {{ my_list | join(', ') }}
Sort: {{ my_list | sort }}
Unique: {{ my_list | unique }}
```

**JSON/YAML:**
```jinja2
{% set my_dict = {'name': 'John', 'age': 30} %}
JSON: {{ my_dict | to_json }}
YAML: {{ my_dict | to_yaml }}
Pretty JSON: {{ my_dict | to_nice_json }}
```

**Type checking:**
```jinja2
{% if port is number %}
Port is a number
{% endif %}

{% if servers is list %}
Servers is a list
{% endif %}
```

### Practical Examples

**1. System information template:**
```jinja2
# System Information Report
# Generated on {{ ansible_date_time.iso8601 }}

Hostname: {{ ansible_hostname }}
FQDN: {{ ansible_fqdn }}
OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
Kernel: {{ ansible_kernel }}
Architecture: {{ ansible_architecture }}

CPU Cores: {{ ansible_processor_vcpus }}
Memory: {{ ansible_memtotal_mb }} MB

Network Interfaces:
{% for interface in ansible_interfaces %}
  - {{ interface }}: {{ hostvars[inventory_hostname]['ansible_' + interface]['ipv4']['address'] | default('N/A') }}
{% endfor %}

Disk Mounts:
{% for mount in ansible_mounts %}
  - {{ mount.mount }} ({{ mount.fstype }}): {{ mount.size_total | filesizeformat }}
{% endfor %}
```

**2. Web server configuration:**
```jinja2
# Nginx Configuration
# Generated for {{ ansible_hostname }}

server {
    listen {{ http_port | default('80') }};
    server_name {{ server_name }};
    
    root {{ document_root }};
    index index.html index.htm;
    
    {% if ssl_enabled | bool %}
    # SSL Configuration
    listen 443 ssl;
    ssl_certificate {{ ssl_cert_path }};
    ssl_certificate_key {{ ssl_key_path }};
    {% endif %}
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    {% if enable_php | default(false) | bool %}
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
    }
    {% endif %}
}
```

**3. Application configuration:**
```jinja2
[application]
name = {{ app_name }}
version = {{ app_version }}
environment = {{ environment | upper }}

[database]
host = {{ db_host }}
port = {{ db_port }}
name = {{ db_name }}
{% if environment == 'production' %}
pool_size = 50
timeout = 30
{% else %}
pool_size = 5
timeout = 10
{% endif %}

[features]
{% for feature, enabled in features.items() %}
{{ feature }} = {{ 'enabled' if enabled else 'disabled' }}
{% endfor %}

[servers]
{% for server in backend_servers %}
backend_{{ loop.index }} = {{ server.host }}:{{ server.port }}
{% endfor %}
```

**4. User list template:**
```jinja2
# User List
# Generated: {{ ansible_date_time.date }}

{% for user in users %}
Username: {{ user.name }}
Full Name: {{ user.fullname | default('N/A') }}
Email: {{ user.email | default(user.name + '@example.com') }}
Groups: {{ user.groups | join(', ') }}
{% if not loop.last %}
---
{% endif %}
{% endfor %}

Total Users: {{ users | length }}
```

**5. MOTD (Message of the Day):**
```jinja2
################################################################
#                Welcome to {{ ansible_hostname }}              #
################################################################

System Information:
  OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
  Kernel: {{ ansible_kernel }}
  CPU: {{ ansible_processor_vcpus }} cores
  Memory: {{ ansible_memtotal_mb }} MB
  IP: {{ ansible_default_ipv4.address }}

{% if 'production' in group_names %}
  *** PRODUCTION SYSTEM ***
  Unauthorized access is strictly prohibited
{% elif 'staging' in group_names %}
  *** STAGING ENVIRONMENT ***
{% else %}
  *** DEVELOPMENT SYSTEM ***
{% endif %}

Last update: {{ ansible_date_time.iso8601 }}
################################################################
```

### Advanced Features

**Macros (reusable blocks):**
```jinja2
{% macro server_block(name, port) %}
server {
    server_name {{ name }};
    listen {{ port }};
}
{% endmacro %}

{{ server_block('web1.example.com', 80) }}
{{ server_block('web2.example.com', 80) }}
```

**Set variables:**
```jinja2
{% set max_memory = ansible_memtotal_mb * 0.7 | int %}
Max Memory: {{ max_memory }} MB

{% set is_prod = 'production' in group_names %}
{% if is_prod %}
Production mode enabled
{% endif %}
```

**Whitespace control:**
```jinja2
{%- if condition -%}    {# Strip whitespace before and after #}
    Content
{%- endif -%}
```

### Template Module Options

```yaml
- name: Deploy template
  template:
    src: config.j2
    dest: /etc/app/config.conf
    owner: app
    group: app
    mode: '0644'
    backup: yes              # Create backup before replacing
    validate: 'check_config %s'  # Validate before applying
```

### Best Practices

1. **Use comments**: Explain complex logic
2. **Set defaults**: Use `| default()` filter
3. **Validate output**: Use `validate` parameter
4. **Keep templates focused**: One config per template
5. **Test templates**: Verify generated output
6. **Handle undefined variables**: Check `is defined`
7. **Format for readability**: Use proper indentation

### Complete Playbook Example

```yaml
---
- name: Deploy templates
  hosts: webservers
  become: yes
  vars:
    app_name: "MyWebApp"
    app_port: 8080
    enable_ssl: true
    backend_servers:
      - { host: '192.168.1.10', port: 8080 }
      - { host: '192.168.1.11', port: 8080 }
  tasks:
    - name: Deploy MOTD
      template:
        src: motd.j2
        dest: /etc/motd
        mode: '0644'
    
    - name: Deploy nginx config
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        validate: 'nginx -t -c %s'
      notify: reload nginx
    
    - name: Deploy application config
      template:
        src: app-config.j2
        dest: /etc/myapp/config.ini
        mode: '0600'
        backup: yes
      notify: restart app
  
  handlers:
    - name: reload nginx
      service:
        name: nginx
        state: reloaded
    
    - name: restart app
      service:
        name: myapp
        state: restarted
```

### Debugging Templates

**Test template output:**
```bash
# Generate template locally
ansible all -m template -a "src=config.j2 dest=/tmp/config.test" --check --diff
```

**View variables:**
```bash
# See all variables for a host
ansible hostname -m debug -a "var=hostvars[inventory_hostname]"
```

### Running the Example

```bash
ansible-playbook site.yaml
```

Templates will be generated with actual variable values and deployed to target hosts.
