#!/usr/bin/env python

import json, urllib2, sys

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

def Main():
    COLUMNS = '%-24s %-8s %-8s %-13s'

    print(COLUMNS % ('Tracking #', 'Shipper', 'Status', 'Delivery Est.'))
    print('=' * 56)
    
    for trackingNo in open('packages', 'r'):
        p = Package(trackingNo)
        i = p.getInfo()

        print(COLUMNS % (p.TrackingNumber,
                         i.data['shipper'],
                         i.data['shipmentStatus'],
                         i.data['deliveryEstimate']
                         ))
        
        print('-' * 56)


if __name__ == '__main__':
    Main()
