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
from resources.lib.common.nethelper import net, cookies
import sys, re, os, cookielib, xbmcaddon, xbmcvfs, xbmcgui 

from bs4 import BeautifulSoup

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
     
        #self.soup = BeautifulSoup(self.html, "html.parser") if self.html != '' else None

        self.serverlink = ''
        self.serveridx = 0
        self.serverid = 28		
		
        #serverlistf = helper.get_profile() + 'serverlist.txt'		
        #serverlistfile = xbmcvfs.File(serverlistf)
        #self.serverlist = serverlistfile.read()
        #serverlistfile.close()		
        self.serverlist = xbmcgui.Window(10000).getProperty('serverlist')				

    def determine_quality(self):
        #helper.start('QualityPlayer.determine_quality')
        #helper.show_error_dialog(['',str(self.url)])
        
        #servers = self.soup.find('div', class_='widget servers')#server row')
        servernames = re.findall(r'" data-name=\\"(.*?)\\">(.*?)<',self.serverlist)
        #helper.show_error_dialog(['',str(servers)])			
		
        #serverinfo = servers.find('span', class_='tabs')#['data-name']		
        #servernames = re.findall(r'data-name="(.*?)">(.*?)<', str(serverinfo))
		
        #helper.show_error_dialog(['',str(servernames[1][0])])
        #helper.show_error_dialog(['',str(helper.serverlist)])			

        servername_dialog =[]
        for element in servernames:		
            servername_dialog.append(element[1]) #['MyCloud', 'RapidVideo', 'Openload']  
			
        self.serveridx = helper.present_selection_dialog('Choose the server from the options below', servername_dialog)    
				        
        server = re.findall(r'data-name=\\"..\\"\\n(.*?)<\\\/ul>\\n                            <\\\/div>\\n', self.serverlist)		
        links = re.findall(r'data-base=\\"(.*?)\\"\\n                            data-comment=\\"(.*?)\\"\\n                            \\n                            href=\\"(.*?)">(.*?)<', server[self.serveridx])		
					
        for element in links:
            if (element[1] == self.database): self.serverlink = element[2].replace('\/','/')[0:-1]

        #helper.show_error_dialog(['',str(self.serverlink)])				
		
		
        #if (self.serveridx == 0):
        #    links_active =	servers.find('div', class_='server active')
        #    links1 = links_active.find_all('a')			

        #    for link in links1:
        #        if (link['data-comment'] == self.database): self.serverlist = link['href']
            #helper.show_error_dialog(['',str(self.serverlist)])				
        #else:
        #    links_active =	servers.find_all('div', class_='server hidden')
            #helper.show_error_dialog(['',str(links_active)])
        #    if (self.serveridx == 1):            
        #    links1 = links_active[self.serveridx-1].find_all('a')			
        #    for link in links1:
        #       if (link['data-comment'] == self.database): self.serverlist = link['href']	
		
        #helper.show_error_dialog(['',str(self.serverlist[idx])])			

        links = {} 		
        if (self.serveridx != -1):	
            self.serverid = servernames[self.serveridx][0]		
            links = self.__get_quality_links()
		
        #helper.show_error_dialog(['',str(self.link)])		
        if (links != {} ):
            if helper.get_setting('preset-quality') == 'Individually select':
                quality_options = [item['label'] for item in links]
                idx = helper.present_selection_dialog('Choose the quality from the options below', quality_options)
                if idx != -1:
                    self.link = links[idx]['file'] 				
                    if ('https://storage.googleapis.com' and '.mp4' in str(self.link)) :
                        helper.resolve_url(self.link)
                        self.link = ''					
                    #helper.show_error_dialog(['',str(self.link)])
            else:
                self.link = self.__get_best_link_for_preset_quality(links)
        #helper.end('QualityPlayer.determine_quality')

		
    def __get_quality_links(self):
        # Grab the API token

        ep_id = self.serverlink.split('/')[-1]        		
        ts = re.search('ts=\"(.*?)\"',self.html).group(1) 		
        extra_para = self.__get_extra_url_parameter(ep_id, ts, self.serverid)	
        
		#url = '%s/ajax/episode/info?id=%s&server=%s' % (helper.domain_url(), ep_id, serverid)
        url = '%s/ajax/episode/info?ts=%s&_=%s&id=%s&server=%s' % (helper.domain_url(), ts, extra_para, ep_id, self.serverid)
        #helper.show_error_dialog(['',str(url)])	
        params_url,e = self.net.get_html(url, self.cookies, helper.domain_url())
        #helper.show_error_dialog(['',str(params_url)])	
        ajax_json = {'params' : {'id': '', 'token': '', 'options': ''}, 'type': 'iframe', 'target': ''}
        
        rot8 = re.search('id\"\:\"(.*?)\"',params_url)#.group(1)
        if rot8 != None : ajax_json['params']['id'] = rot8.group(1)

        rot8 = re.search('type\"\:\"(.*?)\"',params_url)	        
        if rot8 != None : ajax_json['type'] = rot8.group(1)	 
		
        rot8 = re.search('token\"\:\"(.*?)\"',params_url)       		
        if rot8 != None : ajax_json['params']['token'] = self.__cusb64_string(rot8.group(1)[1:])	
	
        rot8 = re.search('options\"\:\"(.*?)\"',params_url)		
        if rot8 != None : ajax_json['params']['options'] = self.__cusb64_string(rot8.group(1)[1:])		
        
        rot8 = re.search('target\"\:\"(.*?)\"',params_url)	        
        if rot8 != None : ajax_json['target'] = rot8.group(1)
	
	
        #if helper.handle_json_errors(ajax_json):
        #    return []

        # Grab the links and their corresponding quality

        if (ajax_json['type'] == 'iframe') : 
            target = ajax_json['target'].replace('\/','/')
            #helper.show_error_dialog(['',str(target)])	   
            if not 'http' in target :
                target = target.replace('//','https://')			
            if 'rapidvideo' in target :
                target = target.replace('www.rapidvideo.com/e/','www.rapidvideo.com/?v=')                			
                params_url,e = self.net.get_html( target, self.cookies, helper.domain_url())				
                #params_url,e = self.net.get_html( '%s&q=360p' % target, self.cookies, helper.domain_url())
                quali = re.findall(r'&q=(.*?)"',params_url)
                quali = quali[::-1]				
                quali_choser = helper.present_selection_dialog('Choose the quality from the options below', quali) 
                if ( quali_choser != -1):		
                    params_url,e = self.net.get_html('%s&q=' % target + quali[quali_choser], self.cookies, helper.domain_url())				
                    #helper.show_error_dialog(['',str(quali)])	
                    target = re.search('<source\ssrc=\"([^\"]+)\"\s.+title=\"([^\"]+)\"\s.+?>', params_url).group(1) #',\ssrc: \"([^\"]+?)\"' 
                    helper.resolve_url(target)
                target = ''
            if 'mcloud.to' in target :
                params_url,e = self.net.get_html(target, self.cookies, helper.domain_url())						
                m3u8_list = re.search('file":"(.*?)"',params_url).group(1)					
                params_url,e = self.net.get_html(m3u8_list, self.cookies, target )
                quali = re.findall(r'hls\/(.*?)\/',params_url)
                quali_choser = helper.present_selection_dialog('Choose the quality from the options below', quali)  
                if ( quali_choser != -1):					
                    target_url = m3u8_list.replace('list.m3u8','hls/%s/%s.m3u8|Referer=%s' % (quali[quali_choser],quali[quali_choser],target))
                    helper.resolve_url(target_url)
                target = ''				
				
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


	#Part from DxCx/plugin.video.9anime taken

    def __get_extra_url_parameter(self, id, ts, server):
        DD = '0a9de5a4' 
        params = [('id', str(id)), ('ts', str(ts)), ('server', str(server))]

        o = self.__s(DD)
        #helper.show_error_dialog(['',str(o)])		
        for i in params:
            o += self.__s(self.__a(DD + i[0], i[1]))
        #helper.show_error_dialog(['',str(o)])        
        return o 

    def __s(self, t):
        i = 0
        for (e, c) in enumerate(t):
            i += ord(c) + e 
        return i

    def __a(self, t, e):
        n = 0
        for i in range(max(len(t), len(e))):
            n *= ord(e[i]) if i < len(e) else 8
            n *= ord(t[i]) if i < len(t) else 8
        #helper.show_error_dialog(['',str(n)])
        return format(n, 'x')  # convert n to hex string		
		
