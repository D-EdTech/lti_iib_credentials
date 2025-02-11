import csv
import json
import os
import time
import sys
from blackboard.api import get_course_id, get_course_users, get_user_details
from utils.file_utils import JSON_FILENAME, CSV_FILENAME, CSV_FIELDNAMES, API_SLEEP_TIME, write_json, regenerate_csv


def pull_students_json(course_external_id, filename_prefix=None):
    """
    Pulls students from Blackboard and updates the core JSON data store.

    For each Blackboard user:
      - If the user's UUID exists in the JSON, update its details (merging new Blackboard data)
        while preserving reserved fields (such as sync_to_inspera and Inspera credentials).
      - If not, create a new entry.

    Then, a CSV file is generated from the JSON data using a fixed column order.

    The following field names are used for clarity:
      - sync_to_inspera: A flag indicating if a user should be synced to Inspera.
      - inspera_sync_timestamp: The timestamp when the Inspera credentials were last updated.
    """
    # Use default filenames unless a prefix is provided.
    if filename_prefix:
        json_filename = f"{filename_prefix}.json"
        csv_filename = f"{filename_prefix}.csv"
    else:
        json_filename = JSON_FILENAME
        csv_filename = CSV_FILENAME

    # Get the Blackboard course ID.
    course_id = get_course_id(course_external_id)
    time.sleep(API_SLEEP_TIME)
    if not course_id:
        print("❌ Course not found in Blackboard.")
        return

    # Retrieve Blackboard users.
    users = get_course_users(course_id)
    total_users = len(users)
    print(f"🔄 Found {total_users} users in course '{course_external_id}'.")

    # Load existing JSON data or start with an empty dictionary.
    if os.path.exists(json_filename):
        try:
            with open(json_filename, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"⚠️ Error reading existing JSON file: {e}")
            data = {}
    else:
        data = {}
        print("ℹ️ JSON file does not exist; starting with an empty dataset.")

    current_sync = time.strftime("%Y-%m-%d %H:%M:%S")

    # Process each Blackboard user.
    for user in users:
        time.sleep(API_SLEEP_TIME)
        user_details = get_user_details(user["userId"])
        uuid_val = user_details.get("uuid", "")
        if not uuid_val:
            # Skip if no UUID.
            continue

        entry = data.get(uuid_val, {})

        # REQUIRED FIELDS for Inspera sync.
        entry["uuid"] = uuid_val
        entry["blackboard_username"] = user_details.get("userName", "")
        entry["name_given"] = user_details.get("name", {}).get("given", "")
        entry["name_family"] = user_details.get("name", {}).get("family", "")
        entry["contact_email"] = user_details.get("contact", {}).get("email", "")

        # METADATA.
        entry["course_external_id"] = course_external_id
        entry["blackboard_sync_timestamp"] = current_sync
        if "inspera_sync_timestamp" not in entry:
            entry["inspera_sync_timestamp"] = "NEVER"
        # RESERVED for Inspera updates (preserve existing values).
        if "inspera_username" not in entry:
            entry["inspera_username"] = "UNKNOWN"
        if "inspera_password" not in entry:
            entry["inspera_password"] = ""
        if "inspera_sync_timestamp" not in entry:
            entry["inspera_sync_timestamp"] = "NEVER"

        data[uuid_val] = entry

    # Write updated JSON data.
    try:
        write_json(data, json_filename)
        print(f"📁 JSON file '{json_filename}' has been updated with {len(users)} records.")
    except Exception as e:
        print(f"❌ Error writing JSON file: {e}")

    # Generate CSV from JSON data.
    records = list(data.values())
    if not records:
        print("ℹ️ No records found in the JSON data. Skipping CSV generation.")
    else:
        try:
            regenerate_csv(records, csv_filename, CSV_FIELDNAMES)
            print(f"📁 CSV file '{csv_filename}' has been created with {len(records)} records.")
        except Exception as e:
            print(f"❌ Error writing CSV file: {e}")


if __name__ == "__main__":
    # Optionally accept the course external id as a command-line argument.
    course_external_id = sys.argv[1] if len(sys.argv) > 1 else "DALIAN_ZOGAJ_INSPERA_AS_Course"
    pull_students_json(course_external_id)
