import subprocess
import time
import requests
from datetime import datetime

while True:
	time.sleep(5)
	now = datetime.now()
	date = now.strftime("%d/%m/%Y %H:%M:%S")
	camerastreamStart = subprocess.getoutput("sudo docker logs --since=5s  scrypted 2>&1 | grep 'destination address'")
	camerastreamEnd = subprocess.getoutput("sudo docker logs --since=5s scrypted  2>&1 | grep 'streaming session killed'")
	if camerastreamStart != "":
		print ("Streaming camera " + camerastreamStart)
		msg = ("Streaming camera " + camerastreamStart + " - " + str(date))
		url = 'discord webhook url'
		myobj = {'content': msg}
		x = requests.post(url, json = myobj)
	if camerastreamEnd != "":
		print ("Stopped camera " + camerastreamEnd)
		msg = ("Stopped camera " + camerastreamEnd + " - " + str(date))
		url = 'discord webhook url'
		myobj = {'content': msg}
		x = requests.post(url, json = myobj)