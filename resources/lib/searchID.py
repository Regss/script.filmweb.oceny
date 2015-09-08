# -*- coding: utf-8 -*-

import xbmc
import os
import re
import json
import urllib

class Search:

    def searchID(self):
        
        if 'movie' in xbmc.getInfoLabel('ListItem.DBTYPE'):
            movieid = xbmc.getInfoLabel('ListItem.DBID')
        else:
            return ''
        
        jsonGet = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"movieid": ' + movieid + ', "properties": ["file", "art", "trailer"]}, "id": 1}')
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
        