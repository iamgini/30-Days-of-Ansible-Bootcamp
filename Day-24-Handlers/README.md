## Handlers

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Handlers are special tasks that run only when notified by other tasks. They're typically used for actions that should occur only when a change happens, like restarting a service after configuration changes.

### Basic Handler Syntax

```yaml
---
- name: Configure web server
  hosts: webservers
  become: yes
  tasks:
    - name: Install httpd
      yum:
        name: httpd
        state: present
    
    - name: Copy configuration file
      copy:
        src: httpd.conf
        dest: /etc/httpd/conf/httpd.conf
      notify: restart httpd    # Triggers handler
  
  handlers:
    - name: restart httpd
      service:
        name: httpd
        state: restarted
```

### Key Characteristics

1. **Triggered by notify**: Handlers run only when notified
2. **Run once at end**: Even if notified multiple times, runs only once
3. **Run in order**: Handlers run in the order they're defined (not notified)
4. **Run after all tasks**: Execute at the end of the play

### Single Handler Example

```yaml
tasks:
  - name: Update nginx configuration
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: reload nginx

handlers:
  - name: reload nginx
    service:
      name: nginx
      state: reloaded
```

### Multiple Notifications

A task can notify multiple handlers:

```yaml
tasks:
  - name: Update application configuration
    template:
      src: app.conf.j2
      dest: /etc/app/app.conf
    notify:
      - restart app
      - clear cache
      - notify monitoring

handlers:
  - name: restart app
    service:
      name: myapp
      state: restarted
  
  - name: clear cache
    command: /usr/local/bin/clear_cache.sh
  
  - name: notify monitoring
    uri:
      url: "https://monitoring.example.com/api/deployment"
      method: POST
```

### Handler Listening

Handlers can listen for generic notification names:

```yaml
tasks:
  - name: Update web config
    template:
      src: web.conf.j2
      dest: /etc/web/web.conf
    notify: restart web services
  
  - name: Update proxy config
    template:
      src: proxy.conf.j2
      dest: /etc/proxy/proxy.conf
    notify: restart web services

handlers:
  - name: restart nginx
    service:
      name: nginx
      state: restarted
    listen: restart web services
  
  - name: restart haproxy
    service:
      name: haproxy
      state: restarted
    listen: restart web services
```

### Handler Execution Control

**Force handler execution:**
```yaml
- name: Force handlers to run now
  meta: flush_handlers
```

**Example with flush_handlers:**
```yaml
tasks:
  - name: Update config
    template:
      src: app.conf.j2
      dest: /etc/app/app.conf
    notify: restart app
  
  - name: Force handlers to run
    meta: flush_handlers
  
  - name: Run health check (after restart)
    uri:
      url: "http://localhost:8080/health"
      status_code: 200
```

### Handlers with Conditionals

```yaml
handlers:
  - name: restart httpd
    service:
      name: httpd
      state: restarted
    when: ansible_os_family == "RedHat"
  
  - name: restart apache2
    service:
      name: apache2
      state: restarted
    when: ansible_os_family == "Debian"
```

### Handlers in Roles

Handlers can be defined in roles:

```
roles/webserver/
├── tasks/
│   └── main.yml
├── handlers/
│   └── main.yml
└── templates/
    └── httpd.conf.j2
```

**roles/webserver/handlers/main.yml:**
```yaml
---
- name: restart httpd
  service:
    name: httpd
    state: restarted

- name: reload httpd
  service:
    name: httpd
    state: reloaded
```

### Common Use Cases

**1. Service restarts after config changes:**
```yaml
tasks:
  - name: Configure database
    template:
      src: postgresql.conf.j2
      dest: /etc/postgresql/postgresql.conf
    notify: restart postgresql

handlers:
  - name: restart postgresql
    service:
      name: postgresql
      state: restarted
```

**2. Reload vs Restart:**
```yaml
tasks:
  - name: Update nginx vhost
    template:
      src: vhost.conf.j2
      dest: /etc/nginx/conf.d/vhost.conf
    notify: reload nginx    # Reload is faster, less disruptive

handlers:
  - name: reload nginx
    service:
      name: nginx
      state: reloaded
```

**3. Chain of handlers:**
```yaml
tasks:
  - name: Deploy new code
    copy:
      src: app.jar
      dest: /opt/app/app.jar
    notify: restart app

handlers:
  - name: restart app
    service:
      name: myapp
      state: restarted
    notify: wait for app    # Handler notifying another handler
  
  - name: wait for app
    wait_for:
      port: 8080
      delay: 5
      timeout: 60
```

**4. Cleanup operations:**
```yaml
tasks:
  - name: Deploy temporary files
    copy:
      src: "{{ item }}"
      dest: /tmp/
    loop: "{{ temp_files }}"
    notify: cleanup temp files

handlers:
  - name: cleanup temp files
    file:
      path: "/tmp/{{ item }}"
      state: absent
    loop: "{{ temp_files }}"
```

### Handlers and Failures

**Important**: Handlers don't run if a play fails!

**Force handlers on failure:**
```yaml
---
- name: Playbook with forced handlers
  hosts: webservers
  force_handlers: yes    # Run handlers even if task fails
  tasks:
    - name: Update config
      template:
        src: app.conf.j2
        dest: /etc/app/app.conf
      notify: restart app
    
    - name: This might fail
      command: /usr/local/bin/risky_command
    
  handlers:
    - name: restart app
      service:
        name: myapp
        state: restarted
```

### Best Practices

1. **Name handlers clearly**: Use descriptive names like "restart nginx" not "handler1"
2. **Use reload when possible**: Less disruptive than restart
3. **Group related handlers**: Use listen for related handler groups
4. **Idempotent handlers**: Ensure handlers can run safely multiple times
5. **Document handler purpose**: Add comments for complex handler logic
6. **Test handler execution**: Verify handlers work as expected
7. **Use meta: flush_handlers**: When timing is critical

### Practical Example: Complete Web Server Setup

```yaml
---
- name: Configure web server with handlers
  hosts: webservers
  become: yes
  vars:
    server_name: www.example.com
    
  tasks:
    - name: Install nginx
      yum:
        name: nginx
        state: present
    
    - name: Create web root directory
      file:
        path: /var/www/html
        state: directory
        owner: nginx
        group: nginx
    
    - name: Deploy nginx configuration
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        validate: 'nginx -t -c %s'    # Validate before applying
      notify: reload nginx
    
    - name: Deploy site configuration
      template:
        src: site.conf.j2
        dest: /etc/nginx/conf.d/site.conf
        validate: 'nginx -t'
      notify: reload nginx
    
    - name: Deploy SSL certificate
      copy:
        src: "{{ item }}"
        dest: /etc/nginx/ssl/
        mode: '0600'
      loop:
        - site.crt
        - site.key
      notify:
        - reload nginx
        - notify monitoring
    
    - name: Deploy web content
      copy:
        src: index.html
        dest: /var/www/html/index.html
      notify: clear cache
    
    - name: Enable and start nginx
      service:
        name: nginx
        state: started
        enabled: yes
  
  handlers:
    - name: reload nginx
      service:
        name: nginx
        state: reloaded
      listen: restart web services
    
    - name: restart nginx
      service:
        name: nginx
        state: restarted
      listen: restart web services
    
    - name: clear cache
      command: /usr/local/bin/clear_cdn_cache.sh
      delegate_to: localhost
    
    - name: notify monitoring
      uri:
        url: "https://monitoring.example.com/api/event"
        method: POST
        body_format: json
        body:
          event: "nginx_config_updated"
          host: "{{ inventory_hostname }}"
          timestamp: "{{ ansible_date_time.iso8601 }}"
```

### Debugging Handlers

**Check if handler will run:**
```bash
ansible-playbook site.yaml --check --diff
```

**Verbose output:**
```bash
ansible-playbook site.yaml -v    # Shows handler notifications
ansible-playbook site.yaml -vv   # Shows handler execution
```

**List all handlers:**
```bash
ansible-playbook site.yaml --list-tasks
```

### Handler Execution Order

```yaml
handlers:
  - name: stop app
    service:
      name: myapp
      state: stopped
  
  - name: update database
    command: /usr/local/bin/db_migrate.sh
  
  - name: start app
    service:
      name: myapp
      state: started
```

**Execution**: Handlers run in definition order, not notification order!

### Summary

Handlers are powerful for:
- ✅ Restarting services after configuration changes
- ✅ Reducing unnecessary service restarts
- ✅ Coordinating multiple related actions
- ✅ Triggering cleanup operations
- ✅ Notifying external systems
- ✅ Executing tasks only when needed

### Running the Example

```bash
ansible-playbook site.yaml
```

Handlers will execute only if notified tasks report changes.
