import subprocess
from subprocess import Popen, PIPE
mypass = "password"
runansible = subprocess.run(['ansible-playbook', 'site.yaml', '--ask-vault-pass'], stdin=PIPE)
Popen.communicate('mypass\n'.encode())

#import pexpect
#child = pexpect.spawn('ansible-playbook main.yml --ask-vault-pass')
#child.expect('password')
#child.sendline('test')
#child.interact()