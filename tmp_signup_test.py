import requests
url = 'https://advertisement-management-api-c2jb.onrender.com/SignUp'
params = {
    'email': 'codextest999@example.com',
    'role': 'User'
}
data = {
    'username': 'codextest',
    'password': 'Password123'
}
resp = requests.post(url, params=params, data=data, timeout=30)
print(resp.status_code)
print(resp.text)
