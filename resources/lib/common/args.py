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


def __init():
    return Args()


class Args(object):
    '''
        A wrapper around the parameters to the add-on.
    '''
    def __init__(self):
        params = dict(helper.queries)
        helper.location('Here are the params: %s' % str(params))
        self.__init_helper(params)

    def override(self, queries):
        self.__init_helper(queries)

    def __init_helper(self, queries):
        self.action = queries.get('action', None)
        self.value = queries.get('value', None)
        self.icon = queries.get('icon', None)
        self.fanart = queries.get('fanart', None)
        self.base_title = queries.get('base_title', None)
        self.full_title = queries.get('full_title', None)
        self.imdb_id = queries.get('imdb_id', None)
        self.tvdb_id = queries.get('tvdb_id', None)
        self.tmdb_id = queries.get('tmdb_id', None)
        self.media_type = queries.get('media_type', None)


args = __init()