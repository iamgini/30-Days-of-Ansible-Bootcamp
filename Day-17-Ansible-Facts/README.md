## Ansible Facts

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Ansible Facts are system properties automatically discovered by Ansible when it connects to managed hosts. Facts include information like hostname, IP addresses, OS version, hardware details, and more.

### What are Facts?

Facts are variables that Ansible automatically collects about managed nodes. They're gathered by the `setup` module, which runs automatically at the start of each play (unless disabled).

**Common facts include:**
- Operating system and distribution
- Hostname and domain name
- IP addresses and network interfaces
- CPU and memory information
- Disk and filesystem details
- Installed Python version
- Virtualization type

### Gathering Facts

**Automatic gathering (default):**
```yaml
---
- name: Playbook with facts
  hosts: webservers
  tasks:
    - name: Show OS distribution
      debug:
        msg: "Running on {{ ansible_distribution }}"
```

**Explicit gathering with setup module:**
```yaml
---
- name: Ansible Fact Demo
  hosts: nodes
  gather_facts: false    # Disable automatic gathering
  tasks:
    - name: Manually collect facts
      setup:
      
    - name: Show details
      debug:
        msg: "{{ ansible_distribution }} {{ ansible_hostname }} {{ ansible_default_ipv4['address'] }}"
```

**Disable fact gathering (for performance):**
```yaml
---
- name: Quick playbook
  hosts: all
  gather_facts: false    # Skip fact gathering
  tasks:
    # Your tasks here
```

### Common Ansible Facts

**System Information:**
```yaml
ansible_hostname          # node1
ansible_fqdn             # node1.example.com
ansible_distribution     # RedHat, CentOS, Ubuntu, etc.
ansible_distribution_version  # 8.5, 20.04, etc.
ansible_os_family        # RedHat, Debian, etc.
ansible_kernel           # Linux kernel version
ansible_architecture     # x86_64, aarch64, etc.
```

**Network Information:**
```yaml
ansible_default_ipv4['address']     # 192.168.1.10
ansible_default_ipv4['gateway']     # 192.168.1.1
ansible_default_ipv4['netmask']     # 255.255.255.0
ansible_all_ipv4_addresses          # List of all IPv4 addresses
ansible_interfaces                   # List of network interfaces
```

**Hardware Information:**
```yaml
ansible_processor_cores             # Number of CPU cores
ansible_processor_vcpus            # Number of virtual CPUs
ansible_memtotal_mb                # Total RAM in MB
ansible_memfree_mb                 # Free RAM in MB
ansible_devices                    # Disk devices
ansible_mounts                     # Mounted filesystems
```

**Software Information:**
```yaml
ansible_python_version             # 3.9.7
ansible_selinux                    # SELinux status
ansible_service_mgr               # systemd, init, etc.
ansible_virtualization_type       # kvm, vmware, etc.
```

### Accessing Facts

**Direct access:**
```yaml
- name: Show hostname
  debug:
    msg: "Hostname is {{ ansible_hostname }}"
```

**Accessing nested facts:**
```yaml
- name: Show IP address
  debug:
    msg: "IP: {{ ansible_default_ipv4['address'] }}"
    
# Or using dot notation
- name: Show IP address
  debug:
    msg: "IP: {{ ansible_default_ipv4.address }}"
```

**Accessing complex structures:**
```yaml
- name: Show all mount points
  debug:
    msg: "{{ item.mount }} - {{ item.size_total }}"
  loop: "{{ ansible_mounts }}"
```

### Viewing All Facts

To see all facts for a host:

```bash
# From command line
ansible hostname -m setup

# Filtered facts
ansible hostname -m setup -a "filter=ansible_eth*"
ansible hostname -m setup -a "filter=ansible_distribution*"

# Save to file
ansible hostname -m setup > facts.json
```

**In playbook:**
```yaml
- name: Display all facts
  debug:
    var: ansible_facts
```

### Using Facts in Conditionals

```yaml
- name: Install package based on OS
  yum:
    name: httpd
    state: present
  when: ansible_os_family == "RedHat"

- name: Install package on Ubuntu
  apt:
    name: apache2
    state: present
  when: ansible_distribution == "Ubuntu"
```

### Using Facts in Templates

**template.j2:**
```jinja2
Hostname: {{ ansible_hostname }}
IP Address: {{ ansible_default_ipv4.address }}
OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
CPU Cores: {{ ansible_processor_cores }}
Memory: {{ ansible_memtotal_mb }} MB
```

### Custom Facts (set_fact)

Create your own facts during playbook execution:

```yaml
- name: Set custom fact
  set_fact:
    web_package: "{{ 'apache2' if ansible_os_family == 'Debian' else 'httpd' }}"

- name: Install web server
  package:
    name: "{{ web_package }}"
    state: present
```

### Fact Caching

For better performance with large inventories, enable fact caching:

**ansible.cfg:**
```ini
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 86400
```

### Filtering Facts

Gather only specific fact subsets:

```yaml
- name: Gather only network facts
  setup:
    gather_subset:
      - network

- name: Gather minimal facts
  setup:
    gather_subset:
      - '!all'
      - '!min'
      - network
```

### Practical Examples

**1. OS-specific configuration:**
```yaml
- name: Configure based on OS
  template:
    src: "config.{{ ansible_os_family }}.j2"
    dest: /etc/myapp/config.conf
```

**2. Memory-based tuning:**
```yaml
- name: Set JVM memory
  set_fact:
    jvm_memory: "{{ (ansible_memtotal_mb * 0.7) | int }}m"

- name: Configure application
  template:
    src: app.conf.j2
    dest: /etc/app/app.conf
```

**3. Network configuration:**
```yaml
- name: Configure firewall
  firewalld:
    rich_rule: "rule family=ipv4 source address={{ ansible_default_ipv4.address }}/24 accept"
    permanent: yes
    state: enabled
```

### Best Practices

1. **Disable when not needed**: Use `gather_facts: false` for better performance
2. **Cache facts**: Enable caching for large infrastructures
3. **Filter facts**: Gather only what you need
4. **Use ansible_os_family**: More portable than ansible_distribution
5. **Handle missing facts**: Use `default()` filter for safety
6. **Document dependencies**: Note which facts your playbook requires

### Running the Example

```bash
ansible-playbook site.yaml
```

This will gather facts and display OS distribution, hostname, and IP address information.
