'''
Created on Sep 15, 2012

@author: carsten
'''
#Import necessary XML Parser modules
import xml.dom.minidom
import urllib2, csv

#Open the TVA file
f = open(r'C:\Users\csels\Documents\SeaChange\Ziggo\Genres script -  Nov 2012\ContentCS.xml')

#Convert XML to string so we can parse it
TVAString = f.read()

#Parse the TVAString
domGenres = xml.dom.minidom.parseString(TVAString)

#Close XML file 'cause not needed anymore
f.close()

#Read CSV
pathGenres = r'C:\Users\csels\Documents\SeaChange\Ziggo\Genres script -  Nov 2012\ZiggoProposalGenres.csv'
csvZiggoGenres = open(pathGenres)
vodusagereader = csv.reader(csvZiggoGenres, delimiter=',')

i=0
lastNode = ''
for row in vodusagereader:
    if i >1:
        genreNo = row[0]
        genreEN = row[1]
        genreNL = row[2]
        termNodes = domGenres.getElementsByTagName('Term')
        
        j=0
        countMatch = 0
        for termNode in termNodes:
            j += 1
            
            #Term ID found
            if termNode.attributes['termID'].value == genreNo:
                print genreNo
                countMatch += 1
                
                #Create new Node for Dutch Genre in XLSX
                x = domGenres.createElement('Name')
                x.setAttribute('xml:lang', 'nl')
                xText = domGenres.createTextNode(genreNL)
                x.appendChild(xText)
                                
                #Find place to append new Node
                try:
                    y = termNode.getElementsByTagName('Definition')[0]
                    termNode.insertBefore(x, y)         
                except:
                    try:
                        y = termNode.getElementsByTagName('Term')[0]
                        termNode.insertBefore(x, y)         
                    except:
                        termNode.appendChild(x)
                        print 'No childnode'
                                
            #Term ID not found --> create it in corresponding hierarchy    
            if (countMatch == 0) and (j==len(termNodes)-1):
                upHier = genreNo[:-2]
                for termNode in termNodes:
                    if termNode.attributes['termID'].value == upHier:
                        
                        #Create new Node for Dutch Genre in XLSX
                        x = domGenres.createElement('Term')
                        x.setAttribute("termID", genreNo)
                        termNode.appendChild(x)
                        
                        #Create new Node for Genre in XLSX: with Dutch and English name subnodes
                        if genreEN != '':
                            x1 = domGenres.createElement('Name')
                            x1.setAttribute('xml:lang', 'en')
                            x1Text = domGenres.createTextNode(genreEN)
                            x1.appendChild(x1Text)
                            x.appendChild(x1)
                        
                        #Create new Node for Dutch Genre in XLSX
                        x2 = domGenres.createElement('Name')
                        x2.setAttribute('xml:lang', 'nl')
                        x2Text = domGenres.createTextNode(genreNL)
                        x2.appendChild(x2Text)
                        
                        x.appendChild(x2)
    i += 1
    
output = open(r'C:\Users\csels\Documents\SeaChange\Ziggo\Genres script -  Nov 2012\%s' % 'ContentCS-Extended-Export.xml', 'w')    
output.write(domGenres.toprettyxml('  '))
print domGenres.toprettyxml()
    
'''    
#Retrieve all catalog_item tags in XML file and save them in a list
termItems = domGenres.getElementsByTagName('Term')
for term in termItems:
    if term.attributes['termID'].value == '3.1':
        x = domGenres.createElement('Name')
        x.setAttribute("xml:lang=\"", 'nl')
        xText = domGenres.createTextNode('Informatief')
        x.appendChild(xText)
        y = term.getElementsByTagName('Term')[0]

        term.insertBefore(x, y)

print domGenres.toxml()
        
     '''   
    
    
#Get the price for each catalog item (returned in a list) and append
#them to the general prices list
'''
prices = []
for item in catalog_items:
    price = item.getElementsByTagName('price')[0]
    prices.append(price)
    

for price in prices:
    print price.toxml()

    
#Get all child nodes of each catalog item
productNode = domTVA.getElementsByTagName('product')[0]
for childNode in productNode.childNodes:
    print childNode.toxml()
    
    '''