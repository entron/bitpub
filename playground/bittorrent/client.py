#! /usr/bin/env python

import requests
import hashlib
import BitTorrent.bencode as bencode
import binascii
from twisted.internet import reactor, protocol
import io

f = open('ubuntu_info_dict.dat', 'rb')
d = f.read()
f.close()
info_hash = hashlib.sha1(d).digest()


peer_id = '-BP0001-901234567890'

anounce_url = 'http://torrent.ubuntu.com:6969/announce'

payload = {'info_hash': info_hash, 'peer_id': peer_id, 'left': '925892608', 'port': '6881', 
           'uploaded':'0', 'downloaded':'0', 'compact': '0', 'no_peer_id':'0', 'event':'started'}
r = requests.get(anounce_url, params=payload)

tracker_response = bencode.bdecode(r.content)

peers = tracker_response['peers']

ip_field0 = int(binascii.b2a_hex(peers[0]),16)
ip_field1 = int(binascii.b2a_hex(peers[1]),16)
ip_field2 = int(binascii.b2a_hex(peers[2]),16)
ip_field3 = int(binascii.b2a_hex(peers[3]),16)
ip = '.'.join([str(ip_field0), str(ip_field1) , str(ip_field2), str(ip_field3)])

port = int(binascii.b2a_hex(peers[4:6]),16)

def parseHandshake(data):
    byte_stream = io.BytesIO()    


class BTClient(protocol.Protocol):
    """A simple BT client"""
    
    def connectionMade(self):
        print('Connection made.')
        self.transport.write(handshake())
    
    def dataReceived(self, data):
        print "Server said:", data
        print len(data)
    
    def connectionLost(self, reason):
        print "connection lost"

class BTFactory(protocol.ClientFactory):
    protocol = BTClient

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()


def handshake():
    pstrlen = '\x13' #Number 19
    pstr = 'BitTorrent protocol'
    reserved = '\0\0\0\0\0\0\0\0'
    
    byte_stream = io.BytesIO()
    byte_stream.write(pstrlen)
    byte_stream.write(pstr)
    byte_stream.write(reserved)
    byte_stream.write(info_hash)
    byte_stream.write(peer_id)
    
    return byte_stream.getvalue()



f = BTFactory()
reactor.connectTCP(ip, port, f)
reactor.run()
