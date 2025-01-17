import requests

auth_url = "http://127.0.0.1:8000/api/v1/sign-in/"
auth_data = {
  "email": "aktanarynov566@gmail.com",
  "password": "stringst",
}
response = requests.post(auth_url, data=auth_data)
token = response.json()['token']
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1/"

auth_headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

def make_request(url, method='GET', data=None):
    if method == 'GET':
        response = requests.get(url, headers=auth_headers)
    elif method == 'POST':
        response = requests.post(url, headers=auth_headers, data=json.dumps(data))
    else:
        raise ValueError("Unsupported HTTP method")

    response.raise_for_status()
    return response.json()

print("Testing CategoryVideo ViewSet:")
print(make_request(f"{BASE_URL}category-video/"))

print("\nTesting Video ViewSet:")
print(make_request(f"{BASE_URL}video/"))

video_id = 1

print("\nChecking access to a video:")
access_check = make_request(f"{BASE_URL}video/{video_id}/check_access/")
print(access_check)

print("\nTesting TestContent ViewSet:")
print(make_request(f"{BASE_URL}test-content/"))

test_content_id = 1

print("\nSubmitting an answer to a test:")
submit_answer = make_request(f"{BASE_URL}test-content/{test_content_id}/submit_answer/", 
                             method='POST', 
                             data={'answer': 'a'})  # 'a' is just an example answer
print(submit_answer)

# print("\nResetting a test:")
# reset_test = make_request(f"{BASE_URL}test-content/{test_content_id}/reset_test/", 
#                           method='POST')
# print(reset_test)

print("\nTesting UserStatistic ViewSet:")
print(make_request(f"{BASE_URL}user-statistic/"))

print("\nTesting UserAnswer ViewSet:")
print(make_request(f"{BASE_URL}user-answer/"))

try:
    make_request(f"{BASE_URL}test-content/999/submit_answer/", 
                 method='POST', 
                 data={'answer': 'e'})
except requests.HTTPError as e:
    print("\nError when submitting answer to non-existent test or with invalid data:")
    print(e.response.json())
