from dotenv import load_dotenv
import os
from datetime import datetime
from utils.gdrive_utils import (
    read_docx,
    create_drive_folder,
    upload_doc,
    export_google_doc_to_pdf,
    update_google_sheet,
)

# Load values from .env
load_dotenv()

TEMPLATE_FILE_ID = os.getenv("TEMPLATE_FILE_ID")
PARENT_FOLDER_ID = os.getenv("PARENT_FOLDER_ID")
FINAL_DOCX_PATH = os.getenv("FINAL_DOCX_PATH")
FINAL_PDF_PATH = os.getenv("FINAL_PDF_PATH")


def main():
    job_title = input('Job title: ')
    job_desc = input('Job description, e.g., Full-Stack or Frontend: ')
    company = input('Name of company: ')
    site = input('Job board: ')
    url = input('URL: ')

    # Writes docx to /tmp
    print("Modifying resume...")
    replace_placeholders(output_path=FINAL_DOCX_PATH, data={
        '[Job Title]': job_title,
        '[Desc]': job_desc
    })

    # Get current date and time
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")

    # Create a new folder inside of the parent
    print("Creating folder on Google Drive...")
    folder_id = create_drive_folder(
        folder_name=(f"{company}-{date_string}"),
        parent_folder_id=PARENT_FOLDER_ID
    )

    # Upload modified doc
    print("Uploading to Google Drive...")
    file_id = upload_doc(file_path=FINAL_DOCX_PATH, folder_id=folder_id)

    # Export doc as PDF
    print("Exporting PDF...")
    export_google_doc_to_pdf(file_id=file_id, output_path=FINAL_PDF_PATH)

    # Update spreadsheet
    print("Updating spreadsheet...")
    update_google_sheet(company=company, site=site, url=url)

    print("Complete!")


def replace_placeholders(
    output_path: str,
    data: dict
) -> None:
    doc = read_docx(TEMPLATE_FILE_ID)

    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if key in paragraph.text:
                for run in paragraph.runs:
                    run.text = run.text.replace(key, value)

    doc.save(output_path)


if __name__ == '__main__':
    main()
