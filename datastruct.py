# -*- coding: utf-8 -*-
# datastruct.py
# Copyright (C) 2018 KunoiSayami and contributors
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
class switch_class:
	def __init__(self, value=0):
		self.int_update(value)

	def int_update(self, privilege):
		self.privilege = bin(privilege)[2:]

	def __int__(self):
		return int(self.privilege, 2)

	# overload operator []
	def __getitem__(self, key):
		if not isinstance(key, int):
			raise TypeError
		try:
			return int(self.privilege[-key])
		except IndexError:
			return 0

	# overload self[key] = value
	def __setitem__(self, key, value):
		if value not in (0,1):
			raise ValueError('right value must be 0 or 1')
		if key <= 0:
			raise IndexError('Key must > 0')
		if not isinstance(key,int):
			raise TypeError('Key must be int')
		tmp = int(self)
		tmp += (1 if value else -1)*(2**key-1)
		self.int_update(tmp)
