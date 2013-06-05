# -*- coding: utf-8 -*-

import urllib2
import json
import os
import datetime
import sqlite3

# We retrieve the API key in `~/.velib`, a text file with just the API key.

with open(os.path.expanduser('~/workspace/VelibApp/.velib'), 'r') as f:
    key = f.read()

# This function generates the full URL from a short REST path.

def geturl(path):
    delim = '&' if '?' in path else '?'  
    return "https://api.jcdecaux.com/vls/v1/{0:s}{1:s}apiKey={2:s}".format(path, delim, key)

# This function returns the requested data in a Python dictionary.

def get(path):
    url = geturl(path)
    return json.loads(urllib2.urlopen(url).read())

# Here, we retrieve the list of all contracts, and show only the `Paris` contract.

filter(lambda d: d['name'] == 'Paris', get('contracts'))

# Now, we retrieve the list of all stations in the Paris contract.

stations = get('stations?contract=Paris')

def write_to_db(stations):
    
    db_name = 'velib.db'
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    result = c.execute('''SELECT * FROM sqlite_master WHERE type='table' AND name='data';''')
    
    if result.fetchall() == []:
        c.execute('''CREATE TABLE data 
             (station_number real, bike_stands real, available_bikes real,
              available_bike_stands real, last_update real)''')
        # Create table
    for station in stations:
        data_to_insert = (station['number'], station['bike_stands'],
                          station['available_bikes'], station['available_bike_stands'],
                            station['last_update'])
        c.execute('INSERT INTO data VALUES (?,?,?,?,?)', data_to_insert)
            
    conn.commit()    
    conn.close()
    
write_to_db(stations)