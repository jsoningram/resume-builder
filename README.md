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

## Setup

To get this script working, we need to give it permission to talk to your Google Drive and Google Sheets. It's like giving a robot a key to a specific room so it can do a job for you. We'll get two special keys from Google.

### Step 1: Create Your Project in Google Cloud

Think of this as creating a new folder for a school project.

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/). You might need to sign in with your Google account.
2.  In the top-left corner, click the project dropdown menu and select **"New Project"**.
3.  Give your project a name, like "My Resume Helper", and click **"Create"**.

### Step 2: Turn on the Google Drive and Sheets Superpowers (APIs)

Now, we need to give our project the superpowers to use Google Drive and Sheets.

1.  Make sure your new project is selected at the top of the page.
2.  Click the navigation menu (the three horizontal lines ☰) in the top-left.
3.  Go to **"APIs & Services"** > **"Library"**.
4.  In the search bar, type **"Google Drive API"** and press Enter.
5.  Click on it and then click the big blue **"Enable"** button.
6.  Go back to the Library and do the same thing for the **"Google Sheets API"**.

### Step 3: Get the First Key (OAuth 2.0 for You)

This key is for you. When you run the script, Google will ask, "Hey, is it really you? Can this app access your files?" This key proves it's you.

1.  In the navigation menu (☰), go to **"APIs & Services"** > **"Credentials"**.
2.  Click **"+ Create Credentials"** at the top and choose **"OAuth client ID"**.
3.  If it asks, click **"Configure Consent Screen"**.
    -   Choose **"External"** and click **"Create"**.
    -   Give your app a name (e.g., "Resume App").
    -   Select your email for the user support and developer contact fields.
    -   Click **"Save and Continue"** all the way to the end.
4.  Go back to the **"Credentials"** tab.
5.  Click **"+ Create Credentials"** > **"OAuth client ID"** again.
6.  For the **"Application type"**, choose **"Desktop app"**.
7.  Click **"Create"**. A window will pop up. Click **"Download JSON"**.
8.  Find the downloaded file and rename it to **`credentials.json`**. Move this file into your project folder.

### Step 4: Get the Second Key (Service Account for the Robot)

This key is for the script itself, like a robot helper that can work on its own without asking for your password every time.

1.  You should still be on the **"Credentials"** page.
2.  Click **"+ Create Credentials"** and choose **"Service Account"**.
3.  Give the service account a name, like "sheet-updater-robot".
4.  Click **"Create and Continue"**.
5.  Click the **"Role"** dropdown and select **"Project"** > **"Editor"**. This lets the robot edit things in your project.
6.  Click **"Continue"**, then **"Done"**.
7.  Find the service account you just created in the list. Click on its email address.
8.  Go to the **"Keys"** tab.
9.  Click **"Add Key"** > **"Create new key"**.
10. Choose **"JSON"** as the key type and click **"Create"**.
11. A file will download automatically. Rename this file to **`keyfile.json`** and move it into your project folder.

### Step 5: Share Your Google Sheet with the Robot

Your robot helper has a key, but you still need to give it permission to open the specific spreadsheet you want it to write in.

1.  Open the `keyfile.json` file. You will see an email address next to `"client_email"`. It will look something like `robot-name@your-project.iam.gserviceaccount.com`. Copy this email address.
2.  Open the Google Sheet you want to use for logging your job applications.
3.  Click the green **"Share"** button in the top-right corner.
4.  Paste the robot's email address into the box and give it **"Editor"** access.
5.  Click **"Share"**.

### Step 6: Fill in Your `.env` File

This is the final step where you tell the script where to find everything.

1.  Make a copy of the `.env.example` file and rename it to `.env`.
2.  Open the `.env` file and fill in the details:
    -   `CLIENT_SECRETS_FILE`: `credentials.json`
    -   `AUTHORIZED_USER_FILE`: `token.json` (the script will create this for you)
    -   `JSON_KEYFILE`: `keyfile.json`
    -   `TEMPLATE_FILE_ID`: Go to your resume template (.docx format) in Google Drive, and the ID is the long string of letters and numbers in the URL.
    -   `PARENT_FOLDER_ID`: Same as above, but for the folder where you want to save the generated resumes. e.g.: 'Resumes'
    -   `SHEET_NAME`: The exact name of your Google Sheet you'll use to keep track of applications. e.g.: 'Applications'

## Install dependencies:

```bash
pip install -r requirements.txt
```

## Run application:

```bash
python resume.py
```

The first time you run the application, a browser window will open asking you to log in to your Google account to give it permission. After that, it will use the `token.json` file to remember you.

