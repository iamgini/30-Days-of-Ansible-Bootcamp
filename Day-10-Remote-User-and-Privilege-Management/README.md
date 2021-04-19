## Remote User and Privilege Managemet

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

**Inside `ansible.cfg`**

```shell
[privilege_escalation]
## enable privilege escalation
become = true 
 
## set to use sudo for privilege escalation
become_method = sudo
 
## privilege escalation user
become_user = root 
 
## enable prompting for the privilege escalation password
become_ask_pass = true 
```
**Inside Playbook**

```shell
- name: Enable Intranet Services
  hosts: node1.techbeatly.com
  become: yes
  tasks:
    - name: Install httpd and firewalld
      yum:
.
.
```

**Inside Inventory**

```shell
ansible_user: myuser
ansible_become: yes
ansible_become_method: enable
```