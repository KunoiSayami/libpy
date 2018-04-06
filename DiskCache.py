# -*- coding: utf-8 -*-
# DiskCache.py
# Copyright (C) 2018 Too-Naive and contributors
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
from Config import Config

class DiskCache:
	def __init__(self, target_file=Config.backup.file, read_mode='r', write_mode='w', default_return_type=None):
		self.target_file = target_file
		self.read_mode = read_mode
		self.write_mode = write_mode
		#self.ignore_readerr = ignore_readerr
		self.default_return_type = default_return_type
	def read(self):
		with open(self.target_file, self.read_mode) as fin:
			return eval(fin.read())
	def write(self, cache_target):
		with open(self.target_file, self.write_mode) as fout:
			fout.write(repr(cache_target))
	def read_without_except(self):
		try:
			return self.read()
		except IOError:
			return self.default_return_type