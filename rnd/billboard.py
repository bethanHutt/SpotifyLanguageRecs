import requests

URL = 'https://www.billboard.com/charts/japan-hot-100'

result = requests.get(URL)

print(result.content)
