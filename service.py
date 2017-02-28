# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import json
import urllib
import re
import os

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path'))

class Monitor(xbmc.Monitor):
    
    def __init__(self):
        xbmc.Monitor.__init__(self)
    
    def onNotification(self, sender, method, data):
        if method == 'VideoLibrary.OnUpdate':
            data = json.loads(data)
            if 'playcount' in data and data['playcount'] > 0:
                if 'item' in data and 'type' in data['item'] and data['item']['type'] == 'movie' and 'id' in data['item']:
                    id = data['item']['id']
                    filmwebID = self.searchID(id)
                    if len(filmwebID) > 0:
                        xbmc.executebuiltin('XBMC.RunScript(' + __addon_id__ + ', ' + filmwebID + ', true)')
    
    def searchID(self, id):
        
        jsonGet = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"movieid": ' + str(id) + ', "properties": ["file", "art", "trailer"]}, "id": 1}')
        jsonGet = unicode(jsonGet, 'utf-8', errors='ignore')
        jsonGetResponse = json.loads(jsonGet)
        
        result = re.findall('fwcdn.pl/po/[^/]+/[^/]+/([0-9]+)/', urllib.unquote(str(jsonGetResponse)))
        if len(result) > 0:
            return result[0]
                
        result = re.findall('fwcdn.pl/ph/[^/]+/[^/]+/([0-9]+)/', urllib.unquote(str(jsonGetResponse)))
        if len(result) > 0:
            return result[0]
                
        result = re.findall('http://mm.filmweb.pl/([0-9]+)/', urllib.unquote(str(jsonGetResponse)))
        if len(result) > 0:
            return result[0]
                
        filePath, fileExt = os.path.splitext(jsonGetResponse['result']['moviedetails']['file'])
        fileNfo = filePath + '.nfo'
        
        if os.path.isfile(fileNfo):
        
            file = open(fileNfo, 'r')
            file_data = file.read()
            file.close()
            
            result = re.findall('fwcdn.pl/po/[^/]+/[^/]+/([0-9]+)/', file_data)
            if len(result) > 0:
                return result[0]
            
            result = re.findall('fwcdn.pl/ph/[^/]+/[^/]+/([0-9]+)/', file_data)
            if len(result) > 0:
                return result[0]
                
            result = re.findall('<trailer>http://mm.filmweb.pl/([0-9]+)/', file_data)
            if len(result) > 0:
                return result[0]
                
            result = re.findall('http://www.filmweb.pl/Film?id=([0-9]+)', file_data)
            if len(result) > 0:
                return result[0]
                
        return ''
        
monitor = Monitor()

while(not xbmc.abortRequested):
    xbmc.sleep(100)
    