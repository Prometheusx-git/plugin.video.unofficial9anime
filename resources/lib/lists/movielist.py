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


from resources.lib.common.helper import helper
from resources.lib.common.args import args
from resources.lib.lists.episodelist import EpisodeList


class MovieList(EpisodeList):
    '''
        Object representation of a movie's page.
    '''
    def __init__(self, episode_list=None, mismatch=False):
        if not episode_list:
            EpisodeList.__init__(self)
            self.mismatch = mismatch
        else:
            # Most likely the mismatch path (ie, categorized as a TV show by accident or by guessing)
            self.html = episode_list.html
            self.soup = episode_list.soup
            self.links = episode_list.links
            self.genres = episode_list.genres
            self.aliases = episode_list.aliases
            self.first_air_date = episode_list.first_air_date
            self.season = episode_list.season
            self.num_episodes = episode_list.num_episodes
            self.related_links = episode_list.related_links
            self.related_data_tips = episode_list.related_data_tips
            self.related_media_type_list = episode_list.related_media_type_list
            self.mismatch = mismatch
            from resources.lib.metadata.metadatahandler import meta
            self.meta = meta
            from resources.lib.common.nethelper import net, cookies
            self.net, self.cookies = net, cookies

    ''' PUBLIC FUNCTIONS '''
    def add_items(self):
        helper.start('MovieList.add_items')
        helper.set_content('movies')

        for link in self.links:
            num = link.string.strip()
            url = link['href']
            # for now, assume media_type is always movie; ignore self.mismatch
            metadata = self.get_metadata(args.base_title)
            query = self._construct_query(url, 'qualityPlayer', metadata)
            #if helper.get_setting('enable-metadata') == 'true':			
            #    metadata['title'] = '%s - %s' % (name, metadata['title'])
            if (query['base_title'] == ''):
                query['base_title'] = args.base_title
            #helper.show_error_dialog(['',str(query)])	            			
            helper.add_video_item(query, metadata, img=args.icon, fanart=args.fanart, contextmenu_items=self._get_contextmenu_items())

        self._add_related_links()

        helper.end_of_directory()
        helper.end('MovieList.add_items')
        return

    def get_metadata(self, name):
        if helper.get_setting('enable-metadata') == 'false':
            return {}

        # If we have no previous metadata, and this isn't a mismatch, then
        # we've already had a legitimate try with no luck.
        if not self.mismatch and (args.imdb_id == None and args.tmdb_id == None):
            helper.log_debug('Not a mismatch and no previous results for movie')
            return {}
        
        imdb_id = args.imdb_id if args.imdb_id and not self.mismatch else ''
        tmdb_id = args.tmdb_id if args.tmdb_id and not self.mismatch else ''
        should_update = self.mismatch
        metadata = self.meta.get_meta('movie', name, imdb_id, tmdb_id, update=should_update)

        # Delete mismtached entries from the tv show cache, since they're not tv shows
        if self.mismatch:
            self.meta.update_meta_to_nothing('tvshow', name)
            helper.log_debug('Movie mismatch - new meta: %s' % str(self.meta))

        return metadata