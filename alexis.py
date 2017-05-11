#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import platform
import sqlite3
import sys
import yaml
import random
import logger
from models import *
from tasks import *

__author__ = 'Nicolás Santisteban, Jonathan Gutiérrez'
__license__ = 'MIT'
__version__ = '0.1.0-dev'


class Alexis(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)

        self.log = logger.get_logger('Alexis')

        db.connect()
        db.create_tables([Post, Ban], True)

        try:
            with open('config.yml', 'r') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            self.log.exception(e)
            raise

    def go(self):
        self.log.info('"Alexis Bot" version {}.'.format(__version__))
        self.log.info('Python {} on {}.'.format(sys.version, sys.platform))
        self.log.info(platform.uname())
        self.log.info('SQLite3 support for version {}.'.format(sqlite3.sqlite_version))
        self.log.info('------')
        self.log.info('Connecting...')

        try:
            self.loop.create_task(posts_loop(self))
            self.run(self.config['token'])
        except Exception as e:
            self.log.exception(e)
            raise

    async def on_ready(self):
        self.log.info('Logged in as:')
        self.log.info(self.user.name)
        self.log.info(self.user.id)
        self.log.info('------')
        await self.change_presence(game=discord.Game(name=self.config['playing']))

    async def on_message(self, message):
        # !ping
        if message.content == '!ping':
            await self.send_message(message.channel, 'pong!')

        # !version
        if message.content == '!version':
            await self.send_message(message.channel, '```{}```'.format(__version__))

        # !ban (no PM)
        elif message.content.startswith('!ban') and message.server is not None:
            for mention in message.mentions:
                if random.randint(0,1):
                    user, created = Ban.get_or_create(user=mention, server=message.server)
                    up = Ban.update(bans=Ban.bans + 1).where(Ban.user == mention, Ban.server == message.server)
                    up.execute()

                    if user.bans + 1 == 1:
                        text = 'Uff, ¡**{}** se fue baneado por primera vez!'.format(mention.name)
                    else:
                        text = '¡**{}** se fue baneado otra vez y registra **{} baneos**!'.format(mention.name, user.bans + 1)
                    await self.send_message(message.channel, text)
                else:
                    text = '¡**{}** se salvo del ban de milagro!'.format(mention.name)
                    await self.send_message(message.channel, text)


if __name__ == '__main__':
    bot = Alexis()
    bot.go()
