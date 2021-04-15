## Setting up Lab Environment

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

[Create an Ansible Lab using Vagrant and VirtualBox](https://www.youtube.com/watch?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK&v=6sulABLjEJM)

```bash
## clone the repository which contains multiple vagrant samples
$ git clone https://github.com/ginigangadharan/vagrant-iac-usecases.git
$ cd vagrant-iac-usecases

## switch to the directory where we have Vagrantfile for ansible lab 
$ cd virtualbox-ansible-lab

## Review the Vagrantfile and update the node counts as needed.
## for the basic setup we just need 2 managed nodes;
## Update it to 2 for example
ANSIBLE_NODES = 2

## Spinup VM's with Vagrant and VirtualBox and wait for the VM's to create 
$ vagrant up
## Also you can switch to the virtualbox GUI and check if VM creation in progress
## Review other files in the directory for your reference.

## check VM Status
$ vagrant status

## Login to the VMs and test access
$ vagrant ssh ansible-engine

## Ansible will be installed Ansible Engine node automatically; verify the same.
[vagrant@ansible-engine ~] ansible --version
[vagrant@ansible-engine ~] exit

## stop VM's once testing done; 
## no need to destroy as you can use the same lab on next day for practicing.
$ vagrant halt
```

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)