# coding: utf-8
import os
import re
import requests

from hippybot.decorators import botcmd


class Plugin(object):
    """Plugin to access log data from Logentries
    """
    def __init__(self):
        """Initialise plugin and load config

        The following environment variables are used to hold configuration

            LE_API_KEY: Account key found on your account screen
            LE_LOGS: List of logs you want to access
                     i.e. "key:host/log,key:host/log"

        """
        self.le_conf = {}
        self.le_conf['api_key'] = os.environ.get('LE_API_KEY','')
        lgs = os.environ.get('LE_LOGS','')
        lgs = { k:v for (k,v) in [ l.split(':') for l in lgs.split(',') ] }
        self.le_conf['logs'] = lgs

    @botcmd(name='le-list')
    def list_logs(self, mess, args):
        """
        Returns a list of available logs to search
        Format: @NickName le-list
        """
        self.bot.log.info("le-list: %s" % mess)
        return u", ".join(self.le_conf['logs'].keys())
