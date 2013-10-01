# -*- coding: utf-8 -*-

import urllib2
import json
import sqlite3

class VelibDataDownloader():
    def __init__(self):
    # We retrieve the API key in `~/.velib`, a text file with just the API key.
        with open('.velib', 'r') as f:
            self.key = f.read()

    def get_data(self):
        if self.key is not None:
            # This function generates the full URL from a short REST path.
            def geturl(path):
                delim = '&' if '?' in path else '?'  
                return "https://api.jcdecaux.com/vls/v1/{0:s}{1:s}apiKey={2:s}".format(path, delim, self.key)
            
            # This function returns the requested data in a Python dictionary.
            def get(path):
                url = geturl(path)
                return json.loads(urllib2.urlopen(url).read())
            
            # Here, we retrieve the list of all contracts, and show only the `Paris` 
            # contract.
            filter(lambda d: d['name'] == 'Paris', get('contracts'))
            
            # Now, we retrieve the list of all stations in the Paris contract.
            stations = get('stations?contract=Paris')
            return stations
    
    def write_to_db(self, stations, db_name = 'velib.db'):
        # open DB
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        result = c.execute('''SELECT * FROM sqlite_master WHERE type='table' AND name='data';''')
        
        # if table doesn't exist, we create it
        if result.fetchall() == []:
            c.execute('''CREATE TABLE data 
                 (station_number real, bike_stands real, available_bikes real,
                  available_bike_stands real, last_update real)''')

        # populating table with the records from the data
        for station in stations:
            data_to_insert = (station['number'], station['bike_stands'],
                              station['available_bikes'], station['available_bike_stands'],
                                station['last_update'])
            c.execute('INSERT INTO data VALUES (?,?,?,?,?)', data_to_insert)
        # closing DB      
        conn.commit()    
        conn.close()
    
if __name__ == '__main__':
    write_to_db(stations)