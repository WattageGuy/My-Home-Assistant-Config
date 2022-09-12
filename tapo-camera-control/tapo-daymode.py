from pytapo import Tapo
import os

user = "" # user you set in Advanced Settings -> Camera Account
password = "" # password you set in Advanced Settings -> Camera Account
host1 = "" # ip of the camera, example: 192.168.1.52

tapoH1 = Tapo(host1, user, password)

print(tapoH1.setDayNightMode("off"))

os.remove("path for file state")