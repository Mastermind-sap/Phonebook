import sqlite3
from tkinter import *
from tkinter import messagebox
import tkinter.messagebox


# ****** GLOBAL VARIABLES ******

objects = []
window = Tk()
window.withdraw()
window.title('PHONEBOOK')

conn = sqlite3.connect('phonebook.db')
c = conn.cursor()
c.execute('''CREATE TABLE if not exists phonebook
             (name text,number int)''')

class popupWindow(object):

    loop = False
    attempts = 0

    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.title('Input Password')
        top.geometry('{}x{}'.format(250, 100))
        top.resizable(width=False, height=False)
        self.l = Label(top, text=" Password: ", font=('Courier', 14), justify=CENTER)
        self.l.pack()
        self.e = Entry(top, show='*', width=30)
        self.e.pack(pady=7)
        self.b = Button(top, text='Submit', command=self.cleanup, font=('Courier', 14))
        self.b.pack()

    def cleanup(self):
        self.value = self.e.get()
        access = '1234'

        if self.value == access:
            self.loop = True
            self.top.destroy()
            window.deiconify()
        else:
            self.attempts += 1
            if self.attempts == 5:
                window.quit()
            self.e .delete(0, 'end')
            messagebox.showerror('Incorrect Password', 'Incorrect password, attempts remaining: ' + str(5 - self.attempts))

class entity_add:

    def __init__(self, master, n, p):
        self.name = n
        self.number = p
        self.window = master

    def write(self):
        global c
        c.execute(f"INSERT INTO phonebook VALUES ('{self.name}',{self.number})")
        global conn
        conn.commit()

class entity_display:

    def __init__(self, master, n, p, i):
        self.name = n
        self.number = p
        self.window = master
        self.i = i

        self.label_name = Label(self.window, text=self.name, font=('Courier', 14))
        self.label_number = Label(self.window, text=self.number, font=('Courier', 14))
        self.deleteButton = Button(self.window, text='X', fg='red', command=self.delete)

    def display(self):
        self.label_name.grid(row=6 + self.i, sticky=W)
        self.label_number.grid(row=6 + self.i, column=1)
        self.deleteButton.grid(row=6 + self.i, column=2, sticky=E)

    def delete(self):
        answer = tkinter.messagebox.askquestion('Delete', 'Are you sure you want to delete this entry?')

        if answer == 'yes':
            global c
            c.execute(f"DELETE FROM phonebook WHERE number={self.number}")
            global conn
            conn.commit()
            self.destroy()

    def destroy(self):
        self.label_name.destroy()
        self.label_number.destroy()
        self.deleteButton.destroy()


# ******* FUNCTIONS *********


def onsubmit():
    p = number.get()
    n = name.get()
    e = entity_add(window, n, p)
    e.write()
    name.delete(0, 'end')
    number.delete(0, 'end')
    messagebox.showinfo('Added Entity', 'Successfully Added, \n' + 'Name: ' + n + '\nPhone number: ' + p)
    readfile()


def clearfile():
    global c
    c.execute("DROP TABLE phonebook")
    global conn
    conn.commit()


def readfile():
    global c
    c.execute("SELECT * FROM phonebook")
    f=c.fetchall()
    count = 0

    for line in f:
        e = entity_display(window, line[0], line[1], count)
        objects.append(e)
        e.display()
        count += 1


# ******* GRAPHICS *********

m = popupWindow(window)

entity_label = Label(window, text='Add Entity', font=('Courier', 18))
name_label = Label(window, text='Name: ', font=('Courier', 14))
number_label = Label(window, text='Phone number: ', font=('Courier', 14))
name = Entry(window, font=('Courier', 14))
number = Entry(window, font=('Courier', 14))
submit = Button(window, text='Add Phone number', command=onsubmit, font=('Courier', 14))

entity_label.grid(columnspan=3, row=0)
name_label.grid(row=1, sticky=E, padx=3)
number_label.grid(row=2, sticky=E, padx=3)

name.grid(columnspan=3, row=1, column=1, padx=2, pady=2, sticky=W)
number.grid(columnspan=3, row=2, column=1, padx=2, pady=2, sticky=W)

submit.grid(columnspan=3, pady=4)

name_label2 = Label(window, text='Name: ', font=('Courier', 14))
number_label2 = Label(window, text='Phone number: ', font=('Courier', 14))

name_label2.grid(row=5)
number_label2.grid(row=5, column=1)

readfile()

window.mainloop()
