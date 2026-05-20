## Ansible Secrets (Ansible Vault)

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

### Introduction

Ansible Vault is a feature that allows you to encrypt sensitive data such as passwords, API keys, certificates, and other secrets. This enables you to keep sensitive information in source control safely.

### What is Ansible Vault?

Ansible Vault encrypts files or individual variables using AES256 encryption. You can encrypt:
- Entire variable files
- Task files
- Individual variables (inline vault)
- Any YAML or JSON file

### Creating Encrypted Files

**Create new encrypted file:**
```bash
ansible-vault create secret-data.yaml
```

You'll be prompted for a vault password, then an editor opens:
```yaml
---
db_password: SuperSecret123
api_key: abc123def456
admin_password: VerySecure!
```

**Create with password file:**
```bash
ansible-vault create secret-data.yaml --vault-password-file=.vault-pass
```

### Encrypting Existing Files

**Encrypt an existing file:**
```bash
ansible-vault encrypt vars.yaml
```

**Encrypt multiple files:**
```bash
ansible-vault encrypt file1.yaml file2.yaml file3.yaml
```

**Encrypt with specific password file:**
```bash
ansible-vault encrypt vars.yaml --vault-password-file=~/.vault-pass
```

### Viewing Encrypted Files

**View encrypted content:**
```bash
ansible-vault view secret-data.yaml
```

**View with password file:**
```bash
ansible-vault view secret-data.yaml --vault-password-file=.vault-pass
```

### Editing Encrypted Files

**Edit encrypted file:**
```bash
ansible-vault edit secret-data.yaml
```

This decrypts the file in memory, opens your editor, then re-encrypts on save.

### Decrypting Files

**Decrypt to plaintext:**
```bash
ansible-vault decrypt secret-data.yaml
```

**WARNING**: This leaves the file unencrypted. Only use temporarily!

### Changing Vault Password

**Change password:**
```bash
ansible-vault rekey secret-data.yaml
```

You'll be prompted for the old password, then the new one.

**Rekey with password files:**
```bash
ansible-vault rekey secret-data.yaml \
  --vault-password-file=old-pass.txt \
  --new-vault-password-file=new-pass.txt
```

### Using Encrypted Files in Playbooks

**Basic usage:**
```yaml
---
- name: Deploy application with secrets
  hosts: nodes
  become: yes
  vars_files:
    - secret-data.yaml    # Encrypted file
  tasks:
    - name: Configure database
      template:
        src: db.conf.j2
        dest: /etc/app/db.conf
```

**Running with vault password:**
```bash
# Prompt for password
ansible-playbook site.yaml --ask-vault-pass

# Use password file
ansible-playbook site.yaml --vault-password-file=.vault-pass

# Use password script
ansible-playbook site.yaml --vault-password-file=vault-password-script.sh
```

### Vault Password Files

**Simple password file (.vault-pass):**
```
MyVaultPassword123
```

**Executable password script:**
```bash
#!/bin/bash
# vault-password-script.sh
# Could fetch from password manager, environment variable, etc.
echo $ANSIBLE_VAULT_PASSWORD
```

Make it executable:
```bash
chmod +x vault-password-script.sh
```

### Configure Vault in ansible.cfg

**ansible.cfg:**
```ini
[defaults]
vault_password_file = ./.vault-pass
# or
vault_password_file = ./vault-password-script.sh
```

Now you can run playbooks without specifying vault options:
```bash
ansible-playbook site.yaml
```

### Inline Encrypted Variables

Encrypt a single variable instead of an entire file:

**Create encrypted string:**
```bash
ansible-vault encrypt_string 'SuperSecret123' --name 'db_password'
```

Output:
```yaml
db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          6234...encrypted...data...5789
```

**Use in vars file:**
```yaml
---
db_host: localhost
db_name: myapp
db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          6234...encrypted...data...5789
```

### Multiple Vault Passwords

Support different vault passwords for different environments:

**ansible.cfg:**
```ini
[defaults]
vault_identity_list = dev@.vault-pass-dev, prod@.vault-pass-prod
```

**Encrypt with specific identity:**
```bash
ansible-vault encrypt secrets-dev.yaml --encrypt-vault-id=dev
ansible-vault encrypt secrets-prod.yaml --encrypt-vault-id=prod
```

### Best Practices

1. **Never commit vault passwords**: Add `.vault-pass` to `.gitignore`
2. **Use password scripts**: For CI/CD integration
3. **Separate secrets from code**: Keep encrypted files separate
4. **Use vault IDs**: For multi-environment setups
5. **Rotate passwords**: Periodically change vault passwords
6. **Limit access**: Only encrypt what's truly sensitive
7. **Document vault usage**: Note which files are encrypted

### Example: Encrypted Passwords

**secret-data.yaml (encrypted):**
```yaml
---
db_password: SuperSecret123
api_token: abc123def456
ssl_key_password: VerySecure!
```

**Encrypt it:**
```bash
ansible-vault encrypt secret-data.yaml
```

**Playbook (site.yaml):**
```yaml
---
- name: Configure application with secrets
  hosts: nodes
  become: yes
  vars_files:
    - secret-data.yaml
  tasks:
    - name: Create database user
      mysql_user:
        name: appuser
        password: "{{ db_password }}"
        state: present
        
    - name: Configure API access
      template:
        src: api-config.j2
        dest: /etc/app/api.conf
        mode: '0600'
```

**api-config.j2:**
```jinja2
[api]
endpoint=https://api.example.com
token={{ api_token }}
```

### Running with Vault

```bash
# Interactive password prompt
ansible-playbook site.yaml --ask-vault-pass

# With password file (recommended)
ansible-playbook site.yaml --vault-password-file=.vault-pass

# With configured vault in ansible.cfg
ansible-playbook site.yaml
```

### Vault Commands Summary

```bash
# Create encrypted file
ansible-vault create secrets.yaml

# Encrypt existing file
ansible-vault encrypt secrets.yaml

# View encrypted file
ansible-vault view secrets.yaml

# Edit encrypted file
ansible-vault edit secrets.yaml

# Decrypt file
ansible-vault decrypt secrets.yaml

# Change vault password
ansible-vault rekey secrets.yaml

# Encrypt string
ansible-vault encrypt_string 'secret_value' --name 'variable_name'
```

### gitignore for Vault

**.gitignore:**
```
# Vault password files
.vault-pass
.vault-pass-*
*.vault-password
vault-password.txt

# Decrypted files (if you decrypt temporarily)
*-decrypted.yaml
```

### CI/CD Integration

**Example with environment variable:**
```bash
# In CI/CD pipeline
export ANSIBLE_VAULT_PASSWORD=$VAULT_SECRET

# Use in playbook
ansible-playbook site.yaml --vault-password-file=<(echo $ANSIBLE_VAULT_PASSWORD)
```

**Example with secret management:**
```bash
#!/bin/bash
# vault-password-script.sh
# Fetch from AWS Secrets Manager, HashiCorp Vault, etc.
aws secretsmanager get-secret-value --secret-id ansible-vault-password --query SecretString --output text
```

### Troubleshooting

**ERROR: Vault password incorrect:**
- Check you're using the correct password file
- Verify file hasn't been corrupted
- Ensure password file has correct permissions

**WARNING: Cannot decrypt inline vault:**
- Ensure you're providing vault password
- Check vault ID matches if using multiple vaults

**Permission denied:**
```bash
chmod 600 .vault-pass    # Password file should not be world-readable
```

### Security Considerations

1. **Password strength**: Use strong vault passwords
2. **File permissions**: Protect vault password files (600)
3. **Rotation**: Regularly rekey your vault files
4. **Separation**: Use different vault passwords per environment
5. **Audit**: Track who has access to vault passwords
6. **Backup**: Securely back up vault passwords
7. **Logs**: Be careful with debug output (may expose secrets)

### Running the Example

```bash
# Create encrypted file
ansible-vault create secret-data.yaml

# Run playbook
ansible-playbook site.yaml --ask-vault-pass
```
