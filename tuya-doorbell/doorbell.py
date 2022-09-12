import requests
import subprocess
import time

response = requests.get('http://192.168.1.5:3333/api/stream/rtsp')
response = response.content
responseDecoded = response.decode("utf-8")

before = "ffmpeg -re -stream_loop -1 -i '"
after = "' -c:v copy -c:a aac -f rtsp rtsp://localhost:8554/doorbell"
ffmpegC = before + responseDecoded + after

print ("Using: '" + ffmpegC + "'")

subprocess.run(ffmpegC, shell=True)

print("Done")
