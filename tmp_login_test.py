import requests
url = 'https://advertisement-management-api-c2jb.onrender.com/Login'
params = {
    'email': 'codextest999@example.com',
    'password': 'Password123'
}
resp = requests.post(url, params=params, timeout=30)
print(resp.status_code)
print(resp.text)
