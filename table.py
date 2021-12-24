import sqlite3
from tkinter import *
from tkinter.ttk import *
import main as main
import tkinter.messagebox as ms
import csv

class Club(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        global screenwidth, screenheight
        width = 500
        heigh = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        self.master.title('Tables')
        self.master.geometry('%dx%d+%d+%d' % (width, heigh, (screenwidth - width) / 2, (screenheight - heigh) / 2))
        self.connect()
        self.whichTable()
        self.SELECT()
        self.back()

    def back(self):
        self.button2 = Button(self.master, text='back', command=self.backBottom)
        self.button2.place(relx=0.6, rely=0.8, relwidth=0.2, relheight=0.05)

    def back2(self):
        self.button3 = Button(self.top, text='back', command=self.backBottom2)
        self.button3.place(relx=0.66, rely=0.8, relwidth=0.2, relheight=0.05)

    def backBottom2(self):
        self.top.destroy()
        Club().__init__()

    def backBottom(self):
        self.master.destroy()
        main.main().__init__()

    def whichTable(self):
        self.stringvar = StringVar()
        self.pull = Combobox(self.master, text=self.stringvar, state='readonly')
        self.cursor.execute("SELECT name FROM sqlite_master where type='table' order by name;")
        # tableName = self.cursor.fetchall()
        tableName = [tableName[0] for tableName in self.cursor.fetchall()]
        print(tableName)
        self.pull["value"] = tableName
        self.pull.current(0)
        self.pull.place(relx=0.4, rely=0.2, relwidth=0.214, relheight=0.055)

    def reply(self):
        global chose
        chose = self.pull.get()
        self.output()
        self.master.destroy()

    def SELECT(self):

        self.button = Button(self.master, text='Go ahead', command=self.reply)
        self.button.place(relx=0.4, rely=0.4, relwidth=0.214, relheight=0.095)

    def output(self):
        self.top = Tk()
        self.top.title("Table - " + self.pull.get())
        width = 1300
        heigh = 500
        self.top.geometry('%dx%d+%d+%d' % (width, heigh, (screenwidth - width) / 2, (screenheight - heigh) / 2))
        self.list = Treeview(self.top)
        self.showAll()
        # self.label1 = Label(self.top, text=self.pull.get(),
        #                     font=('', 15, 'bold'))
        # self.label1.place(relx=0.5, rely=0.02, relwidth=0.45, relheight=0.047)
        # self.INSERT()
        self.back2()
        self.list.place(relx=0.025, rely=0.1, relwidth=0.95, relheight=0.5)
        self.outputBottom()

    def connect(self):
        global DB
        try:
            self.DB = sqlite3.connect("Football.db")
            self.cursor = self.DB.cursor()
            print("success!")
        except:
            print("warning, connect fail!")

    def outputBottom(self):
        self.button3 = Button(self.top, text='Make CSV', command=self.reply3)
        self.button3.place(relx=0.2, rely=0.8, relwidth=0.2, relheight=0.05)

    def reply3(self):
        self.outputCSV()

    def outputCSV(self):
        root = Tk()
        root.withdraw()
        try:
            with open( chose + ".csv", "w", newline='') as file:
                self.csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                self.csv_writer.writerow(column)
                data = self.cursor.execute(sql)
                for row in data:
                    self.csv_writer.writerow(row)
            ms.showinfo("Success!", "Output csv file: \"" + chose + ".csv\"")
        except:
            ms.showerror("Error!", "Should close same csv file window! before you make a new one ")
        root.destroy()


    def INSERT(self):
        self.enter = Entry(self.top)
        self.enter.place(relx=0.4, rely=0.7, relwidth=0.214, relheight=0.095)

    def insert(self, cName, ctName, nickName, foundYear, officialSite):
        sql = "INSERT INTO '%s' (cName, ctName, NickName, foundYear, officialSite) VALUE (?,?,?,?);" % self.pull.get()
        self.cursor.execute(sql)

    def showAll(self):
        global column
        global sql
        sql = "SELECT * from '%s'" % chose
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
