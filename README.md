# Blackboard & Inspera Integrity Browser Credential Tool

This tool generates user credentials for Inspera Integrity Browser (IIB) without requiring SSO authentication, utilizing only LTI integration. It consists of two main scripts:

1. **Pull Students from Blackboard**  
   This script retrieves student data from Blackboard for a specified course and saves the data in a JSON file (the core data store) and exports it to a CSV file.

2. **Generate Credentials for Inspera Integrity Browser**  
   This script reads the CSV file and, for each student marked for credential generation, creates or updates their password entry in Inspera. It respects any manually provided password in the CSV and updates the Inspera username in the JSON record using the API response.  
   **Note:** This script does not create new Inspera users; it only generates login credentials for IIB.

## Table of Contents

- [Overview](#overview)
- [File Structure](#file-structure)
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [How to Use the Tool](#how-to-use-the-tool)
  - [Step 1: Pull Students from Blackboard](#step-1-pull-students-from-blackboard)
  - [Step 2: Generate Credentials for Inspera](#step-2-generate-credentials-for-inspera)
- [Configuration](#configuration)
- [Environment Variables](#environment-variables)
- [Dependencies](#dependencies)
- [Additional Setup for Blackboard REST API](#additional-setup-for-blackboard-rest-api)
- [Troubleshooting](#troubleshooting)
- [Contact and Support](#contact-and-support)

## Overview

This tool works in two stages:

1. **Pull Students from Blackboard:**  
   The script `pull_students_from_blackboard.py` connects to Blackboard, retrieves student information for a given course, and saves the data in:
   - A JSON file (e.g., `data/blackboard_users.json`)
   - A CSV file (e.g., `data/blackboard_users.csv`) with a fixed column order

2. **Generate Credentials for Inspera:**  
   The script `sync_students_to_inspera.py` reads the CSV file and for each student with a `generate_iib_credentials` flag of "true":
   - Checks the corresponding JSON record.
   - Uses the provided password from the CSV (if available) or the JSON record; if none is available, it generates a new one.
   - Updates the student’s credentials in Inspera via the API (without changing the username).
   - If the update is successful, it updates the Inspera username (based on the API response) and records the current timestamp in the JSON file.

## File Structure

```
LTI_IIB_SYNC
├── .venv/  # Virtual environment
├── blackboard/
│   ├── __init__.py
│   ├── api.py
│   ├── auth.py
├── config/
│   ├── __init__.py
│   ├── settings.py  # Configuration settings (file names, API sleep time, etc.)
├── data/
│   ├── blackboard_users.csv  # CSV data file
│   ├── blackboard_users.json  # JSON data store
├── inspera/
│   ├── __init__.py
│   ├── api.py
│   ├── auth.py
├── utils/
│   ├── __init__.py
│   ├── file_utils.py  # Helper functions for reading/writing JSON and CSV files
│   ├── helpers.py  # Utility functions (e.g., generate_password, parse_sync_flag)
├── .env  # Environment variables file (must be created)
├── pull_students_from_blackboard.py
├── sync_students_to_inspera.py
├── README.md
├── requirements.txt  # Dependencies
```

*Note:* The JSON and CSV files are stored in the `data` folder, as configured in the settings.

## Requirements

- **Python 3.10 or Higher**  
  Ensure you have Python 3.10 + installed.

- **API Access**  
  You must have proper access and credentials for the Blackboard and Inspera REST APIs.

## Environment Variables

For this tool to function properly, you must create a `.env` file in the project root and define the following variables:

```
BLACKBOARD_BASE_URL=https://your.blackboard.tenant.com/
BLACKBOARD_CLIENT_ID=
BLACKBOARD_CLIENT_SECRET=

INSPERA_BASE_URL=https://your.inspera.tenant.com/api
INSPERA_API_KEY=
INSPERA_CLIENT_ID=

INSPERA_LTI_DEPLOYMENT_ID=
```

These variables provide necessary API credentials and configurations required for communication between Blackboard and Inspera.

## Setup and Installation

1. **Download or Clone the Project**  
   Place all files into a single folder on your computer.

2. **Create the Data Folder**  
   Ensure there is a folder named `data` in the project root. (The configuration automatically creates it if missing.)

3. **Create the `.env` File**  
   Manually create a `.env` file in the root directory and populate it with the required environment variables.

4. **Configure Settings**  
   Open `config/settings.py` and verify:
   - **Data Directory:** The JSON and CSV files are stored in the `data` folder.
   - **API_SLEEP_TIME:** The delay between API calls (default is 0.5 seconds) can be adjusted if needed.

5. **Install Dependencies**  
   Create a `requirements.txt` file with the following content:

   ```
   certifi==2025.1.31
   charset-normalizer==3.4.1
   idna==3.10
   python-dotenv==1.0.1
   requests==2.32.3
   urllib3==2.3.0
   ```

   Then run:
   ```bash
   pip install -r requirements.txt
   ```

## Additional Setup for Blackboard REST API

- Enable the REST API in Blackboard.
- Configure API credentials.
- Ensure network connectivity for API calls.

## Troubleshooting

- **Missing Files:** Run the Blackboard pull script first.
- **Invalid `generate_iib_credentials` Flag:** Ensure it contains only `"true"` or `"false"`.
- **API Errors:** Verify credentials and network connection.
- **Password Issues:** Ensure passwords in the CSV are correctly entered.

Enjoy using the Blackboard & Inspera Integrity Browser Credential Tool!

