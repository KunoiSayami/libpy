# -*- coding: utf-8 -*-
# DaemonThread.py
# Copyright (C) 2018 Too-Naive and contributors
#
# This module is part of libpy and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
from threading import Thread
from libpy import Log
import os
import traceback

def exitWithTrace(banner=None):
	if banner is not None:
		banner += '\n'
	Log.error('{}{}', banner, traceback.format_exc())
	os._exit(1)

class DaemonThread(object):
	def __init__(self, target=None, args=()):
		def __run(target, args):
			try:
				target(*args)
			except:
				exitWithTrace('Daemon thread raised exception')
		self._t = Thread(target=__run, args=(target or self.run, args))
		self._t.daemon = True

	def start(self):
		self._t.start()

	def join(self, timeout=None):
		self._t.join(timeout=timeout)

	def isAlive(self):
		return self._t.isAlive()

	def run(self, *args):
		raise NotImplementedError('The subclass of `DaemonThread` should implement `run()`')
