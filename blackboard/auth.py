import requests
from config.settings import BLACKBOARD_BASE_URL, BLACKBOARD_CLIENT_ID, BLACKBOARD_CLIENT_SECRET


def get_blackboard_token():
    url = f"{BLACKBOARD_BASE_URL}/learn/api/public/v1/oauth2/token"
    print(url)
    auth = (BLACKBOARD_CLIENT_ID, BLACKBOARD_CLIENT_SECRET)
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, auth=auth, data=data)
    response.raise_for_status()
    return response.json().get("access_token")
