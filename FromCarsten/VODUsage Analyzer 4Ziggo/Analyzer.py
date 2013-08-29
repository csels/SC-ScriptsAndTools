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

connection = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.2.69.;DATABASE=PRODIS_REPORTING;UID=sa;PWD=Xs4ep0!')
uniqueMismatches = []

def readVODUsage(vodusagereader):
    vodusagereader = csv.reader(csvf, delimiter=',')
    i=0
    purchasesCSV = []
    startDateTime = ""
    endDateTime = ""
    for row in vodusagereader:
        if i != 0:
            #Get StartDate for SQL Query
            if i == 1:
                startDateTime = datetime.datetime(int(float(row[2][0:4])), int(float(row[2][4:6])), int(float(row[2][6:8])), int(float(row[2][8:10])), int(float(row[2][10:12])), int(float(row[2][12:14])))
            
            #Get important data for every transaction
            purchaseDateString = row[2]
            purchaseDateTime = datetime.datetime(int(float(purchaseDateString[0:4])), int(float(purchaseDateString[4:6])), int(float(purchaseDateString[6:8])), int(float(purchaseDateString[8:10])), int(float(purchaseDateString[10:12])), int(float(purchaseDateString[12:14])))
            entitlementId, productName, stbId, endDateTime = row[16], row[5], row[3], row[2]
            
            #GetVBOIDByEntitlementID
            vboid = getVBOIDBYEntitlementID(entitlementId)
            
            purchaseCSV = Purchase.Purchase(productName, entitlementId, stbId, purchaseDateTime, vboid)
            purchasesCSV.append(purchaseCSV)
            
            #Set first occurrence
            if len(uniqueMismatches) != 0:
                for uM in uniqueMismatches:
                    if purchaseCSV.productName == uM.productName:
                        if uM.firstOccurrence == "Never found":
                            uM.firstOccurrence = datetime.datetime(int(float(purchaseDateString[0:4])), int(float(purchaseDateString[4:6])), int(float(purchaseDateString[6:8])), int(float(purchaseDateString[8:10])), int(float(purchaseDateString[10:12])), int(float(purchaseDateString[12:14])))
            
            #Set EndDateTime for SQL query
            endDateTime = datetime.datetime(int(float(endDateTime[0:4])), int(float(endDateTime[4:6])), int(float(endDateTime[6:8])), int(float(endDateTime[8:10])), int(float(endDateTime[10:12])), int(float(endDateTime[12:14])))
        i+=1   
    return (purchasesCSV, startDateTime, endDateTime)




def getVBOIDBYEntitlementID(eId):
    cursor = connection.cursor()

    #Execute SQL statement with paramters as ?
    cursor.execute(r"""select ProductId FROM TVodPurchases WHERE EntitlementId=?""", eId)
    result = cursor.fetchone()
    
    return result[0]




def getPurchasesDB(startDateTime, endDateTime):
        cursor = connection.cursor()
        
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
    
    
    
    
def getMismatches(purchasesDB, purchasesCSV):
    mismatches = []
    i=0
    print len(purchasesDB), len(purchasesCSV)
    if (len(purchasesDB) != len(purchasesCSV)) & (len(purchasesDB) > len(purchasesCSV)):  
        #Compare list of CSV transactions with list of DB transactions
        for p in purchasesDB:
            countMatches = 0
            for p1 in purchasesCSV:
                if (p.entitlementId.lower() == p1.entitlementId.lower()) & (p.VBOID == p1.VBOID):
                    countMatches += 1
            if countMatches == 0:
                mismatches.append(p)        
        
        #Find out unique mismatches and add to new uniqueMismatches list
        for m in mismatches:
            if len(uniqueMismatches) != 0:
                
                countMatches = 0
                for uM in uniqueMismatches:
                    if m.VBOID == uM.VBOID:
                        countMatches += 1
                        uM.countUnique += 1
                        uM.lastMismatchDate = m.purchaseDate
                if countMatches == 0:
                    uM.lastMismatchDate = m.purchaseDate
                    uniqueMismatches.append(m)
            else:
                uniqueMismatches.append(m)
    return mismatches

'''
Main application starts here
'''
                
path = r'C:\VODUsageFiles1\07'
uniqueMismatches = []
vodUsageFiles = os.listdir(path)

csvNo=0
for csvfile in vodUsageFiles:
    pattern = re.compile('Transactions')
    if re.search(pattern, os.path.join(path, csvfile)) is not None:
        csvNo+=1
        print os.path.join(path, csvfile)
        print '%i/%i' % (csvNo, len(vodUsageFiles))
        csvf = open(path, csvfile)
        
        #Retrieve all purchases from current CSV and fill list of purchases
        purchasesCSV, startDateTime, endDateTime = readVODUsage(csvf)
        
        #Retrieve all purchases from current DB and fill list of purchases
        purchasesDB = getPurchasesDB(startDateTime, endDateTime)
        
        #Retrieve all mismatches between PurchasesDB and PurchasesCSV lists
        mismatches = getMismatches(purchasesDB, purchasesCSV)
        
        #Show all mismatches for the file
        for m in mismatches:
            print '\t', m.productName, '\t', m.stbID, '\t', m.purchaseDate
                    
#Retrieve all uniqueMismatches: This is a global list that spreads over all VOD Usage Files        
i=0
for uM in uniqueMismatches:
    #if uM.countUnique > 20:
    i+=1
    print i, "\t", uM.productName, '\t', uM.VBOID, '\t', uM.countUnique, '\t', uM.lastMismatchDate, '\t', uM.firstOccurrence
    
    

        
