import requests
from blackboard.auth import get_blackboard_token
from config.settings import BLACKBOARD_BASE_URL

def get_course_id(external_id):
    """Fetch Blackboard Course ID from external ID"""
    token = get_blackboard_token()
    url = f"{BLACKBOARD_BASE_URL}/learn/api/public/v1/courses?externalId={external_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    courses = response.json().get("results", [])
    return courses[0]["id"] if courses else None

def get_course_users(course_id):
    """Get only users with the role of 'Student' from Blackboard Course"""
    token = get_blackboard_token()
    url = f"{BLACKBOARD_BASE_URL}/learn/api/public/v1/courses/{course_id}/users"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Filter out only students
    users = response.json().get("results", [])
    student_users = [user for user in users if user.get("courseRoleId") == "Student"]

    return student_users

def get_user_details(user_id):
    """Get Blackboard User Details"""
    token = get_blackboard_token()
    url = f"{BLACKBOARD_BASE_URL}/learn/api/public/v1/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
