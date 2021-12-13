# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 10:43:14 2021

@author: jimmy
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


def readTable(path):
    dataframe = pd.read_csv(path)
   
    return dataframe


def insertStadium(connection, df):
    
    for row in range(df.shape[0]):
        
        insertion = "INSERT INTO stadium (sName, ctName, capacity, Year of Built) VALUES ({}, {}, {}, {})".format(df.iloc[row]['sName'],df.iloc[row]['ctName'],df.iloc[row]['capacity'], df.iloc[row]['yearOfBuilt'])
        s.execute_query(connection, insertion)
    
    return

def insertClub(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO club (cName, nickName, foundYear, ctName, officialSite) VALUES ({}, {}, {}, {}, {})".format(df.iloc[row]['cName'],df.iloc[row]['nickname'],df.iloc[row]['foundYear'], df.iloc[row]['ctName'], df.iloc[row]['officialSite'])
        s.execute_query(connection, insertion)
    
    return
###以下需要改对应csv colum的名字
def insertAttend(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO attend (ID, matchID) VALUES ({}, {})".format(df.iloc[row]['AAA'],df.iloc[row]['BBB'])
        s.execute_query(connection, insertion)
    
    return

def insertBelong(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO belong (ID,ctName ) VALUES ({}, {})".format(df.iloc[row]['AAA'],df.iloc[row]['BBB'])
        s.execute_query(connection, insertion)
    
    return

def insertCountry(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO country (ctName) VALUES ({})".format(df.iloc[row]['AAA'])
        s.execute_query(connection, insertion)
    
    return

def insertEvent(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO event (eName,season,cName) VALUES ({},{},{})".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'])
        s.execute_query(connection, insertion)
    
    return

def insertFriendly(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO friendly (eName) VALUES ({})".format(df.iloc[row]['AAA'])
        s.execute_query(connection, insertion)
    
    return

def insertHomeCourt(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO homeCourt (sName,cName) VALUES ({},{})".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'])
        s.execute_query(connection, insertion)
    
    return

def insertHostStadium(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO hostStadium (host,sName) VALUES ({},{})".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'])
        s.execute_query(connection, insertion)
    
    return

def insertLeague(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO league (eName,ctName,size) VALUES ({},{},{})".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'])
        s.execute_query(connection, insertion)
    
    return

def insertMatch(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO match (eName,ctName,size) VALUES ({},{},{})".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'])
        s.execute_query(connection, insertion)
    
    return

def insertMatchTable(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO matchTable (host,visit,matchDate,eName,awayShots,homeShots,awayBooks,homeBooks) VALUES ({},{},{},{},{},{},{},{}".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],)
        s.execute_query(connection, insertion)
    return

def insertParticipate(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO participate (cName,eName) VALUES ({},{})".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'])
        s.execute_query(connection, insertion)
    return 

def insertPeople(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO people (ID) VALUES ({})".format(df.iloc[row]['AAA'])
        s.execute_query(connection, insertion)
    return 

def insertPlayer(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO player (ID,cName,pName,DOB) VALUES ({},{},{},{})".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'],df.iloc[row]['AAA'])
        s.execute_query(connection, insertion)
    return 

def insertRounds(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO rounds (size,numberOfRounds) VALUES ({},{})".format(df.iloc[row]['AAA'],df.iloc[row]['AAA'])
        s.execute_query(connection, insertion)
    return 

def insertTournamnet(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO tournament (eName) VALUES ({})".format(df.iloc[row]['AAA'])
        s.execute_query(connection, insertion)
    return 