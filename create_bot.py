

import requests



def send_telegram():
    token = "2119047086:AAG2tUZmRULNasX8Rkb1tTUb4uEDwkQ640k"
    url = "https://api.telegram.org/bot"
    channel_id = "-736190786"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": 'fefeg'
    })

    if r.status_code != 200:
        raise Exception("post_text error")

