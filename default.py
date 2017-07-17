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


import time
t_start = time.time()

from resources.lib.common.helper import helper
from resources.lib.common.args import args
from resources.lib.common import controller
import dat1guy.shared.timestamper as t_s
t_s.timestamps_on = helper.debug_timestamp()

timestamper = t_s.TimeStamper('default.py', t0=t_start, t1_msg='Default imports')
helper.location("Default entry point, version %s" % helper.get_version())

if helper.debug_import():
    from resources.lib.appdata import account, lastvisited
    from resources.lib.common import constants, nethelper
    from resources.lib.lists import episodelist, locallist, medialist, movielist, specialslist, trendinglist, upcominglist, watchlist
    from resources.lib.metadata import metadatafinder, metadatahandler
    from resources.lib.metadata.metadatahandler import meta
    from resources.lib.players import videoplayer, qualityplayer
    timestamper.stamp('Importing everything else')

control_table = {
    None:                lambda c: c.main_menu(),
    'localList':         lambda c: c.show_local_list(),
    'sortList':          lambda c: c.show_sort_list(),
    'watchList':         lambda c: c.show_watch_list(),
    'mediaList':         lambda c: c.show_media_list(),
    'trendingList':      lambda c: c.show_trending_list(),
    'upcomingList':      lambda c: c.show_upcoming_list(),
    'episodeList':       lambda c: c.show_episode_list(),
    'qualityPlayer':     lambda c: c.choose_quality_play_video(),
    'search':            lambda c: c.search(),
    'findmetadata':      lambda c: c.find_metadata(),
    'clearmetadata':      lambda c: c.clear_metadata(),	
    'lastvisited':       lambda c: c.show_last_visited(),
    'account':           lambda c: c.account_login_logout(),
    'addBookmark':       lambda c: c.add_bookmark(),
    'removeBookmark':    lambda c: c.remove_bookmark(),
    'showqueue':         lambda c: helper.show_queue(),
    'settings':          lambda c: helper.show_settings()
}

if control_table.has_key(args.action):
    control_table[args.action](controller.Controller())
else:
    helper.log_error("WHAT HAVE YOU DONE?")
    helper.show_error_dialog(['Something went wrong.  Please restart the addon.'])

helper.location("Default exit point")
timestamper.stamp_and_dump('All non-imported execution')