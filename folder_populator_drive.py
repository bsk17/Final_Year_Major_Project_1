# this program creates the folder and populates it with the photographs taken by open cv

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import glob
from PIL import Image

# If modifying these scopes, delete the file token.pickle.
# this is the base url to upload our files
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # this service will contains the credentials and will help us to communicate with the folders inside drive
    service = build('drive', 'v3', credentials=creds)

    # this is the id of the folder named INVOICE in Colab Notebook in google drive
    folder_id = '1zLxJ-kUlVP3CX1pWgpVcK_awrsiGMstt'

    # this is the additional info we provide to this program
    for filename in glob.glob('TrainingImage/*.jpg'):
        file_metadata = {
                'name': filename,
                'parents': [folder_id]
        }

        # need to improve this filename for proper uploading of images
        media = MediaFileUpload(filename,
                                mimetype='image/jpg',
                                resumable=True)
        file = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()

        print('File ID: %s' % file.get('id'))


if __name__ == '__main__':
    main()