## Ansible Variable Arrays and Dictionaries

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Ansible supports complex data structures like lists (arrays) and dictionaries (hashes). These allow you to organize related data together and iterate over multiple values efficiently.

### Lists (Arrays)

A list is an ordered collection of values.

**Simple list:**
```yaml
packages:
  - httpd
  - firewalld
  - vim
  - git
```

**Usage in tasks:**
```yaml
- name: Install packages
  yum:
    name: "{{ packages }}"
    state: latest
```

**Accessing list items:**
```yaml
first_package: "{{ packages[0] }}"     # httpd
second_package: "{{ packages[1] }}"    # firewalld
```

### Dictionaries (Hashes/Maps)

A dictionary is a collection of key-value pairs.

**Simple dictionary:**
```yaml
web_service:
  package: httpd
  service: httpd
  port: 80
  config: /etc/httpd/conf/httpd.conf
```

**Usage in tasks:**
```yaml
- name: Install {{ web_service.package }}
  yum:
    name: "{{ web_service.package }}"
    state: latest

- name: Start {{ web_service.service }}
  service:
    name: "{{ web_service.service }}"
    port: "{{ web_service.port }}"
```

**Accessing dictionary values:**
```yaml
# Dot notation
package_name: "{{ web_service.package }}"

# Bracket notation (useful for keys with special characters)
package_name: "{{ web_service['package'] }}"
```

### Nested Structures

You can combine lists and dictionaries for complex data:

**user_list.yaml:**
```yaml
users:
  john:
    firstname: John
    lastname: Smith
    designation: Admin
    location: London
  linda:
    firstname: Linda
    lastname: Marry
    designation: Operator
    location: NewYork
```

### Iterating Over Lists

**With simple list:**
```yaml
- name: Install multiple packages
  yum:
    name: "{{ item }}"
    state: latest
  loop:
    - httpd
    - firewalld
    - vim
```

**With variable:**
```yaml
vars:
  packages:
    - httpd
    - firewalld
    - vim

tasks:
  - name: Install packages
    yum:
      name: "{{ item }}"
      state: latest
    loop: "{{ packages }}"
```

### Iterating Over Dictionaries

**Method 1: Using dict2items filter:**
```yaml
- name: Show user information
  debug:
    msg: "User {{ item.key }}: {{ item.value.firstname }} {{ item.value.lastname }}"
  loop: "{{ users | dict2items }}"
```

**Method 2: Using with_dict (legacy):**
```yaml
- name: Create users
  user:
    name: "{{ item.key }}"
    comment: "{{ item.value.firstname }} {{ item.value.lastname }}"
  with_dict: "{{ users }}"
```

### List of Dictionaries

A common pattern for structured data:

```yaml
servers:
  - name: web1
    ip: 192.168.1.10
    role: webserver
  - name: db1
    ip: 192.168.1.20
    role: database
  - name: lb1
    ip: 192.168.1.30
    role: loadbalancer
```

**Iterating:**
```yaml
- name: Configure servers
  debug:
    msg: "Server {{ item.name }} ({{ item.ip }}) - Role: {{ item.role }}"
  loop: "{{ servers }}"
```

### Accessing Nested Values

**Example data:**
```yaml
users:
  john:
    firstname: John
    lastname: Smith
    designation: Admin
    location: London
```

**Accessing:**
```yaml
# Get John's location
john_location: "{{ users.john.location }}"        # London
john_location: "{{ users['john']['location'] }}"  # Also works

# Get all users' names
user_names: "{{ users.keys() | list }}"           # ['john', 'linda']
```

### Combining Variables

**Merging lists:**
```yaml
base_packages:
  - vim
  - git

web_packages:
  - httpd
  - mod_ssl

all_packages: "{{ base_packages + web_packages }}"
```

**Merging dictionaries:**
```yaml
defaults:
  port: 80
  protocol: http

overrides:
  port: 443
  protocol: https

final_config: "{{ defaults | combine(overrides) }}"
# Result: { port: 443, protocol: https }
```

### Example Playbook

**site.yaml:**
```yaml
---
- name: Create users
  hosts: nodes
  become: true
  vars_files:
    - user_list.yaml 
  tasks:
    - name: Show all users
      debug:
        msg: "{{ users }}"
    
    - name: Show each user's details
      debug:
        msg: "{{ item.value.firstname }} {{ item.value.lastname }} - {{ item.value.designation }} from {{ item.value.location }}"
      loop: "{{ users | dict2items }}"
```

### Useful Filters for Arrays/Dictionaries

```yaml
# Get list length
package_count: "{{ packages | length }}"

# Get dictionary keys
user_names: "{{ users.keys() | list }}"

# Get dictionary values
user_data: "{{ users.values() | list }}"

# Convert dict to list of items
user_items: "{{ users | dict2items }}"

# Convert list of items back to dict
users_dict: "{{ user_items | items2dict }}"

# Select specific attribute from list of dicts
server_names: "{{ servers | map(attribute='name') | list }}"
```

### Best Practices

1. **Use meaningful names**: `web_servers` instead of `servers1`
2. **Group related data**: Use dictionaries for related properties
3. **Keep it simple**: Don't over-nest; 2-3 levels max
4. **Document structure**: Add comments explaining complex structures
5. **Validate data**: Check for required keys before using them
6. **Use defaults**: Provide fallback values for optional fields

### Running the Example

```bash
ansible-playbook site.yaml
```

This will display the user data from the dictionary structure.

### Common Patterns

**1. Service configuration:**
```yaml
services:
  web:
    package: httpd
    port: 80
  database:
    package: postgresql
    port: 5432
```

**2. Environment configuration:**
```yaml
environments:
  production:
    db_host: prod-db.example.com
    api_key: "{{ vault_prod_api_key }}"
  staging:
    db_host: staging-db.example.com
    api_key: "{{ vault_staging_api_key }}"
```

**3. User management:**
```yaml
users:
  - name: john
    groups: ['wheel', 'developers']
    state: present
  - name: jane
    groups: ['operators']
    state: present
```
