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
from resources.lib.common.helper import helper
from resources.lib.common.args import args
from resources.lib.appdata.account import Account


class Controller:
    '''
        Top level logic hub - creates top level objects and invokes their methods.
    '''
    def main_menu(self):
        helper.start('main_menu')
        from resources.lib.lists.locallist import LocalList
        LocalList().add_directories(self.__get_main_menu_src())
        helper.end('main_menu')

    def __get_main_menu_src(self):
        main_menu = constants.main_menu
        from resources.lib.appdata.lastvisited import LastVisited
        last_show_queries = LastVisited().get_last_show_visited()
        if last_show_queries:
            (last_visited_title, queries) = main_menu[0]
            title = '%s - %s' % (last_show_queries.get('full_title'), last_visited_title)
            queries['icon'] = last_show_queries.get('icon', '')
            queries['fanart'] = last_show_queries.get('fanart', '')
            main_menu[0] = (title, queries)
        return main_menu

    def show_local_list(self):
        helper.start('show_local_list')
        from resources.lib.lists.locallist import LocalList
        LocalList().add_directories(constants.ui_table[args.value])
        helper.end('show_local_list')

    def show_sort_list(self):
        if helper.get_setting('preset-sorting') != 'Individually select':
            self.show_media_list()
            return

        helper.start('show_sort_list')
        sort_list = []
        for (sort_type, sort_url) in constants.sort_types.iteritems():
            d = {'action':'mediaList'}
            d['value'] = args.value + sort_url
            sort_list.append((sort_type, d))
        from resources.lib.lists.locallist import LocalList
        LocalList().add_directories(sort_list)
        helper.end('show_sort_list')

    def __show_web_list(self, list):
        list.parse()
        list.add_items()

    def show_media_list(self):
        helper.start('show_media_list')
        if helper.get_setting('preset-sorting') != 'Individually select' and 'page=' not in args.value and 'sort=' not in args.value:
            args.value += constants.sort_types[helper.get_setting('preset-sorting')]
        from resources.lib.lists.medialist import MediaList
        self.__show_web_list(MediaList())        
        helper.end('show_media_list')

    def show_trending_list(self):
        helper.start('show_trending_list')
        from resources.lib.lists.trendinglist import TrendingList
        self.__show_web_list(TrendingList())
        helper.end('show_trending_list')

    def show_upcoming_list(self):
        helper.start('show_upcoming_list')
        from resources.lib.lists.upcominglist import UpcomingList
        self.__show_web_list(UpcomingList())        
        helper.end('show_upcoming_list')

    def show_episode_list(self):
        helper.start('show_episode_list with media_type %s' % args.media_type)
        if args.media_type == 'tvshow':
            from resources.lib.lists.episodelist import EpisodeList
            l = EpisodeList()
        elif args.media_type == 'movie':
            from resources.lib.lists.movielist import MovieList
            l = MovieList()
        elif args.media_type == 'special':
            from resources.lib.lists.episodelist import EpisodeList #from resources.lib.lists.specialslist import SpecialsList
            l = EpisodeList() #SpecialsList()
        else:
            # media_type == 'preview', which means we don't know media type
            from resources.lib.lists.episodelist import EpisodeList
            l = EpisodeList()

        self.__show_web_list(l)
        from resources.lib.appdata.lastvisited import LastVisited
        LastVisited().update_last_show_visited()
        helper.end('show_episode_list')

    def choose_quality_play_video(self):
        helper.start('choose_quality_play_video')
        from resources.lib.players.qualityplayer import QualityPlayer
        qp = QualityPlayer()
        qp.determine_quality()
        qp.play()
        helper.end('choose_quality_play_video')

    def search(self):
        helper.start('search')
        search_string = helper.get_user_input('Search for show title')
        if search_string:
            import urllib
            url = '%s/search?keyword=%s' % (helper.domain_url(), urllib.quote_plus(search_string))
            helper.log_debug('Searching for show %s using url %s' % (search_string, url))
            plugin_url = helper.build_plugin_url({'action':'mediaList', 'value':url})
            helper.update_page(plugin_url)

        helper.end('search')

    def find_metadata(self):
        helper.start('find_metadata')
        from resources.lib.metadata import metadatafinder
        finder = metadatafinder.MetadataFinder()
        finder.search_and_update()
        helper.end('find_metadata')

    def clear_metadata(self):
        helper.start('clear_metadata')
        from resources.lib.metadata import metadatahandler
        finder1 = metadatahandler.meta
        finder1.update_meta_to_nothing( args.media_type, args.base_title)
        helper.end('clear_metadata')		
		
    def show_last_visited(self):
        helper.start('show_last_visited')
        from resources.lib.appdata.lastvisited import LastVisited
        last_show_queries = LastVisited().get_last_show_visited()
        if not last_show_queries:
            helper.show_ok_dialog(['Visit a show to populate this directory.'], 'Last Show Visited not set')
        else:
            args.override(last_show_queries)
            if helper.debug_import():
                from resources.lib.lists import episodelist, weblist
                reload(weblist)
                reload(episodelist)
            from resources.lib.lists.episodelist import EpisodeList
            self.__show_web_list(EpisodeList())
        helper.end('show_last_visited')

    def show_watch_list(self):
        if not Account().is_logged_in():
            Account().log_in_saved()            		
        if Account().is_logged_in():
            preset_watchlist_type = helper.get_setting('watch-list-type')
            if args.value == 'submenu_watchlist' and preset_watchlist_type == 'Select':
                self.show_local_list()
            else:
                #helper.show_error_dialog(['','Ping'])			
                from resources.lib.lists.watchlist import WatchList
                self.__show_web_list(WatchList())
        else:
            helper.show_error_dialog(['Failed to access account watch list.  Please login if you have not already.'])

    def account_login_logout(self):
        Account().log_in_or_out()

    def _account_operation(self, fn):
        if Account().is_logged_in():
            fn()
        else:
            helper.show_error_dialog(['Must be logged in to do this operation.  Please log in inside the settings.'])

    def add_bookmark(self):
        self._account_operation(Account().add_bookmark)

    def remove_bookmark(self):
        self._account_operation(Account().remove_bookmark)
