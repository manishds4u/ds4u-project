# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 15:46:45 2019

@author: Manish
"""

import mysql.connector

local_connection = mysql.connector.connect(
                                           host="localhost",
                                           user="root",
                                           passwd="",
                                           database="rasadb"
                                           )
local_cursor = local_connection.cursor()
#local_cursor = local_connection.cursor()
#sql = "insert into rasatb (message, reply) values ('%s','%s')" %(inp_msg,replied)
sql="select message from rasatb WHERE people=2"
local_cursor.execute(sql)
myresult = local_cursor.fetchall()
#fetch=1
#myresult = local_cursor.fetchmany(fetch)
#print(type(myresult))
for row in myresult:
    rows=row[0]
    
print(rows)
    print(row[0])
    print(list(row))
    #print(type(row))
    print(row[0])
    for i in row["message"]:
        print(i)
    
    print("column_names:", x.column_names, end='\n\n')
  

  print(type(x[0]))


for i in range(len(myresult)):
    print (myresult[i])