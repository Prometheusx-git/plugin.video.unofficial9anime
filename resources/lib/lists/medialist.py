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
import dat1guy.shared.timestamper as t_s
from dat1guy.shared import threadpool

class MediaList(WebList):
    '''
        Object representation of a page of shows (aka media).  Special types of pages of shows 
        should extend this class.
    '''
    def __init__(self, url_val=args.value, form_data=None):
        timestamper = t_s.TimeStamper('MediaList.init')
        WebList.__init__(self, url_val, form_data)
        self.has_next_page = False
        self.data_tips = []
        self.media_type_list = []
        timestamper.stamp_and_dump()

    ''' PUBLIC FUNCTIONS '''
    def parse(self):
        if self.soup == None:
            return

        helper.start('MediaList.parse')
        timestamper = t_s.TimeStamper('MediaList.parse')
        self.links, self.data_tips, self.media_type_list = self._parse_links_from_grid()
        helper.log_debug('# of links found with class=name: %d' % len(self.links))
        self._find_next_page_link()
        helper.end('MediaList.parse')
        timestamper.stamp_and_dump()

    def worker(self, tuple):
        (idx, link) = tuple					
        name , url = link.find('img', alt=True)['alt'], link['href'] 		
        #name, url = link.string.strip(), link['href']
        #helper.show_error_dialog(['',str(name)])	
        metadata, media_type = self.get_metadata(name, self.media_type_list[idx])
        self.links_with_metadata[idx] = (name, url, metadata, media_type)

    def add_items(self, title_prefix=None):
        helper.start('MediaList.add_items')
        timestamper = t_s.TimeStamper('MediaList.add_items')
        end_dir = (title_prefix == None)
        title_prefix = title_prefix if title_prefix else ''
        if end_dir:
            helper.set_content('tvshows')
        mlinks = self.links[:-1] if self.has_next_page else self.links
        #helper.show_error_dialog(['',str(self.links)])
        # Grabbing metadata is a huge bottleneck, so grabbing it in parallel speeds up things
        self.links_with_metadata = [None] * len(mlinks)
        if helper.debug_metadata_threads():
            map(lambda x: self.worker(x), enumerate(mlinks))#mc_links)		
        else:
            pool = threadpool.ThreadPool(4)
            pool.map(self.worker, enumerate(mlinks))
            pool.wait_completion()
            #for link in mlinks:
            #    name = 	link['href'].split('/')[-1].split('.')[0].replace('-',' ')
            #    url = link['href']				
            #helper.show_error_dialog(['',str(name)])					
        timestamper.stamp('Grabbing metadata with threads')
        #helper.show_error_dialog(['',str(self.links_with_metadata)])

        try:		
            for (name, url, metadata, media_type) in self.links_with_metadata:
                icon, fanart = self._get_art_from_metadata(metadata)
                query = self._construct_query(url, 'episodeList', metadata, name, media_type)
                contextmenu_items = self._get_contextmenu_items(url, name, metadata, media_type)
                metadata['title'] = title_prefix + name # adjust title for sub and dub
                helper.add_directory(query, metadata, img=icon, fanart=fanart, contextmenu_items=contextmenu_items, total_items=len(mlinks))
        except: pass
        self._add_next_page_link()

        if end_dir:
            helper.end_of_directory()
        timestamper.stamp_and_dump('Adding all items')
        helper.end('MediaList.add_items')

    def get_metadata(self, name, media_type):
        if helper.get_setting('enable-metadata') == 'false' or name == 'Next':
            return {},  ''
        helper.start('MediaList.get_metadata - name: %s, media_type: %s' % (name, media_type))

        name_for_movie_search = self.clean_name(name)
        name_for_tv_search = self.clean_tv_show_name(name_for_movie_search)

        metadata = {}
        if media_type == 'tvshow' or media_type == 'special' or media_type == 'preview':
            metadata = self.meta.get_meta('tvshow', name_for_tv_search)
            if metadata['tvdb_id'] == '':
                # If tvshow search failed, and if there was a year in the name, try tv without it
                import re
                if re.search('( \([12][0-9]{3}\))$', name_for_tv_search) != None:
                    metadata = self.meta.get_meta('tvshow', name_for_tv_search[:-7], update=True)
                    if metadata['imdb_id'] != '':
                        metadata = self.meta.update_meta('tvshow', name_for_tv_search, imdb_id='', new_imdb_id=metadata['imdb_id'])
            if metadata['tvdb_id'] != '' and media_type == 'preview':
                media_type = 'tvshow'
            helper.log_debug('Metadata for show %s: %s' % (name_for_tv_search, metadata))
        
        if media_type == 'movie' or media_type == 'preview':
            metadata = self.meta.get_meta('movie', name_for_movie_search)
            if metadata['tmdb_id'] != '' and media_type == 'preview':
                media_type = 'preview'
            helper.log_debug('Metadata for movie %s: %s' % (name_for_movie_search, metadata))

        helper.end('MediaList.get_metadata')
        return metadata, media_type

    def clean_tv_show_name(self, name):
        cleaned_name = name.replace(' (TV)', '').replace(' Second Season', '').replace(' 2nd Season', '')
        cleaned_name = self._strip_by_re(cleaned_name, '( Season [0-9])$', end=-9)
        cleaned_name = self._strip_by_re(cleaned_name, '( S[0-9])$', end=-3)
        cleaned_name = self._strip_by_re(cleaned_name, '( II)$', end=-3)
        cleaned_name = self._strip_by_re(cleaned_name, '( [0-9])$', end=-2)
        return cleaned_name

    ''' PROTECTED FUNCTIONS '''
    def _get_contextmenu_items(self, url, name, metadata, media_type):
        contextmenu_items = [('Show information', 'XBMC.Action(Info)')]

        # Queueing shows with related links on means that Kodi will try to queue those related
        # link folders and fail, and will continue to do so in an infinite loop
        if helper.get_setting('related-links') == 'false':
            contextmenu_items.append(('Queue item', 'XBMC.Action(Queue)'))
            show_queue_query = self._construct_query('', 'showqueue')
            show_queue_context_item = constants.runplugin % helper.build_plugin_url(show_queue_query)
            contextmenu_items.append(('Show queue', show_queue_context_item))

        find_metadata_query = self._construct_query(url, 'findmetadata', metadata, name)
        find_metadata_context_item = constants.runplugin % helper.build_plugin_url(find_metadata_query)
        find_or_fix = ('Find' if self.meta.is_metadata_empty(metadata, media_type) else 'Fix') + ' metadata'
        contextmenu_items.append((find_or_fix, find_metadata_context_item))

        #clear_metadata_query = self._construct_query(url, 'clearmetadata', metadata, name, media_type )		
        #cm_item = constants.runplugin % helper.build_plugin_url(clear_metadata_query)		
        #contextmenu_items.append(('Clear Metadata', cm_item))
		
        id = self._get_bookmark_id(url)
        query = self._construct_query(id, 'addBookmark', metadata, name, media_type)
        cm_item = constants.runplugin % helper.build_plugin_url(query)
        contextmenu_items.append(('Add bookmark', cm_item))

        return contextmenu_items

    def _find_next_page_link(self):        
        paging_section = self.soup.find('div', class_='paging')
        if paging_section != None:
            next_page_link = paging_section.find('a', class_='btn btn-lg btn-primary pull-right ')
            if next_page_link:
                self.links.append(next_page_link)
                self.has_next_page = True

    def _add_next_page_link(self, list_type='mediaList'):
        if self.has_next_page:
            next_link = '/%s' % self.links[-1]['href']
            query = self._construct_query(next_link, list_type)
            helper.add_directory(query, {'title': 'Next'})

