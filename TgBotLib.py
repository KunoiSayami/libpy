# -*- coding: utf-8 -*-
# TgBotLib.py
# Copyright (C) 2017 Too-Naive and contributors
#
# This module is part of libpy and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
from __future__ import unicode_literals
import telepot
import libpy.TelepotBotBase as TelepotBotBase
import libpy.Log as Log
from libpy.Config import Config
import time


class telepot_bot:
	def __init__(self):
		Log.debug(2,'Enter telepot_bot.__init__()')
		WAIT_TIME = 0.03
		Log.debug(2,'[bot_token = {}]',Config.bot.bot_token)
		Log.info('Initializing bot settings...')
		self.bot = TelepotBotBase.Bot(Config.bot.bot_token)
		self.bot_id = int(Config.bot.bot_token[:Config.bot.bot_token.find(':')])
		Log.info('Success login telegram bot with Token {}**************',
			Config.bot.bot_token[:Config.bot.bot_token.find(':')+5])
		Log.info('Loading telepot_bot.custom_init()')
		self.custom_init()
		Log.info('Loading telepot_bot.custom_init() successful')
		Log.info('Bot settings initialized successful!')
		Log.debug(2,'Exit telepot_bot.__init__()')

	# Reserved for user init
	def custom_init(self,*args,**kwargs):
		pass

	def message_loop(self,on_message_function):
		Log.info('Starting message_loop()')
		self.bot.message_loop(on_message_function)
		Log.info('message_loop() is now started!')

	def getid(self):
		Log.debug(2,'Calling telepot_bot.getid() [return {}]',self.bot_id)
		return self.bot_id

	def sendMessage(self,chat_id,message,**kwargs):
		while True:
			try:
				Log.debug(2,'Calling telepot_bot.sendMessage() [chat_id = {},message = \'{}\', kwargs = {}]',
					chat_id,message,kwargs)
				self.bot.sendMessage(chat_id,message,**kwargs)
				break
			except telepot.exception.TelegramError as e:
				raise e
			except Exception as e:
				Log.error('Exception {} occurred',e.__name__)
				Log.debug(1,'on telepot_bot.sendMessage() [chat_id = {},message = \'{}\', kwargs = {}]',
					chat_id,message,kwargs)
				time.sleep(self.WAIT_TIME)

	def glance(self,msg):
		while True:
			try:
				Log.debug(2,'Calling telepot.glance()')
				content_type, chat_type, chat_id = telepot.glance(msg)
				Log.debug(2,'Exiting telepot.glance() [content_type = {}, chat_type = {}, chat_id = {}]',
					content_type, chat_type, chat_id)
				break
			except telepot.exception.TelegramError as e:
				raise e
			except Exception as e:
				Log.error('Exception {} occurred',e.__name__)
				time.sleep(0.03)
		return (content_type, chat_type, chat_id)

	def onMessage(self,msg):
		content_type, chat_type, chat_id = self.glance(msg)
		self.sendMessage(chat_id,'received')