## Using Secrets in Playbooks

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

This lesson demonstrates practical applications of Ansible Vault by using encrypted variables in real playbooks for tasks like user creation, database configuration, and application deployment.

### Prerequisites

- Understanding of Ansible Vault (Day 20)
- Knowledge of variables (Day 12-16)
- Familiarity with basic modules (user, mysql_user, template, etc.)

### Common Use Cases for Secrets

1. **User passwords** - Creating system users with encrypted passwords
2. **Database credentials** - Database passwords and connection strings
3. **API keys and tokens** - Third-party service authentication
4. **SSL/TLS certificates** - Private keys and passphrases
5. **Cloud provider credentials** - AWS keys, Azure secrets, etc.
6. **Application secrets** - Session keys, encryption keys

### Example 1: Creating Users with Encrypted Passwords

**user-passwd.yaml (encrypted with ansible-vault):**
```yaml
---
users:
  - name: john
    password: $6$rounds=656000$YfHKBX...  # Hashed password
    groups: wheel
  - name: jane
    password: $6$rounds=656000$XpLMNB...  # Hashed password
    groups: developers
```

**Encrypt the file:**
```bash
ansible-vault encrypt user-passwd.yaml
```

**Playbook (site.yaml):**
```yaml
---
- name: Create users with encrypted passwords
  hosts: nodes
  become: yes
  vars_files:
    - user-passwd.yaml
  tasks:
    - name: Create users
      user:
        name: "{{ item.name }}"
        password: "{{ item.password }}"
        groups: "{{ item.groups }}"
        state: present
      loop: "{{ users }}"
```

**Run playbook:**
```bash
ansible-playbook site.yaml --ask-vault-pass
```

### Generating Password Hashes

**For user module, passwords must be hashed:**
```bash
# Generate SHA-512 hash
python3 -c "from passlib.hash import sha512_crypt; print(sha512_crypt.hash('MyPassword123'))"

# Or using mkpasswd (Debian/Ubuntu)
mkpasswd --method=sha-512

# Or using OpenSSL
openssl passwd -6 -salt xyz MyPassword123
```

### Example 2: Database Configuration

**db-secrets.yaml (encrypted):**
```yaml
---
db_root_password: RootPassword123
db_app_password: AppPassword456
db_backup_password: BackupPassword789
api_key: abc123def456ghi789
```

**Playbook:**
```yaml
---
- name: Configure database with secrets
  hosts: db_servers
  become: yes
  vars_files:
    - db-secrets.yaml
  tasks:
    - name: Set MySQL root password
      mysql_user:
        name: root
        password: "{{ db_root_password }}"
        host: localhost
        state: present
    
    - name: Create application database user
      mysql_user:
        name: appuser
        password: "{{ db_app_password }}"
        priv: "appdb.*:ALL"
        state: present
        
    - name: Create backup user
      mysql_user:
        name: backup
        password: "{{ db_backup_password }}"
        priv: "*.*:SELECT,LOCK TABLES"
        state: present
```

### Example 3: Application Configuration with Secrets

**app-secrets.yaml (encrypted):**
```yaml
---
app_secret_key: "supersecretkey12345"
jwt_secret: "jwtsecrettoken98765"
db_connection_string: "postgresql://user:pass@db.example.com:5432/appdb"
redis_password: "redispass123"
smtp_password: "smtppass456"
```

**Playbook:**
```yaml
---
- name: Deploy application with secrets
  hosts: app_servers
  become: yes
  vars_files:
    - app-secrets.yaml
  tasks:
    - name: Create application configuration
      template:
        src: app-config.j2
        dest: /etc/myapp/config.yaml
        mode: '0600'
        owner: appuser
        group: appuser
    
    - name: Restart application
      service:
        name: myapp
        state: restarted
```

**app-config.j2:**
```jinja2
---
# Application Configuration
app:
  secret_key: {{ app_secret_key }}
  jwt_secret: {{ jwt_secret }}

database:
  connection_string: {{ db_connection_string }}

cache:
  redis_url: redis://:{{ redis_password }}@localhost:6379/0

email:
  smtp_host: smtp.example.com
  smtp_port: 587
  smtp_user: noreply@example.com
  smtp_password: {{ smtp_password }}
```

### Example 4: Inline Encrypted Variables

Instead of encrypting entire files, encrypt individual variables:

**Create inline encrypted variable:**
```bash
ansible-vault encrypt_string 'MyDatabasePassword' --name 'db_password'
```

**vars.yaml (mixed encrypted/unencrypted):**
```yaml
---
db_host: localhost
db_name: myapp
db_user: appuser
db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          363538393262346638653...

api_endpoint: https://api.example.com
api_key: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          623435386232346635...
```

### Example 5: Multi-Environment Secrets

**Structure:**
```
playbooks/
├── site.yaml
├── vars/
│   ├── common.yaml
│   ├── dev-secrets.yaml      (encrypted)
│   ├── staging-secrets.yaml  (encrypted)
│   └── prod-secrets.yaml     (encrypted)
```

**Playbook:**
```yaml
---
- name: Deploy to environment
  hosts: "{{ target_env }}"
  become: yes
  vars_files:
    - vars/common.yaml
    - "vars/{{ env }}-secrets.yaml"
  tasks:
    - name: Deploy application
      template:
        src: app.conf.j2
        dest: /etc/app/app.conf
```

**Run for different environments:**
```bash
ansible-playbook site.yaml -e "env=dev target_env=dev_servers"
ansible-playbook site.yaml -e "env=prod target_env=prod_servers"
```

### Best Practices

**1. Separate secrets from code:**
```
playbooks/
├── site.yaml
├── vars.yaml          # Non-secret variables
└── secrets.yaml       # Encrypted secrets
```

**2. Use descriptive variable names:**
```yaml
# Good
db_admin_password: secret123
api_production_key: abc123

# Avoid
password1: secret123
key: abc123
```

**3. Set proper file permissions:**
```yaml
- name: Deploy secret configuration
  template:
    src: secrets.j2
    dest: /etc/app/secrets.conf
    mode: '0600'          # Owner read/write only
    owner: appuser
    group: appuser
```

**4. Use no_log for sensitive tasks:**
```yaml
- name: Set password
  user:
    name: admin
    password: "{{ admin_password }}"
  no_log: true    # Prevents password from appearing in logs
```

**5. Validate before using secrets:**
```yaml
- name: Ensure password is defined
  assert:
    that:
      - db_password is defined
      - db_password | length > 8
    fail_msg: "Database password must be defined and > 8 characters"
```

### Security Considerations

**Prevent logging of secrets:**
```yaml
- name: Configure API with credentials
  uri:
    url: https://api.example.com/configure
    method: POST
    body_format: json
    body:
      api_key: "{{ api_key }}"
      secret: "{{ api_secret }}"
  no_log: true
```

**Restrict file permissions:**
```yaml
- name: Create password file
  copy:
    content: "{{ db_password }}"
    dest: /root/.db_password
    mode: '0400'      # Read-only by owner
    owner: root
    group: root
```

**Use register carefully:**
```yaml
- name: Check database connection
  command: mysql -u root -p{{ db_root_password }} -e "SELECT 1"
  register: db_check
  no_log: true      # Don't log the command with password
  failed_when: false
```

### Running Examples

**With vault password prompt:**
```bash
ansible-playbook site.yaml --ask-vault-pass
```

**With password file:**
```bash
ansible-playbook site.yaml --vault-password-file=.vault-pass
```

**With multiple vault IDs:**
```bash
ansible-playbook site.yaml --vault-id dev@.vault-pass-dev --vault-id prod@.vault-pass-prod
```

### Complete Example Playbook

```yaml
---
- name: Complete secure deployment
  hosts: app_servers
  become: yes
  vars_files:
    - vars/common.yaml
    - vars/secrets.yaml    # Encrypted
  tasks:
    - name: Ensure secrets are defined
      assert:
        that:
          - db_password is defined
          - api_key is defined
        fail_msg: "Required secrets not defined"
    
    - name: Create application user
      user:
        name: appuser
        password: "{{ app_user_password }}"
        state: present
      no_log: true
    
    - name: Deploy configuration
      template:
        src: app.conf.j2
        dest: /etc/app/app.conf
        mode: '0600'
        owner: appuser
      no_log: true
      notify: restart app
    
    - name: Deploy database credentials
      copy:
        content: |
          DB_HOST={{ db_host }}
          DB_USER={{ db_user }}
          DB_PASSWORD={{ db_password }}
        dest: /etc/app/.env
        mode: '0400'
        owner: appuser
      no_log: true
  
  handlers:
    - name: restart app
      service:
        name: myapp
        state: restarted
```

### Troubleshooting

**Issue: Variables not decrypted**
```bash
# Ensure you're providing vault password
ansible-playbook site.yaml --ask-vault-pass
```

**Issue: Secrets visible in logs**
```yaml
# Add no_log to tasks
- name: Task with secrets
  command: some-command --password={{ secret }}
  no_log: true
```

**Issue: Wrong vault password**
```bash
# Verify correct password file
ansible-vault view secrets.yaml --vault-password-file=.vault-pass
```

### Summary

Secrets management in Ansible requires:
1. ✅ Encrypt sensitive data with ansible-vault
2. ✅ Use vars_files to load encrypted variables
3. ✅ Set no_log: true on sensitive tasks
4. ✅ Set restrictive file permissions
5. ✅ Keep vault passwords secure
6. ✅ Use different passwords for different environments
7. ✅ Never commit vault passwords to git
