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


from collections import OrderedDict


plugin_name = 'plugin.video.unofficial9anime'
runplugin = 'XBMC.RunPlugin(%s)'
appdata_cache_path = 'appdata.db'
watch_list = '/user/watchlist'

# Most lists on 9anime can be sorted in a variety of different ways
sort_types = OrderedDict([
    ('No order', ''),
    ('Default order', '&sort=default'),
    ('Sort by most watched', '&sort=views'),
    ('Sort by recently updated', '&sort=episode_last_added_at'),
    ('Sort by recently added', '&sort=post_date'),
    ('Sort by release date', '&sort=release_date'),
    ('Sort alphabetically', '&sort=title'),
    ('Sort by scores', '&sort=scores')
])

main_menu = [
    ('Last show visited', {'value':'sql', 'action':'lastvisited'}),
    ('Browse', {'value':'submenu_browse', 'action':'localList'}),
    ('Watch list', {'value':'submenu_watchlist', 'action':'watchList'}),
    ('Search', {'value':'search', 'action':'search'}),
    ('Settings', {'value':'settings', 'action':'settings'})
]

# 9anime's watch list has multiple categories
submenu_watchlist = [
    ('All', {'value':'all', 'action':'watchList'}),
    ('Watching', {'value':'watching', 'action':'watchList'}),
    ('Completed', {'value':'watched', 'action':'watchList'}),
    ('On-hold', {'value':'onhold', 'action':'watchList'}),
    ('Dropped', {'value':'dropped', 'action':'watchList'}),
    ('Plan to watch', {'value':'planned', 'action':'watchList'}),
]

submenu_browse = [
    ('Most Watched', {'value':'/filter?sort=views', 'action':'mediaList'}),
    ('Trending', {'value':'/', 'action':'trendingList'}),
    ('Last updated', {'value':'/filter?sort=episode_last_added_at', 'action':'mediaList'}),
    ('Newest', {'value':'/filter?sort=release_date', 'action':'mediaList'}),
    #('Upcoming', {'value':'/upcoming', 'action':'upcomingList'}),
    ('Year', {'value':'submenu_year', 'action':'localList'}),
    ('Genre', {'value':'submenu_genres', 'action':'localList'}),
    ('Movies', {'value':'/filter?type%5B%5D=movie', 'action':'sortList'}),
    ('OVAs, ONAs, and Specials', {'value':'/filter?type%5B%5D=ova&type%5B%5D=ona&type%5B%5D=special', 'action':'sortList'}),
    ('Currently airing', {'value':'/filter?status%5B%5D=airing', 'action':'sortList'}),
    ('Finished', {'value':'/filter?status%5B%5D=finished', 'action':'sortList'}),
    ('Dubbed', {'value':'/filter?language=dubbed', 'action':'sortList'}),
    ('Subbed', {'value':'/filter?language=subbed', 'action':'sortList'})
]

submenu_year = [
    ('2017', {'value':'/filter?release%5B%5D=2017', 'action':'sortList'}),
    ('2016', {'value':'/filter?release%5B%5D=2016', 'action':'sortList'}),
    ('2015', {'value':'/filter?release%5B%5D=2015', 'action':'sortList'}),
    ('2014', {'value':'/filter?release%5B%5D=2014', 'action':'sortList'}),
    ('2013', {'value':'/filter?release%5B%5D=2013', 'action':'sortList'}),
    ('2012', {'value':'/filter?release%5B%5D=2012', 'action':'sortList'}),
    ('2011', {'value':'/filter?release%5B%5D=2011', 'action':'sortList'}),
    ('2010', {'value':'/filter?release%5B%5D=2010', 'action':'sortList'}),
    ('2009', {'value':'/filter?release%5B%5D=2009', 'action':'sortList'}),
    ('2008', {'value':'/filter?release%5B%5D=2008', 'action':'sortList'}),
    ('2007', {'value':'/filter?release%5B%5D=2007', 'action':'sortList'}),
    ('Older', {'value':'/filter?release%5B%5D=Older', 'action':'sortList'})
]

submenu_genres = [
    ('Action', {'value':'/filter?genre%5B%5D=1', 'action':'sortList'}),
    ('Adventure', {'value':'/filter?genre%5B%5D=2', 'action':'sortList'}),
    ('Cars', {'value':'/filter?genre%5B%5D=3', 'action':'sortList'}),
    ('Comedy', {'value':'/filter?genre%5B%5D=4', 'action':'sortList'}),
    ('Dementia', {'value':'/filter?genre%5B%5D=5', 'action':'sortList'}),
    ('Demons', {'value':'/filter?genre%5B%5D=6', 'action':'sortList'}),
    ('Drama', {'value':'/filter?genre%5B%5D=7', 'action':'sortList'}),
    ('Ecchi', {'value':'/filter?genre%5B%5D=8', 'action':'sortList'}),
    ('Fantasy', {'value':'/filter?genre%5B%5D=9', 'action':'sortList'}),
    ('Game', {'value':'/filter?genre%5B%5D=10', 'action':'sortList'}),
    ('Harem', {'value':'/filter?genre%5B%5D=11', 'action':'sortList'}),
    ('Historical', {'value':'/filter?genre%5B%5D=12', 'action':'sortList'}),
    ('Horror', {'value':'/filter?genre%5B%5D=13', 'action':'sortList'}),
    ('Josei', {'value':'/filter?genre%5B%5D=14', 'action':'sortList'}),
    ('Kids', {'value':'/filter?genre%5B%5D=15', 'action':'sortList'}),
    ('Magic', {'value':'/filter?genre%5B%5D=16', 'action':'sortList'}),
    ('Martial Arts', {'value':'/filter?genre%5B%5D=17', 'action':'sortList'}),
    ('Mecha', {'value':'/filter?genre%5B%5D=18', 'action':'sortList'}),
    ('Military', {'value':'/filter?genre%5B%5D=19', 'action':'sortList'}),
    ('Music', {'value':'/filter?genre%5B%5D=20', 'action':'sortList'}),
    ('Mystery', {'value':'/filter?genre%5B%5D=21', 'action':'sortList'}),
    ('Parody', {'value':'/filter?genre%5B%5D=22', 'action':'sortList'}),
    ('Police', {'value':'/filter?genre%5B%5D=23', 'action':'sortList'}),
    ('Psychological', {'value':'/filter?genre%5B%5D=24', 'action':'sortList'}),
    ('Romance', {'value':'/filter?genre%5B%5D=25', 'action':'sortList'}),
    ('Samurai', {'value':'/filter?genre%5B%5D=26', 'action':'sortList'}),
    ('School', {'value':'/filter?genre%5B%5D=27', 'action':'sortList'}),
    ('Sci-Fi', {'value':'/filter?genre%5B%5D=28', 'action':'sortList'}),
    ('Seinen', {'value':'/filter?genre%5B%5D=29', 'action':'sortList'}),
    ('Shoujo', {'value':'/filter?genre%5B%5D=30', 'action':'sortList'}),
    ('Shoujo Ai', {'value':'/filter?genre%5B%5D=31', 'action':'sortList'}),
    ('Shounen', {'value':'/filter?genre%5B%5D=32', 'action':'sortList'}),
    ('Shounen Ai', {'value':'/filter?genre%5B%5D=33', 'action':'sortList'}),
    ('Slice of Life', {'value':'/filter?genre%5B%5D=34', 'action':'sortList'}),
    ('Space', {'value':'/filter?genre%5B%5D=35', 'action':'sortList'}),
    ('Sports', {'value':'/filter?genre%5B%5D=36', 'action':'sortList'}),
    ('Super Power', {'value':'/filter?genre%5B%5D=37', 'action':'sortList'}),
    ('Supernatural', {'value':'/filter?genre%5B%5D=38', 'action':'sortList'}),
    ('Thriller', {'value':'/filter?genre%5B%5D=39', 'action':'sortList'}),
    ('Vampire', {'value':'/filter?genre%5B%5D=40', 'action':'sortList'}),
    ('Yaoi', {'value':'/filter?genre%5B%5D=41', 'action':'sortList'}),
    ('Yuri', {'value':'/filter?genre%5B%5D=42', 'action':'sortList'})
]

ui_table = {
    'submenu_watchlist': submenu_watchlist, 
    'submenu_browse': submenu_browse,
    'submenu_year': submenu_year,
    'submenu_genres': submenu_genres
}