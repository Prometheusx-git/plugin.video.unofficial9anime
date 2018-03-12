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


class SpecialsList(EpisodeList):
    '''
        Object representation of a page of specials/OVAs/ONAs, where episodes are displayed.
    '''
    ''' PUBLIC FUNCTIONS '''
    def add_items(self):
        helper.start('SpecialsList.add_items')
        helper.set_content('episodes')

        icon, fanart = self._get_art_for_season0()

        for link in self.links:
            num = link.string.strip()
            url = link['href']
            metadata = self.get_metadata(args.base_title + ' - ' + num)
            query = self._construct_query(url, 'qualityPlayer', metadata)
            helper.add_directory(query, metadata, img=args.icon, fanart=args.fanart, contextmenu_items=self._get_contextmenu_items())

        self._add_related_links()

        helper.end_of_directory()
        helper.end('SpecialsList.add_items')
        return

    def get_metadata(self, show_name):
        return {'title': show_name}