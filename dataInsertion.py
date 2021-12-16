# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 10:43:14 2021

@author: Echozzz, igumiao
"""


#import libraries
import pandas as pd
import sqlite3 as s
import codecs
from sqlite3 import Error

def createConnection(path):
    connection = None
    try:
        connection = s.connect(path)
    except Error as e:
        print(e)
        
    return connection

#网上照抄的execute query sqlite 本身没有execute query这个function 但有其他的
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("it works")
    except Error as e:
        print(f"The error '{e}' occurred")

#insert的顺序要注意 因为我们现在有commit了
def main():
    dbName="Football.db"
    Connection=createConnection(dbName)
    fileName1="ClubStadium.csv"
    insertClub(Connection, readTable(fileName1))
    insertStadium(Connection, readTable(fileName1))
    

    
def readTable(path):
    #这里 gb2312是我网上找的 因为我们的csv不是utf-8 能应对utf-8 encoding 报错 目前还没有问题 
    dataframe = pd.read_csv(path,encoding = 'gb2312')
    return dataframe


def insertStadium(connection, df):
    
    for row in range(df.shape[0]):
        
        insertion = "INSERT INTO stadium (sName, ctName, capacity,yearOfBuilt) VALUES ('{}', '{}', {}, {});".format(df.iloc[row]['sName'],df.iloc[row]['ctName'],df.iloc[row]['capacity'], df.iloc[row]['yearOfBuilt'])
        execute_query(connection, insertion)


def insertClub(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO club (cName, nickName, foundYear, ctName, officialSite) VALUES ('{}', '{}', {}, '{}', '{}');".format(df.iloc[row]['host'],df.iloc[row]['nickName'],df.iloc[row]['foundYear'], df.iloc[row]['ctName'], df.iloc[row]['officialSite'])
        print(insertion)
        execute_query(connection, insertion)

def insertAttend(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO attend (ID, matchID) VALUES ({}, {})".format(df.iloc[row]['AAA'],df.iloc[row]['BBB'])
        execute_query(connection, insertion)

def insertBelong(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO belong (ID,ctName) VALUES ({}, {})".format(df.iloc[row]['AAA'],df.iloc[row]['BBB'])
        execute_query(connection, insertion)

def insertCountry(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT OR IGNORE INTO country (ctName) VALUES ({})".format(df.iloc[row]['ctName'])
        execute_query(connection, insertion)


def insertEvent(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO event (eName,season,cName) VALUES ({},{},{})".format(df.iloc[row]['eName'],df.iloc[row]['season'],df.iloc[row]['cName'])
        execute_query(connection, insertion)


def insertLeague(connection, df):
    for row in range(df.shape[0]):
        insertion = "INSERT INTO league (eName,ctName,size) VALUES ('{}','{}',{})".format(df.iloc[row]['eName'],df.iloc[row]['season'], int(df.iloc[row]['size']))
        execute_query(connection, insertion)


def insertFriendly(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO friendly (eName) VALUES ({})".format(df.iloc[row]['AAA'])
        execute_query(connection, insertion)
    


def insertHomeCourt(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO homeCourt (sName,cName) VALUES ({},{})".format(df.iloc[row]['sName'],df.iloc[row]['host'])
        execute_query(connection, insertion)
    

#两个dataframe,一个比赛记录，一个stadiums和俱乐部名字
def insertHostStadium(connection, match, stadiums):
    
    for row in range(match.shape[0]):
        club = match.iloc[row]['Home Team']
        stadium = stadium.stadiums.loc[stadiums['host'] == club]['sName']
        insertion = "INSERT INTO hostStadium (host,sName) VALUES ({},{})".format(club, stadium)
        execute_query(connection, insertion)



    


def insertMatch(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO match (eName,ctName,size) VALUES ({},{},{})".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'])
        execute_query(connection, insertion)


def insertMatchTable(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO matchTable (host,visit,matchDate,eName,awayShots,homeShots,awayBooks,homeBooks) VALUES ({},{},{},{},{},{},{},{}".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],)
        execute_query(connection, insertion)


def insertParticipate(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO participate (cName,eName) VALUES ({},{})".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'])
        execute_query(connection, insertion)


#先输入一遍所有people，然后Player和referee都按顺序reference 
def insertPeople(connection, num):
    
    for row in range(num):
        insertion = "INSERT INTO people () VALUES ()"
        execute_query(connection, insertion)

#输入Players
def insertPlayer(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO player (ID,cName,pName,DOB) VALUES ({},{},{},{})".format(row, df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'])
        execute_query(connection, insertion)

#从Player最后一个的ID开始给referee id
def insertReferee(connection, df, startNum):
    for row in range(df.shape[0]):
        insertion = "INSERT INTO referee (ID, rName) VALUES({}, '{}')".format(row+startNum , df.iloc[row]['rName'])

def insertRounds(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO rounds (size,numberOfRounds) VALUES ({},{})".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'])
        execute_query(connection, insertion)


def insertTournamnet(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO tournament (eName) VALUES ({})".format(df.iloc[row]['AAA'])
        execute_query(connection, insertion)
    
if __name__ == "__main__":
    main()
