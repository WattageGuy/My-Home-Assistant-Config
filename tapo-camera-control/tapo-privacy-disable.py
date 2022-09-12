from pytapo import Tapo
import os

user = "" # user you set in Advanced Settings -> Camera Account
password = "" # password you set in Advanced Settings -> Camera Account
host1 = "" # ip of the camera, example: 192.168.1.52
host2 = "" # ip of the camera, example: 192.168.1.52
host3 = "" # ip of the camera, example: 192.168.1.52
host4 = "" # ip of the camera, example: 192.168.1.52

tapoH1 = Tapo(host1, user, password)
tapoH2 = Tapo(host2, user, password)
tapoH3 = Tapo(host3, user, password)
tapoH4 = Tapo(host4, user, password)

print(tapoH1.setPrivacyMode(""))
print(tapoH2.setPrivacyMode(""))
print(tapoH3.setPrivacyMode(""))
print(tapoH4.setPrivacyMode(""))

os.remove("path to file state")

import requests

url = 'discord webhook url'
myobj = {'content': 'Tapo kameror har återgått till normalt läge'}

x = requests.post(url, json = myobj)

print(x.text)