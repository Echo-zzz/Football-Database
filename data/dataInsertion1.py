# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 10:43:14 2021

@author: Echozzz, igumiao
"""


#import libraries
import pandas as pd
import sqlite3 as s
from sqlite3 import Error

def createConnection(path):
    connection = None
    try:
        connection = s.connect(path)
    except Error as e:
        print(e)
        
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("it works")
    except Error as e:
        print(f"The error '{e}' occurred")


def main():
    dbName="Football.db"
    connection=createConnection(dbName)
    #这里全都是能跑的 用我发的新的csv打包文件
    #check一下csv里面是不是我们想要的内容
    #除了friendly,Tournamnet, matchtable,participate  其他应该都ok了
    
    insertCountry(connection, readTable("ctName.csv"))
    insertClub(connection, readTable("ClubStadium.csv"))
    insertStadium(connection, readTable("ClubStadium.csv"))
    insertEvent(connection, readTable("ChampionEventSize.csv"))
    insertPeople(connection, 556)  #556 是hardcode的数字
    insertPlayer(connection, readTable("playersALL.csv"))
    insertReferee(connection, readTable("referee.csv"))
    insertRounds(connection,readTable("ChampionEventSize.csv"))
    insertMatch(connection, readTable("EnglandMatch.csv"))
    insertAttend(connection,readTable("EnglandMatch.csv"),readTable("referee.csv"))
    insertBelong(connection, readTable("playersALL.csv"))
    insertLeague(connection, readTable("ChampionEventSize.csv"))
    insertHomeCourt(connection, readTable("ClubStadium.csv"))
    insertHostStadium(connection, readTable("EnglandMatch.csv"), readTable("ClubStadium.csv"))
    insertMatchTable( connection, readTable("EnglandMatch.csv"))
    insertParticipate(connection, readTable("EnglandMatch.csv"))
    connection.close()
    
    

    
def readTable(path):
    #不用转encoding了  我把csv全部转utf-8编码了
    dataframe = pd.read_csv(path)
    return dataframe


def insertStadium(connection, df):
    
    for row in range(df.shape[0]):
        
        insertion = "INSERT INTO stadium (sName, ctName, capacity,yearOfBuilt) VALUES ('{}', '{}', {}, {});".format(df.iloc[row]['sName'],df.iloc[row]['ctName'],df.iloc[row]['capacity'], df.iloc[row]['yearOfBuilt'])

        execute_query(connection, insertion)


def insertClub(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO club (cName, nickName, foundYear, ctName, officialSite) VALUES ('{}', '{}', {}, '{}', '{}');".format(df.iloc[row]['host'],df.iloc[row]['nickName'],df.iloc[row]['foundYear'], df.iloc[row]['ctName'], df.iloc[row]['officialSite'])
        execute_query(connection, insertion)
        
#你看看这里跨表格数据采集 能不能写的更好 我对datframe的Loc iloc不太熟
def insertAttend(connection, match,referees):
    
    for row in range(match.shape[0]):
        rName=match.iloc[row]['Referee']
        refereeID=referees.loc[referees['rName'] == rName]
        insertion = "INSERT INTO attend (ID, matchID) VALUES ({}, {})".format(refereeID.iloc[0]['ID'],match.iloc[row]['id'])
        execute_query(connection, insertion)

def insertBelong(connection, df):
    
    for row in range(df.shape[0]):
        
        insertion = "INSERT INTO belong (ID,ctName) VALUES ({}, '{}')".format(df.iloc[row]['id'],df.iloc[row]['ctName'])
        execute_query(connection, insertion)

def insertCountry(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO country (ctName) VALUES ('{}')".format(df.iloc[row]['ctName'])
        execute_query(connection, insertion)


def insertEvent(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO event (eName,season,cName) VALUES ('{}','{}','{}')".format(df.iloc[row]['eName'],df.iloc[row]['season'],df.iloc[row]['champion'])
        execute_query(connection, insertion)


def insertLeague(connection, df):
    for row in range(df.shape[0]):
        insertion = "INSERT INTO league (eName,ctName,size) VALUES ('{}','{}',{})".format(df.iloc[row]['eName'],df.iloc[row]['season'], int(df.iloc[row]['size']))
        execute_query(connection, insertion)

#这个就放着吧
def insertFriendly(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO friendly (eName) VALUES ({})".format(df.iloc[row]['AAA'])
        execute_query(connection, insertion)
    


def insertHomeCourt(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO homeCourt (sName,cName) VALUES ('{}','{}')".format(df.iloc[row]['sName'],df.iloc[row]['host'])
        execute_query(connection, insertion)
    

#两个dataframe,一个比赛记录，一个stadiums和俱乐部名字
#这里也是跨表格数据
def insertHostStadium(connection, match, stadiums):
    
    for row in range(match.shape[0]):
        club = match.iloc[row]['HomeTeam']
        stadium = stadiums.loc[stadiums['host'] == club]
        insertion = "INSERT INTO hostStadium (match,sName) VALUES ('{}','{}')".format(match.iloc[row]['id'], stadium.iloc[0]['sName'])
        execute_query(connection, insertion)
#这里也是跨表格数据
def insertMatch(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO match (matchID,matchDate,host,visit,eName) VALUES ({},'{}','{}','{}','{}')".format(df.iloc[row]['id'],df.iloc[row]['Date'],df.iloc[row]['HomeTeam'],df.iloc[row]['AwayTeam'],df.iloc[row]['eName'])
        execute_query(connection, insertion)


def insertMatchTable(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO matchTable (host,visit,matchDate,eName,awayGoal,homeGoal,awayBooks,homeBooks) VALUES ('{}','{}','{}','{}',{},{},{},{})".format(df.iloc[row]['HomeTeam'],df.iloc[row]['AwayTeam'],df.iloc[row]['Date'],df.iloc[row]['eName'],df.iloc[row]['FTAG'],df.iloc[row]['HTHG'],df.iloc[row]['AR'],df.iloc[row]['HR'])
        execute_query(connection, insertion)


def insertParticipate(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT OR IGNORE INTO participate (cName,eName) VALUES ({},{})".format(df.iloc[row]['HomeTeam'],df.iloc[row]['eName'])
        execute_query(connection, insertion)


#先输入一遍所有people，然后Player和referee都按顺序reference 
#我直接hardcode 人数 看main
def insertPeople(connection, num):
    
    for row in range(num):
        insertion = "INSERT INTO people () VALUES ()"
        execute_query(connection, insertion)

#输入Players
def insertPlayer(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO player (ID,cName,pName,DOB) VALUES ({},'{}','{}',{})".format(df.iloc[row]['id'], df.iloc[row]['cName'],df.iloc[row]['pName'],df.iloc[row]['DOB'])
        execute_query(connection, insertion)

#我用了最原始的最保险的办法  直接在referee.csv前面排个序
def insertReferee(connection, df):
    for row in range(df.shape[0]):
        insertion = "INSERT INTO referee (ID, rName) VALUES({}, '{}')".format(df.iloc[row]['ID'] , df.iloc[row]['rName'])
        execute_query(connection, insertion)

def insertRounds(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT OR IGNORE INTO rounds (size,numberOfRounds) VALUES ({},{})".format(df.iloc[row]['size'],df.iloc[row]['numOfRounds'])
        execute_query(connection, insertion)


def insertTournamnet(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO tournament (eName) VALUES ({})".format(df.iloc[row]['AAA'])
        execute_query(connection, insertion)
    
if __name__ == "__main__":
    main()
