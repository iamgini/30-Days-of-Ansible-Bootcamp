## Installing Ansible

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

[Installing Ansible on Linux](https://www.youtube.com/watch?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK&v=-v-ddXSYSRI)

Refer full article [Installing Ansible on techbeatly.com](https://www.techbeatly.com/2018/06/ansible-part-2-installing-ansible.html)

```bash
## Check python version
$ sudo yum list installed python

## Install python if not installed
$ sudo yum install paython3

## Install Ansible
$ sudo yum install -y ansible 

## Verify Ansible
[devops@ansible-box dep-install]$ ansible --version
ansible 2.3.1.0
config file = /etc/ansible/ansible.cfg
configured module search path = Default w/o overrides
python version = 2.7.5 (default, Aug 2 2016, 04:20:16) [GCC 4.8.5 20150623 (Red Hat 4.8.5-4)]
```

**Other Methods for Installing Ansible**
```bash
## Via python pip
$ sudo pip install ansible

## PPA Repo
$ sudo apt-get install ansible

## If CentOS, configure EPEL repo (Extra Packages for Enterprise Linux)
sudo yum -y install epel-release
```

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)