# coding: utf-8
import os
import shlex
import urllib

import requests

from hippybot.decorators import botcmd


class Plugin(object):
    """Plugin to access log data from Logentries
    """
    def __init__(self):
        """Initialise plugin

        The following environment variables are used to hold configuration

            LE_API_URL: Override the default API URL
            LE_API_KEY: Account key found on your account screen
            LE_LOGS: List of logs you want to access
                     i.e. "key:host/log,key:host/log"
            LE_GEN_URL: Boolean -
                        Return a full URL for the search (reveals API Key)

        """
        self.le_api_url = os.environ.get('LE_API_URL','https://api.logentries.com/')
        self.le_api_key = os.environ.get('LE_API_KEY','')
        lgs = os.environ.get('LE_LOGS','')
        lgs = { k:v for (k,v) in [ l.split(':') for l in lgs.split(',') ] }
        self.le_logs = lgs
        self.le_gen_url = os.environ.get('LE_GEN_URL', 'false') \
                                    .lower() in ('true','t','yes','1')

    @botcmd(name='le-list')
    def list_logs(self, mess, args):
        """List available logs

        Returns a list of available logs to search

        Format: @NickName le-list

        """
        self.bot.log.info("le-list: %s" % mess)
        logs = u", ".join(self.le_logs.keys())

        if logs:
            return logs
        else:
            return u"There are no logs defined..."

    @botcmd(name='le-search')
    def search_logs(self, mess, args):
        """Search logs

        Returns logs entries matching query
        The log key can be found by using the le-list command

        Format: @NickName le-search <log> <query>

        """
        self.bot.log.info("le-search: %s" % mess)

        log, query = shlex.split(args.encode('utf8'))
        url = self.gen_url(log, query)
        req = requests.get(url)
        reply = req.content

        if self.le_gen_url:
            reply = "{}\n{}".format(reply, url)

        return reply

    def gen_url(self, log, query):
        """Generate search URL

        Compose a valid search URL to query the API

        """
        params = (('filter',query),('limit',5))
        url = "{}{}/hosts/{}/?{}".format(self.le_api_url, self.le_api_key,
                                        self.le_logs[log], urllib.urlencode(params))
        return url
