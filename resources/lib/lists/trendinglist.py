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
from resources.lib.lists.medialist import MediaList


class TrendingList(MediaList):
    '''
        Object representation of a page of trending media.
    '''
    ''' PUBLIC FUNCTIONS '''
    def parse(self):
        if self.soup == None:
            return
        helper.start('TrendingList.parse')
        attrs = {'data-name': 'trending'}
        self.links, self.data_tips, self.media_type_list = self._parse_links_from_grid(attrs)
        helper.end('TrendingList.parse')        