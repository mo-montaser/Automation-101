import os
import ssh
import GoogleDrive
import slack

# ssh server info
host = 'add host here!'
username = 'add username here!'
password = 'add password here!'

# ssh opertions
ssh_opertions = ssh.ssh_session(host, username, password)
file_password = ssh_opertions.run()

# upload the file to google drive
my_drive = GoogleDrive.GDrive()
Gdrive_folder_id = 'add Google drive folder id here!'
file_path = os.path.expanduser('~/')
file_name = os.popen(f'ls {file_path} | grep BACKUP').read().strip()
my_drive.upload_file(Gdrive_folder_id, file_name, file_path)

# remove the file from local
os.popen(f'rm -rf ~/{file_name}')

# send the password to Slack
url = 'add Slack Webhook URL here!'
message = f'{file_name} --> {file_password}'
slack_message = slack.SendMessage(url, message)
slack_message.send()
