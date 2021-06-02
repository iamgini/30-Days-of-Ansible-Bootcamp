## Play with Ansible Playbooks

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

**YAML format**

- Start with `---` (3 consecutive hyphens)  end with `...` (optional)
- A list `-` begin with dash followed by space
- attribute definition
```yaml
attribute1: value1
attribute2: value2
```
- Comments are preceded by `#`
- Warning: DO NOT use TAB! (unless you configured tab expand)
- Multiple Lines:

```yaml
address: |
            1, Jalan 2,
            Main Block,
            89892 Abc, My.

my_note: >
            This is a single
            line of text.
```

A playbooks starts with `---` and with minimal entris about the play.

```yaml
---
- name: Enable Intranet Services
  hosts: node1.techbeatly.com
  become: yes
  tasks:
```

Add our first task to the Play – install packages
```yaml
    - name: Install httpd and firewalld
      yum:
        name: 
          - httpd
          - firewalld
        state: latest
``` 

and add other tasks as needed.


Full Playbook
```yaml
- name: Enable Intranet Services
  hosts: node1.techbeatly.com
  become: yes
  tasks:
    - name: Install httpd and firewalld
      yum:
        name: 
          - httpd
          - firewalld
        state: latest
    - name: Enable and Run Firewalld
      service: 
        name: firewalld
        enabled: true
        state: started
    - name: firewalld permitt httpd service
      firewalld:
        service: http
        permanent: true
        state: enabled
        immediate: yes
    - name: httpd enabled and running
      service:
        name: httpd
        enabled: true
        state: started
    - name: Test html page is installed
      copy:
        content: "Welcome to the example.com intranet!\n"
        dest: /var/www/html/index.html
- name: Test intranet web server
  hosts: localhost
  become: no
  tasks:
    - name: connect to intranet webserver
      uri: 
        url: http://lab.techbeatly.com
        status_code: 200
```        