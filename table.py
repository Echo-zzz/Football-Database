import sqlite3
from tkinter import *
from tkinter.ttk import *
import main as main

class Club(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('main')
        self.master.geometry('500x500')
        self.connect()
        self.whichTable()
        self.SELECT()
        self.back()

    def back(self):
        self.button2 = Button(self.master, text='back', command=self.backBottom)
        self.button2.place(relx=0.6, rely=0.8, relwidth=0.2, relheight=0.05)

    def backBottom(self):
        self.master.destroy()
        main.main().__init__()

    def whichTable(self):
        self.stringvar = StringVar()
        self.pull = Combobox(self.master, text=self.stringvar, state='readonly')
        self.cursor.execute("SELECT name FROM sqlite_master where type='table' order by name;")
        tableName = self.cursor.fetchall()
        print(tableName)
        self.pull["value"] = tableName
        self.pull.current(0)
        self.pull.place(relx=0.4, rely=0.2, relwidth=0.214, relheight=0.055)

    def reply(self):
        self.output()

    def SELECT(self):

        self.button = Button(self.master, text='go ahead', command=self.reply)
        self.button.place(relx=0.4, rely=0.4, relwidth=0.214, relheight=0.095)

    def output(self):
        self.top = Tk()
        self.top.title("output")
        self.top.geometry('1000x500')
        self.list = Treeview(self.top)
        self.showAll()
        self.list.pack()
        self.INSERT()

    def connect(self):
        global DB
        try:
            self.DB = sqlite3.connect("Football.db")
            self.cursor = self.DB.cursor()
            print("success!")
        except:
            print("warning, connect fail!")

    def INSERT(self):

        self.enter = Entry(self.top)
        self.enter.place(relx=0.4, rely=0.7, relwidth=0.214, relheight=0.095)

    def insert(self, cName, ctName, nickName, foundYear, officialSite):
        sql = "INSERT INTO '%s' (cName, ctName, NickName, foundYear, officialSite) VALUE (?,?,?,?);" % self.pull.get()
        self.cursor.execute(sql)

    def showAll(self):
        sql = "SELECT * from '%s'" % self.pull.get()
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        column = [column[0] for column in self.cursor.description]  # return the heading name
        print(column)
        self.list["columns"] = column
        for i in column:
            self.list.column(i, anchor="center")
            self.list.heading(i, text=i)

        count = 1
        for row in data:
            print(row)
            self.list.insert("", count, text="{}".format(count), values=row)
            count = count + 1
