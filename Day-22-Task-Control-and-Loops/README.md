## Task Control and Loops

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Loops allow you to repeat a task multiple times with different values, making your playbooks more efficient and reducing code duplication. Ansible provides several loop constructs for different use cases.

### Basic Loop Syntax

**Modern syntax (loop keyword):**
```yaml
- name: Install multiple packages
  yum:
    name: "{{ item }}"
    state: present
  loop:
    - httpd
    - firewalld
    - vim
```

**Loop over variable:**
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
      state: present
    loop: "{{ packages }}"
```

### Loop with List of Dictionaries

```yaml
- name: Create users
  user:
    name: "{{ item.name }}"
    state: present
    groups: "{{ item.groups }}"
  loop:
    - { name: 'john', groups: 'wheel' }
    - { name: 'jane', groups: 'developers' }
    - { name: 'bob', groups: 'operators' }
```

**Or using YAML list format:**
```yaml
- name: Create users
  user:
    name: "{{ item.name }}"
    groups: "{{ item.groups }}"
    password: "{{ item.password }}"
  loop:
    - name: john
      groups: wheel
      password: "{{ john_password }}"
    - name: jane
      groups: developers
      password: "{{ jane_password }}"
```

### Loop Control

**Index and item:**
```yaml
- name: Display with index
  debug:
    msg: "Item {{ loop_index }}: {{ item }}"
  loop:
    - apple
    - banana
    - cherry
```

**Loop variables:**
- `loop_index` - Current iteration (1-indexed)
- `loop_index0` - Current iteration (0-indexed)
- `loop_first` - True on first iteration
- `loop_last` - True on last iteration
- `loop_length` - Total number of items
- `loop_revindex` - Iterations remaining (1-indexed)
- `loop_revindex0` - Iterations remaining (0-indexed)

**Example with loop variables:**
```yaml
- name: Process items
  debug:
    msg: "Processing {{ item }} ({{ loop_index }}/{{ loop_length }})"
  loop: "{{ my_list }}"
```

### Nested Loops

**Using loop with subelements:**
```yaml
users:
  - name: john
    groups:
      - wheel
      - developers
  - name: jane
    groups:
      - operators

tasks:
  - name: Add users to groups
    user:
      name: "{{ item.0.name }}"
      groups: "{{ item.1 }}"
      append: yes
    loop: "{{ users | subelements('groups') }}"
```

**Product (Cartesian product):**
```yaml
- name: Create combinations
  debug:
    msg: "{{ item.0 }} - {{ item.1 }}"
  loop: "{{ ['a', 'b'] | product(['1', '2']) | list }}"
# Output: a-1, a-2, b-1, b-2
```

### Loop with Conditions

```yaml
- name: Install packages conditionally
  yum:
    name: "{{ item }}"
    state: present
  loop:
    - httpd
    - nginx
    - apache2
  when: item != "apache2" or ansible_os_family == "Debian"
```

### Loop with Register

```yaml
- name: Check multiple services
  systemd:
    name: "{{ item }}"
  loop:
    - httpd
    - firewalld
    - sshd
  register: service_status

- name: Show results
  debug:
    msg: "{{ item.item }} status: {{ item.status }}"
  loop: "{{ service_status.results }}"
```

### Loop Control Options

**Pause between iterations:**
```yaml
- name: Restart services one by one
  service:
    name: "{{ item }}"
    state: restarted
  loop:
    - service1
    - service2
    - service3
  loop_control:
    pause: 5    # Wait 5 seconds between iterations
```

**Custom loop variable name:**
```yaml
- name: Process users
  debug:
    msg: "Creating {{ user.name }}"
  loop: "{{ users }}"
  loop_control:
    loop_var: user    # Use 'user' instead of 'item'
```

**Label for cleaner output:**
```yaml
- name: Create users
  user:
    name: "{{ item.name }}"
    password: "{{ item.password }}"
  loop: "{{ users }}"
  loop_control:
    label: "{{ item.name }}"    # Only show name in output, not password
```

### Range Loop

**Create sequence of numbers:**
```yaml
- name: Create numbered files
  file:
    path: "/tmp/file{{ item }}.txt"
    state: touch
  loop: "{{ range(1, 11) | list }}"    # 1 through 10
```

**With step:**
```yaml
- name: Create even-numbered files
  file:
    path: "/tmp/file{{ item }}.txt"
    state: touch
  loop: "{{ range(0, 21, 2) | list }}"    # 0, 2, 4, ..., 20
```

### Loop with Dict

**Dictionary iteration:**
```yaml
vars:
  services:
    web: httpd
    database: postgresql
    cache: redis

tasks:
  - name: Install services
    yum:
      name: "{{ item.value }}"
      state: present
    loop: "{{ services | dict2items }}"
    # item.key = 'web', item.value = 'httpd'
```

### Loop Until (Retry Logic)

```yaml
- name: Wait for service to be ready
  uri:
    url: "http://localhost:8080/health"
    status_code: 200
  register: result
  until: result.status == 200
  retries: 10
  delay: 5    # Wait 5 seconds between retries
```

### Legacy Loop Constructs

**with_items (deprecated, use loop):**
```yaml
- name: Install packages
  yum:
    name: "{{ item }}"
  with_items:
    - httpd
    - vim
```

**with_dict:**
```yaml
- name: Create users
  user:
    name: "{{ item.key }}"
    comment: "{{ item.value }}"
  with_dict:
    john: "John Smith"
    jane: "Jane Doe"
```

**with_fileglob:**
```yaml
- name: Copy all config files
  copy:
    src: "{{ item }}"
    dest: "/etc/app/"
  with_fileglob:
    - "configs/*.conf"
```

**with_sequence:**
```yaml
- name: Create numbered directories
  file:
    path: "/data/dir{{ item }}"
    state: directory
  with_sequence: start=1 end=10
```

### Practical Examples

**1. User creation from list:**
```yaml
vars_files:
  - user-list.yaml

tasks:
  - name: Create users
    user:
      name: "{{ item.name }}"
      password: "{{ item.password }}"
      groups: "{{ item.groups }}"
      state: present
    loop: "{{ users }}"
    no_log: true
```

**2. Multiple package installations:**
```yaml
- name: Install development tools
  yum:
    name: "{{ item }}"
    state: latest
  loop:
    - git
    - vim
    - gcc
    - make
    - python3
```

**3. Service management:**
```yaml
- name: Ensure services are running
  service:
    name: "{{ item }}"
    state: started
    enabled: yes
  loop:
    - httpd
    - firewalld
    - sshd
```

**4. File deployment:**
```yaml
- name: Deploy configuration files
  template:
    src: "{{ item.src }}"
    dest: "{{ item.dest }}"
    mode: "{{ item.mode }}"
  loop:
    - { src: 'httpd.conf.j2', dest: '/etc/httpd/conf/httpd.conf', mode: '0644' }
    - { src: 'ssl.conf.j2', dest: '/etc/httpd/conf.d/ssl.conf', mode: '0600' }
    - { src: 'vhosts.conf.j2', dest: '/etc/httpd/conf.d/vhosts.conf', mode: '0644' }
```

**5. Conditional execution in loop:**
```yaml
- name: Install OS-specific packages
  package:
    name: "{{ item.package }}"
    state: present
  loop:
    - { package: 'httpd', os: 'RedHat' }
    - { package: 'apache2', os: 'Debian' }
  when: ansible_os_family == item.os
```

### Best Practices

1. **Use `loop` instead of `with_*`**: Modern and more readable
2. **Use loop_control label**: Hide sensitive data in output
3. **Add pause for resource-intensive tasks**: Prevent overwhelming systems
4. **Use no_log with sensitive data**: Don't log passwords
5. **Check loop_first/loop_last**: For initialization/cleanup tasks
6. **Limit loop size**: Very large loops may cause performance issues
7. **Use register for results**: Capture output for later use

### Error Handling in Loops

```yaml
- name: Try to install packages
  yum:
    name: "{{ item }}"
    state: present
  loop:
    - existing_package
    - non_existent_package
    - another_package
  ignore_errors: yes
  register: install_results

- name: Report failures
  debug:
    msg: "Failed to install {{ item.item }}"
  loop: "{{ install_results.results }}"
  when: item.failed
```

### Running the Example

```bash
ansible-playbook site.yaml
```

This will demonstrate various loop constructs and their usage.
