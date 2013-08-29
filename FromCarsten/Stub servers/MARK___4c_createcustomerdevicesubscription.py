import xml.dom.minidom
import requests
import os

crmUri = 'http://172.16.118.155:9100/CrmService'
customerDevicePrefix = 'prftst-'
numberOfDevices = 30000
deviceNumberOffset = 10002
subscriptionProduct = 'TVCHOICE_XL'

def createDevice(device):
	url = crmUri + '/Devices/' + device
	headers = {'content-type': 'application/xml'}
	payload = '<?xml version="1.0" encoding="utf-8" ?>\r\n <Device id="' + device + '" xmlns="urn:eventis:crm:2.0" />'
	r = requests.put(url, data=payload, headers=headers)

	print 'Device: ' + str(r.status_code)

def createCustomer(customer):
	url = crmUri + '/Customers/' + customer
	headers = {'content-type': 'application/xml'}
	payload = '<?xml version="1.0" encoding="utf-8" ?>\r\n <Customer id="' + customer + '" xmlns="urn:eventis:crm:2.0" />'
	r = requests.put(url, data=payload, headers=headers)
	
	print 'Customer: ' + str(r.status_code)

def createCustomerDeviceAssociation(customer,device):
	url = crmUri + '/Customers/' + customer + '/Devices/' + device
	headers = {'content-type': 'application/xml'}
	r = requests.put(url, headers=headers)
	
	print 'CustomerDevice: ' + str(r.status_code) + '\r\n'

def createCustomerSubscription(customer,subscription):
	url = crmUri + '/Customers/' + customer + '/SubscriptionProducts/' + subscription
	headers = {'content-type': 'application/xml'}
	r = requests.put(url, headers=headers)
	
	print 'CustomerSubscription: ' + str(r.status_code) + '\r\n'

i = 0
while i <= numberOfDevices:
	deviceId = customerDevicePrefix + 'dev-' + str(deviceNumberOffset)
	customerId = customerDevicePrefix + 'cus-' + str(deviceNumberOffset)
	print deviceId + '/' + customerId + '/' + subscriptionProduct
	createDevice(deviceId)
	createCustomer(customerId)
	createCustomerDeviceAssociation(customerId,deviceId)
	createCustomerSubscription(customerId,subscriptionProduct)
	i = i + 1
	deviceNumberOffset = deviceNumberOffset + 1

#createDevice('mark')
#createCustomer('mark')
#createCustomerDeviceAssociation('mark','mark')