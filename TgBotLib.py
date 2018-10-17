# -*- coding: utf-8 -*-
# TgBotLib.py
# Copyright (C) 2017-2018 Too-Naive and contributors
#
# This module is part of libpy and is released under
# the AGPL v3 License: https://www.gnu.org/licenses/agpl-3.0.txt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from __future__ import unicode_literals
import time
import telepot
import libpy.Log as Log
from libpy.Config import Config
import libpy.TelepotBotBase as TelepotBotBase

class telepot_bot:
	def __init__(self, *args, **kwargs):
		Log.debug(2,'Enter telepot_bot.__init__()')
		WAIT_TIME = 0.03
		Log.debug(2,'[bot_token = {}]',Config.bot.bot_token)
		Log.info('Initializing bot settings...')
		self.bot = TelepotBotBase.Bot(Config.bot.bot_token)
		self.bot_id = int(Config.bot.bot_token[:Config.bot.bot_token.find(':')])
		Log.info('Success login telegram bot with Token {}**************',
			Config.bot.bot_token[:Config.bot.bot_token.find(':')+5])
		Log.info('Loading telepot_bot.custom_init()')
		self.fail_with_md = None
		self.custom_init(*args, **kwargs)
		Log.info('Loading telepot_bot.custom_init() successful')
		Log.info('Bot settings initialized successful!')
		Log.debug(2,'Exit telepot_bot.__init__()')

	# Reserved for user init
	def custom_init(self, *args, **kwargs):
		pass

	def message_loop(self, on_message_function):
		Log.info('Starting message_loop()')
		self.bot.message_loop(on_message_function)
		Log.info('message_loop() is now started!')

	def getid(self):
		Log.debug(2,'Calling telepot_bot.getid() [return {}]',self.bot_id)
		return self.bot_id

	def sendMessage(self, chat_id, message, **kwargs):
		return_value = None
		while True:
			try:
				Log.debug(2,'Calling telepot_bot.sendMessage() [chat_id = {},message = {}, kwargs = {}]',
					chat_id, repr(message), kwargs)
				return_value = self.bot.sendMessage(chat_id, message, **kwargs)
				break
			except telepot.exception.TelegramError as e:
				# Markdown fail
				if self.fail_with_md is not None and e[-1]['error_code'] == 400 and \
					'Can\'t find end of the entity starting at byte' in e[-1]['description']:
					# Must fail safe
					return_value = self.bot.sendMessage(chat_id,'Error: {}\nRaw description: {}'.format(self.fail_with_md, e[-1]['description']))
					break
				else:
					Log.error('Raise exception: {}',repr(e))
					raise e
			except Exception as e:
				Log.error('Exception {} occurred',e.__name__)
				Log.debug(1,'on telepot_bot.sendMessage() [chat_id = {},message = {}, kwargs = {}]',
					chat_id, repr(message), kwargs)
				time.sleep(self.WAIT_TIME)
		return return_value

	def glance(self, msg):
		while True:
			try:
				Log.debug(2,'Calling telepot.glance()')
				content_type, chat_type, chat_id = telepot.glance(msg)
				Log.debug(2,'Exiting telepot.glance() [content_type = {}, chat_type = {}, chat_id = {}]',
					content_type, chat_type, chat_id)
				break
			except telepot.exception.TelegramError as e:
				Log.error('Raise exception: {}',e.__name__)
				raise e
			except Exception as e:
				Log.error('Exception {} occurred',e.__name__)
				time.sleep(0.03)
		return (content_type, chat_type, chat_id)

	def onMessage(self, msg):
		content_type, chat_type, chat_id = self.glance(msg)
		self.sendMessage(chat_id,'received')
