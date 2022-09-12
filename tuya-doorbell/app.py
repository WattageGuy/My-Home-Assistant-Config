#!/usr/bin/python
# -*- coding: UTF-8 -*-

import base64
import hashlib
import ssl
import websocket
import json
import time
import requests

try:
    import thread
except ImportError:
    import _thread as thread

# env
MQ_ENV_PROD = "event"
MQ_ENV_TEST = "event-test"

# accessId, accessKey，serverUrl，MQ_ENV
ACCESS_ID = ""
ACCESS_KEY = ""
WSS_SERVER_URL = "wss://mqe.tuyaeu.com:8285/"
MQ_ENV = MQ_ENV_TEST

# basic config
WEB_SOCKET_QUERY_PARAMS = "?ackTimeoutMillis=3000&subscriptionType=Failover"
SSL_OPT = {"cert_reqs": ssl.CERT_NONE}

CONNECT_TIMEOUT_SECONDS = 3
CHECK_INTERVAL_SECONDS = 3

PING_INTERVAL_SECONDS = 30
PING_TIMEOUT_SECONDS = 3

RECONNECT_MAX_TIMES = 1000

# global variable
global ws
ws = None

global reconnect_count
reconnect_count = 1

global connect_status
connect_status = 0


# topic env
def get_topic_url():
    return WSS_SERVER_URL + "ws/v2/consumer/persistent/" + ACCESS_ID + "/out/" + MQ_ENV + "/" + ACCESS_ID + "-sub" + WEB_SOCKET_QUERY_PARAMS


# handler message
def message_handler(payload):
    # print("payload:%s" % payload)
    dataMap = json.loads(payload)
    decryptContentDataStr = dataMap['data']
    print("\ndecryptContentData={}".format(decrypt_by_aes(decryptContentDataStr, ACCESS_KEY)))
    pyCheck = format(decrypt_by_aes(decryptContentDataStr, ACCESS_KEY))
    print('pyCheck')

    import re
    regexp = re.compile(r'doorbell') # <-- What to check for in data string
    if regexp.search(pyCheck):
        url = 'http://192.168.1.6:8123/api/webhook/doorbell' # Webscoket URL to scypted
        myobj = {}
        x = requests.post(url, data=myobj)
        url2 = 'http://192.168.1.5:11080/endpoint/30/public/' # Webscoket URL to scypted
        myobj2 = {}
        x = requests.post(url2, data=myobj2)
        print('Doorbell action found! Websocket sent')
    else:
        print('Data string found but not any doorbell press activity')

    regexMotion = re.compile(r'movement_detect_pic') # <-- What to check for in data string
    if regexMotion.search(pyCheck):
        url = 'http://192.168.1.5:11080/endpoint/29/public/' # # Webscoket URL to scypted
        myobj = {}
        x = requests.post(url, data=myobj)
        print('Motion triggered')
    else:
        print('Data string found but no motion where triggered')


# decrypt
def decrypt_by_aes(raw, key):
    import base64
    from Crypto.Cipher import AES
    raw = base64.b64decode(raw)
    key = key[8:24]
    cipher = AES.new(key, AES.MODE_ECB)
    raw = cipher.decrypt(raw)
    res_str = raw.decode('utf-8')
    res_str = eval(repr(res_str).replace('\\r', ''))
    res_str = eval(repr(res_str).replace('\\n', ''))
    res_str = eval(repr(res_str).replace('\\f', ''))
    return res_str


def md5_hex(md5_str):
    md = hashlib.md5()
    md.update(md5_str.encode('utf-8'))
    return md.hexdigest()


def gen_pwd():
    md5_hex_key = md5_hex(ACCESS_KEY)
    mix_str = ACCESS_ID+md5_hex_key
    return md5_hex(mix_str)[8:24]


def on_error(ws, error):
    print("on error is: %s" % error)


def reconnect():
    global reconnect_count
    print("ws-client connect status is not ok.\ntrying to reconnect for the %d time" % reconnect_count)
    reconnect_count += 1
    if reconnect_count < RECONNECT_MAX_TIMES:
        thread.start_new_thread(connect, ())


def on_message(ws, message):
    message_json = json.loads(message)
    payload = base64_decode_as_string(message_json["payload"])
    print("---\nreceived message origin payload: %s" % payload)
    # handler payload
    try:
        message_handler(payload)
    except Exception as e:
        print("handler message, a business exception has occurred,e:%s" % e)
    send_ack(message_json["messageId"])


def on_close(obj):
    print("Connection closed!")
    obj.close()
    global connect_status
    connect_status = 0


def connect():
    print("---\nws-client connecting...")
    ws.run_forever(sslopt=SSL_OPT, ping_interval=PING_INTERVAL_SECONDS, ping_timeout=PING_TIMEOUT_SECONDS)


def send_ack(message_id):
    json_str = json.dumps({"messageId": message_id})
    ws.send(json_str)


def base64_decode_as_string(byte_string):
    byte_string = base64.b64decode(byte_string)
    return byte_string.decode('ascii')


def main():
    header = {"Connection": "Upgrade",
              "username": ACCESS_ID,
              "password": gen_pwd()}

    websocket.setdefaulttimeout(CONNECT_TIMEOUT_SECONDS)
    global ws
    ws = websocket.WebSocketApp(get_topic_url(),
                                header=header,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    thread.start_new_thread(connect, ())
    while True:
        time.sleep(CHECK_INTERVAL_SECONDS)
        global reconnect_count
        global connect_status
        try:
            if ws.sock.status == 101:
                print("ws-client connect status is ok.")
                reconnect_count = 1
                connect_status = 1
        except Exception:
            connect_status = 0
            reconnect()


if __name__ == '__main__':
    main()