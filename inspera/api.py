import requests
import time
from inspera.auth import get_inspera_token
from config.settings import INSPERA_BASE_URL, INSPERA_LTI_DEPLOYMENT_ID

def get_inspera_user(uuid, default_user_id=True):
    """Fetch user from Inspera by UUID"""
    token = get_inspera_token()
    if not token:
        return None

    if default_user_id:
        url = f"{INSPERA_BASE_URL}/v1/users/external/LTI/{INSPERA_LTI_DEPLOYMENT_ID}{uuid}?includeStudent=True"
    else:
        url = f"{INSPERA_BASE_URL}/v1/users/external/LTI/{uuid}?includeStudent=True"

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        #print(f"⚠️ Inspera user for UUID {uuid} not found.")
        return None

def update_inspera_user(user_data):
    """Create a user in Inspera"""
    token = get_inspera_token()
    if not token:
        return None

    url = f"{INSPERA_BASE_URL}/v1/users/student"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=user_data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error updating Inspera user: {e}")
        return None
