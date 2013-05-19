#!/usr/bin/env python

""" A REST client to retrieve information from the Vélib bicycle system, 
heavily inspired by http://www.bortzmeyer.org/velib-rest.html. """

__PROGRAM__ = "get-station"
__VERSION__ = "0.0"
__AUTHOR__ = "flothesof"

import sys 
import urllib
import xml.etree.cElementTree as ElementTree

base_url = "http://www.velib.paris.fr/service/stationdetails/paris/"

class AppURLopener(urllib.FancyURLopener):
    version = "%s/%s (get-station.py; Python %s)" % (__PROGRAM__, __VERSION__, sys.version[0:5])
    
def usage():
    print >>sys.stderr, ("Usage: %s station-number" % sys.argv[0])
    

def get_station_data(station):
    
    url = base_url + str(station)
    
    urllib._urlopener = AppURLopener()
    data = urllib.urlopen(url).read()
    
    xmltree = ElementTree.fromstring(data)
    
    time_updated = xmltree.find("updated").text
    available = int (xmltree.find("available").text)
    total = int (xmltree.find("total").text)
    free = int (xmltree.find("free").text)
    
    return (time_updated, available, free, total)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    else:
        station = int(sys.argv[1])
        (time_updated, available, free, total) = get_station_data(station)    
        print "Available bikes - Free slots - Total slots  at station %s updated at %s" % (station, time_updated)
        print "           %4u         %4u          %4u" % (available, free, total)

