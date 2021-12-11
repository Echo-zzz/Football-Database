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
        insertion = "INSERT INTO stadium (sName, ctName, capacity, Year of Built) VALUES ({}, {}, {}, {}, {})".format(df.iloc[row]['sName'],df.iloc[row]['ctName'],df.iloc[row]['capacity'], df.iloc[row]['Year of Built'])
        s.execute_query(connection, insertion)
    
    return

def insertClub(connection, df):
    
    for row in range(df.shape[0]):
        insertion = "INSERT INTO club (cName, ctName, Nickname, found Date, official site) VALUES ({}, {}, {}, {}, {} {})".format(df.iloc[row]['cName'],df.iloc[row]['ctName'],df.iloc[row]['Nickname'], df.iloc[row]['found Date'], df.iloc[row]['official site'])
        s.execute_query(connection, insertion)
    
    return




