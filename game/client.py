import requests

# 注册
r = requests.post('http://127.0.0.1:8000/game/register',
    data={'username': 'runtu881', 'password': 'runtuRmumu233', 'email': 'dsa@me.com'})

print(r.status_code)
print(r.text)
