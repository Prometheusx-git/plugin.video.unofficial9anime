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
from resources.lib.metadata import metadatahandler
from resources.lib.common import nethelper
from bs4 import BeautifulSoup

class WebList(object):
    '''
        Base object representation of a webpage on 9anime.  Other classes should extend this class
        to represent a web page.
        
        The main components of this class are the __init__, parse, and add_items methods.  The 
        first grabs the HTML, the second parses it, and the third adds it with any metadata to a 
        list to be displayed by Kodi.

        Other functions included are shared among child classes.
    '''
    def __init__(self, url_val=args.value, form_data=None):
        self.html = ''
        self.soup = None
        self.links = []
        self.has_next_page = False


        self.meta = metadatahandler.meta
        self.net, self.cookies = nethelper.net, nethelper.cookies

        if not url_val:
            return

        self.url = url_val if 'http' in url_val else (helper.domain_url() + url_val)	
        self.html, e = self.net.get_html(self.url, self.cookies, helper.domain_url(), form_data)
        self.html = helper.handle_html_errors(self.html, e)
        helper.log_debug('HTML length: %s' % len(self.html))
 
        self.soup = BeautifulSoup(self.html, "html.parser") if self.html != '' else None

    def parse(self):
        pass

    def add_items(self):
        pass

    def get_metadata(self):
        pass

    def clean_name(self, name, specials=True):
        cleaned_name = name.replace(' (Sub)', '').replace(' (Dub)', '')
        if specials:
            cleaned_name = cleaned_name.replace(' (OVA)', '').replace(' Specials ', '').replace(' OVA ', ' ')
            cleaned_name = self._strip_by_re(cleaned_name, '( OVA)$', end=-4)
            cleaned_name = self._strip_by_re(cleaned_name, '( Special)$', end=-8)
            cleaned_name = self._strip_by_re(cleaned_name, '( Specials)$', end=-9)
        cleaned_name = self._strip_by_re(cleaned_name, '( \(1080p\))$', end=-8)
        cleaned_name = self._strip_by_re(cleaned_name, '( \((720|480|360)p\))$', end=-8)
        return cleaned_name

    ''' PROTECTED FUNCTIONS '''
    def _get_bookmark_id(self, url):
        return url.split('.')[-1].split('?')[0]

    def _get_art_from_metadata(self, metadata):
        icon = metadata.get('cover_url', args.icon)
        fanart = metadata.get('backdrop_url', args.fanart)
        return (icon, fanart)

    def _construct_query(self, value, action, metadata={}, full_title='', media_type=''):
        icon, fanart = self._get_art_from_metadata(metadata)
        base_title = metadata.get('title', '')
        imdb_id = metadata.get('imdb_id', '')
        tvdb_id = metadata.get('tvdb_id', '')
        tmdb_id = metadata.get('tmdb_id', '')
        query = {'value':value, 'action':action, 'imdb_id':imdb_id, 
                 'tvdb_id':tvdb_id, 'tmdb_id':tmdb_id, 'icon':icon, 'fanart':fanart,
                 'base_title':base_title, 'full_title':full_title, 'media_type':media_type}
        return query

    def _parse_links_from_grid(self, subcontainer_attrs=None):
        ''' 9anime often organizes a page of shows in a grid called list-film '''

        if subcontainer_attrs:
            listfilm = self.soup.find('div', attrs=subcontainer_attrs)
        #helper.show_error_dialog(['',str(listfilm)])			
		
        listfilm = self.soup.find('div', class_='film-list')	
        links = listfilm.find_all('a', class_='poster')
        data_tips = links #listfilm.find_all('a', class_='poster')
        #helper.show_error_dialog(['',str(data_tips)])		
        items = listfilm.find_all('div', class_='item')
        media_type_list = []
        for item in items:
            if item.find('div', class_='movie'):
                media_type_list.append('movie')
            elif item.find('div', class_='ova') or item.find('div', class_='type ona') or \
                item.find('div', class_='special'):
                media_type_list.append('special')
            elif item.find('div', class_='preview'):
                media_type_list.append('preview')
            else:
                media_type_list.append('tvshow')

        return links, data_tips, media_type_list
    
    # This may belong somewhere else...
    def _strip_by_re(self, string, filter, end, start=0):
        import re
        return string[start:end] if re.search(filter, string) != None else string