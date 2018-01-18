# -*- coding: utf-8 -*-
# AsyncLock.py
# Copyright (C) 2017-2018 Too-Naive and contributors
#
# This module is part of libpy and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
import time
from threading import Thread

class AsyncLock:
	def __init__(self,wait_time,sleep_time=0.01):
		self.setDelay(wait_time,sleep_time)
		self.lock = False
	def setLock(self):
		if self.lock:
			self.waitForUnlock()
		self.lock = True
		t = Thread(target=self.sleepProcess)
		t.daemon = True
		t.start()
	def sleepProcess(self):
		time.sleep(self.wait_time)
		self.lock = False
	def waitForUnlock(self):
		while self.lock:
			time.sleep(self.sleep_time)
	def setDelay(self,wait_time,sleep_time=0.01):
		self.wait_time = wait_time
		self.sleep_time = sleep_time