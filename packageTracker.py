#!/usr/bin/env python

import json, urllib2, sys, datetime

class PackagePayload:
	def __init__(self, jsonString):
		self.__dict__ = json.loads(jsonString)

class Package:
	API_BASE_URL = 'http://api.boxoh.com'
	API_VERSION = 'v2'
	API_PROTOCOL = 'rest'
	API_AUTH_SCHEME = 'key'

	def __init__(self, trackingNumber):
		self.TrackingNumber = trackingNumber.strip()
		self.APIKey = open('apikey', 'r').read().strip()
		self.APIUrl = '{0}/{1}/{2}/{3}/{4}/track/{5}/data/'.format(
				self.API_BASE_URL,
				self.API_VERSION,
				self.API_PROTOCOL,
				self.API_AUTH_SCHEME,
				self.APIKey,
				self.TrackingNumber
				)

	def getPayload(self):
		try:
			response = urllib2.urlopen(self.APIUrl)
		except urllib2.URLError as e:
			print(e.reason)
			print('Make sure your internet connection is active')
			sys.exit(1)

		return response.read()

	def getInfo(self):
		payload = self.getPayload()
		return PackagePayload(payload)

def GetReason(errorCode):
	if errorCode == 601:
		return 'Invalid API key'
	elif errorCode == 602:
		return 'Failed to find tracking number from shipper'
	elif errorCode == 604:
		return 'Map API key is required but not found'
	elif errorCode == 605:
		return 'Invalid alias provided'
	else:
		return 'Unknown error'

def Main():
	COLUMNS = '%-24s %-10s %-10s %-13s'

	print(COLUMNS % ('Tracking #', 'Shipper', 'Status', 'Delivery Est.'))
	print('=' * 60)

	for trackingNo in open('packages', 'r'):
		if (trackingNo.isspace()):
			continue

		p = Package(trackingNo.strip())
		i = p.getInfo()

		if i.result == 'error':
			print(COLUMNS % (p.TrackingNumber,
							 '* Error: %s *' % GetReason(i.error['errorCode']),
							 '',
							 ''))
			continue

		if i.data['deliveryEstimate'] == None or i.data['deliveryEstimate'] == False:
			i.data['deliveryEstimate'] = ' - '
		else:
			try:
				i.data['deliveryEstimate'] = datetime.datetime.fromtimestamp(i.data['deliveryEstimate']).strftime('%a, %b %d')
			except:
				pass # If we couldn't parse it, then let's just try to print it!

		print(COLUMNS % (p.TrackingNumber,
						 i.data['shipper'],
						 i.data['shipmentStatus'].title(),
						 i.data['deliveryEstimate']
						))

if __name__ == '__main__':
	Main()
