from tkinter import *
from tkinter.ttk import Combobox
from tkinter import ttk
from tkinter import scrolledtext
import tkinter as tk
from datetime import *
from tkcalendar import Calendar, DateEntry
import create_bot
from data_base import sqlite_db

sourse = ('Сайт(жалобы)', 'Сайт(обратная связь', 'info@tabletri.ua', 'Телефон', 'Facebook',
                   'Appstore', 'Playmarket', 'Instagram', 'Отзывы из приложений','')
status = ['В работе','Закрыта','Жалоба неудовлетворена','']
type_of_complains = ['Не соответсвует цена','Товар не выдали','Не соответсвует адлесс','Не соответсвует режим работы','Не соответсвует товар','Прочее' ]
type_of_appeal = ['Жалоба общая', 'Жалоба на аптеку','Предложение','Вопрос','Похвала']
id_manager = {'ivk': 1821564597,'tun': 1248740780, 'sia': 807661373} #1011022316
id_chat = -736190786

#42975

def save():
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
    print(text_appeal)
    print(len(text_appeal))
    text_answer = ''
    status = combo_status.get()
    parametr_pharma = sqlite_db.sql_select_pharma(code_store)
    address_store = parametr_pharma[0]
    code_chain = parametr_pharma[1]
    name_chain = parametr_pharma[2]
    manager = parametr_pharma[3]
    sqlite_db.sql_insert_request(number, date_request, date, sourse,  type_appeal, type_complains, client, email, phone, number_order, code_store, address_store, text_appeal, text_answer, status, code_chain, name_chain, manager)

    number += 1
    sqlite_db.number_json_save(number)
    lbl_number.configure(text=number)
    if type_appeal == type_of_appeal[1]:
        try:
            report = sqlite_db.sql_select_pharma(code_store)  # нужно сделать проверку на ошибку
            adress = report[0]
            code = report[1]
            name = report[2]
            manager = report[3]
            id_user = id_manager.get(manager)
            if type_complains == type_of_complains[0] or type_of_complains[1]:

                create_bot.send_telegram(number, client, phone, email, code_store, adress, code, name, number_order,
                                         text_appeal, id_user)
                pass
            else:
                create_bot.send_telegram(number, client, phone, email, code_store, adress, code, name, number_order,
                                         text_appeal, id_chat)
                pass
        except:
                create_bot.send_telegram_group(number, client, phone, email, code_store,  number_order, text_appeal)
                pass
    zero = ''
    txt.delete (1.0,END)
    entry_code_store.delete(0, END)
    entry_order_number.delete(0, END)
    entry_name.delete(0, END)
    entry_phone.delete(0, END)
    entry_email.delete(0, END)
    lbl_code_chain.configure(text=zero)
    lbl_name_chain.configure(text=zero)
    lbl_address_store.configure(text=zero)

def check ():
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
# def load ():
#     try:
#         number_appeal = entry_appeal_number.get()
#         report = sqlite_db.sql_select_pharma(code_store)
#         adress = report[0]
#         code = report[1]
#         name = report[2]
#         lbl_address_store.configure(text=adress)
#         lbl_code_chain.configure(text=code)
#         lbl_name_chain.configure(text=name)
#         return report
#     except:
#         pass
def load_appeal_detales ():
    number_appeal = entry_appeal_number.get()
    try:
        report = sqlite_db.sql_select_requests(number_appeal)
        # parametr_chain = sqlite_db.sql_select_pharma(report[5])
        # report = list(report)
        # report.insert(5, parametr_chain[1])
        # i = 0
        # print(report)
        i = 0
        for key, value in object_label_dict.items():
            if i >= 9:
                pass
            else:
                value.label.configure(text=report[i])

                i += 1
    except:
        pass

def load_appeal_detales_all ():

    no_finish = sqlite_db.sql_select_requests_all(status[0])
    # parametr_chain = sqlite_db.sql_select_pharma(report[5])
    # report = list(report)
    # report.insert(5, parametr_chain[1])
    # i = 0
    # print(report)
    g = len(no_finish)
    print(no_finish)
    print(g)

    list_all =[]
    for x in no_finish:
        y=list(x)
        list_all.extend(y)
    q = len(list_all)
    print(q)
    print(list_all)
    i=0
    a=0

    for key, value in object_label_dict.items():
        i += 1
        if i > 9 and i <= 9+q:

             value.label.configure(text=list_all[a])
             a += 1

        else:
            value.label.configure(text='')

# доделать логткуdef
def save_new_status ():
   status = object_combo_list[0].combo_status.get()
   print(status)

   number = object_label_dict.get('3Номер').label.cget('text')
   print(number)
   sqlite_db.update_status(status, number)

   load_appeal_detales()
   load_appeal_detales_all()

def save_new_status_mass ():
    for i in range (1, 13):
        status = object_combo_list[i].combo_status.get()
        print(status)
        number_key = str(i+5) + 'Номер'
        print(number_key)
        number = object_label_dict.get(number_key).label.cget('text')
        print(number)
        sqlite_db.update_status(status, number)
        load_appeal_detales_all()
        #load_appeal_detales()










now = datetime.now().date()
window = tk.Tk()
window.title("Обработка обращений от пользователей")
window.geometry('1210x550')
tab_control = ttk.Notebook(window)
tab_1 = ttk.Frame(tab_control)
tab_2 = ttk.Frame(tab_control)
tab_control.add(tab_1, text='Обработка входящих')
tab_control.add(tab_2, text='Изменение статуса')

lbl_number_title = Label(tab_1, text='Номер:')
lbl_number_title .grid(column=0, row=0, sticky=W, padx=10, pady=10)

lbl_number = Label(tab_1,  fg='green', font='Times 12')
lbl_number.grid(column=1, row=0, pady=9)
lbl_number.configure(text=sqlite_db.number_json_load())

lbl_date_title = Label(tab_1, text='Дата:')
lbl_date_title.grid(column=2, row=0, sticky=W, padx=10, pady=10)

lbl_date = Label(tab_1, text=now, fg='green', font='Times 10')
lbl_date.grid(column=3, row=0, pady=10)

lbl_date_appeal_title = Label(tab_1, text='Дата обращения:', width=18)
lbl_date_appeal_title.grid(column=4, row=0, sticky=W, padx=10, pady=10)

calendar = DateEntry(tab_1,state='readonly', width=30, bg="darkblue", fg="white", year=now.year, month=now.month, day=now.day)
calendar.grid(column=5, row=0, padx=10, pady=10)

lbl_source = Label(tab_1, text='Источник:')
lbl_source.grid(column=0, row=1, sticky=W, padx=10, pady=10)

combo_source = Combobox(tab_1, state='readonly',  width=30)
combo_source['values'] = sourse
combo_source.grid(column=1, row=1,  columnspan=1, padx=10, pady=10)

lbl_type_of_appeal = Label(tab_1, text='Тип обращений:')
lbl_type_of_appeal.grid(column=2, row=1,sticky=W, padx=10, pady=10)

combo_type_of_appeal = Combobox(tab_1, state='readonly', width=30)
combo_type_of_appeal['values'] = type_of_appeal
combo_type_of_appeal.grid(column=3, row=1, columnspan=1,padx=10, pady=10)

lbl_status = Label(tab_1, text='Статус:')
lbl_status.grid(column=0, row=2, sticky=W, padx=10, pady=10)

combo_status = Combobox(tab_1, state='readonly', width=30)
combo_status['values'] = status
combo_status.current(0)
combo_status.grid(column=1, row=2, columnspan=1, padx=10, pady=10)

lbl_type_of_complains = Label(tab_1, text='Тип жалоб:')
lbl_type_of_complains.grid(column=2, row=2, sticky=W, padx=10, pady=10)

combo_type_of_complains = Combobox(tab_1, state='readonly', width=30)
combo_type_of_complains['values'] = type_of_complains
combo_type_of_complains.grid(column=3, row=2, columnspan=1)

lbl_customer = Label(tab_1, text=' Данные пользователя', fg='blue', font='Times 12')
lbl_customer.grid(column=0, row=3, sticky=W, padx=10, pady=5)

lbl_name = Label(tab_1, text='Ф.И.О.:')
lbl_name.grid(column=0, row=4, sticky=W, padx=10, pady=10)

entry_name = Entry(tab_1, width=95)
entry_name.grid(column=1, row=4, sticky=W, padx=10, pady=10, columnspan=3)

lbl_phone = Label(tab_1, text='Телефон:')
lbl_phone.grid(column=0, row=5, sticky=W, padx=10, pady=10)

entry_phone = Entry(tab_1, width=25)
entry_phone.grid(column=1, row=5, sticky=W,  padx=10, pady=10, columnspan=1)

lbl_email = Label(tab_1, text='Email:')
lbl_email.grid(column=2, row=5, sticky=W, padx=10, pady=10)

entry_email = Entry(tab_1, width=35)
entry_email.grid(column=3, row=5, sticky=W, padx=10, pady=10, columnspan=2)

lbl_pharma = Label(tab_1, text=' Данные аптек', fg='blue', font='Times 12')
lbl_pharma.grid(column=0, row=6, sticky=W, padx=10, pady=10)

lbl_code_store = Label(tab_1, text='Код аптеки:')
lbl_code_store.grid(column=0, row=7, sticky=W, padx=10, pady=10)

entry_code_store = Entry(tab_1)
entry_code_store.grid(column=1, row=7, sticky=W, padx=10, pady=10)

lbl_address_store_title = Label(tab_1, text='Адрес аптеки:')
lbl_address_store_title.grid(column=2, row=7, sticky=W, padx=10, pady=10)

lbl_address_store = Label(tab_1,  bg="lightblue", width=30)
lbl_address_store.grid(column=3, row=7, sticky=W, padx=10, pady=10,columnspan=2)

lbl_code_chain_title = Label(tab_1, text='Код сети:')
lbl_code_chain_title.grid(column=0, row=8, sticky=W, padx=10, pady=10)

lbl_code_chain = Label(tab_1,  bg="lightblue", width=17)
lbl_code_chain.grid(column=1, row=8, sticky=W, padx=10, pady=10)

lbl_name_chain_title = Label(tab_1, text='Наименование сети:')
lbl_name_chain_title.grid(column=2, row=8, sticky=W, padx=10, pady=10)

lbl_name_chain = Label(tab_1,  bg="lightblue", width=30)
lbl_name_chain.grid(column=3, row=8, sticky=W, padx=10, pady=10, columnspan=2)

lbl_order_number = Label(tab_1, text='Номер заказа:')
lbl_order_number.grid(column=0, row=9, sticky=W, padx=10, pady=10)

entry_order_number = Entry(tab_1)
entry_order_number.grid(column=1, row=9, sticky=W, padx=10, pady=10)

btn_check = Button(tab_1, text='Проверить', width=30,bg="orange", fg="green",command=check)
btn_check.grid(column=3, row=9,  padx=10, pady=10)

lbl_text = Label(tab_1, text='Текст обращения', fg='blue', font='Times 12')
lbl_text.grid(column=4, row=1, sticky=W, padx=10, pady=10)

txt = scrolledtext.ScrolledText(tab_1, width=45, height=20)
txt.grid(column=4, row=0, sticky=W, rowspan=35, columnspan=3)

btn_save = Button(tab_1, text='Сохранить', width=20, bg="yellow", fg="red", command= save)
btn_save.grid(column=0, row=10,  padx=10, pady=30)

class Label_class:
    def __init__ (self, row, column, bg, fg, columnspan, width, padx, pady, text):
        self.label = Label(tab_2, bg=bg, fg=fg, width=width, text=text)
        self.label.grid(column=column, row=row, columnspan=columnspan, padx=padx, pady=pady)
class Combo_class:
    def __init__(self, row):
        self.combo_status = Combobox(tab_2, state='readonly', width=18)
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
param_1_1 = ['light blue', 'blue', 1, 10, 1, 1]
param_2_1 = ['light blue', 'blue', 1, 20, 1, 1]
param_3_1 = ['light blue', 'blue', 1, 40, 1, 1]

label_parametr_dict = {'Дата ': param_1, 'Номер': param_1, 'Ф.И.О': param_2, 'Телефон': param_1, 'Email': param_1, 'Код сети': param_1, 'Аптека': param_2, 'Текст': param_3, 'Статус': param_1, 'Новый статус': param_2}
label_parametr_dict_1 = {'Дата ': param_1_1, 'Номер': param_1_1, 'Ф.И.О': param_2_1, 'Телефон': param_1_1, 'Email': param_1_1, 'Код сети': param_1_1, 'Аптека': param_2_1, 'Текст': param_3_1, 'Статус': param_1_1}

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
print (object_label_dict)
lbl_store = Label(tab_2, text='Поиск и изменения статуса одного обрашения', fg='blue', font='Times 12')
lbl_store.grid(column=0, row=0, sticky=W, padx=10, pady=5, columnspan=4)
entry_appeal_number = Entry(tab_2, width=12)
entry_appeal_number.grid(column=0, row=1, sticky=W, padx=5, pady=5)
btn_load = Button(tab_2, text='Загрузить', bg="light green", fg="orange", command=load_appeal_detales)
btn_load.grid(column=1, row=1,  padx=5, pady=5)
btn_save_status_one = Button(tab_2, text='Сохранить',  bg="yellow", fg="red", command=save_new_status)
btn_save_status_one.grid(column=2, row=1,  padx=5, pady=5)
lbl_store_mass = Label(tab_2, text='Контроль  обрашений без конечного статуса', fg='blue', font='Times 12')
lbl_store_mass.grid(column=0, row=4, sticky=W, padx=10, pady=5, columnspan=4)
btn_save_status_mass = Button(tab_2, text='Сохранить всё' ,  bg="yellow", fg="red", command=save_new_status_mass)
btn_save_status_mass.grid(column=0, row=17,  padx=10, pady=10, columnspan=10, sticky=E)

#object_label_title_list[1].label.config(text ='1233')


    #         colm_1 += 1
    #         obj = G_v(row, colm_1, text, bg = 'red' , fg='blue', width= 10)
    #         object_list.append(obj)
    # elif row == 5:
    #     colm_2 = 0
    #     for text in title_list:
    #         colm_2 += 1
    #         obj = G_v(row, colm_2,text, bg = 'red' , fg='blue', width= 10)
    #         object_list.append(obj)
    # else:
    #     for y in range (8):
    #
    #         obj = G_v(row, column=y+1, text= '_', bg = 'lightblue', fg='red', width= 10)
    #
    #         object_list.append(obj)
    #     obj_rad = G_v()
    #     #obj_rad.


#object_list[0].label.configure(text='gd')



tab_control.pack(expand=1, fill='both')

sqlite_db.sql_start()
load_appeal_detales_all()
window.mainloop()
