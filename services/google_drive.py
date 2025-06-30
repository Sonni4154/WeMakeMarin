import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
TOKEN_FILE = os.path.join(os.path.dirname(__file__), '..', 'drive_token.json')
CREDENTIALS_FILE = os.environ.get('GOOGLE_OAUTH_FILE', 'credentials.json')

def get_credentials():
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def list_files():
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=100, fields="files(id,name,mimeType,modifiedTime)").execute()
    return results.get('files', [])

def download_file(file_id, out_path):
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(out_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.close()
    return out_path