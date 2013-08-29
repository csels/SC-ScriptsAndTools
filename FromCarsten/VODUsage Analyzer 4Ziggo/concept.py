'''
Created on Nov 14, 2012

@author: csels
'''
import pyodbc
import csv

connection = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.2.69.;DATABASE=PRODIS_BI;UID=sa;PWD=Xs4ep0!')
cursor = connection.cursor()

#Execute SQL statement with paramters as ?
cursor.execute(r"""select top 1000 * 
                    from FactTvodPurchases""")
results = cursor.fetchall()


#Read csv file
csvf = open(r'C:\VODUsageFiles\04\VODSessions_000100_20120425133047.csv')
vodusagereader = csv.reader(csvf, delimiter=',')
i=0
for row in vodusagereader:
    if i != 0:
        print row[1], row[2], row[3], row[4], row[5]
    i+=1


for result in results:
    print result