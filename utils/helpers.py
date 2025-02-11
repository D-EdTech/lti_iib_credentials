import random
import string
import json
import csv
import os

def generate_password(length=8):
    """Generate a random password"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def save_users_to_json(users, filename="data/users.json"):
    """Save users data to a JSON file"""
    with open(filename, "w") as f:
        json.dump(users, f, indent=4)


def save_users_to_csv(users, filename="data/users.csv"):
    """Save users data to a CSV file dynamically based on actual user structure"""

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if not users:
        print("❌ No users to save.")
        return

    # Dynamically get the correct keys from the latest user structure
    keys = users[0].keys()  # Extract fields dynamically

    # Write to CSV file
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(users)


def parse_sync_flag(value):
    """
    Normalizes and validates the sync_to_inspera flag.

    Strips leading/trailing whitespace and converts to lowercase.
    Returns:
      - "true" or "false" if valid,
      - None if the value is invalid.
    """
    if not value:
        return None
    normalized = value.strip().lower()
    if normalized in ("true", "false"):
        return normalized
    else:
        print(f"⚠️ Invalid sync_to_inspera flag value: '{value}'")
        return None
