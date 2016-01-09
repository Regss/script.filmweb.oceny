# -*- coding: utf-8 -*-

import json
import xbmcgui
import xbmc
import re
import sys
import os
import xbmcaddon

__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path'))
__lang__                = __addon__.getLocalizedString
__path__                = os.path.join(__addonpath__, 'resources', 'lib' )
__path_img__            = os.path.join(__addonpath__, 'resources', 'media' )

sys.path.append(__path__)

ACTION_PREVIOUS_MENU        = 10
ACTION_MOVE_LEFT            = 1
ACTION_MOVE_RIGHT           = 2
ACTION_MOVE_UP              = 3
ACTION_MOVE_DOWN            = 4
ACTION_STEP_BACK            = 21
ACTION_NAV_BACK             = 92
ACTION_MOUSE_RIGHT_CLICK    = 101
ACTION_MOUSE_MOVE           = 107
ACTION_BACKSPACE            = 110
KEY_BUTTON_BACK             = 275

import searchID
import filmweb
import debug

class GUI():
    def __init__(self):
        
        self.main()
        
    def main(self):
        
        try:
            filmwebID = str(sys.argv[1])
        except:
            filmwebID = searchID.Search().searchID()
        else:
            if 'false' in __addon__.getSetting('onStopPlaying'):
                return False
            
        try:
            self.runFromService = str(sys.argv[2])
        except:
            self.runFromService = 'false'
            
        if len(filmwebID) == 0:
            debug.debug('Nie mogę znaleźć ID')
            return False
        
        user = [
            {'name': __addon__.getSetting('name_u1'), 
			'login': __addon__.getSetting('login_u1'), 
            'pass': __addon__.getSetting('pass_u1')}
        ]
        
        if 'true' in __addon__.getSetting('secUser'):
            user.append(
                {'name': __addon__.getSetting('name_u2'),
				'login': __addon__.getSetting('login_u2'),
                'pass': __addon__.getSetting('pass_u2')}
            )
        
        for userData in user:
            self.getVotes(filmwebID, userData)
        
    def getVotes(self, filmwebID, userData):
        film_vote = filmweb.Filmweb().getUserFilmVotes(filmwebID, userData)
        if film_vote == False:
            return False
        
        debug.debug('Pobrana ocena: ' + film_vote[1])
        
        if 'true' in self.runFromService and film_vote[1] != '0' and 'true' in __addon__.getSetting('onlyNotRated'):
            return False
        
        # display window rating
        display = WindowRating(filmwebID, film_vote[0], int(film_vote[1]), userData)
        display.doModal()
        del display
        
class WindowRating(xbmcgui.WindowDialog):
    
    def __init__(self, filmwebID, title, rating, userData):
        
        # set window property to true
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        self.window.setProperty('FilmwebOceny', 'true')
        
        # set vars
        self.filmwebID = filmwebID
        self.rating = rating
        self.userData = userData
        self.button = []
        
        # create window
        bgResW = 520
        bgResH = 200
        bgPosX = (1280 - bgResW) / 2
        bgPosY = (720 - bgResH) / 2
        self.bg = xbmcgui.ControlImage(bgPosX, bgPosY, bgResW, bgResH, __path_img__+'//bg.png')
        self.addControl(self.bg)
        self.labelName = xbmcgui.ControlLabel(bgPosX+20, bgPosY+22, bgResW-40, bgResH-40, '[B]' + self.userData['name'] + '[/B]', 'font14', '0xFFE60000',  alignment=2)
        self.addControl(self.labelName)
        self.labelTitle = xbmcgui.ControlLabel(bgPosX+20, bgPosY+60, bgResW-40, bgResH-40, '[B]Filmweb - oceń film:[/B]', 'font14', '0xFF0084ff',  alignment=2)
        self.addControl(self.labelTitle)
        self.label = xbmcgui.ControlLabel(bgPosX+20, bgPosY+94, bgResW-40, bgResH-40, title, 'font13', '0xFFFFFFFF',  alignment=2)
        self.addControl(self.label)
        
        # create button list
        self.starLeft = bgPosX+40
        self.starTop = bgPosY+136
        for i in range(11):
            if i == 0:
                self.button.append(xbmcgui.ControlButton(self.starLeft, self.starTop, 30, 30, "", focusTexture=__path_img__ + '//star0f.png', noFocusTexture=__path_img__ + '//star0.png'))
            else:
                if i <= self.rating:
                    self.button.append(xbmcgui.ControlButton(self.starLeft+(i*40), self.starTop, 30, 30, "", focusTexture=__path_img__ + '//star2f.png', noFocusTexture=__path_img__ + '//star2.png'))
                else:
                    self.button.append(xbmcgui.ControlButton(self.starLeft+(i*40), self.starTop, 30, 30, "", focusTexture=__path_img__ + '//star2f.png', noFocusTexture=__path_img__ + '//star1.png'))
                
            self.addControl(self.button[i])
        self.setFocus(self.button[self.rating])
        
    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU or action == ACTION_STEP_BACK or action == ACTION_BACKSPACE or action == ACTION_NAV_BACK or action == KEY_BUTTON_BACK or action == ACTION_MOUSE_RIGHT_CLICK:
            self.close()
        if action == ACTION_MOVE_RIGHT or action == ACTION_MOVE_UP:
            if self.rating < 10:
                self.rating = self.rating + 1
            self.setFocus(self.button[self.rating])
        if action == ACTION_MOVE_LEFT or action == ACTION_MOVE_DOWN:
            if self.rating > 0:
                self.rating = self.rating - 1
            self.setFocus(self.button[self.rating])
        
    def onControl(self, control):
        # save tag using JSON
        for i in range(11):
            if control == self.button[i]:
                filmweb.Filmweb().addUserFilmVote(self.filmwebID, str(i), self.userData)
                self.close()
        
window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
if window.getProperty('FilmwebOceny') != 'true':
    GUI()
    window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    window.setProperty('FilmwebOceny', 'false')