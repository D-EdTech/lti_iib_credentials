import csv
import json
import os
import time
import sys
from inspera.api import get_inspera_user, update_inspera_user
from utils.helpers import generate_password, parse_sync_flag
from utils.file_utils import JSON_FILENAME, CSV_FILENAME, CSV_FIELDNAMES, API_SLEEP_TIME, write_json, regenerate_csv


def sync_inspera(json_filename=JSON_FILENAME, csv_filename=CSV_FILENAME):
    """
    Reads the CSV file and, for each row flagged with sync_to_inspera=="true",
    performs the following:
      - Checks if the user (by UUID) exists in the core JSON data store.
        If not, the row is skipped.
      - Loads the corresponding JSON record.
      - If inspera_password is empty, uses the password provided in CSV if available;
        otherwise, generates a new random password.
      - Checks if the user exists in Inspera (using get_inspera_user).
        (This script never creates new users in Inspera.)
      - Calls the Inspera API to update the user (updating password and other fields,
        but not username).
      - On success, sets inspera_sync_timestamp to the current timestamp and updates
        inspera_username with the username returned from update_inspera_user.
        On failure, sets inspera_sync_timestamp to "LAST UPDATE FAILED".
      - Does NOT update the sync_to_inspera flag (leaves it as is).

    Finally, the JSON file is overwritten with the updated data and the CSV file is
    regenerated from the JSON data using a static column order.
    """
    # Load JSON core data.
    if not os.path.exists(json_filename):
        print(f"❌ JSON file '{json_filename}' not found.")
        return

    try:
        with open(json_filename, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return

    # Load CSV rows.
    if not os.path.exists(csv_filename):
        print(f"❌ CSV file '{csv_filename}' not found.")
        return

    try:
        with open(csv_filename, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            csv_rows = [row for row in reader]
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return

    current_sync = time.strftime("%Y-%m-%d %H:%M:%S")

    # Process each CSV row flagged for syncing.
    for index, row in enumerate(csv_rows, start=1):
        # Normalize and validate the sync flag.
        sync_flag = parse_sync_flag(row.get("sync_to_inspera", ""))
        if sync_flag is None:
            print(f"⚠️ Row {index}: sync_to_inspera flag value is invalid; skipping row.")
            continue
        if sync_flag != "true":
            continue  # Skip rows not marked "true".

        uuid_val = row.get("uuid", "")
        if not uuid_val:
            print(f"⚠️ Row {index}: Missing UUID; skipping update.")
            continue

        if uuid_val not in data:
            print(f"⚠️ Row {index}: UUID {uuid_val} not found in JSON; skipping update.")
            continue

        record = data[uuid_val]

        # Use the password from CSV if available.
        csv_password = row.get("inspera_password", "").strip()
        if csv_password:
            password = csv_password
            record["inspera_password"] = csv_password
        else:
            # Otherwise, use the existing JSON password (if any) or generate a new one.
            password = record.get("inspera_password", "")
            if not password:
                password = generate_password()
                record["inspera_password"] = password

        # Check if the Inspera user exists (do not create new users).
        inspera_user = get_inspera_user(uuid_val)
        time.sleep(API_SLEEP_TIME)
        if not (inspera_user and isinstance(inspera_user, list) and len(inspera_user) > 0):
            print(f"⚠️ Row {index}: Inspera user for UUID {uuid_val} not found; skipping update.")
            continue

        # Use the existing username from Inspera.
        inspera_user_data = inspera_user[0]
        updated_user = {
            "username": inspera_user_data["username"],  # Username remains unchanged.
            "firstName": record.get("name_given", ""),
            "lastName": record.get("name_family", ""),
            "email": record.get("contact_email", ""),
            "password": password
        }

        response = update_inspera_user(updated_user)
        time.sleep(API_SLEEP_TIME)
        if response and response.get("success"):
            record["inspera_sync_timestamp"] = current_sync
            # Update the inspera_username with the username from the response.
            new_username = response.get("username")
            if new_username:
                record["inspera_username"] = new_username
            print(f"✅ Row {index}: Updated Inspera user for UUID {uuid_val}.")
        else:
            record["inspera_sync_timestamp"] = "LAST UPDATE FAILED"
            print(f"❌ Row {index}: Failed to update Inspera user for UUID {uuid_val}.")

    try:
        write_json(data, json_filename)
        print(f"📁 JSON file '{json_filename}' updated with the latest Inspera sync info.")
    except Exception as e:
        print(f"❌ Error writing JSON file: {e}")
        return

    records = list(data.values())
    try:
        regenerate_csv(records, csv_filename, CSV_FIELDNAMES)
        print(f"📁 CSV file '{csv_filename}' has been regenerated with updated data.")
    except Exception as e:
        print(f"❌ Error writing CSV file: {e}")


if __name__ == "__main__":
    sync_inspera()
