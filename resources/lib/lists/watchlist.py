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


from resources.lib.common import constants
from resources.lib.common.args import args
from resources.lib.common.helper import helper
from resources.lib.lists.medialist import MediaList


class WatchList(MediaList):
    '''
        Object representation of a user's watch list.
    '''
    def __init__(self):	
        watch_list_c = constants.watch_list
        if ('/user/watchlist') in args.value:
		    watch_list_c = args.value
		#helper.show_error_dialog(['',watch_list_c])
        MediaList.__init__(self, watch_list_c)

        list_type_values = {}
        for (title, query) in constants.submenu_watchlist:
            list_type_values[title] = query['value']

        # If preset_list_type is Select, then we'll default to what the user selected (args.value)
        preset_list_type = helper.get_setting('watch-list-type')
        self.list_type = list_type_values.get(preset_list_type, args.value)
        if ('folder=planned') in args.value:
            self.list_type = 'planned'
        if ('folder=all') in args.value:
            self.list_type = 'all'
        if ('folder=on-hold') in args.value:
            self.list_type = 'onhold'
        if ('folder=completed') in args.value:
            self.list_type = 'watched'			
        if ('folder=watching') in args.value:
            self.list_type = 'watching'
        if ('folder=dropped') in args.value:
            self.list_type = 'dropped'			
			
    ''' PUBLIC FUNCTIONS '''
    def parse(self):
        if self.soup == None:
            return
        helper.start('WatchList.parse with list_type %s' % self.list_type)	
        watchlist_container = self.soup.find('div', class_='widget watchlist').\
            find('div', attrs={'data-name':self.list_type})
        if watchlist_container == None:
            helper.end('WatchList.parse - watch list is empty')
            return
        #helper.show_error_dialog(['',str(watchlist_container)])
        link_containers = watchlist_container.find_all('div', class_='item '+ self.list_type)
        self.links = [container.find('a') for container in link_containers]
        self.media_type_list = ['preview'] * len(self.links)
        self._find_next_page_link()        
        helper.end('WatchList.parse')

    ''' PROTECTED FUNCTIONS '''
    def _get_contextmenu_items(self, url, name, metadata, media_type):
        # Append remove bookmark context menu item
        items = MediaList._get_contextmenu_items(self, url, name, metadata, media_type)
        id = self._get_bookmark_id(url)
        query = self._construct_query(id, 'removeBookmark', metadata, name, media_type)
        cm_item = constants.runplugin % helper.build_plugin_url(query)
        items.append(('Remove bookmark', cm_item))

        # Change 'Add bookmark' to move
        (add_title, query) = items[2]
        if (add_title == 'Add bookmark'):
            items[2] = ('Move bookmark', query)
        else:
            (add_title, query) = items[4]
            if (add_title == 'Add bookmark'):
                items[4] = ('Move bookmark', query)			
        return items

    def _find_next_page_link(self):        
        paging_section = self.soup.find_all('div', class_='paging')
        if paging_section != None:
            if (self.list_type == 'all'): 
                sec = 0
            elif (self.list_type == 'watching'): 
                sec = 1	
            elif (self.list_type == 'watched'): 
                sec = 2	
            elif (self.list_type == 'onhold'): 
                sec = 3	
            elif (self.list_type == 'dropped'): 
                sec = 4	
            elif (self.list_type == 'planned'): 
                sec = 5					
            #helper.show_error_dialog(['',str(paging_section[2])])           
            pages = paging_section[sec].find_all('a')
            for link in pages:		
            #helper.show_error_dialog(['',pages[0].get_text()])	
                    next_link = '/%s' % link["href"]
                    query = self._construct_query(next_link,'watchList')
                    helper.add_directory(query, {'title': link.get_text()})

				