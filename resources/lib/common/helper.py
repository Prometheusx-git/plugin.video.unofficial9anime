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


import sys
from dat1guy.shared import helper as shared_helper
from resources.lib.common import constants


def __init():
    return Helper(constants.plugin_name, argv=sys.argv)


class Helper(shared_helper.Helper):
    '''
        Contains common helper functions.
    '''
    def domain(self):
        return helper.get_setting('domain')

    def domain_url(self):
        return '%s://%s' % (helper.get_setting('http-type'), helper.domain())

    def handle_html_errors(self, html, e):
        if html == '':
            import urllib2
            self.log_debug('Failed to grab HTML' + ('' if e == None else ' with exception %s' % str(e)))
            if isinstance(e, urllib2.HTTPError) and e.code == 503:
                self.show_error_dialog(['The service is currently unavailable.', '', 'If it does not respond after 1 more try, the site may be temporarily down.'])
            if isinstance(e, urllib2.HTTPError) and e.code == 522:
                self.show_error_dialog(['The connection to the website timed out, so the website may be down.', '', 'Try changing domains in the setting.'])
            elif isinstance(e, urllib2.HTTPError):
                self.show_error_dialog(['Encountered a http error.', '', ('HTTP error code: %s' % e.code)])
            else:
                self.show_error_dialog(['Failed to parse the 9anime website.', '', ('Error details: %s' % str(e))])

        return html

    def handle_json_errors(self, json):
        error = json.get('error', None)
        if error == None:
            return False

        helper.log_debug('JSON error: %s' % error)
        if error == 404:
            helper.show_error_dialog(['Failed to find JSON resource (error 404).', '', 'Check that this resource exists on the website before contacting the developer.'])
        elif error == -1:
            helper.show_error_dialog(['Invalid JSON request.', '', 'Please contact the developer of this add-on.'])
        else:
            helper.show_error_dialog(['JSON request failed.', '', ('Error details: %s' % error)])

        return True    
		
helper = __init()