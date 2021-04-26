import requests

x = requests.get("http://192.168.86.178:5000/bpm")
print(x.text)