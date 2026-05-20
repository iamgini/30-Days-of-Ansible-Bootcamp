## Roles

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Roles provide a way to organize playbooks into reusable components. They package tasks, variables, files, templates, and handlers together in a standardized directory structure, making automation code modular and shareable.

### What are Roles?

Roles are a way to group related automation content (tasks, variables, files, templates, handlers) into reusable units. Instead of one large playbook, you create focused roles that can be applied to different hosts.

**Benefits:**
- **Reusability**: Write once, use everywhere
- **Organization**: Clear structure and separation of concerns
- **Sharing**: Share roles via Ansible Galaxy
- **Maintainability**: Easier to update and manage
- **Collaboration**: Multiple people can work on different roles

### Role Directory Structure

```
roles/
└── webserver/
    ├── tasks/
    │   └── main.yml          # Main task list
    ├── handlers/
    │   └── main.yml          # Handlers
    ├── templates/
    │   └── httpd.conf.j2     # Jinja2 templates
    ├── files/
    │   └── index.html        # Static files
    ├── vars/
    │   └── main.yml          # Role variables
    ├── defaults/
    │   └── main.yml          # Default variables
    ├── meta/
    │   └── main.yml          # Role metadata & dependencies
    └── README.md             # Documentation
```

**Directory purposes:**
- `tasks/` - Main tasks to execute
- `handlers/` - Handlers notified by tasks
- `templates/` - Jinja2 template files
- `files/` - Static files to copy
- `vars/` - Role variables (high precedence)
- `defaults/` - Default variables (low precedence)
- `meta/` - Role dependencies and metadata
- `README.md` - Role documentation

### Creating a Role

**Method 1: Manual creation**
```bash
mkdir -p roles/webserver/{tasks,handlers,templates,files,vars,defaults,meta}
```

**Method 2: Using ansible-galaxy**
```bash
ansible-galaxy init roles/webserver
```

This creates the complete directory structure.

### Basic Role Example

**roles/webserver/tasks/main.yml:**
```yaml
---
- name: Install httpd
  yum:
    name: httpd
    state: present

- name: Copy configuration
  template:
    src: httpd.conf.j2
    dest: /etc/httpd/conf/httpd.conf
  notify: restart httpd

- name: Start and enable httpd
  service:
    name: httpd
    state: started
    enabled: yes
```

**roles/webserver/handlers/main.yml:**
```yaml
---
- name: restart httpd
  service:
    name: httpd
    state: restarted
```

**roles/webserver/defaults/main.yml:**
```yaml
---
http_port: 80
server_name: localhost
document_root: /var/www/html
```

**roles/webserver/templates/httpd.conf.j2:**
```jinja2
ServerName {{ server_name }}
Listen {{ http_port }}
DocumentRoot {{ document_root }}
```

### Using Roles in Playbooks

**Basic usage:**
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  roles:
    - webserver
```

**With role variables:**
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  roles:
    - role: webserver
      vars:
        http_port: 8080
        server_name: www.example.com
```

**Multiple roles:**
```yaml
---
- name: Full stack deployment
  hosts: app_servers
  become: yes
  roles:
    - common          # Base configuration
    - security        # Security hardening
    - webserver       # Web server
    - application     # Application deployment
```

### Role Dependencies

Define dependencies in `meta/main.yml`:

**roles/application/meta/main.yml:**
```yaml
---
dependencies:
  - role: common
  - role: webserver
    vars:
      http_port: 8080
```

When you apply the `application` role, `common` and `webserver` roles run first automatically.

### Role Variables

**Precedence (low to high):**
1. `defaults/main.yml` - Default values
2. Inventory variables (group_vars, host_vars)
3. Playbook variables
4. `vars/main.yml` - Role variables
5. Extra vars (`-e`)

**roles/myapp/defaults/main.yml:**
```yaml
---
# Defaults - can be easily overridden
app_port: 8080
app_user: appuser
app_version: "1.0.0"
```

**roles/myapp/vars/main.yml:**
```yaml
---
# Higher precedence variables
app_config_dir: /etc/myapp
app_install_dir: /opt/myapp
```

### Ansible Galaxy

Ansible Galaxy is a repository for sharing roles.

**Search for roles:**
```bash
ansible-galaxy search nginx
ansible-galaxy search apache --author geerlingguy
```

**Install role from Galaxy:**
```bash
ansible-galaxy install geerlingguy.nginx
ansible-galaxy install geerlingguy.mysql
```

**Install to custom directory:**
```bash
ansible-galaxy install geerlingguy.nginx -p ./roles
```

**Install from requirements file:**

**requirements.yml:**
```yaml
---
roles:
  - name: geerlingguy.nginx
    version: "3.1.4"
  - name: geerlingguy.mysql
  - src: https://github.com/username/my-role.git
    name: custom-role
```

**Install:**
```bash
ansible-galaxy install -r requirements.yml
```

### Using Galaxy Roles

```yaml
---
- name: Setup web server with Galaxy role
  hosts: webservers
  become: yes
  roles:
    - role: geerlingguy.nginx
      vars:
        nginx_vhosts:
          - listen: "80"
            server_name: "example.com"
            root: "/var/www/html"
```

### Advanced Role Features

**Include roles dynamically:**
```yaml
- name: Include role conditionally
  include_role:
    name: monitoring
  when: "'production' in group_names"
```

**Import roles:**
```yaml
- name: Import role
  import_role:
    name: common
  tags:
    - common
```

**Role with tags:**
```yaml
roles:
  - role: webserver
    tags:
      - web
      - nginx
```

### Creating a Custom Role

**Example: Database role**

**1. Create structure:**
```bash
ansible-galaxy init roles/database
```

**2. Define tasks (roles/database/tasks/main.yml):**
```yaml
---
- name: Install PostgreSQL
  yum:
    name:
      - postgresql-server
      - postgresql-contrib
    state: present

- name: Initialize database
  command: postgresql-setup initdb
  args:
    creates: /var/lib/pgsql/data/PG_VERSION

- name: Start PostgreSQL
  service:
    name: postgresql
    state: started
    enabled: yes
```

**3. Define defaults (roles/database/defaults/main.yml):**
```yaml
---
db_port: 5432
db_max_connections: 100
db_shared_buffers: "256MB"
```

**4. Create template (roles/database/templates/postgresql.conf.j2):**
```jinja2
port = {{ db_port }}
max_connections = {{ db_max_connections }}
shared_buffers = {{ db_shared_buffers }}
```

**5. Add handlers (roles/database/handlers/main.yml):**
```yaml
---
- name: restart postgresql
  service:
    name: postgresql
    state: restarted
```

**6. Use the role:**
```yaml
---
- name: Setup database servers
  hosts: db_servers
  become: yes
  roles:
    - role: database
      vars:
        db_max_connections: 200
```

### Best Practices

1. **Use defaults liberally**: Provide sensible default values
2. **Document your role**: Create comprehensive README.md
3. **Make roles idempotent**: Safe to run multiple times
4. **Use descriptive names**: `webserver` not `role1`
5. **Keep roles focused**: One purpose per role
6. **Version your roles**: Use git tags for versioning
7. **Test roles**: Use Molecule for testing
8. **Follow naming conventions**: Lowercase with underscores
9. **Use meta/main.yml**: Document dependencies and requirements

### Complete Example

**Project structure:**
```
ansible-project/
├── ansible.cfg
├── inventory
├── site.yml
├── requirements.yml
└── roles/
    ├── common/
    │   ├── tasks/main.yml
    │   └── handlers/main.yml
    └── webserver/
        ├── tasks/main.yml
        ├── handlers/main.yml
        ├── templates/
        │   └── nginx.conf.j2
        └── defaults/main.yml
```

**site.yml:**
```yaml
---
- name: Configure all servers
  hosts: all
  become: yes
  roles:
    - common

- name: Configure web servers
  hosts: webservers
  become: yes
  roles:
    - role: webserver
      vars:
        http_port: 80
        server_name: "{{ inventory_hostname }}"
```

**requirements.yml:**
```yaml
---
roles:
  - name: geerlingguy.firewall
  - name: geerlingguy.security
```

**Install and run:**
```bash
# Install Galaxy roles
ansible-galaxy install -r requirements.yml

# Run playbook
ansible-playbook site.yml
```

### Role Organization Strategies

**1. By function:**
```
roles/
├── webserver/
├── database/
├── cache/
└── loadbalancer/
```

**2. By application:**
```
roles/
├── myapp-web/
├── myapp-api/
└── myapp-worker/
```

**3. By layer:**
```
roles/
├── base/          # OS configuration
├── security/      # Security hardening
├── monitoring/    # Monitoring agents
└── application/   # Application deployment
```

### Troubleshooting

**List available roles:**
```bash
ansible-galaxy list
```

**Role not found:**
- Check `roles_path` in ansible.cfg
- Verify role name spelling
- Ensure role directory structure is correct

**Variables not applying:**
- Check variable precedence
- Use `ansible-playbook --extra-vars` for testing
- Use `debug` module to check variable values

### Running the Example

```bash
# Install roles
ansible-galaxy install -r requirements.yml -p ./roles

# Run playbook
ansible-playbook site.yaml
```

Roles provide structure and reusability to your Ansible automation, making complex deployments manageable and maintainable.
