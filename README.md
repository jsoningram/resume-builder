# Python Resume Builder
A simple automation tool for generating tailored resumes and organizing job applications using Google Drive and Sheets.

This script reads a Word document (`.docx`), replaces placeholder values like `[Job Title]` and `[Desc]`, uploads the result to a Google Drive folder (named by company and date), exports a PDF copy, and logs the job application in a Google Sheet.

## Features

- Reads and modifies a `.docx` resume file
- Uploads the generated resume to Google Drive
- Exports the uploaded Google Doc to PDF
- Saves both `.docx` and `.pdf` locally
- Logs job applications in a Google Sheet with company, date, site, and job link

---

## Requirements

Python 3.13+

## Install dependencies:

```bash
pip install -r requirements.txt
```

## Run application:

```bash
python resume.py
```
