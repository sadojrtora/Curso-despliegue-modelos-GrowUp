import requests
url = "http://127.0.0.1:8000"
r = requests.get(f"{url}/")
print(r.json())
pacient = {

  "sbp": 160,

  "Tabaco": 12,

  "ldl": 5.73,

  "Adiposidad": 23.11,

  "Familia": "Presente",

  "Tipo": 49,

  "Obesidad": 25.3,

  "Alcohol": 97.2,

  "Edad": 62

}
r = requests.post(f"{url}/predict", json=pacient)
print(r.json())