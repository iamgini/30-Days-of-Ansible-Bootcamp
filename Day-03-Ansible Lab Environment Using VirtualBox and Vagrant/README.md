## Setting up Lab Environment

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)

[Setting up a Lab Environment using Vagrant and VirtualBox](https://www.youtube.com/watch?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK&v=qoliqxGvX84)

### Install VirtualBox

[Download](https://www.virtualbox.org/wiki/Downloads) and [install](https://www.virtualbox.org/manual/ch02.html) VirtualBox on your Laptop or Workstation. Select the appropriate package for your OS platform (Linux, Windows or Mac)

### Install Vagrant

[Download](https://www.vagrantup.com/downloads) and [install](https://www.vagrantup.com/docs/installation) Vagrant on your workstation or laptop.

**Spin up a test VM with Vagrant**

```bash
## initialize the VM and Vagrantfile
$ vagrant init centos/8

## spinup vagrant vm
$ vagrant up
 
## login to the VM
$ vagrant ssh

## destroy vagrant VM once tested
$ vagrant destroy
```

*Note: We have read-to-use `Vagrantfile` for setting up the Ansible Lab, so do not need to worry on this configurations.*

[Ansible Full Course – YouTube Playlist](https://youtu.be/K4wGqwS2RLw?list=PLH5uDiXcw8tSW9Y6FsVsSQJQ88tMPBsbK)