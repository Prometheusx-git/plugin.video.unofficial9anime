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
from resources.lib.lists.weblist import WebList
from resources.lib.lists import medialist


class EpisodeList(WebList):
    '''
        Object representation of a show's page, where episodes are displayed.  Special types of 
        show pages should extend this class.
    '''
    def __init__(self):
        WebList.__init__(self)
        self.genres = []
        self.aliases = []
        self.related_links = []
        self.related_data_tips = []
        self.related_media_type_list = []
        self.first_air_date = ''
        self.season = None
        self.num_episodes = 0
        self.id = self._get_bookmark_id(self.url)

    ''' PUBLIC FUNCTIONS '''
    def parse(self):
        helper.start('EpisodeList.parse')
        if self.soup == None:
            return

        servers = self.soup.find_all('div', class_='widget servers')#server row')
        #server_names = map(lambda x: x.label.string, servers)       		
        links_active =	servers[0].find_all('div', class_='server active')
        links_hidden =	servers[0].find_all('div', class_='server hidden')
        links1 = links_active[0].find_all('a')
        links2 = links_hidden[-1].find_all('a')#servers[-2].find_all('a')
        counter1 = len(links1)
        counter2 = len(links2)

        if (counter1 > counter2):
            links = links1		
            #helper.show_error_dialog(['',str(counter1)])			
        else:
            links = links2	
        #helper.show_error_dialog(['',str(links2)])			
        for link in links:	
            link['href'] = link['href'].split('/')[-2] + '!!!!' + link['data-base']		
            #helper.show_error_dialog(['',str(link)])
        #links2 = servers[-1].find_all('a')
        #for link in links2:	
        #    link['href'] = link['href'].split('/')[-2] + '!!!!' + link['data-base']	

        self.links = links
			
        #helper.show_error_dialog(['',str(server)])	
		
        self._parse_show_metadata()
        self.related_links, self.related_data_tips, self.related_media_type_list = self._parse_links_from_grid()

    def add_items(self):
        helper.start('EpisodeList.add_items')
        if self.links == []:
            return

        half_eps = 0
        episodes = []
        for link in self.links:
            num = link['data-base']#.string.strip()
            url = link['href']
            if self.__is_half_episode(num): # 1a and 1b
                half_eps += 1

            episodes.append((num, url))

        self.num_episodes = len(episodes)

        helper.log_debug('We have effectively %d episodes with %d half episodes' % (self.num_episodes, half_eps))

        all_metadata = self.get_metadata(args.base_title)
        helper.log_debug('We have %d metadata entries' % len(all_metadata))
        offset = -1
        for idx, (name, url) in enumerate(episodes):
            if self.__is_half_episode(name):
                offset -= 1
            metadata = all_metadata[int(name)+offset] if int(name)+offset < len(all_metadata) else {'title':name}
            icon, fanart = self._get_art_from_metadata(metadata)
            query = self._construct_query(url, 'qualityPlayer', metadata, media_type=self.media_type)
            cm_items = self._get_contextmenu_items()
            if helper.get_setting('enable-metadata') == 'true':			
                metadata['title'] = '%s - %s' % (name, metadata['title'])
            helper.add_video_item(query, metadata, img=icon, fanart=fanart, contextmenu_items=cm_items)

        self._add_related_links()

        helper.set_content('episodes')
        helper.add_sort_methods(['episode', 'title'])
        helper.end_of_directory()
        helper.end('EpisodeList.add_items')
        return

    def get_metadata(self, name):
        if (helper.get_setting('enable-metadata') == 'false' or 
            (args.imdb_id == None and args.tvdb_id == None)):
            return []
        
        all_metadata = self.meta.get_episodes_meta(name, args.imdb_id, args.tvdb_id, self.num_episodes,
                                                   self.first_air_date, self.season)
        return all_metadata

    ''' PROTECTED FUNCTIONS '''
    def _get_contextmenu_items(self):
        contextmenu_items = [('Show information', 'XBMC.Action(Info)'), ('Queue item', 'XBMC.Action(Queue)')]
        show_queue_query = self._construct_query('', 'showqueue')
        show_queue_context_item = constants.runplugin % helper.build_plugin_url(show_queue_query)
        contextmenu_items.append(('Show queue', show_queue_context_item))
        return contextmenu_items

    def _parse_show_metadata(self):
        # A bunch of show metadata is organized in a table
        metadata_table = self.soup.find('div', class_='widget info').find('dl', class_='meta col-sm-12')
        values = metadata_table.find_all('dd')
        #helper.show_error_dialog(['',str(values)])			
        self.genres = map(lambda x: x.string, values[4].find_all('a'))
        raw_first_air_date = values[2].string.split(' to ')[0].strip()
        self.first_air_date = helper.get_datetime(raw_first_air_date, '%b %d, %Y').strftime("%Y-%m-%d")
        
        media_type_table = {
            u'TV Series': 'tvshow', u'Movie': 'movie', u'OVA': 'special', u'ONA': 'special', u'Special': 'special'
        }
        self.media_type = media_type_table[values[0].string]        

        # Only keep aliases that do not contain CJK (eg, Japanese) characters
        try:
            #tmp_aliases = values[0].string.split('; ')
            alias1 = self.soup.find('div', class_='widget info').find('p', class_='alias')
            tmp_aliases = str(alias1).replace('<p class="alias">','').replace('</p>','')			
            tmp_aliases = tmp_aliases.split('; ')				
            keep_fn = lambda x: ord(x) <= 3000
            self.aliases = filter(lambda y: filter(keep_fn, y), tmp_aliases)
        except:
            # Sometimes there are no aliases
            self.aliases = []
            
    def _add_related_links(self):
        # Add related links using the ML (since they're all just media)
        if len(self.related_links) > 0 and helper.get_setting('related-links') == 'true':
            mlist = medialist.MediaList(None)
            mlist.links = self.related_links
            mlist.media_type_list = self.related_media_type_list
            mlist.data_tips = self.related_data_tips
            mlist.add_items(title_prefix='Related: ')

    def _get_art_for_season0(self):
        # Mainly for specials; maybe it should be moved there
        helper.start('_get_art_for_season0 for name %s and imdb_id %s' % (args.base_title, args.imdb_id))
        if helper.get_setting('enable-metadata') == 'false':
            return None, ''

        season_covers = self.meta.get_seasons(args.base_title, args.imdb_id, ['0'])
        if len(season_covers) > 0:
            icon = season_covers[0]['cover_url']
            fanart = season_covers[0]['backdrop_url']
        else:
            icon = args.icon
            fanart = args.fanart
        return icon, fanart

    ''' PRIVATE FUNCTIONS '''
    def __is_half_episode(self, name):
        import re
        is_half = re.search('([0-9]{1,3}-[Bb])$', name) != None
        return is_half