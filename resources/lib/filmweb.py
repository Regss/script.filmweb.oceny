# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import urllib
import urllib2
import hashlib
import os
import re
import datetime

__addon__       = xbmcaddon.Addon()
__addon_id__    = __addon__.getAddonInfo('id')
__addonpath__   = xbmc.translatePath(__addon__.getAddonInfo('path'))
__path__        = os.path.join(__addonpath__, 'resources', 'lib' )
__path_img__    = __addonpath__ + '/images/'
__lang__        = __addon__.getLocalizedString

import debug

LOGIN           = __addon__.getSetting('login')
PASS            = __addon__.getSetting('pass')

API_URL         = 'https://ssl.filmweb.pl/api';
API_KEY         = 'qjcGhW2JnvGT9dfCt3uT_jozR3s';
API_ID          = 'android';
API_VER         = '2.2';

class Filmweb:
            
    def getUserFilmVotes(self, filmwebID):
        if self.login() == False:
            return False
        
        # pobranie oceny
        debug.debug('Zalogowano')
        vote_array = {}
        api_method = 'getUserFilmVotes [null, null]\n'.encode('string_escape')
        string = self.sendRequest(api_method, 'get')
        matches = re.findall('\[([0-9]+),[^,]+,([0-9]+),', string)
        if len(matches) > 0:
            for m in matches:
                vote_array[m[0]] = m[1]
            
        # pobranie tytułu
        api_method = 'getFilmsInfoShort [[' + filmwebID + ']]\n'.encode('string_escape')
        string = self.sendRequest(api_method, 'get')
        matches = re.findall('\[\["([^"]+)",', string)
        if len(matches) > 0:
            title = matches[0]
        else:
            title = ''
            
        if filmwebID in vote_array.keys():
            return [title, vote_array[filmwebID]]
        else:
            return [title, '0']
        
    def addUserFilmVote(self, filmwebID, vote):
        if self.login() == False:
            return False
        
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if vote == '0':
            api_method = 'removeUserFilmVote [' + filmwebID + ']\n'.encode('string_escape')
        else:
            api_method = 'addUserFilmVote [[' + filmwebID + ',' + vote + ',"",0]]\nupdateUserFilmVoteDate [' + filmwebID + ', ' + date + ']\n'.encode('string_escape')
        self.sendRequest(api_method, 'post')
    
    def login(self):
        self.login = True
        self.cookie = ''
        api_method = 'login [' + LOGIN + ',' + PASS + ',1]\n'.encode('string_escape')
        
        page = self.sendRequest(api_method, 'post')
        self.login = False
        
        if len(re.findall('^err', page)) > 0:
            debug.debug('Błędny login lub hasło')
            debug.notify('Błędny login lub hasło')
            return False
            
    def create_sig(self, methods):
        
        return '1.0,' + hashlib.md5(methods + API_ID + API_KEY).hexdigest()
        
    def sendRequest(self, api_method, http_method):
        
        values = { 'methods': api_method, 'signature': self.create_sig(api_method), 'appId': API_ID, 'version': API_VER }
        data = urllib.urlencode(values)
        
        if 'get' in http_method:
            req = urllib2.Request(API_URL + '?' + data)
            
        else:
            req = urllib2.Request(API_URL, data)
            
        req.add_header('cookie', self.cookie)
        try:
            response = urllib2.urlopen(req)
        except:
            debug.notify('Błąd połaczenia')
            
        if self.login == True:
            self.cookie = response.headers.get('Set-Cookie')
        page = response.read()
        debug.debug('Odpowiedź z serwera - ' + page)
        return page
        