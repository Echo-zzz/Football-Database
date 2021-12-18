import sqlite3
from tkinter import *
from tkinter.ttk import *
import table as ta
import csv
import tkinter.messagebox as ms


class main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master.title('FootBall')
        self.master.geometry('1000x1000')

        self.connect()
        self.eventList()
        self.show()
        self.SELECT()

    def connect(self):
        global DB
        try:
            self.DB = sqlite3.connect("Football.db")
            self.cursor = self.DB.cursor()
            print("success!")
        except:
            print("warning, connect fail!")

    def eventList(self):
        global chose
        self.stringvar = StringVar()
        self.pull = Combobox(self.master, text=self.stringvar, state='readonly')
        self.stringvar = ["Get information about specific players", "Number of home team wins"]
        self.pull["value"] = [i for i in self.stringvar]
        self.pull.current(0)
        self.pull.place(relx=0.3, rely=0.2, relwidth=0.45, relheight=0.047)

    def SELECT(self):
        self.button2 = Button(self.master, text='Go', command=self.reply)
        self.button2.place(relx=0.4, rely=0.4, relwidth=0.214, relheight=0.095)

    def SELECT2(self):
        self.button3 = Button(self.jump, text='Go', command=self.reply2)
        self.button3.place(relx=0.4, rely=0.5, relwidth=0.214, relheight=0.095)

    def reply(self):
        # everytime join a new event, create a new
        global chose
        chose = self.pull.get()
        if chose == self.stringvar[0]:
            self.chosePage()
        if chose == self.stringvar[1]:
            self.eventPage(1)
        self.master.destroy()

    def reply2(self):
        self.eventPage(0)
        self.jump.destroy()

    def reply3(self):
        self.outputCSV()


    def eventPage(self, inx):
        self.top = Tk()
        self.top.title("output")
        self.top.geometry('1000x500')
        self.event(inx)

    def chosePage(self):
        self.jump = Tk()
        self.jump.title("chose a player")
        self.jump.geometry('500x500')
        self.stringvar2 = StringVar()
        self.pull2 = Combobox(self.jump, text=self.stringvar2, state='readonly')
        self.cursor.execute("SELECT pName FROM player;")
        tableName = self.cursor.fetchall()
        self.pull2["value"] = [str(i[0]) for i in tableName]
        self.pull2.current(0)
        self.pull2.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.055)
        self.SELECT2()
        self.cancel()

    def event(self, index):

        global SQL

        # here to SQL
        if index == 0:
            SQL = "SELECT * from player where pName ='%s'" % self.pull2.get()
        if index == 1:
            SQL = "select host, count(*) from matchTable T where T.homeGoals>T.awayGoals " \
                  "GROUP by host " \
                  "order by count(*) DESC"
        # here to SQL

        global column
        data = self.cursor.execute(SQL)
        column = [column[0] for column in self.cursor.description]  # return the heading name
        print(column)

        self.list = Treeview(self.top)

        self.list["columns"] = column

        for i in column:
            self.list.column(i, anchor="center")
            self.list.heading(i, text=i)
        count = 1
        for row in data:
            self.list.insert("", count, text="{}".format(count), values=row)
            count = count + 1
        self.list.pack()
        self.back()
        self.outputBottom()

    def outputBottom(self):
        self.button3 = Button(self.top, text='Make CSV', command=self.reply3)
        self.button3.place(relx=0.2, rely=0.8, relwidth=0.2, relheight=0.05)

    def outputCSV(self):

        root = Tk()
        root.withdraw()
        try:
            with open(chose + ".csv", "w", newline='') as file:
                self.csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                self.csv_writer.writerow(column)
                data = self.cursor.execute(SQL)
                for row in data:
                    self.csv_writer.writerow(row)
            ms.showinfo("Success!", "Output csv file: \"" + chose + ".csv\"")
        except:
            ms.showerror("Error!", "Should close csv file window!")
        root.destroy()

    def cancel(self):
        self.button5 = Button(self.jump, text='cancel', command=self.cancelBottom)
        self.button5.place(relx=0.6, rely=0.8, relwidth=0.2, relheight=0.05)

    def cancelBottom(self):
        self.jump.destroy()
        self.__init__()

    def back(self):
        self.button4 = Button(self.top, text='back', command=self.backBottom)
        self.button4.place(relx=0.6, rely=0.8, relwidth=0.2, relheight=0.05)

    def backBottom(self):
        self.top.destroy()
        self.__init__()

    def show(self):
        self.button = Button(self.master, text='Show all table details', command=self.showBottom)
        self.button.place(relx=0.6, rely=0.8, relwidth=0.2, relheight=0.05)

    def showBottom(self):
        self.master.destroy()
        ta.Club().__init__()


if __name__ == '__main__':
    main_window = main()
    main_window.mainloop()
