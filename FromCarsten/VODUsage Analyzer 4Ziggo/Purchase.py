'''
Created on Nov 22, 2012

@author: csels
'''
class Purchase:
    productName = ""
    stbID = ""
    entitlementId = ""
    purchaseDate = ""
    VBOID = ""
    firstOccurrenceInCSV = ""
    lastMismatchDate = ''
    countUnique = 1

    def __init__(self, name, productEntitlementId, cpeId, purchaseTime, vboid="ffff-ffff-ffff-ffff"):
        self.productName = name
        self.stbID = cpeId
        self.entitlementId = productEntitlementId
        self.purchaseDate = purchaseTime
        self.VBOID = vboid
        
    