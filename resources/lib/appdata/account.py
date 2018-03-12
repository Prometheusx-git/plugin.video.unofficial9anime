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
import re

class Account(object):
    '''
        Wraps up any functionality related to an account on the website, including bookmarks.
    '''
    def __init__(self):
        from resources.lib.common.nethelper import net, cookies
        self.net, self.cookies = net, cookies

        self.html = ''
        self.html, e = self.net.get_html(helper.domain_url() , self.cookies, helper.domain_url())
        #self.html = helper.handle_html_errors(self.html, e)
		
		
    ''' PUBLIC FUNCTIONS '''
    def log_in_saved(self):    
        username = helper.get_setting('username')	
        password = helper.get_setting('password')
        helper.show_busy_notification()
        logged_in = self.__login(username, password)
        msg = '%s into %s' % (('Successfully logged' if logged_in else 'Failed to log'), username)
        helper.close_busy_notification()
        helper.show_small_popup(msg=msg)
	
    def log_in_or_out(self):
        if self.is_logged_in():
            proceed = helper.show_yes_no_dialog('Are you sure you want to log out of your account?')
            if proceed:
                username = helper.get_setting('username')
                self.__logout()
                helper.show_small_popup(msg=('Successfully logged out of %s' % username))
        else:
            username = helper.get_user_input('Please enter your username')
            if username == None:
                return

            password = helper.get_user_input('Please enter your password', hidden=True)
            if password == None:
                return

            helper.show_busy_notification()
            logged_in = self.__login(username, password)
            msg = '%s into %s' % (('Successfully logged' if logged_in else 'Failed to log'), username)
            helper.close_busy_notification()
            helper.show_small_popup(msg=msg)

    def is_logged_in(self):
        username = helper.get_setting('username')
        if len(username) == 0:
            return False

        required_cookies = 0
        for cookie in self.net._cj:
            if helper.domain() not in cookie.domain:
                continue
            if cookie.name.lower() == 'session' or 'remember_web_' in cookie.name.lower():
                required_cookies += 1

        return (required_cookies == 2)

    def add_bookmark(self):
        options = [x[0] for x in constants.submenu_watchlist]
        options.remove('All')
        idx = helper.present_selection_dialog('Choose the list to which the bookmark should be added', options)
        list_type = constants.submenu_watchlist[idx+1][1]['value']

        self.__bookmark_operation(list_type, add=True, list_str=options[idx])

    def remove_bookmark(self):
        self.__bookmark_operation('remove', add=False, list_str='watch')

    ''' PRIVATE FUNCTIONS '''
    def __login(self, username, password):
        #url = helper.domain_url() + '/user/ajax/login'
        form_data = {'username': username, 'password': password, 'remember': 1}
	
        ts = re.search('ts=\"(.*?)\"',self.html).group(1)
        url_base = re.search('href=\"(.*?)\"',self.html).group(1) 			
        
        extra_para = self.__get_extra_url_parameter(username,password,ts) #1673
        url = '%s/user/ajax/login?ts=%s&_=%s' % (url_base, ts, extra_para )
        
        #helper.show_error_dialog(['',str(extra_para)])			
        json = self.net.get_json(url, self.cookies, helper.domain_url(), form_data)
        helper.log_debug('login response: %s' % json)
        #helper.show_error_dialog(['',str(json)])

        if helper.handle_json_errors(json) or json.get('success', False) == False:
            return False

        helper.set_setting('username', username)
        helper.set_setting('password', password)		
        return True
    
    def __logout(self):
        self.net.refresh_cookies(self.cookies)
        helper.set_setting('username', '')

    def __bookmark_operation(self, folder, add, list_str):
        str1 = 'add the show to' if add else 'remove the show from'
        str2 = 'added the show to' if add else 'removed the show from'

        url = '%s/user/ajax/edit-watchlist?folder=%s&id=%s&Q=1' % (helper.domain_url(), folder, args.value)
        json = self.net.get_json(url, self.cookies, helper.domain_url())
        # returns status == False on failure
        if helper.handle_json_errors(json) or json.get('status', False) == False:
            msg = 'Failed to %s the %s list' % (str1, list_str)
        else:
            msg = 'Successfully %s the %s list' % (str2, list_str)

        helper.show_small_popup(msg=msg)
        helper.refresh_page()

		
    def __get_extra_url_parameter(self, username, password, ts):
        DD = 'iQDWcsGqN'		
        params = [('username', str(username)), ('password', str(password)),('remember', '1'), ('ts', str(ts))]
        o = self.__s(DD)
        for i in params:
            o += self.__s(self.__a(DD + i[0], i[1]))
        return o 

    def __s(self, t):
        i = 0
        for (e, c) in enumerate(t):
            i += ord(c) + e 
        return i

    def __a(self, t, e):
        n = 0
        for i in range(max(len(t), len(e))):
            n += ord(e[i]) if i < len(e) else 0
            n += ord(t[i]) if i < len(t) else 0
        return format(n, 'x')  # convert n to hex string		