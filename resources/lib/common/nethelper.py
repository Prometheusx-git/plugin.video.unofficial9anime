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


import os, xbmcvfs
from dat1guy.shared.nethelper import NetHelper
from resources.lib.common.helper import helper


def __init():
    '''
        Contains all network related functionality.
    '''
    cookies = helper.get_profile() + 'cookies.txt'
    net = NetHelper(cookies, False)

    # Make sure the cookies exist
    if not os.path.exists(cookies):
        cookiesfile = xbmcvfs.File(cookies, 'w')
        cookiesfile.close()

    return net, cookies

net, cookies = __init()