# -*- coding: utf-8 -*-
# AsyncLock.py
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