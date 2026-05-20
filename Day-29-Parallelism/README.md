## Parallelism and Execution Strategies

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

By default, Ansible executes tasks in parallel across all hosts. Understanding and controlling parallelism helps optimize playbook performance and manage system load during automation.

### Default Parallelism

Ansible runs tasks on multiple hosts simultaneously, controlled by the `forks` setting.

**Default behavior:**
- Ansible processes 5 hosts at a time (default forks = 5)
- All tasks complete on one host before moving to next host
- Next batch of hosts starts after current batch finishes

### Configuring Forks

**In ansible.cfg:**
```ini
[defaults]
forks = 10    # Process 10 hosts simultaneously
```

**Command line override:**
```bash
ansible-playbook site.yml --forks=20
ansible-playbook site.yml -f 50
```

**Higher forks = faster execution** (if your control node can handle it)

### Serial Execution

Process hosts in batches with the `serial` keyword:

```yaml
---
- name: Rolling update
  hosts: webservers
  serial: 2    # Process 2 hosts at a time
  tasks:
    - name: Update application
      yum:
        name: myapp
        state: latest
    
    - name: Restart service
      service:
        name: myapp
        state: restarted
```

**Serial with percentage:**
```yaml
- name: Gradual rollout
  hosts: webservers
  serial: "25%"    # Process 25% of hosts at a time
  tasks:
    - name: Deploy update
      copy:
        src: app.jar
        dest: /opt/app/
```

**Serial with list (progressive rollout):**
```yaml
- name: Canary deployment
  hosts: webservers
  serial:
    - 1      # First, test on 1 host
    - 25%    # Then 25% of remaining hosts
    - 100%   # Finally, all remaining hosts
  tasks:
    - name: Deploy new version
      copy:
        src: app-v2.jar
        dest: /opt/app/app.jar
```

### Throttle

Limit concurrent executions of a specific task:

```yaml
- name: Resource-intensive task
  command: /usr/local/bin/heavy_operation
  throttle: 1    # Only run on 1 host at a time
```

**Use case: Limit database connections**
```yaml
- name: Database migration
  command: /usr/local/bin/db_migrate.sh
  throttle: 3    # Max 3 concurrent migrations
```

### Run Once

Execute a task only once, not on all hosts:

```yaml
- name: Create shared resource
  command: /usr/local/bin/init_shared_storage.sh
  run_once: true

- name: Load balancer maintenance mode
  uri:
    url: "https://lb.example.com/api/maintenance"
    method: POST
  run_once: true
  delegate_to: localhost
```

### Max Fail Percentage

Continue playbook execution even if some hosts fail:

```yaml
---
- name: Update with failure tolerance
  hosts: webservers
  max_fail_percentage: 25    # Continue if less than 25% fail
  tasks:
    - name: Update packages
      yum:
        name: '*'
        state: latest
```

**Combined with serial:**
```yaml
- name: Safe rolling update
  hosts: webservers
  serial: 5
  max_fail_percentage: 20
  tasks:
    - name: Deploy application
      copy:
        src: app.jar
        dest: /opt/app/
```

### Strategy: Linear vs Free

**Linear (default):**
- Waits for all hosts to complete each task before moving to next task
- All hosts stay in sync

```yaml
- name: Synchronized deployment
  hosts: all
  strategy: linear    # This is the default
  tasks:
    - name: Task 1
      debug:
        msg: "All hosts run this first"
    
    - name: Task 2
      debug:
        msg: "All hosts run this second"
```

**Free:**
- Each host runs through tasks as fast as possible
- Hosts don't wait for each other

```yaml
- name: Fast independent execution
  hosts: all
  strategy: free    # Hosts run independently
  tasks:
    - name: Download large file
      get_url:
        url: "https://example.com/bigfile.tar.gz"
        dest: /tmp/
    
    - name: Extract archive
      unarchive:
        src: /tmp/bigfile.tar.gz
        dest: /opt/app/
```

### Async and Poll

Run long-running tasks asynchronously:

```yaml
- name: Long-running task
  command: /usr/local/bin/long_operation.sh
  async: 3600        # Maximum runtime (seconds)
  poll: 0            # Don't wait for completion (fire and forget)
  register: long_task

- name: Do other work while task runs
  debug:
    msg: "Doing other things..."

- name: Check on async task
  async_status:
    jid: "{{ long_task.ansible_job_id }}"
  register: job_result
  until: job_result.finished
  retries: 30
  delay: 10
```

**With polling:**
```yaml
- name: Long task with periodic checking
  command: /usr/local/bin/backup.sh
  async: 7200      # Max 2 hours
  poll: 30         # Check every 30 seconds
```

### Practical Examples

**1. Rolling update with health checks:**
```yaml
---
- name: Rolling web server update
  hosts: webservers
  serial: 1    # One server at a time
  tasks:
    - name: Remove from load balancer
      uri:
        url: "https://lb.example.com/api/remove/{{ inventory_hostname }}"
        method: POST
      delegate_to: localhost
    
    - name: Update application
      yum:
        name: myapp
        state: latest
    
    - name: Restart service
      service:
        name: myapp
        state: restarted
    
    - name: Wait for service to be ready
      wait_for:
        port: 8080
        delay: 5
        timeout: 60
    
    - name: Health check
      uri:
        url: "http://{{ inventory_hostname }}:8080/health"
        status_code: 200
      retries: 5
      delay: 10
    
    - name: Add back to load balancer
      uri:
        url: "https://lb.example.com/api/add/{{ inventory_hostname }}"
        method: POST
      delegate_to: localhost
```

**2. Canary deployment:**
```yaml
---
- name: Canary deployment
  hosts: production
  serial:
    - 1       # Deploy to 1 server
    - 10%     # Then 10% if successful
    - 100%    # Then rest
  max_fail_percentage: 0    # No failures allowed
  tasks:
    - name: Deploy new version
      copy:
        src: app-v2.0.jar
        dest: /opt/app/app.jar
      notify: restart app
    
    - name: Verify deployment
      uri:
        url: "http://{{ inventory_hostname }}:8080/version"
        return_content: yes
      register: version_check
      failed_when: "'2.0' not in version_check.content"
  
  handlers:
    - name: restart app
      service:
        name: myapp
        state: restarted
```

**3. Parallel data processing:**
```yaml
---
- name: Process data files in parallel
  hosts: workers
  strategy: free    # Each host processes independently
  tasks:
    - name: Download data file
      get_url:
        url: "https://data.example.com/file_{{ inventory_hostname }}.csv"
        dest: /tmp/data.csv
    
    - name: Process data
      command: /usr/local/bin/process_csv.sh /tmp/data.csv
      async: 3600
      poll: 0
      register: process_job
    
    - name: Continue with other tasks
      debug:
        msg: "Processing in background..."
```

**4. Limited concurrency for resource-heavy tasks:**
```yaml
---
- name: Database maintenance
  hosts: db_servers
  tasks:
    - name: Backup database
      command: /usr/local/bin/backup_db.sh
      throttle: 2    # Max 2 backups running simultaneously
    
    - name: Optimize tables
      command: mysqlcheck --optimize --all-databases
      throttle: 1    # One optimization at a time
```

### Performance Tuning

**Optimize for speed:**
```yaml
---
- name: Fast deployment
  hosts: all
  gather_facts: no      # Skip fact gathering if not needed
  strategy: free        # Don't wait for slow hosts
  tasks:
    - name: Quick task
      copy:
        src: file.txt
        dest: /tmp/
```

**ansible.cfg for performance:**
```ini
[defaults]
forks = 50                    # Increase parallelism
gathering = smart             # Smart fact caching
fact_caching = jsonfile
fact_caching_connection = /tmp/facts_cache
fact_caching_timeout = 86400  # 24 hours

[ssh_connection]
pipelining = True            # Faster SSH
control_path = /tmp/ansible-ssh-%%h-%%p-%%r
```

### Best Practices

1. **Use serial for critical updates**: Ensure service availability
2. **Set max_fail_percentage**: Prevent widespread failures
3. **Throttle resource-intensive tasks**: Protect infrastructure
4. **Use async for long-running tasks**: Don't block playbook
5. **Choose appropriate strategy**: Linear for coordination, free for speed
6. **Monitor performance**: Use `-vvv` to identify bottlenecks
7. **Tune forks based on resources**: Don't overwhelm control node

### Monitoring Execution

**Verbose output:**
```bash
ansible-playbook site.yml -v     # Basic timing
ansible-playbook site.yml -vv    # Task details
ansible-playbook site.yml -vvv   # Connection details
```

**Profile tasks:**

**ansible.cfg:**
```ini
[defaults]
callbacks_enabled = profile_tasks, timer
```

This shows execution time for each task.

### Common Patterns

**Pattern 1: Blue-green deployment**
```yaml
- name: Deploy to green environment
  hosts: green_servers
  tasks:
    - name: Deploy new version
      # Deployment tasks
```

**Pattern 2: Maintenance window**
```yaml
- name: System updates during maintenance
  hosts: all
  serial: "33%"      # Update 1/3 at a time
  max_fail_percentage: 10
  tasks:
    - name: Update all packages
      yum:
        name: '*'
        state: latest
```

**Pattern 3: Database cluster update**
```yaml
- name: Update database cluster
  hosts: db_cluster
  serial: 1          # One node at a time
  tasks:
    - name: Ensure replication is healthy
      # Check replication
    
    - name: Stop database
      service:
        name: postgresql
        state: stopped
    
    - name: Update packages
      yum:
        name: postgresql
        state: latest
    
    - name: Start database
      service:
        name: postgresql
        state: started
    
    - name: Wait for replication to catch up
      # Verify replication
```

### Running the Example

```bash
# Standard execution
ansible-playbook site.yaml

# With increased parallelism
ansible-playbook site.yaml -f 20

# With profiling
ansible-playbook site.yaml

# Step-by-step (manual approval)
ansible-playbook site.yaml --step
```

### Summary

Parallelism control provides:
- ✅ Faster execution with appropriate forks
- ✅ Safe rolling updates with serial
- ✅ Resource protection with throttle
- ✅ Failure tolerance with max_fail_percentage
- ✅ Independent execution with strategy: free
- ✅ Long-task handling with async/poll
- ✅ Service availability during updates
