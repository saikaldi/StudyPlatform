import requests
import json

# Authentication endpoint
auth_url = 'https://api.recordonline.kg/api/v1/sign-in/'
auth_data = {
    'email': 'admin@gmail.com',
    'password': 'adminadmin'
}

# Function to get authentication token
def get_auth_token():
    response = requests.post(auth_url, json=auth_data)
    if response.status_code == 200:
        return response.json().get('token', None)
    else:
        print("Authentication failed:", response.status_code, response.text)
        return None

# Get the authentication token
token = get_auth_token()
if not token:
    exit()

# Common headers with token
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Base URL for API endpoints
base_url = 'http://localhost:8000/api/v1'

# Fetching all subjects
def get_all_subjects():
    url = f'{base_url}/subjects/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Subjects:", response.json())
    else:
        print("Failed to retrieve subjects:", response.status_code)

# Creating a new subject
def create_subject():
    url = f'{base_url}/subjects/'
    data = {'name': 'Physics'}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("Subject created successfully:", response.json())
    else:
        print("Failed to create subject:", response.status_code, response.text)

# Updating a graduate
def update_graduate():
    graduate_id = 1
    url = f'{base_url}/graduates/{graduate_id}/'
    data = {'score': 200}
    response = requests.patch(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Graduate updated successfully:", response.json())
    else:
        print("Failed to update graduate:", response.status_code, response.text)

# Deleting a teacher
def delete_teacher():
    teacher_id = 1
    url = f'{base_url}/teachers/{teacher_id}/'
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print("Teacher deleted successfully")
    else:
        print("Failed to delete teacher:", response.status_code, response.text)

# Creating feedback
def create_feedback():
    url = f'{base_url}/feedbacks/'
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'phone_number': '+996777123456',
        'text': 'Great experience!',
        'email': 'john.doe@example.com'  # Optional for unauthenticated users
    }
    # Feedback doesn't need authentication token as per your setup
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("Feedback submitted successfully:", response.json())
    else:
        print("Failed to submit feedback:", response.status_code, response.text)

# Execute all functions
get_all_subjects()
create_subject()
update_graduate()
delete_teacher()
create_feedback()
