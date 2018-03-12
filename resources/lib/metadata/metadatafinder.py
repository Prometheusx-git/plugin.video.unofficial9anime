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


from resources.lib.common.args import args
from resources.lib.common.helper import helper


class MetadataFinder(object):
    '''
        Allows the user to fix metadata for a given piece of media.  It does this by allowing the
        user to input a search query, and then updating metadata for the piece of media if any
        results are found.
    '''
    def __init__(self):
        helper.show_busy_notification()
        from resources.lib.metadata.metadatahandler import meta
        from resources.lib.lists import episodelist
        self.meta = meta
        self.ep_list = episodelist.EpisodeList()
        self.ep_list.parse()
        self.options = ['Manual search', args.base_title] + self.ep_list.aliases
        helper.close_busy_notification()

    def search_and_update(self):
        # Grab the search string from the user
        while True:
            idx = helper.present_selection_dialog('Choose a title to search for', self.options)
            helper.log_debug('User selected index %d' % idx)
            if idx == -1:
                helper.show_small_popup('Cancelled attempt to fix metadata')
                return

            default_text = self.options[idx] if idx != 0 else ''
            search_string = helper.get_user_input('Type the show to find metadata for', default_text)
            if search_string == None:
                helper.log_debug('User cancelled manual metadata search')
                return
            elif not search_string:
                helper.show_ok_dialog(['Invalid search query.  Please try again'])
            else:
                break

        helper.show_busy_notification()

        # Grab the metadata
        from resources.lib.lists import medialist
        mlist = medialist.MediaList(None)
        metadata, media_type = mlist.get_metadata(search_string, self.ep_list.media_type)
        if media_type == 'special':
            media_type = 'tvshow'
        helper.log_debug('search and update media type: %s' % media_type)

        # Grab the ID and the actual title, which might have gotten stripped of
        # the year because of a mismatch...
        if media_type == 'movie':
            tmdb_id = metadata.get('tmdb_id', '')
            actual_title = mlist.clean_name(args.full_title)
        else:
            tmdb_id = metadata.get('tvdb_id', '')
            actual_title = mlist.clean_tv_show_name(mlist.clean_name(args.full_title))

        helper.log_debug('Metadatafinder results: %s, %s, %s' % (tmdb_id, media_type, metadata))
        if tmdb_id:
            helper.log_debug('Found metadata from search for %s; refreshing the page' % args.base_title)
            helper.show_small_popup(msg='Updating show with newly found metadata...')
            self.meta.update_meta(media_type, actual_title, imdb_id='', new_tmdb_id=tmdb_id, new_imdb_id=metadata.get('imdb_id'))
            helper.refresh_page()
        else:
            helper.show_ok_dialog(['Did not find any metadata from the search query.  Please try again.'])
        helper.close_busy_notification()