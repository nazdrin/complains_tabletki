from tkinter import *
from tkinter.ttk import Combobox
from tkinter import ttk, messagebox, scrolledtext
import tkinter as tk
from datetime import *
from tkcalendar import Calendar, DateEntry
import create_bot
from data_base import sqlite_db

sourse = ('Сайт(жалобы)', 'Сайт(обратная связь', 'info@tabletri.ua', 'Телефон', 'Facebook',
                   'Appstore', 'Playmarket', 'Instagram', 'Отзывы из приложений')
status = ['В работе', 'Закрыта', 'Жалоба неудовлетворена']
type_of_complains = ['Не соответсвует цена', 'Бронь не выдали', 'Не соответсвует адрес', 'Не соответсвует режим работы','Выдали не тот товар', 'Выдали не все товары', 'Прочее']
type_of_appeal = ['Жалоба общая', 'Жалоба на аптеку', 'Предложение', 'Вопрос', 'Похвала']
id_manager = {'ivk': 1821564597, 'tun': 1248740780, 'sia': 1011022316}# 807661373
id_chat = -494225948 #-736190786

def save():  # сохранение обращения в базу данных, логика по отправке жалоб
    number = sqlite_db.number_json_load()
    date_request = calendar.get()
    date = now
    sourse = combo_source.get()
    type_appeal = combo_type_of_appeal.get()
    type_complains = combo_type_of_complains.get()
    client = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    number_order = entry_order_number.get()
    code_store = entry_code_store.get()
    text_appeal = txt.get(1.0, END)[:-1]
    text_answer = ''
    status = combo_status.get()
    parametr_pharma = sqlite_db.sql_select_pharma(code_store)
    address_store = parametr_pharma[0]
    code_chain = parametr_pharma[1]
    name_chain = parametr_pharma[2]
    manager = parametr_pharma[3]
    sqlite_db.sql_insert_request(str(number), date_request, date, sourse,  type_appeal, type_complains, client, email, phone, number_order, code_store, address_store, text_appeal, text_answer, status, code_chain, name_chain, manager)
    messagebox.showinfo('Сохранение', 'Обрашение № ' + str(number) + ' сохранено.')
    number += 1
    sqlite_db.number_json_save(number)
    lbl_number.configure(text=number)
    if type_appeal == type_of_appeal[1]:
        report = sqlite_db.sql_select_pharma(code_store)
        adress = report[0]
        code = report[1]
        name = report[2]
        manager = report[3]
        id_user = id_manager.get(manager)
        if id_user == None:
            create_bot.send_telegram_group(number, type_complains, client, phone, email, code_store, adress, code, name, number_order, text_appeal)
        else:
            if type_complains == type_of_complains[0]:
                create_bot.send_telegram(number, type_complains, client, phone, email, code_store, adress, code, name, number_order, text_appeal, id_user)
                pass
            elif type_complains == type_of_complains[1]:
                create_bot.send_telegram(number, type_complains, client, phone, email, code_store, adress, code, name, number_order, text_appeal, id_user)
                pass
            else:
                create_bot.send_telegram_group(number, type_complains, client, phone, email, code_store, adress, code, name, number_order, text_appeal)
                pass
    zero = ''
    txt.delete(1.0, END)
    entry_code_store.delete(0, END)
    entry_order_number.delete(0, END)
    entry_name.delete(0, END)
    entry_phone.delete(0, END)
    entry_email.delete(0, END)
    lbl_code_chain.configure(text=zero)
    lbl_name_chain.configure(text=zero)
    lbl_address_store.configure(text=zero)

def check (): # проверка наличия аптеки по серийному номеру
    try:
        code_store = entry_code_store.get()
        report = sqlite_db.sql_select_pharma(code_store)
        adress = report[0]
        code = report[1]
        name = report[2]
        lbl_address_store.configure(text=adress)
        lbl_code_chain.configure(text=code)
        lbl_name_chain.configure(text=name)
        return report
    except:
        pass

def load_appeal_detales (): # Загрузка данных по одному обращению
    number_appeal = entry_appeal_number.get()
    try:
        report = sqlite_db.sql_select_requests(number_appeal)
        i = 0
        for key, value in object_label_dict.items():
            if i >= 9:
                pass
            else:
                value.label.delete(1.0, END)
                value.label.insert(1.0, report[i])
                i += 1
    except:
        pass

def load_appeal_detales_all (): # загрузка данных по обращениям в статусе в работе

    no_finish = sqlite_db.sql_select_requests_all(status[0])
    list_all =[]
    for x in no_finish:
        y=list(x)
        list_all.extend(y)
    q = len(list_all)
    i=0
    a=0
    for key, value in object_label_dict.items():
        i += 1
        if i > 9 and i <= 9+q:
             value.label.delete(1.0, END)
             value.label.insert(1.0, list_all[a])
             a += 1
        else:
            value.label.delete(1.0, END)
            value.label.insert(1.0, '')
    for i in range(1, 12):
        object_combo_list[i].combo_status.current(0)

def save_new_status ():# сохранение нового статуса обращения
   status = object_combo_list[0].combo_status.get()
   number = object_label_dict.get('3Номер').label.get(1.0, END)[:-1]
   sqlite_db.update_status(status, number)
   load_appeal_detales()
   load_appeal_detales_all()

def save_new_status_mass (): # сохранение статусов всех
    for i in range(1, 11):
        status = object_combo_list[i].combo_status.get()
        number_key = str(i+5) + 'Номер'
        number = object_label_dict.get(number_key).label.get(1.0, END)[:-1]
        sqlite_db.update_status(status, number)
    load_appeal_detales_all()

#...................................................................................................................
now = datetime.now().date()
window = tk.Tk()
window.title("Обработка обращений от пользователей")
window.geometry('1255x550')
tab_control = ttk.Notebook(window)
tab_1 = ttk.Frame(tab_control)
tab_2 = ttk.Frame(tab_control)
tab_control.add(tab_1, text='Обработка входящих')
tab_control.add(tab_2, text='Изменение статуса')
f1 = LabelFrame(tab_1, relief=RIDGE, borderwidth=2)
f2 = LabelFrame(tab_1, relief=RIDGE, borderwidth=2, text='Данные пользователя')
f3 = LabelFrame(tab_1, relief=RIDGE, borderwidth=2, text='Данные аптек')
text_frame = LabelFrame(tab_1, relief=RIDGE, borderwidth=2, text='Текст')
date_frame = LabelFrame(tab_1, relief=RIDGE, borderwidth=2)
#............................................................................................................
lbl_number_title = Label(f1, text='Номер:')
lbl_number_title .grid(column=0, row=0, sticky=W, padx=10, pady=10)

lbl_number = Label(f1,  fg='green', font='Times 10')
lbl_number.grid(column=1, row=0, padx=10)
lbl_number.configure(text=sqlite_db.number_json_load())

lbl_date_title = Label(f1, text='Дата:')
lbl_date_title.grid(column=2, row=0, sticky=W, padx=10)

lbl_date = Label(f1, text=now, fg='green', font='Times 10')
lbl_date.grid(column=3, row=0)

lbl_date_appeal_title = Label(date_frame, text='Дата обращения:')
lbl_date_appeal_title.grid(column=4, row=0, sticky=W, padx=10)

calendar = DateEntry(date_frame, state='readonly', width=30, bg="darkblue", fg="white", year=now.year, month=now.month, day=now.day)
calendar.grid(column=5, row=0, padx=10, pady=10)

lbl_source = Label(f1, text='Источник:')
lbl_source.grid(column=0, row=1, sticky=W, padx=10, pady=10)

combo_source = Combobox(f1, state='readonly')
combo_source['values'] = sourse
combo_source.grid(column=1, row=1, padx=10)

lbl_type_of_appeal = Label(f1, text='Тип обращений:')
lbl_type_of_appeal.grid(column=2, row=1, sticky=W, padx=10)

combo_type_of_appeal = Combobox(f1, state='readonly')
combo_type_of_appeal['values'] = type_of_appeal
combo_type_of_appeal.grid(column=3, row=1, padx=10)

lbl_status = Label(f1, text='Статус:')
lbl_status.grid(column=0, row=2, sticky=W, padx=10, pady=10)

combo_status = Combobox(f1, state='readonly')
combo_status['values'] = status
combo_status.current(0)
combo_status.grid(column=1, row=2, padx=10)

lbl_type_of_complains = Label(f1, text='Тип жалоб:')
lbl_type_of_complains.grid(column=2, row=2, sticky=W, padx=10)

combo_type_of_complains = Combobox(f1, state='readonly')
combo_type_of_complains['values'] = type_of_complains
combo_type_of_complains.grid(column=3, row=2, padx=10)

lbl_name = Label(f2, text='Ф.И.О.:')
lbl_name.grid(column=0, row=4, sticky=W, padx=10, pady=10)

entry_name = Entry(f2, width=71)
entry_name.grid(column=1, row=4, sticky=W, padx=10, pady=10, columnspan=4)

lbl_phone = Label(f2, text='Телефон:')
lbl_phone.grid(column=0, row=5, sticky=W, padx=10, pady=10)

entry_phone = Entry(f2)
entry_phone.grid(column=1, row=5, sticky=W, padx=10, pady=10)

lbl_email = Label(f2, text='Email:')
lbl_email.grid(column=2, row=5, sticky=W, padx=10, pady=10)

entry_email = Entry(f2, width=37)
entry_email.grid(column=3, row=5, sticky=W, padx=10, pady=10)

lbl_code_store = Label(f3, text='Код аптеки:')
lbl_code_store.grid(column=0, row=7, sticky=W, padx=10, pady=10)

entry_code_store = Entry(f3)
entry_code_store.grid(column=1, row=7, sticky=W, padx=10, pady=10)

lbl_address_store_title = Label(f3, text='Адрес аптеки:')
lbl_address_store_title.grid(column=2, row=7, sticky=W, padx=10, pady=10)

lbl_address_store = Label(f3,  bg="lightblue", width=16)
lbl_address_store.grid(column=3, row=7, sticky=W, padx=10, pady=10)

lbl_code_chain_title = Label(f3, text='Код сети:')
lbl_code_chain_title.grid(column=0, row=8, sticky=W, padx=10, pady=10)

lbl_code_chain = Label(f3,  bg="lightblue", width=17)
lbl_code_chain.grid(column=1, row=8, sticky=W, padx=10, pady=10)

lbl_name_chain_title = Label(f3, text='Наименование сети:')
lbl_name_chain_title.grid(column=2, row=8, sticky=W, padx=10, pady=10)

lbl_name_chain = Label(f3,  bg="lightblue", width=16)
lbl_name_chain.grid(column=3, row=8, sticky=W, padx=10, pady=10)

lbl_order_number = Label(f3, text='Номер заказа:')
lbl_order_number.grid(column=0, row=9, sticky=W, padx=10, pady=10)

entry_order_number = Entry(f3)
entry_order_number.grid(column=1, row=9, sticky=W, padx=10, pady=10)

btn_check = Button(f3, text='Проверить', bg="orange", fg="green",command=check, width=16)
btn_check.grid(column=3, row=9)

txt = scrolledtext.ScrolledText(text_frame, width=38, height=18)
txt.grid(column=5, row=2, padx=10, pady=10)

btn_save = Button(tab_1, text='Сохранить', bg="yellow", fg="red", width=16, command=save)
btn_save.grid(column=0, row=10, sticky=W, padx=5)
#....................................................................................................................

class Label_class:
    def __init__ (self, row, column, bg, fg, columnspan, width, padx, pady, text):
        self.label = Text(tab_2, bg=bg, fg=fg, width=width, height=1)
        self.label.insert(1.0, text)
        self.label.grid(column=column, row=row, columnspan=columnspan, padx=padx, pady=pady)
class Combo_class:
    def __init__(self, row):
        self.combo_status = Combobox(tab_2, state='readonly', width=15)
        self.combo_status['values'] = status
        self.combo_status.current(0)
        self.combo_status.grid(column=9, row=row, padx=1, pady=1)

object_combo_list = []

combo_row = [3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

for row in combo_row:
    obj = Combo_class(row)
    object_combo_list.append(obj)

object_label_title_list = []
object_label_dict = {}

param_1 = ['light gray', 'green', 1, 10, 1, 1]
param_2 = ['light gray', 'green', 1, 20, 1, 1]
param_3 = ['light gray', 'green', 1, 40, 1, 1]
param_4 = ['light gray', 'green', 1, 5, 1, 1]
param_5 = ['light gray', 'green', 1, 15, 1, 1]
param_1_1 = ['white', 'black', 1, 10, 1, 1]
param_2_1 = ['white', 'black', 1, 20, 1, 1]
param_3_1 = ['white', 'black', 1, 40, 1, 1]
param_4_1 = ['white', 'black', 1, 5, 1, 1]
param_5_1 = ['white', 'black', 1, 15, 1, 1]

label_parametr_dict = {'Дата ': param_1, 'Номер': param_4, 'Ф.И.О.': param_2, 'Телефон': param_1, 'Email': param_5, 'Сеть': param_4, 'Аптека': param_2, 'Текст': param_3, 'Статус': param_1, 'Новый статус': param_5}
label_parametr_dict_1 = {'Дата ': param_1_1, 'Номер': param_4_1, 'Ф.И.О.': param_2_1, 'Телефон': param_1_1, 'Email': param_5_1, 'Сеть': param_4_1, 'Аптека': param_2_1, 'Текст': param_3_1, 'Статус': param_1_1}

label_row = [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

for row in label_row:
    if row == 2:
        col = 0
        for key, value in label_parametr_dict.items():
            obj = Label_class(row, col, value[0], value[1], value[2], value[3], value[4], value[5], key)
            col += 1
            object_label_title_list.append(obj)
    elif row == 5:
        col_1 = 0
        for key, value in label_parametr_dict.items():
            obj = Label_class(row, col_1, value[0], value[1], value[2], value[3],value[4], value[5], key)
            col_1 += 1
            object_label_title_list.append(obj)
    else:
        col_2 = 0
        for key, value in label_parametr_dict_1.items():
            ind = str(row) + str(key)
            obj = Label_class(row, col_2, value[0], value[1], value[2], value[3],value[4], value[5], '')
            col_2 += 1
            object_label_dict[ind] = obj

lbl_store = Label(tab_2, text='Поиск и изменение статуса одного обрашения')
lbl_store.grid(column=0, row=0, sticky=W, padx=5, pady=5, columnspan=4)
entry_appeal_number = Entry(tab_2, width=12)
entry_appeal_number.grid(column=0, row=1, sticky=W, padx=5, pady=5)
btn_load = Button(tab_2, text='Загрузить', bg="light green", fg="orange", command=load_appeal_detales)
btn_load.grid(column=1, row=1,  padx=5, pady=5, columnspan = 2)
btn_save_status_one = Button(tab_2, text='Сохранить',  bg="yellow", fg="red", command=save_new_status)
btn_save_status_one.grid(column=3, row=1,  padx=5, pady=5)
lbl_store_mass = Label(tab_2, text='Контроль  обрашений без конечного статуса')
lbl_store_mass.grid(column=0, row=4, sticky=W, padx=5, pady=5, columnspan=4)
btn_save_status_mass = Button(tab_2, text='Сохранить всё',  bg="yellow", fg="red", command=save_new_status_mass)
btn_save_status_mass.grid(column=0, row=17,  padx=10, pady=10, columnspan=10, sticky=E)
btn_update_appeals_mass = Button(tab_2, text='Обновить всё',  bg="light green", fg="orange", command=load_appeal_detales_all)
btn_update_appeals_mass.grid(column=0, row=17,  padx=10, pady=10, columnspan=10, sticky=W)
#......................................................................................................................
f1.grid(column=0, row=0, sticky=NW, padx=5, pady=5, rowspan=3 )
f2.grid(column=0, row=3, sticky=NW, padx=5, pady=5)
f3.grid(column=0, row=5, sticky=NW, padx=5, pady=5)
date_frame.grid(column=5, row=0, sticky=NW, padx=5, pady=5)
text_frame.grid(column=5, row=1, sticky=NW, padx=5, pady=5, rowspan=8)

tab_control.pack(expand=1, fill='both')

sqlite_db.sql_start()
load_appeal_detales_all()

window.mainloop()
