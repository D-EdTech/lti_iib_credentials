import requests
from config.settings import INSPERA_BASE_URL, INSPERA_API_KEY, INSPERA_CLIENT_ID

def get_inspera_token():
    """Retrieve Inspera access token"""
    auth_url = f"{INSPERA_BASE_URL}/authenticate/token/"
    auth_params = {"client_id": INSPERA_CLIENT_ID, "grant_type": "authorization_code"}

    try:
        response = requests.post(auth_url, data=auth_params, headers={"code": INSPERA_API_KEY})
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Failed to authenticate with Inspera: {e}")
        return None
