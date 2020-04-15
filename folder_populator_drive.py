# this program creates the folder and populates it with the photographs taken by open cv if not present in the drive

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

    # this is the id of the folder named Captured_Images in Colab Notebook in google drive
    folder_id = '1zLxJ-kUlVP3CX1pWgpVcK_awrsiGMstt'

    # this function will check for the image in Drive already present or not
    # if present then we skip the image and upload only if it is not present
    def checkFile(name):
        found = False
        # this is to search for the image already present or not

        page_token = None

        while True:
            response = service.files().list(q="mimeType='image/jpeg' and name =" + "'"+name+"'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()

            for file in response.get('files', []):
                print('Found file: %s (%s)' % (file.get('name'), file.get('id')))

                found = True

            page_token = response.get('nextPageToken', None)

            if page_token is None:
                break

        if found:
            return True
        else:
            return False

    # this is the additional info we provide to this program
    for filename in glob.glob('TrainingImage/*.jpg'):

        # we call the function with the argument as the file name already present
        if checkFile(filename.split(" ", 1)[-1]):
            print("File already present")

        # this means the file is not present so we have to upload
        else:
            print("Image "+filename.split(" ", 1)[-1] + " is uploading")

            file_metadata = {
                # this will take only he name from
                'name': filename.split(" ", 1)[-1],
                'parents': [folder_id]
            }

            media = MediaFileUpload(filename,
                                    mimetype='image/jpg',
                                    resumable=True)

            file = service.files().create(body=file_metadata,
                                          media_body=media,
                                          fields='id').execute()

            print('Uploaded Image ID: %s' % file.get('id'))


if __name__ == '__main__':
    main()