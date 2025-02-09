# import requests

# tk = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2NTMzMTMyLCJpYXQiOjE3MzY1MzI4MzIsImp0aSI6ImNjODcwZmMwNzhiYjQwZWNhYjYwMzk2OTQxYTYyZmQzIiwidXNlcl9pZCI6Mn0.MS3gY990HbaevDOwxUO1RDjqfJ9w6Mq4danL-PcVpcs"

# BASE_URL = "http://127.0.0.1:8000/api/v1"
# HEADERS = {
#     "Authorization": f"Bearer {tk}",
#     "Content-Type": "application/json",
# }

# def create_user_answer():
#     url = f"{BASE_URL}/confirm-user-status-priveligion/"
#     data = {
#         "email": "aktanarynov567@gmail.com"
#     }

#     try:
#         response = requests.post(url, json=data, headers=HEADERS)
#         response.raise_for_status()  # Генерирует исключение для статусов 4xx, 5xx
        
#         print("Успех:", response.status_code, response.json())
#     except requests.exceptions.HTTPError as http_err:
#         # Распечатываем весь ответ с ошибкой
#         print(f"HTTP ошибка произошла: {http_err}")
#         print("Ответ:", response.text)  # Логируем тело ответа для более подробной информации
#     except Exception as err:
#         print(f"Произошла другая ошибка: {err}")

# create_user_answer()
import requests

# Base URL for your API
base_url = "http://localhost:8000/api/v1/"

# Headers for authentication, assuming you have a token for an admin or manager
# Note: You should replace 'your_jwt_token_here' with an actual JWT token for an authenticated user.
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM2Njg1MjU4LCJpYXQiOjE3MzY2ODQ5NTgsImp0aSI6IjBhZjQzZjFlMDU3YTQzZDA5YzlhYmJkNWZhOWIwMjI5IiwidXNlcl9pZCI6Mn0.mXggdwGQPR6FMAQkw7_x3MJ4VqLQCxLTrNOFEMNzMho",
    "Content-Type": "application/json"
}

# Test Subject List
def test_subject_list():
    response = requests.get(f"{base_url}subjects/")
    if response.status_code == 200:
        print("Subject list fetched successfully.")
        print(response.json())
    else:
        print(f"Failed to fetch subjects. Status code: {response.status_code}")

# Test Create Subject (only for admin/manager/teacher)
def test_create_subject():
    new_subject = {
        "name": "Физика"
    }
    response = requests.post(f"{base_url}subjects/", json=new_subject, headers=headers)
    if response.status_code == 201:
        # print("Subject created successfully.")
        print(response.json())
    else:
        # print(f"Failed to create subject. Status code: {response.status_code}")
        print(response.json())

# Test Graduate Detail (Assuming there's a graduate with slug 'ivan-ivanov')
def test_graduate_detail():
    slug = "ivan-ivanov"
    response = requests.get(f"{base_url}graduates/{slug}/")
    if response.status_code == 200:
        print("Graduate detail fetched successfully.")
        print(response.json())
    else:
        print(f"Failed to fetch graduate details. Status code: {response.status_code}")

# Test Create Feedback (only for admin/manager/teacher)
def test_create_feedback():
    new_feedback = {
        "first_name": "Тест",
        "last_name": "Тестов",
        "email": "test@example.com",
        "phone_number": "+996700123456",
        "text": "Это тестовый отзыв."
    }
    response = requests.post(f"{base_url}feedbacks/", json=new_feedback, headers=headers)
    if response.status_code == 201:
        # print("Feedback created successfully.")
        print(response.json())
    else:
        # print(f"Failed to create feedback. Status code: {response.status_code}")
        print(response.json())

# Test functions
test_subject_list()
test_create_subject()
test_graduate_detail()
test_create_feedback()
