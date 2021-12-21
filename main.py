import sqlite3
from itertools import count
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
        self.stringvar = ["Get the name of the stadiums a specific player has been to", "Number of home team wins", "Get existial clubs that participate a specific event",
                          "Find all players without a last name and not from the England", "Number of expatriate players per club", "Teams that score more goals at home than on the road",
                          "The team that has not lost at home in the league", "Number of shutouts", "Winning percentage of home games enforced by each referee", "Referees who have participated in both tournament and league"]
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
            self.chosePage(0)
        if chose == self.stringvar[1]:
            self.eventPage(1)
        if chose == self.stringvar[2]:
            self.chosePage(2)
        if chose == self.stringvar[3]:
            self.eventPage(3)
        if chose == self.stringvar[4]:
            self.eventPage(4)
        if chose == self.stringvar[5]:
            self.eventPage(5)
        if chose == self.stringvar[6]:
            self.eventPage(6)
        if chose == self.stringvar[7]:
            self.eventPage(7)
        if chose == self.stringvar[8]:
            self.eventPage(8)
        if chose == self.stringvar[9]:
            self.eventPage(9)

        self.master.destroy()

    def reply2(self):
        self.eventPage(which)
        self.jump.destroy()

    def reply3(self):
        self.outputCSV()


    def eventPage(self, inx):
        self.top = Tk(CENTER)
        self.top.title("output")
        self.top.geometry('1000x500')
        self.event(inx)

    def chosePage(self, index):
        self.jump = Tk()
        self.jump.geometry('500x500')
        global which
        which = index
        if which == 0:
            self.jump.title("chose a Player")
            self.cursor.execute("SELECT pName FROM player;")
        if which == 2:
            self.jump.title("chose a Event")
            self.cursor.execute("SELECT eName FROM event;")

        self.stringvar2 = StringVar()
        self.pull2 = Combobox(self.jump, text=self.stringvar2, state='readonly')
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
            SQL = "select distinct sName as Stdium, pName as Player from player " \
                  "natural join club join match " \
                  "on " \
                  "match.visit = club.cName " \
                  "natural join hostStadium where pName = '%s'" % self.pull2.get()
        if index == 1:
            SQL = "select host as Team, count(*) as Winner from matchTable T where T.homeGoals>T.awayGoals " \
                  "GROUP by host " \
                  "order by count(*) DESC"
        if index == 2:
            SQL = "select cName from club c where exists (select eName from participate p " \
                  "where eName = '%s' AND p.cName = c.cName)" % self.pull2.get()
        if index == 3:
            SQL = "select pName,ctName from player p natural join country c natural join belong b " \
                  "where b.ctName != 'England' and pName not like '%.%' " \
                  "GROUP by ctName " \
                  "ORDER by ctName"
        if index == 4:
            SQL = " SELECT cName, count(pName) as foreignPlayer FROM player NATURAL join belong where player.cName in  " \
                  "(SELECT cName from club NATURAL join country  " \
                  "where club.ctName!=belong.ctName) GROUP by cName order by foreignPlayer " \

        if index == 5:
            SQL = "SELECT cName, SUM(case when m.host = cName then homeGoals else 0 end) " \
                  "AS HomeGoals,  SUM(case when m.visit = cName then awayGoals else 0 end) " \
                  "AS AwayGoals  FROM club c JOIN match m ON m.host = c.cName OR m.visit = c.cName " \
                  "NATURAL JOIN matchTable " \
                  "GROUP BY cName " \
                  "HAVING SUM(case when m.host = cName then homeGoals else 0 end) > " \
                  "SUM(case when m.visit = cName then awayGoals else 0 end) "
        if index == 6:
            SQL = "SELECT cName AS Club , COUNT(matchID) AS Undefeated FROM club JOIN match ON " \
                  "match.host = club.cName NATURAL JOIN matchTable WHERE NOT EXISTS(SELECT matchID " \
                  "FROM match NATURAL JOIN matchTable WHERE match.host = Club.cName AND awayGoals > homeGoals)" \
                  "GROUP BY Club HAVING match.eName = 'premium league'"
        if index == 7:
            SQL = "SELECT cName AS Club, " \
                  "(COUNT(case when m.host = cName AND mt.awayGoals = 0 then 1 else NULL end) + " \
                  "COUNT(case when m.visit = cName AND mt.homeGoals = 0 then 1 else NULL end)) " \
                  "AS Cleansheets FROM club c JOIN match m ON m.host = c.cName OR m.visit = c.cName N" \
                  "ATURAL JOIN matchTable mt GROUP BY cName ORDER BY Cleansheets DESC"
        if index == 8:
            SQL = " SELECT rName AS Referees, ROUND" \
                  "((COUNT(case when mt.homeGoals > mt.awayGoals then 1 else NULL end)*1.0 / COUNT(matchID))*100,2)  " \
                  "AS HometeamWinrate FROM referee NATURAL JOIN attend " \
                  "NATURAL JOIN match NATURAL JOIN matchTable mt GROUP BY Referees ORDER BY HometeamWinrate DESC"
        if index == 9:
            SQL = "SELECT rName AS Referee FROM referee WHERE EXISTS " \
                  "(SELECT matchID FROM match m NATURAL JOIN matchTable NATURAL JOIN attend a " \
                  "WHERE a.ID = Referee.ID AND m.eName = 'UEFA Champions League') " \
                  "AND EXISTS " \
                  "(SELECT matchID FROM match m NATURAL JOIN matchTable NATURAL JOIN attend a " \
                  "WHERE a.ID = Referee.ID AND m.eName = 'premier league')"
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
            ms.showerror("Error!", "Should close same csv file window! before you make a new one ")
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
