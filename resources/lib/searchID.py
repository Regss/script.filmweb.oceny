# -*- coding: utf-8 -*-

import xbmc
import os
import re

class Filmweb:

    def searchID(self):
        ret = self.tryThumb()
        if len(ret) > 0:
            return ret[0]
            
        ret = self.tryFanart()
        if len(ret) > 0:
            return ret[0]
            
        ret = self.tryNfo()
        if len(ret) > 0:
            return ret[0]
            
        return ''
        
    def tryThumb(self):
        label = xbmc.getInfoLabel('ListItem.Thumb')
        result = re.findall('fwcdn.pl/po/[^/]+/[^/]+/([0-9]+)/', label)
        return result
    
    def tryFanart(self):
        label = xbmc.getInfoLabel('ListItem.Art(fanart)')
        result = re.findall('fwcdn.pl/ph/[^/]+/[^/]+/([0-9]+)/', label)
        return result
        
    def tryTrailer(self):
        label = xbmc.getInfoLabel('ListItem.Trailer')
        result = re.findall('mm.filmweb.pl/([0-9]+)/', label)
        return result
        
    def tryNfo(self):
        filePath = xbmc.getInfoLabel('ListItem.Path')
        fileName = xbmc.getInfoLabel('ListItem.FileName')
        fileExt = xbmc.getInfoLabel('ListItem.FileExtension')
        fileNfo = filePath + fileName.replace(fileExt, 'nfo' )
        
        if os.path.isfile(fileNfo):
        
            file = open(fileNfo, 'r')
            file_data = file.read()
            file.close()
            
            result = re.findall('fwcdn.pl/po/[^/]+/[^/]+/([0-9]+)/', file_data)
            if len(result) > 0:
                return result
            
            result = re.findall('fwcdn.pl/ph/[^/]+/[^/]+/([0-9]+)/', file_data)
            if len(result) > 0:
                return result
                
            result = re.findall('<trailer>http://mm.filmweb.pl/([0-9]+)/', file_data)
            if len(result) > 0:
                return result
                
            result = re.findall('http://www.filmweb.pl/Film?id=([0-9]+)', file_data)
            if len(result) > 0:
                return result
                
        return ''
        