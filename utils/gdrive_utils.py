from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from docx import Document
from datetime import datetime
from dotenv import load_dotenv
import gspread
import io
import os

# Load values from .env
load_dotenv()

SHEET_NAME = os.getenv("SHEET_NAME")
AUTHORIZED_USER_FILE = os.getenv("AUTHORIZED_USER_FILE")  # token.json
CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRETS_FILE")  # credentials.json
JSON_KEYFILE = os.getenv("JSON_KEYFILE")  # keyfile.json

# Scopes for Sheets and Drive
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]


# Load or request authorization
def authenticate():
    creds = None

    if os.path.exists(AUTHORIZED_USER_FILE):
        creds = Credentials.from_authorized_user_file(
            AUTHORIZED_USER_FILE,
            SCOPES
        )

    # If no valid credentials, ask user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save credentials
        with open(AUTHORIZED_USER_FILE, "w") as token:
            token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)

    return service


def read_docx(file_id):
    """Download a .docx from Google Drive and read it using python-docx."""
    service = authenticate()

    # Request the file content as a stream
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False

    while not done:
        status, done = downloader.next_chunk()

    # Reset the stream pointer to the beginning
    fh.seek(0)

    # Read the Word document from the BytesIO stream
    document = Document(fh)

    return document


def create_drive_folder(folder_name, parent_folder_id=None):
    """
    Creates a folder in Google Drive and returns its folder ID.

    Parameters:
    folder_name (str): Name of the folder to be created.
    parent_folder_id (str, optional): ID of the parent folder. 
                                      If None, the folder is created in the root.

    Returns:
    str: The ID of the newly created folder.
    """
    # Authenticate and initialize Drive API client
    service = authenticate()

    # Metadata for the new folder
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    # If a parent folder ID is provided, set it as the parent of this new folder
    if parent_folder_id:
        folder_metadata['parents'] = [parent_folder_id]

    # Create the folder
    folder = service.files().create(
        body=folder_metadata,
        fields='id'  # Only return the folder ID
    ).execute()

    return folder.get('id')


def upload_doc(file_path, folder_id=None):
    service = authenticate()
    mimetype = (
        'application/'
        'vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

    file_metadata = {
        'name': os.path.basename(file_path),
        'mimeType': "application/vnd.google-apps.document",
    }

    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(
        file_path,
        mimetype=mimetype
    )

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return file.get('id')


def export_google_doc_to_pdf(file_id, output_path):
    """Export a Google Doc (not .docx) to PDF and save it locally."""
    service = authenticate()

    request = service.files().export_media(
        fileId=file_id,
        mimeType='application/pdf'
    )

    with open(output_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)

        done = False

        while not done:
            status, done = downloader.next_chunk()


def update_google_sheet(company: str, site: str, url: str = None):
    # Load credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        JSON_KEYFILE,
        SCOPES
    )

    # Authorize the client
    client = gspread.authorize(creds)

    # Open the Google Sheet by name or URL
    sheet = client.open(SHEET_NAME).sheet1  # First sheet

    # Get current date and time
    now = datetime.now()
    date_string = now.strftime("%m/%d/%Y")

    # 3. Append a new row
    sheet.append_row([company, date_string, site, url])
