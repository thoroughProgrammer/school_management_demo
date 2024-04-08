from datetime import datetime
from sqlite3 import OperationalError as SQLOperationalError
from django.db.utils import OperationalError as DjangoOperationalError
import os
from main.settings import MEDIA_ROOT, FOLDER_ID, GOOGLE_PROJECT_ID, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from googleapiclient.http import MediaFileUpload
from django.db.utils import ProgrammingError


from main.settings import BASE_DIR

import json
import base64


def generate_school_id():
    from .models import User

    try:
        if User.objects.all().count() == 0:
            return "B000000"
        current_year = datetime.now().year
        last_user_id = User.objects.last().id
        return "B{}".format(str(current_year)[-2:]) + str(last_user_id + 1 + 1000)
    except AttributeError:
        return "B000000"
    except SQLOperationalError:
        return "B000000"
    except DjangoOperationalError:
        return "B000000"
    except ProgrammingError:
        pass


def upload_user_pic(school_id, profile_pic_url):

    file_path = os.listdir(MEDIA_ROOT)[0]

    SCOPES = ["https://www.googleapis.com/auth/drive"]

    """
    Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
<<<<<<< HEAD
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_config = {
                "installed": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "project_id": GOOGLE_PROJECT_ID,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uris": ["http://localhost"]
                }
            }

            flow = InstalledAppFlow.from_client_config(
                client_config, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
=======
    try:
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                client_config = {
                    "installed": {
                        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                        "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                        "redirect_uris": ["http://localhost"],
                    }
                }

                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    except Exception as E:
        print("creds error: ", E)
>>>>>>> 81d667a33dc2a4dea5a41db5c289d0766c81e239

    try:
        service = build("drive", "v3", credentials=creds)

        file_metadata = {"name": f"{school_id}", "parents": [FOLDER_ID]}

        media = MediaFileUpload(
            os.path.join(MEDIA_ROOT, file_path),
            mimetype=f"image/{file_path.split('.')[-1]}",
        )

        if profile_pic_url:

            file = (
                service.files()
                .update(
                    fileId=profile_pic_url.split("=")[-1],
                    media_body=media,
                )
                .execute()
            )

            return "https://drive.google.com/uc?id=" + file.get("id")

        file = (
            service.files()
            .create(
                body=file_metadata,
                media_body=media,
                fields="id",
            )
            .execute()
        )

        # print(f'File ID: {file.get("id")}')

        # response = (
        #     service.files()
        #     .list(
        #         q="mimeType = 'application/vnd.google-apps.folder'",
        #         spaces="drive",
        #         fields="nextPageToken, " "files(id, name)",
        #     )
        #     .execute()
        # )
        # print(response)
        # for file in response.get("files", []):
        #     # Process change
        #     print(f'Found file: {file.get("name")}, {file.get("id")}')

        return "https://drive.google.com/uc?id=" + file.get("id")

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")

    except Exception as e:
        print("error: ", e)
