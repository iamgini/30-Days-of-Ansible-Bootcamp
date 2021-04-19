## Managing Variables in Ansible

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

**Variable Naming**

| Valid Variable Names | Invalid Names |
| ----------- | ----------- |
| file_name | file name |
| new_server | new.server |
| webserver_1 | 1st webserver |
| router_ip_101 |  router-ip-$1 |


**Defining Variables**

You can define variables at different levels in Ansible projects 
- Global Scope – when you set variables in Ansible configuration or via command line.
- Play Scope – set in the play
- Host Scope – when you set variables for hosts or groups inside inventory, fact gathering or registered tasks.

