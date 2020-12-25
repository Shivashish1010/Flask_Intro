import requests, random
url = 'http://localhost:5000/event'

types = ["increment", "decrement"]

for i in range(100):
    value = random.randint(1,5)
    type = random.choice(types)
    myobj = {"value":value, "type": type}
    x = requests.post(url, json=myobj)
    print(x.json())

# print(x.json())