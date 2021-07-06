import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload


class GDrive():
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        self.service = build('drive', 'v3', credentials=creds)

    def upload_file(self, Gdrive_folder_id, file_name, file_path):
        file_metadata = {
            'name': file_name,
            'parents': [Gdrive_folder_id]
        }
        media = MediaFileUpload(file_path + file_name, mimetype='application/zip')
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print('File was uploaded successfully')
