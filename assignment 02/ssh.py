import os
import paramiko
import random
from scp import SCPClient
from string import ascii_letters, punctuation


class ssh_session():
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.client = ''
        self.file_password = ''

    def commands(self):
        self.commands = ['''sudo mkdir BACKUP-$(date +"%d-%m-%Y");
                            sudo cp /etc/{hosts,fstab,resolv.conf,sysctl.conf,network/interfaces} BACKUP-$(date +"%d-%m-%Y");
                            zip -er BACKUP-$(date +"%d-%m-%Y").zip BACKUP-$(date +"%d-%m-%Y") -P ''' + self.file_password + ''';''',
                         'sudo rm -rf BACKUP-$(date +"%d-%m-%Y") BACKUP-$(date +"%d-%m-%Y").zip'
                         ]
        return self.commands

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(self.host, username=self.username, password=self.password)

    def close_connection(self):
        self.client.close()

    def generate_password(self):
        # Generate password for the compressed file
        for x in range(20):
            self.file_password += random.choice(ascii_letters) + str(random.randint(0, 9))

    def exec_commands(self, command):
        session = self.client.get_transport().open_session()
        session.set_combine_stderr(True)
        session.get_pty()
        session.exec_command(command)
        stdin = session.makefile('wb', -1)
        stdout = session.makefile('rb', -1)
        stdin.write(self.password + '\n')
        stdin.flush()
        stdout.read().decode("utf-8")

    def move_file(self):
        os.system(f'sshpass -p {self.password} scp -r {self.username}@{self.host}:~/BACKUP-$(date +"%d-%m-%Y").zip ~/BACKUP-$(date +"%d-%m-%Y").zip')

    def run(self):
        self.connect()
        self.generate_password()
        self.exec_commands(self.commands()[0])
        self.move_file()
        self.exec_commands(self.commands[1])
        self.close_connection()
        print('Backup file is ready!')
        return self.file_password
