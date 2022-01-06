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
id_manager = {'ivk':1821564597,'tun':1248740780, 'sia':807661373} #1011022316
id_chat = -736190786



def save():
    number = sqlite_db.number_json_load()
    number += 1
    sqlite_db.number_json_save(number)
    lbl_number.configure(text=number)
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
    text_appeal = txt.get(1.0,END)
    text_answer = ''
    status = combo_status.get()
    sqlite_db.sql_insert_request(number, date_request, date, sourse, type_appeal, type_complains, client, email, phone, number_order, code_store, text_appeal, text_answer, status)
    report = sqlite_db.sql_select_pharma(code_store)# нужно сделать проверку на ошибку
    adress = report[0]
    code = report[1]
    name = report[2]
    manager = report[3]
    id_user = id_manager.get(manager)
    print (id_user)
    if type_appeal == type_of_appeal[1]:
        if type_complains == type_of_complains[0] or type_of_complains[1]:

            create_bot.send_telegram(number, client, phone, email, code_store, adress, code, name, number_order, text_appeal, id_user)
            pass
        else:
            create_bot.send_telegram(number, client, phone, email, code_store, adress, code, name, number_order,
                                     text_appeal, id_chat)
            pass

    zero = ''


    txt.delete (1.0,END)

    combo_status.current(3)


    #Label(tab_1, textvariable=lbl_number, fg='green', font='Times 10').grid(column=1, row=0, pady=10)

    # report = sqlite_db.sql_select_pharma(code_store)
    # if report == []:
    #     print('некорректный код ')
    #     pass
    # else:
    #      sqlite_db.sql_insert_request(number_request, date_request, date, sourse,  type_request, type_complaint,
    #                    client, email, phone, number_order, code_store, text_request, text_answer)
    #      if type_request == 'Жалоба на аптеку':
    #          create_bot.send_telegram(number_request, date_request, date, sourse,  type_request, type_complaint,
    #                    client, email, phone, number_order, code_store, text_request, text_answer)

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
    except:
        pass


now = datetime.now().date()
window = tk.Tk()
window.title("Обработка обращений от пользователей")
window.geometry('1200x600')
tab_control = ttk.Notebook(window)
tab_1 = ttk.Frame(tab_control)
tab_2 = ttk.Frame(tab_control)
tab_control.add(tab_1, text='Обработка входящих')
tab_control.add(tab_2, text='Изменение статуса')

lbl_number_title = Label(tab_1, text='Номер:')
lbl_number_title .grid(column=0, row=0, sticky=W, padx=10, pady=10)
# lbl_number = StringVar()
# lbl_number.set(sqlite_db.number_json_load())
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

tab_control.pack(expand=1, fill='both')

sqlite_db.sql_start()
window.mainloop()


#create_bot.send_telegram()
#executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

# ---------------------------------------------\
# class Interface:
#     def label(self, name, value, pos_x, pos_y):
#         name = Label(tab_1, text=value)
#         name.grid(column=pos_x, row=pos_y)
#     def entry(self, name, pos_x, pos_y):
#         name = Entry(tab_1)
#         name.grid(column=pos_x, row=pos_y)
#     def combobox(self, name, value, pos_x, pos_y):
#         name = Combobox(tab_1)
#         name['position'] = value
#         name.grid(column=pos_x, row=pos_y)
#     def button(self):
#         print(self.name)



# Inter = Interface()
# Inter.button()
# Inter.label('lbl_number_title', 'Номер:', 0, 0)
# Inter.label('lbl_number', 1, 1, 0)
# Inter.label('lbl_date', 'Дата', 2, 0)
#
# tab_control.pack(expand=1, fill='both')

# from datetime import date
#
# root = tk.Tk()
# # change ttk theme to 'clam' to fix issue with downarrow button
# style = ttk.Style(root)
# style.theme_use('clam')
#
# class MyDateEntry(DateEntry):
#     def __init__(self, master=None, **kw):
#         DateEntry.__init__(self, master=None, **kw)
#         # add black border around drop-down calendar
#         self._top_cal.configure(bg='black', bd=1)
#         # add label displaying today's date below
#         tk.Label(self._top_cal, bg='gray90', anchor='w',
#                  text='Today: %s' % date.today().strftime('%x')).pack(fill='x')
#
# # create the entry and configure the calendar colors
# de = MyDateEntry(root, year=2016, month=9, day=6,
#                  selectbackground='gray80',
#                  selectforeground='black',
#                  normalbackground='white',
#                  normalforeground='black',
#                  background='gray90',
#                  foreground='black',
#                  bordercolor='gray90',
#                  othermonthforeground='gray50',
#                  othermonthbackground='white',
#                  othermonthweforeground='gray50',
#                  othermonthwebackground='white',
#                  weekendbackground='white',
#                  weekendforeground='black',
#                  headersbackground='white',
#                  headersforeground='gray70')
# de.pack()
# root.mainloop()

