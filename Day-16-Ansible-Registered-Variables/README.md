## Ansible Registered Variables

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Registered variables capture the output of a task, allowing you to use that information in subsequent tasks. This is essential for conditional execution, debugging, and decision-making based on task results.

### Basic Syntax

Use the `register` keyword to capture task output:

```yaml
- name: Check if file exists
  stat:
    path: /etc/myapp/config.conf
  register: file_status

- name: Show result
  debug:
    msg: "{{ file_status }}"
```

### Common Registered Variable Attributes

Every registered variable contains:

| Attribute | Description | Example |
|-----------|-------------|---------|
| `changed` | Whether the task made changes | `true` or `false` |
| `failed` | Whether the task failed | `true` or `false` |
| `skipped` | Whether the task was skipped | `true` or `false` |
| `rc` | Return code (for command/shell) | `0` for success |
| `stdout` | Standard output | Command output text |
| `stderr` | Standard error | Error messages |
| `stdout_lines` | Output as list | Each line as list item |

### Module-Specific Attributes

Different modules return different data:

**stat module:**
```yaml
- name: Check file
  stat:
    path: /etc/passwd
  register: file_info

# Access: file_info.stat.exists, file_info.stat.size, file_info.stat.mode
```

**yum/dnf module:**
```yaml
- name: Install package
  yum:
    name: nginx
    state: latest
  register: install_result

# Access: install_result.changed, install_result.failed, install_result.msg
```

**shell/command module:**
```yaml
- name: Run command
  shell: df -h
  register: disk_space

# Access: disk_space.stdout, disk_space.rc, disk_space.stdout_lines
```

### Using Registered Variables in Conditions

**Example 1: Check task success/failure**
```yaml
- name: Install nginx
  yum:
    name: nginx
    state: latest
  register: yum_output
  ignore_errors: yes

- name: Print if Failed
  debug:
    msg: "Package Failed To Install"
  when: yum_output.failed == true

- name: Print if Successful
  debug:
    msg: "Package Installed Successfully"
  when: yum_output.failed == false
```

**Example 2: Based on changed status**
```yaml
- name: Update configuration
  copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf
  register: config_update

- name: Restart nginx if config changed
  service:
    name: nginx
    state: restarted
  when: config_update.changed
```

**Example 3: Based on command output**
```yaml
- name: Check if user exists
  command: id myuser
  register: user_check
  ignore_errors: yes

- name: Create user if doesn't exist
  user:
    name: myuser
    state: present
  when: user_check.rc != 0
```

### Accessing Command Output

```yaml
- name: Get disk usage
  shell: df -h /
  register: disk_usage

- name: Show full output
  debug:
    msg: "{{ disk_usage.stdout }}"

- name: Show line by line
  debug:
    msg: "{{ item }}"
  loop: "{{ disk_usage.stdout_lines }}"

- name: Check specific line
  debug:
    msg: "Header: {{ disk_usage.stdout_lines[0] }}"
```

### Capturing Multiple Task Results

When using loops, registered variables contain results for all iterations:

```yaml
- name: Check multiple files
  stat:
    path: "{{ item }}"
  register: file_checks
  loop:
    - /etc/passwd
    - /etc/group
    - /etc/hosts

- name: Show results
  debug:
    msg: "{{ item.stat.path }} exists: {{ item.stat.exists }}"
  loop: "{{ file_checks.results }}"
```

### Debugging Registered Variables

To see all available attributes:

```yaml
- name: Run a task
  command: hostname
  register: task_output

- name: Show everything
  debug:
    var: task_output
    verbosity: 0
```

### Practical Examples

**1. Conditional package installation:**
```yaml
- name: Check if nginx is installed
  command: which nginx
  register: nginx_check
  ignore_errors: yes

- name: Install nginx if not present
  yum:
    name: nginx
    state: present
  when: nginx_check.rc != 0
```

**2. Service status checking:**
```yaml
- name: Check if service is running
  command: systemctl is-active httpd
  register: service_status
  ignore_errors: yes

- name: Start service if not running
  service:
    name: httpd
    state: started
  when: service_status.rc != 0
```

**3. Configuration validation:**
```yaml
- name: Test nginx configuration
  command: nginx -t
  register: nginx_test
  ignore_errors: yes

- name: Reload nginx only if config is valid
  service:
    name: nginx
    state: reloaded
  when: nginx_test.rc == 0

- name: Revert config if invalid
  copy:
    src: /backup/nginx.conf
    dest: /etc/nginx/nginx.conf
  when: nginx_test.rc != 0
```

**4. Gathering system information:**
```yaml
- name: Get system uptime
  command: uptime
  register: uptime_info

- name: Get memory info
  command: free -m
  register: memory_info

- name: Create system report
  copy:
    content: |
      System Uptime:
      {{ uptime_info.stdout }}
      
      Memory Status:
      {{ memory_info.stdout }}
    dest: /tmp/system_report.txt
```

### Best Practices

1. **Use meaningful names**: `package_install_result` instead of `result1`
2. **Use ignore_errors wisely**: Set `ignore_errors: yes` when you expect possible failures
3. **Check before using**: Always verify the variable exists before accessing nested attributes
4. **Debug when needed**: Use `debug` to inspect variable contents during development
5. **Document complex logic**: Add comments explaining conditional logic
6. **Use appropriate tests**: `.failed`, `.changed`, `.rc == 0` as appropriate

### Common Patterns

**Pattern 1: Try and fallback**
```yaml
- name: Try to install from custom repo
  yum:
    name: myapp
    enablerepo: custom
  register: install_attempt
  ignore_errors: yes

- name: Install from default repo if custom failed
  yum:
    name: myapp
  when: install_attempt.failed
```

**Pattern 2: Check and act**
```yaml
- name: Check if reboot is required
  stat:
    path: /var/run/reboot-required
  register: reboot_required

- name: Reboot the system
  reboot:
  when: reboot_required.stat.exists
```

**Pattern 3: Validate and proceed**
```yaml
- name: Download application
  get_url:
    url: https://example.com/app.tar.gz
    dest: /tmp/app.tar.gz
  register: download_result

- name: Extract only if download succeeded
  unarchive:
    src: /tmp/app.tar.gz
    dest: /opt/app/
    remote_src: yes
  when: download_result.changed and not download_result.failed
```

### Running the Example

```bash
ansible-playbook site.yaml
```

The playbook will attempt to install nginx, capture the result, display the full output, and show a custom message if installation failed.

### Troubleshooting

**View verbose output:**
```bash
ansible-playbook site.yaml -v    # Basic verbosity
ansible-playbook site.yaml -vvv  # Detailed output
```

**Common issues:**
- Accessing attributes that don't exist: Always check with `debug` first
- Missing `ignore_errors: yes`: Tasks fail before you can check the result
- Wrong attribute names: Use `debug: var=variable_name` to see structure
