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


class VideoPlayer(object):
    '''
        Object representation of a video player.
    '''
    def __init__(self, url=''):
        helper.log_debug('Initializing VideoPlayer with url: %s' % url)
        self.link = url

    ''' PUBLIC FUNCTIONS '''
    def play(self):
        if self.link == '':
            return

        import urlresolver

        ''' 
            Kodi v17 updated to Python 2.7.10 from 2.7.5 in v16, which introduced this error when 
            trying to resolve the url:
            http://stackoverflow.com/questions/27835619/ssl-certificate-verify-failed-error

            In Kodi v16, python would not verify the SSL certs or at least ignore, but they changed
            with the upgrade to v17.  Sometimes the cert from the initial decrypted URL is invalid,
            so to avoid errors, we temporarily disable SSL to get the resolved URL.  Although this
            workaround isn't secure, I figure it's not any worse than before...
        '''
        try:
            url = urlresolver.resolve(self.link)
        except:
            helper.log_debug('Attempt to resolve URL failed; trying again with SSL temporarily disabled (v16 behavior)')
            import ssl
            default_context = ssl._create_default_https_context # save default context
            ssl._create_default_https_context = ssl._create_unverified_context
            url = urlresolver.resolve(self.link)
            ssl._create_default_https_context = default_context # restore default context

        helper.log_debug("UrlResolver's resolved link: %s" % url)
        helper.resolve_url(url)