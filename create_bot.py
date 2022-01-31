import requests

def send_telegram(number,type_complains, client, phone, email, code_store, adress, code, name, number_order, text_appeal, id_user):
    token = "1732218726:AAF6wQSMBvFx-zHbr0DSmDMquRTjiRh3VJw"#"2119047086:AAG2tUZmRULNasX8Rkb1tTUb4uEDwkQ640k"
    url = "https://api.telegram.org/bot"
    channel_id = id_user # "-736190786"
    url += token
    method = url + "/sendMessage"
    text = 'Номер обращения: ' + str(number) +'\nТип жалобы: ' + str(type_complains) + '\nИмя пользователя: ' + str(client) + '\nТелефон: ' + str(phone) +'\nПочта: ' + str(email) + '\nСерийный: ' + str(code_store) + '\nАдрес аптеки: ' + str(adress) + '\nКод сети: ' + str(code) + '\nНаименование сети: ' + str(name) +'\nНомер брони: ' + str(number_order) + '\nТекст обращения: ' +str(text_appeal)
    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })

    if r.status_code != 200:
        raise Exception("post_text error")
def send_telegram_group(number,type_complains, client, phone, email, code_store, adress, code, name, number_order,
                                        text_appeal):
    token = "1732218726:AAF6wQSMBvFx-zHbr0DSmDMquRTjiRh3VJw"
    url = "https://api.telegram.org/bot"
    channel_id = -494225948#-736190786
    url += token
    method = url + "/sendMessage"
    text = 'Номер обращения: ' + str(number) + '\nТип жалобы: ' + str(type_complains) + '\nИмя пользователя: ' + str(
        client) + '\nТелефон: ' + str(phone) + '\nПочта: ' + str(email) + '\nСерийный: ' + str(
        code_store) + '\nАдрес аптеки: ' + str(adress) + '\nКод сети: ' + str(code) + '\nНаименование сети: ' + str(
        name) + '\nНомер брони: ' + str(number_order) + '\nТекст обращения: ' + str(text_appeal)
    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })
    if r.status_code != 200:
        raise Exception("post_text error")

