import sqlite3
from tkinter import *
from tkinter.ttk import *
import table as ta


class main(Frame):
    def __init__(self, master1=None):
        Frame.__init__(self, master1)

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
        self.stringvar = StringVar()
        self.pull = Combobox(self.master, text=self.stringvar, state='readonly')
        self.stringvar = ["Teams participating in both the Champions League and the League", "All winners to win "
                                                                                             "derbies"]
        self.pull["value"] = [i for i in self.stringvar]
        self.pull.current(0)
        self.pull.place(relx=0.3, rely=0.2, relwidth=0.45, relheight=0.047)

    def SELECT(self):
        self.button2 = Button(self.master, text='Go', command=self.reply)
        self.button2.place(relx=0.4, rely=0.4, relwidth=0.214, relheight=0.095)

    def reply(self):
        if self.pull.get() == self.stringvar[0]:
            self.eventPage(0)
        if self.pull.get() == self.stringvar[1]:
            self.eventPage(1)

    def eventPage(self, inx):
        self.top = Tk()
        self.top.title("output")
        self.event(inx)
        self.top.geometry('1000x500')

    def event(self, index):

        #插这儿 插这儿 快插这里
        global SQL
        if index == 0:
            print("1")
            SQL = "SELECT * from league"
        if index == 1:
            print("2")
            SQL = "SELECT * from event"
        #插上面点

        data = self.cursor.execute(SQL)

        column = [column[0] for column in self.cursor.description]  # return the heading name

        self.list = Treeview(self.top)

        self.list["columns"] = column

        for i in column:
            self.list.column(i, anchor="center")

        for i in column:
            self.list.heading(i, text=i)
        count = 1
        for row in data:
            print(row)
            self.list.insert("", count, text="{}".format(count), values=row)
            count = count + 1
        self.list.pack()

    def show(self):
        self.button = Button(self.master, text='Show all table details', command=self.showBottom)
        self.button.place(relx=0.6, rely=0.8, relwidth=0.2, relheight=0.05)

    def showBottom(self):
        self.master.destroy()
        ta.Club().__init__()


if __name__ == '__main__':
    main_window = main()
    main_window.mainloop()
