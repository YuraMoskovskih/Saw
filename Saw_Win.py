#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter    # module for displaying windows and widgets
from tkinter import messagebox, Menu  # module for displaying the menu
import time       # module for recording date and time in the log
import locale     # module for russification of date


def window():  # create a window and all widgets
    global thickness_entry, width_entry, long_boards_entry
    global itog, cvar, pieces_entry, price_entry, root
    root = tkinter.Tk()
    # root["bg"] = "#C3FFFE"
    root.title("Расчёт объёма и стоимости доски")
    root.geometry()
    # root.bind("<Escape>", quit)

    menu = Menu(root, font='Droid 10')  # program menu
    new_item = Menu(menu)
    new_item.add_command(label='Помощь', command=man)
    new_item.add_separator()
    new_item.add_command(label='О программе', command=about)
    new_item.add_separator()
    new_item.add_command(label='Выход', command=root.destroy)
    # menu.add_cascade(label='', menu=new_item)
    menu.add_cascade(label='Справка', menu=new_item, font='Droid 11')
    root.config(menu=menu)

    thickness_label = tkinter.Label(font='Droid 12',
                                    text="Толщина доски в мм.:")
    width_label = tkinter.Label(font='Droid 12',
                                text="Ширина доски в мм.:")
    long_boards_label = tkinter.Label(font='Droid 12',
                                      text="Длина доски в М.:")
    pieces_label = tkinter.Label(font='Droid 12',
                                 text="Количество доски в шт.:")
    price_label = tkinter.Label(font='Droid 12',
                                text="Цена за куб. метр в руб.:")

    thickness_label.grid(row=0, column=0, sticky="w")
    width_label.grid(row=1, column=0, sticky="w")
    long_boards_label.grid(row=2, column=0, sticky="w")
    pieces_label.grid(row=3, column=0, sticky="w")
    price_label.grid(row=4, column=0, sticky="w")

    thickness_entry = tkinter.Entry(font='Droid 12')
    width_entry = tkinter.Entry(font='Droid 12')
    long_boards_entry = tkinter.Entry(font='Droid 12')
    pieces_entry = tkinter.Entry(font='Droid 12')
    price_entry = tkinter.Entry(font='Droid 12')

    thickness_entry.grid(row=0, column=1, padx=5, pady=5)
    width_entry.grid(row=1, column=1, padx=5, pady=5)
    long_boards_entry.grid(row=2, column=1, padx=5, pady=5)
    pieces_entry.grid(row=3, column=1, padx=5, pady=5)
    price_entry.grid(row=4, column=1, padx=5, pady=5)

    # default input fields
    #        thickness_entry.insert(0, "25")
    #        width_entry.insert(0, "100")
    #        long_boards_entry.insert(0, "3")
    #        pieces_entry.insert(0, "500")
    #        price_entry.insert(0, "9000")

    # create three buttons: "Вычислить", "Очистить поля",
    #                       "Показать журнал", "Очистить журнал"
    calculation_button = tkinter.Button(text="Вычислить", width=45, height=3,
                                        font='Droid 12', bg="#CECECE", command=calculation)
    clear_button = tkinter.Button(text="Очистить поля", width=15, height=1,
                                  font='Droid 12', bg="#CECECE", command=clear)
    journal_button = tkinter.Button(text="Показать журнал", width=15, height=1,
                                    font='Droid 12', bg="#CECECE", command=journal)
    clear_log_button = tkinter.Button(text="Очистить журнал", width=15,
                                      height=1, font='Droid 12', bg="#CECECE",
                                      command=clear_log)

    calculation_button.grid(row=5, column=0, columnspan=3)
    clear_button.grid(row=6, column=0, columnspan=1)
    journal_button.grid(row=6, column=1, columnspan=4)
    clear_log_button.grid(row=10, column=1, columnspan=4)

    # output field
    itog = tkinter.Text(width=40, height=4, bg="white", fg='black',
                        font='Droid 14', wrap=tkinter.WORD)
    itog.grid(row=9, column=0, columnspan=3, padx=1, pady=1)

    # checkbox for logging
    cvar = tkinter.BooleanVar()
    cvar.set(True)    # default value
    c1 = tkinter.Checkbutton(text="Записывать расчёты в журнал", variable=cvar,
                             onvalue=1, offvalue=0, font='Droid 11')
    c1.grid(row=10, column=0, columnspan=1)

    # display the program in an infinite loop
    root.mainloop()


def clear():  # function to clear all fields
    thickness_entry.delete(0, tkinter.END)
    width_entry.delete(0, tkinter.END)
    long_boards_entry.delete(0, tkinter.END)
    pieces_entry.delete(0, tkinter.END)
    price_entry.delete(0, tkinter.END)
    itog.delete('1.0', tkinter.END)


def calculation():  # calculation function

    # calculation by clicking a widget calculation
    itog.delete('1.0', tkinter.END)
    thickness = int(thickness_entry.get())
    width = int(width_entry.get())
    long_boards = float(long_boards_entry.get())
    pieces = int(pieces_entry.get())
    price = int(price_entry.get())
    thickness1 = thickness/1000
    width1 = width/1000
    cube = (long_boards*thickness1*width1)*pieces
    cube = float('{:.3f}'.format(cube))
    cost = price*cube
    cost = float('{:.3f}'.format(cost))
    res = "Ваша доска: {}×". format(thickness_entry.get())+format(
           width_entry.get())+"×"+format(long_boards_entry.get(
           ))+"   Кол-во: {}".format(pieces_entry.get())+" шт.\n"
    itog.insert(1.0, res)
    res2 = "Общий объем: {}". format(str(cube))+" куб. метров.\
    \nОбщая стоимость: {}". format(str(cost))+" рублей."
    itog.insert(2.0, res2)

    itog.tag_add('title', 1.0, '1.end')
    itog.tag_add('title', 2.0, '2.end')
    itog.tag_add('title', 3.0, '3.end')
    itog.tag_config('title', justify=tkinter.CENTER)

    write_journal(thickness, width, long_boards, pieces, cube, cost)


def write_journal(thickness, width, long_boards, pieces, cube, cost):  # loggin
    if cvar.get():    # logging if cvar - True
        thickness = str(thickness)
        width = str(width)
        long_boards = str(long_boards)
        pieces = str(pieces)
        cube = str(cube)
        cost = str(cost)
        log = open('journal', 'a', encoding='utf-8')
        locale.setlocale(locale.LC_ALL, "ru_RU.utf8")
        log.write(time.strftime("%A, %d. %B %Y %H:%M")+'\n')
        log.writelines("Ваша доска: "+thickness+"×"+width+"×"+long_boards+(
                       "  Кол-во: ")+pieces+" шт.")
        log.writelines("\nОбщий объем: "+cube+" куб. метров. "
                       "Общая стоимость: "+cost+" рублей.\n\n\n")
        log.close()


def journal():  # log file display function

    from tkinter import scrolledtext

    child = tkinter.Toplevel(root)   # creating a child window
    child.title('Журнал')
    child.minsize(width=600, height=600)
    child.maxsize(width=600, height=600)

    text = scrolledtext.ScrolledText(child, width=600,
                                     height=600, font='Droid 11')
    text.pack()
    data = open('journal', encoding='utf-8')
    text.delete('1.0', tkinter.END)
    text.insert('1.0', data.read())
    data.close()

    # window launch
    root.mainloop()


def clear_log():  # log cleanup function
    log = open('journal', 'w')
    log.close()


def man():  # display help window

    from tkinter import scrolledtext

    child2 = tkinter.Toplevel(root)   # creating a child window
    child2.title('Помощь')
    child2.minsize(width=600, height=600)
    child2.maxsize(width=600, height=600)

    text = scrolledtext.ScrolledText(child2, width=500,
                                     height=500, font='Droid 11')
    text.pack()
    data = open('help', encoding='utf-8')
    text.delete('1.0', tkinter.END)
    text.insert('1.0', data.read())
    data.close()

    # window launch
    root.mainloop()


def about():  # menu item "about the program"
    messagebox.showinfo('О программе', 'Raw\
        \n\nПростой и удобный инструмент для расчёта объёма и стоимости доски.\
        \nCopyright 2021 Юрий Московских <yuramoskovskih@gmail.com>')


window()
