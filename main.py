from tkinter import *
from tkinter.ttk import Combobox
from tkinter import ttk
import tkinter as tk
from datetime import *
from tkcalendar import Calendar, DateEntry
import create_bot
from data_base import sqlite_db

sourse = []
status = []
type_of_complains = []

type_of_appeal = ['сайт(жалобы)', 'сайт(обратная связь', 'info@tabletri.ua', 'Телефон', 'Facebook',
                   'Appstore', 'Playmarket', 'Instagram', 'Отзывы из приложений']



now = datetime.now().date()
window = tk.Tk()
window.title("Обработка обращений от пользователей")
window.geometry('1000x750')
tab_control = ttk.Notebook(window)
tab_1 = ttk.Frame(tab_control)
tab_2 = ttk.Frame(tab_control)
tab_control.add(tab_1, text='Обработка входящих')
tab_control.add(tab_2, text='Изменение статуса')

tab_control.pack(expand=1, fill='both')
lbl_number_title = Label(tab_1, text='Номер:')
lbl_number = Label(tab_1, text='1',  fg='green', font='Times 10')
lbl_date_title = Label(tab_1, text='Дата:')
lbl_date = Label(tab_1, text=now, fg='green', font='Times 10')
lbl_date_appeal_title = Label(tab_1, text='Дата обращения:', width=18)
#entry_date_appeal = Entry(tab_1)
#entry_date_appeal.insert(0, now)
lbl_source = Label(tab_1, text='Источник:', height=2)
combo_source = Combobox(tab_1, state='readonly')
combo_source['values'] = sourse

lbl_type_of_appeal = Label(tab_1, text='Тип обращений:')
combo_type_of_appeal = Combobox(tab_1, state='readonly')
combo_type_of_appeal['values'] = type_of_appeal
lbl_status = Label(tab_1, text='Статус:')
combo_status = Combobox(tab_1, state='readonly')
combo_status['values'] = status
lbl_type_of_complains = Label(tab_1, text='Тип жалоб:')
combo_type_of_complains = Combobox(tab_1, state='readonly')
combo_type_of_complains['values'] = type_of_complains


cal = DateEntry(tab_1, width=30, bg="darkblue", fg="white", year= now.year, month=now.month, day=now.day)

cal.grid(column=6, row=0)

lbl_number_title.grid(column=0, row=0)
lbl_number.grid(column=1, row=0)
lbl_date_title.grid(column=2, row=0)
lbl_date.grid(column=3, row=0)
lbl_date_appeal_title.grid(column=4, row=0)
cal.grid(column=5, row=0)
#entry_date_appeal.grid(column=5, row=0)
lbl_source.grid(column=0, row=1)
combo_source.grid(column=1, row=1,  columnspan=3)
lbl_type_of_appeal.grid(column=4, row=1)
combo_type_of_appeal.grid(column=5, row=1, columnspan=3)
lbl_status.grid(column=0, row=3)
combo_status.grid(column=1, row=3, columnspan=3)
lbl_type_of_complains.grid(column=4, row=3)
combo_type_of_complains.grid(column=5, row=3, columnspan=3)
tab_control.pack(expand=1, fill='both')
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
def check (code_store):
    pass
     # address_store = report[0]
     # code_chain = report[1]
     # name_chain = report[2]
     #
     # print(address_store, code_chain, name_chain)


def save (number_request, date_request, date, sourse,  type_request, type_complaint,
                       client, email, phone, number_order, code_store, text_request, text_answer):
    report = sqlite_db.sql_select_pharma(code_store)
    if report == []:
        print('некорректный код ')
        pass
    else:
         sqlite_db.sql_insert_request(number_request, date_request, date, sourse,  type_request, type_complaint,
                       client, email, phone, number_order, code_store, text_request, text_answer)
         if type_request == 'Жалоба на аптеку':
             create_bot.send_telegram(number_request, date_request, date, sourse,  type_request, type_complaint,
                       client, email, phone, number_order, code_store, text_request, text_answer)




window.mainloop()

#create_bot.send_telegram()
#executor.start_polling(dp, skip_updates=True, on_startup=on_startup)



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

