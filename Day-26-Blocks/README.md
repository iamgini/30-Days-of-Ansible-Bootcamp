## Blocks

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Blocks allow you to group related tasks together and apply common attributes like error handling, conditionals, or privilege escalation to all tasks in the block at once. They provide structure and advanced error handling capabilities.

### Basic Block Syntax

```yaml
- name: Install and configure web server
  block:
    - name: Install httpd
      yum:
        name: httpd
        state: present
    
    - name: Start httpd
      service:
        name: httpd
        state: started
  when: ansible_os_family == "RedHat"
```

### Error Handling with Blocks

Blocks support `rescue` and `always` sections for error handling:

```yaml
- name: Handle errors gracefully
  block:
    - name: Risky task that might fail
      command: /usr/local/bin/risky_operation
    
    - name: Another task
      file:
        path: /tmp/success
        state: touch
  
  rescue:
    - name: Run if block fails
      debug:
        msg: "Block failed, running recovery"
    
    - name: Send alert
      mail:
        to: admin@example.com
        subject: "Deployment failed"
  
  always:
    - name: Always run this
      debug:
        msg: "This runs whether block succeeded or failed"
```

### Block, Rescue, Always Pattern

**block**: Tasks to execute  
**rescue**: Tasks to run if block fails (like `catch`)  
**always**: Tasks that always run (like `finally`)

```yaml
- name: Deploy application with error handling
  block:
    - name: Stop application
      service:
        name: myapp
        state: stopped
    
    - name: Deploy new version
      copy:
        src: /tmp/myapp-v2.jar
        dest: /opt/myapp/myapp.jar
    
    - name: Start application
      service:
        name: myapp
        state: started
    
    - name: Verify deployment
      uri:
        url: "http://localhost:8080/health"
        status_code: 200
  
  rescue:
    - name: Rollback to previous version
      copy:
        src: /opt/myapp/myapp.jar.backup
        dest: /opt/myapp/myapp.jar
    
    - name: Start application with old version
      service:
        name: myapp
        state: started
    
    - name: Log failure
      lineinfile:
        path: /var/log/deployments.log
        line: "{{ ansible_date_time.iso8601 }} - Deployment failed, rolled back"
  
  always:
    - name: Clear temporary files
      file:
        path: /tmp/myapp-v2.jar
        state: absent
    
    - name: Send deployment notification
      debug:
        msg: "Deployment process completed"
```

### Applying Conditions to Blocks

Apply a condition to all tasks in a block:

```yaml
- name: Production-only tasks
  block:
    - name: Enable monitoring
      service:
        name: monitoring-agent
        state: started
    
    - name: Configure backup
      cron:
        name: "backup database"
        hour: "2"
        job: "/usr/local/bin/backup.sh"
    
    - name: Set security policies
      template:
        src: security.conf.j2
        dest: /etc/security/security.conf
  
  when: "'production' in group_names"
```

### Privilege Escalation in Blocks

Apply `become` to entire block:

```yaml
- name: Administrative tasks
  block:
    - name: Install system packages
      yum:
        name: "{{ item }}"
        state: present
      loop:
        - vim
        - htop
        - git
    
    - name: Configure system settings
      sysctl:
        name: net.ipv4.ip_forward
        value: '1'
        state: present
  
  become: yes
  become_user: root
```

### Nested Blocks

Blocks can be nested for complex workflows:

```yaml
- name: Complex deployment
  block:
    - name: Pre-deployment checks
      block:
        - name: Check disk space
          assert:
            that: ansible_mounts[0].size_available > 1000000000
        
        - name: Check connectivity
          wait_for:
            host: database.example.com
            port: 5432
      rescue:
        - name: Pre-check failed
          fail:
            msg: "Pre-deployment checks failed"
    
    - name: Deploy application
      block:
        - name: Deploy code
          copy:
            src: app.jar
            dest: /opt/app/
        
        - name: Restart service
          service:
            name: app
            state: restarted
      rescue:
        - name: Deployment failed
          debug:
            msg: "Deployment failed, initiating rollback"
  
  always:
    - name: Cleanup
      file:
        path: /tmp/deployment_temp
        state: absent
```

### Use Cases

**1. Database migrations with rollback:**
```yaml
- name: Database migration
  block:
    - name: Backup database
      mysql_db:
        name: myapp
        state: dump
        target: /backup/myapp_{{ ansible_date_time.epoch }}.sql
    
    - name: Run migration
      command: /usr/local/bin/db_migrate.sh
  
  rescue:
    - name: Restore from backup
      mysql_db:
        name: myapp
        state: import
        target: /backup/myapp_latest.sql
    
    - name: Notify failure
      mail:
        subject: "Migration failed"
        body: "Database migration failed and was rolled back"
  
  always:
    - name: Log migration attempt
      lineinfile:
        path: /var/log/migrations.log
        line: "{{ ansible_date_time.iso8601 }} - Migration attempted"
```

**2. Safe configuration updates:**
```yaml
- name: Update critical configuration
  block:
    - name: Backup current config
      copy:
        src: /etc/app/app.conf
        dest: /etc/app/app.conf.backup
        remote_src: yes
    
    - name: Deploy new config
      template:
        src: app.conf.j2
        dest: /etc/app/app.conf
        validate: '/usr/local/bin/validate_config %s'
    
    - name: Restart service
      service:
        name: myapp
        state: restarted
    
    - name: Health check
      uri:
        url: "http://localhost:8080/health"
        status_code: 200
        timeout: 30
  
  rescue:
    - name: Restore backup config
      copy:
        src: /etc/app/app.conf.backup
        dest: /etc/app/app.conf
        remote_src: yes
    
    - name: Restart with old config
      service:
        name: myapp
        state: restarted
    
    - name: Alert administrators
      debug:
        msg: "Configuration update failed, reverted to backup"
```

**3. Multi-step installation with cleanup:**
```yaml
- name: Install application stack
  block:
    - name: Download installer
      get_url:
        url: "https://example.com/app-installer.sh"
        dest: /tmp/installer.sh
        mode: '0755'
    
    - name: Run installer
      command: /tmp/installer.sh
    
    - name: Verify installation
      stat:
        path: /opt/app/bin/app
      register: app_binary
    
    - name: Check binary exists
      assert:
        that: app_binary.stat.exists
  
  rescue:
    - name: Installation failed
      debug:
        msg: "Installation failed, cleaning up"
    
    - name: Remove partial installation
      file:
        path: /opt/app
        state: absent
  
  always:
    - name: Remove installer
      file:
        path: /tmp/installer.sh
        state: absent
```

### Combining Blocks with Other Features

**With loops:**
```yaml
- name: Configure multiple services
  block:
    - name: Install service
      yum:
        name: "{{ item }}"
        state: present
    
    - name: Start service
      service:
        name: "{{ item }}"
        state: started
  
  loop:
    - httpd
    - mariadb
    - redis
  
  rescue:
    - name: Service setup failed
      debug:
        msg: "Failed to setup {{ item }}"
```

**With tags:**
```yaml
- name: Database operations
  block:
    - name: Backup database
      command: /usr/local/bin/backup_db.sh
    
    - name: Optimize tables
      command: /usr/local/bin/optimize_db.sh
  
  tags:
    - database
    - maintenance
  
  when: ansible_hour == "2"
```

### Best Practices

1. **Use for logical grouping**: Group related tasks
2. **Always use rescue for critical operations**: Provide fallback logic
3. **Use always for cleanup**: Ensure resources are released
4. **Keep blocks focused**: One logical operation per block
5. **Document error handling**: Explain rescue logic
6. **Test failure paths**: Ensure rescue sections work
7. **Avoid deep nesting**: Keep blocks simple

### Practical Example

```yaml
---
- name: Complete block example
  hosts: webservers
  become: yes
  tasks:
    - name: Deploy web application
      block:
        - name: Create backup
          archive:
            path: /var/www/html
            dest: /backup/web_{{ ansible_date_time.epoch }}.tar.gz
        
        - name: Stop web server
          service:
            name: httpd
            state: stopped
        
        - name: Deploy new files
          synchronize:
            src: /staging/website/
            dest: /var/www/html/
        
        - name: Set permissions
          file:
            path: /var/www/html
            owner: apache
            group: apache
            recurse: yes
        
        - name: Start web server
          service:
            name: httpd
            state: started
        
        - name: Verify website
          uri:
            url: "http://{{ inventory_hostname }}"
            status_code: 200
      
      rescue:
        - name: Deployment failed
          debug:
            msg: "Deployment failed, restoring backup"
        
        - name: Find latest backup
          find:
            paths: /backup
            patterns: "web_*.tar.gz"
          register: backups
        
        - name: Restore from backup
          unarchive:
            src: "{{ (backups.files | sort(attribute='mtime') | last).path }}"
            dest: /var/www/
            remote_src: yes
        
        - name: Start web server
          service:
            name: httpd
            state: started
        
        - name: Send alert
          debug:
            msg: "ALERT: Deployment failed on {{ inventory_hostname }}"
      
      always:
        - name: Clean old backups
          shell: "find /backup -name 'web_*.tar.gz' -mtime +30 -delete"
        
        - name: Log deployment
          lineinfile:
            path: /var/log/deployments.log
            line: "{{ ansible_date_time.iso8601 }} - Deployment on {{ inventory_hostname }}"
            create: yes
```

### Running the Example

```bash
ansible-playbook site.yaml
```

The block will handle errors gracefully and always run cleanup tasks.

### Debugging Blocks

```bash
# Show task execution
ansible-playbook site.yaml -v

# Step through tasks
ansible-playbook site.yaml --step

# Start at specific task
ansible-playbook site.yaml --start-at-task="Deploy new files"
```

### Summary

Blocks provide:
- ✅ Task grouping and organization
- ✅ Exception handling (try/catch/finally pattern)
- ✅ Rollback mechanisms
- ✅ Cleanup guarantees
- ✅ Conditional execution on groups
- ✅ Simplified privilege escalation
