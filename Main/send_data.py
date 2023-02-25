from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests
import threading

def send_data_to_server(level, user, deaths, time):
    key = b'Ae7nM4dG53Lo7pA4pqr474tgf47GT5z='
    iv = bytearray(16)
    url = "http://localhost:3000/save-score"
    cipher = AES.new(key, AES.MODE_CBC, iv)
    message = '{"level": %d,"data": {"name": "%s","deaths": %d,"time": "%s"}}' % (level, user, deaths, time)
    padded_message = pad(message.encode(), 16)
    encrypted_message = cipher.encrypt(padded_message)
    encoded_message = encrypted_message.hex()

    try:
        response = requests.post(url, json={"data": encoded_message})
        return response.status_code
    except:
        pass

def send_data_to_server_thread(level, user, deaths, time):
    thread = threading.Thread(target=send_data_to_server, args=(level, user, deaths, time))
    thread.start()

#send_data_to_server(3, "John", 5, "00:14")