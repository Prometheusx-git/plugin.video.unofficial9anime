# -*- coding: utf-8 -*-
'''
    The Unofficial Plugin for 9anime, aka UP9anime - a plugin for Kodi
    Copyright (C) 2016 dat1guy

    This file is part of UP9anime.

    UP9anime is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    UP9anime is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with UP9anime.  If not, see <http://www.gnu.org/licenses/>.
'''


# Huge shoutout to https://github.com/Aerol/plugin.video.9anime/ for the parse function


from resources.lib.common.helper import helper
from resources.lib.common.args import args
from resources.lib.players.videoplayer import VideoPlayer
import sys, re, os, cookielib, xbmcaddon 
from resources.lib.common.nethelper import net, cookies

Addon = xbmcaddon.Addon(id='plugin.video.unofficial9anime') 
sys.path.append(os.path.join(Addon.getAddonInfo('path'), r'resources', r'lib'))

#if not 'nodejs' in os.environ["PATH"] :
#    os.environ["PATH"]="/storage/nodejs/bin:"+os.environ["PATH"]

#import execjs
#execjs.eval("{a:true,b:function (){}}")

#import requests

class QualityPlayer(VideoPlayer):
    def __init__(self):
        VideoPlayer.__init__(self)      
        self.net, self.cookies = net, cookies
        self.url = '/watch/' + args.value.split('!!!!')[0]
        self.database = args.value.split('!!!!')[-1]		
		
        self.html = ''
        self.html, e = self.net.get_html(helper.domain_url() + self.url, self.cookies, helper.domain_url())
        self.html = helper.handle_html_errors(self.html, e)
     
        from bs4 import BeautifulSoup
        self.soup = BeautifulSoup(self.html, "html.parser") if self.html != '' else None

        self.serverlist = {}
        self.serveridx = 0
        self.serverid = {}		

    def determine_quality(self):
        helper.start('QualityPlayer.determine_quality')
        #helper.show_error_dialog(['',str(args.value)])
        
        servers = self.soup.find_all('div', class_='server row')
        servernames = []       
        i=0	
		
        while i < len(servers):	
            self.serverid[i] = servers[i]['data-id'] 		
            server = servers[i].find_all('a')	
            servernames = servernames + [servers[i].find('label').get_text()]
            for link in server:
                if (link['data-base'] == self.database): self.serverlist[i] = link['href']
            i = i + 1						
        i=0
		
        self.serveridx = helper.present_selection_dialog('Choose the server from the options below', servernames)        
		
        #helper.show_error_dialog(['',str(self.serverlist[idx])])			
		
        links = self.__get_quality_links()
        #helper.show_error_dialog(['',str(self.link)])		
        if (links != {} ):
            if helper.get_setting('preset-quality') == 'Individually select':
                quality_options = [item['label'] for item in links]
                idx = helper.present_selection_dialog('Choose the quality from the options below', quality_options)
                if idx != -1:
                    self.link = links[idx]['file'] 
                    #redirect = requests.head( self.link , allow_redirects=True)
                    #self.link = redirect.url
                    #helper.show_error_dialog(['',str(redirect.url)])
                    #if ('302' in str(redirect.history) ) :					
                    #    helper.resolve_url(redirect.url)
                    #    self.link = ''						
                    #if ('https://storage.googleapis.com' and '.mp4' in str(self.link)) :
                    #    helper.resolve_url(self.link)
                    #    self.link = ''					
                    #helper.show_error_dialog(['',str(self.link)])
            else:
                self.link = self.__get_best_link_for_preset_quality(links)
        helper.end('QualityPlayer.determine_quality')

		
    def __get_quality_links(self):
        # Grab the API token
        
        #token, e = self.net.get_html(helper.domain_url() +'/token?v1', self.cookies, helper.domain_url())

        #token = token.decode('utf-8')
        #token = token.split(';')[1]
        #funname = token[0]
        #token = token.replace(',0',';')		
		
        #js = 'var start=""; %s=function(mm){return start+=String.fromCharCode(mm)};' %funname#'var document = this; this.location = "https://9anime.to"; var jscookie = %s;'
        #ctx = execjs.compile(js)
        #rk1 = ctx.exec_('return '+token)

        ##helper.show_error_dialog(['',str(rk1)])			
		
        #ck = cookielib.Cookie(version=0, name='reqkey', value=rk1, port=None, port_specified=False,
		#domain=helper.domain(), domain_specified=False, domain_initial_dot=False, 
		#path='/', path_specified=True, secure=False, expires=None, discard=False, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)		
        
        ##self.net._cj.clear(helper.domain(),'/','reqkey')
        
        #self.net._cj.set_cookie(ck)
        #self.net.save_cookies(self.cookies)
				
		##helper.set_setting('reqkey', reqkey)
        ##helper.show_error_dialog(['',str(rk)])	

        ep_id = self.serverlist[self.serveridx].split('/')[-1] #args.value.split('/')[-1]        		
        ts_encode = re.search('ts=\"(.*?)\"',self.html).group(1) 
        ts = self.__ts_decode(ts_encode)

        serverid = self.serverid[self.serveridx]
        extra_para = self.__get_extra_url_parameter(ep_id, 0, ts, serverid)	
		
        url = '%s/ajax/episode/info?ts=%s&_=%s&id=%s&server=%s' % (helper.domain_url(), ts, extra_para, ep_id, serverid)
        url = url+'&update=0'
        #url = 'https://9anime.is/ajax/episode/info?ts=1511679600&_=2718&id=wnzwz7&server=22&update=0'	
        #helper.show_error_dialog(['',str(extra_para)])		
        params_url,e = self.net.get_html(url, self.cookies, helper.domain_url())

        #params_url = params_url.replace('.','')
        #helper.show_error_dialog(['',str(params_url)])		
        #import simplejson
        #ajax_json = simplejson.loads(params_url)
        ajax_json = {'params' : {'id': '', 'token': '', 'options': ''}, 'type': '', 'target': ''}
        
        rot8 = re.search('id\"\:\"(.*?)\"',params_url).group(1)
        ajax_json['params']['id'] = rot8
        rot8 = re.search('type\"\:\"(.*?)\"',params_url).group(1)		        
        ajax_json['type'] = rot8 
		
        rot8 = re.search('token\"\:\"(.*?)\"',params_url)       		
        if rot8 != None : ajax_json['params']['token'] = self.__cusb64_string(rot8.group(1)[1:])	
	
        rot8 = re.search('options\"\:\"(.*?)\"',params_url)		
        if rot8 != None : ajax_json['params']['options'] = self.__cusb64_string(rot8.group(1)[1:])		
        
        rot8 = re.search('target\"\:\"(.*?)\"',params_url)	        
        if rot8 != None : ajax_json['target'] = self.__cusb64_string(rot8.group(1)[1:])

		
        #helper.show_error_dialog(['',str(ajax_json)])		
	
        #ajax_json = self.net.get_json(url, self.cookies, helper.domain_url(), {})

        if helper.handle_json_errors(ajax_json):
            return []

        # Grab the links and their corresponding quality

        if (ajax_json['type'] == 'iframe') : 
            target = ajax_json['target'].replace('\/','/')
            if not 'http' in target :
                target = target.replace('//','https://')			
            self.link = target
            links = {} 			
			#helper.show_error_dialog(['',str(target)])
        else:		
            vid_id = ajax_json['params']['id']
            token = ajax_json['params']['token']
            options = ajax_json['params']['options']
		
            grab_url = '%s/grabber-api/?id=%s&token=%s&options=%s' % (helper.domain_url(), vid_id, token, options)
            json = self.net.get_json(grab_url, self.cookies, helper.domain_url(), {})
            #helper.show_error_dialog(['',str(json)])
            if helper.handle_json_errors(json):
                return []

            links = json['data']
            links.reverse()
        return links

    def __get_best_link_for_preset_quality(self, links):
        preset_quality = int(helper.get_setting('preset-quality').strip('p'))        
        url_to_play = None
        for item in links:
            quality = item['label']
            if preset_quality >= int(quality.strip('p')):
                helper.log_debug('Found media to play at matching quality: %s' % quality)
                url_to_play = item['file']
                break

        if url_to_play == None:
            helper.log_debug('No matching quality found; using the lowest available')
            url_to_play = links[-1]['file']
        
        return url_to_play

    def __get_extra_url_parameter(self, id, update, ts, server):
        DD = 'gIXCaNh'		
        params = [('id', str(id)), ('update', str(update)), ('ts', str(ts)), ('server', str(server))]
        o = self.__s(DD)
        for i in params:
            o += self.__s(self.__a(DD + i[0], i[1]))
        return o 

    def __s(self, t):
        i = 0
        for (e, c) in enumerate(t):
            i += ord(c) * e 
        return i

    def __a(self, t, e):
        n = 0
        for i in range(max(len(t), len(e))):
            n += ord(e[i]) if i < len(e) else 0
            n += ord(t[i]) if i < len(t) else 0
        return format(n, 'x')  # convert n to hex string		
		
    def __ts_decode(self,ts):
        firstCharMap = []
        secondCharMap = []
        for n in range(65, 91):
            firstCharMap.append(chr(n))
            if n % 2 != 0:
                secondCharMap.append(chr(n))
        for n in range(65, 91):
            if n % 2 == 0:
                secondCharMap.append(chr(n))

        result = ""
        for i in range(len(ts)):
            charReplaced = False
            for y in range(len(secondCharMap)):
                if ts[i] == secondCharMap[y]:
                    result += firstCharMap[y]
                    charReplaced = True
                    break
            if not charReplaced:
                result += ts[i]
        real_ts = result.decode('base64')
        return real_ts

    def __cusb64_string(self, content):
        from string import ascii_lowercase as lc, ascii_uppercase as uc, maketrans	
        _CUSB64_MAP_TABLE = [i for i in lc if ord(i) % 2 != 0] + [i for i in lc if ord(i) % 2 == 0]
        decoded = ""
        for c in content:
            replaced = False
            if c not in _CUSB64_MAP_TABLE:
                decoded += c
                continue
            decoded += lc[_CUSB64_MAP_TABLE.index(c)]

        missing_padding = len(decoded) % 4
        if missing_padding:
            decoded += b'=' * (4 - missing_padding)
        return decoded.decode("base64")
 
		
		