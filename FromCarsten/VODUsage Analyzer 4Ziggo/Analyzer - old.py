'''
Created on Nov 14, 2012

@author: csels
'''
import Purchase
import pyodbc
import csv
import datetime
import os
import re

def getPurchasesDB(startDateTime, endDateTime):
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.2.69.;DATABASE=PRODIS_REPORTING;UID=sa;PWD=Xs4ep0!')
        cursor = connection.cursor()
        print startDateTime, endDateTime
        
        #Execute SQL statement with paramters as ?
        cursor.execute(r"""select p.Name, t.EntitlementId, t.StbId, t.PurchaseCompletedTimeStamp, t.ProductId 
                            FROM TVodPurchases as t, ProductDefinitions as p
                            where PurchaseCompleted = ?
                            and PurchaseCompletedTimeStamp>=? 
                            AND PurchaseCompletedTimeStamp<=?
                            and t.ProductId = p.VodBackOfficeId""", 1, startDateTime, endDateTime)
        results = cursor.fetchall()
        
        purchasesDB = []
        #Fill list with transactions from DB
        for r in results:
            purchaseDB = Purchase.Purchase(r[0], r[1], r[2], r[3], r[4])
            purchasesDB.append(purchaseDB)
            
        return purchasesDB
        

path = r'C:\VODUsageFiles1\07'
uniqueMismatches = []
for csvfile in os.listdir(path):
    pattern = re.compile('Transactions')
    if re.search(pattern, os.path.join(path, csvfile)) is not None:
        print os.path.join(path, csvfile)
        csvf = open(os.path.join(path, csvfile))
        vodusagereader = csv.reader(csvf, delimiter=',')
        
        i=0
        purchasesCSV = []
        for row in vodusagereader:
            if i != 0:
                #Get StartDate for SQL Query
                if i == 1:
                    startDateTime = datetime.datetime(int(float(row[2][0:4])), int(float(row[2][4:6])), int(float(row[2][6:8])), int(float(row[2][8:10])), int(float(row[2][10:12])), int(float(row[2][12:14])))
                
                #Get important data for every transaction
                purchaseDateString = row[2]
                purchaseDateTime = datetime.datetime(int(float(purchaseDateString[0:4])), int(float(purchaseDateString[4:6])), int(float(purchaseDateString[6:8])), int(float(purchaseDateString[8:10])), int(float(purchaseDateString[10:12])), int(float(purchaseDateString[12:14])))
                entitlementId, productName, stbId, endDateTime = row[16], row[5], row[3], row[2]
                purchaseCSV = Purchase.Purchase(productName, entitlementId, stbId, purchaseDateTime)
                purchasesCSV.append(purchaseCSV)
                
                #Set firstOccurenceDate
                if len(uniqueMismatches) != 0:
                    for uM in uniqueMismatches:
                        if purchaseCSV.productName == uM.productName:
                            if uM.firstOccurrence == "Not found":
                                uM.firstOccurrence = datetime.datetime(int(float(purchaseDateString[0:4])), int(float(purchaseDateString[4:6])), int(float(purchaseDateString[6:8])), int(float(purchaseDateString[8:10])), int(float(purchaseDateString[10:12])), int(float(purchaseDateString[12:14])))
                 
                #Set EndDateTime for SQL query
                endDateTime = datetime.datetime(int(float(endDateTime[0:4])), int(float(endDateTime[4:6])), int(float(endDateTime[6:8])), int(float(endDateTime[8:10])), int(float(endDateTime[10:12])), int(float(endDateTime[12:14])))
            i+=1
        
        
        purchasesDB = getPurchasesDB(startDateTime, endDateTime)
        
        mismatches = []
        i=0
        print len(purchasesDB), len(purchasesCSV)
        if (len(purchasesDB) != len(purchasesCSV)) & (len(purchasesDB) > len(purchasesCSV)):  
            #Compare list of CSV transactions with list of DB transactions
            for p in purchasesDB:
                countMatches = 0
                for p1 in purchasesCSV:
                    if p.entitlementId.lower() == p1.entitlementId.lower():
                        countMatches += 1
                if countMatches == 0:
                    mismatches.append(p)        
            
            #Find out unique mismatches and add to new uniqueMismatches list
            for m in mismatches:
                print '\t', m.productName, '\t', m.VBOID     
                           
                if len(uniqueMismatches) != 0:
                    
                    countMatches = 0
                    for uM in uniqueMismatches:
                        if m.productName == uM.productName:
                            countMatches += 1
                            uM.countUnique += 1
                    if countMatches == 0:
                        uniqueMismatches.append(m)
                else:
                    uniqueMismatches.append(m)
                    
        
for uM in uniqueMismatches:
    print uM.productName, uM.firstOccurrence, uM.countUnique
    
    

        
