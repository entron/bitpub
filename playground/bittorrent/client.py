#! /usr/bin/env python

import requests
import hashlib

f = open('ubuntu_info_dict.dat', 'rb')
d = f.read()
f.close()
info_hash = hashlib.sha1(d).hexdigest()


peer_id = 'BP-12345678901234567'

anounce_url = 'http://torrent.ubuntu.com:6969/announce'

payload = {'info_hash': info_hash, 'peer_id': peer_id, 'left': '925892608', 'port': '6881', 
           'uploaded':'0', 'downloaded':'0', 'compact': '0', 'no_peer_id':'0', 'event':'started'}
r = requests.get(anounce_url, params=payload)

