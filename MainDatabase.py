# -*- coding: utf-8 -*-
# MainDatabase.py
# Copyright (C) 2017-2019 KunoiSayami and contributors
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
import MySQLdb
from libpy.Config import Config

class MainDatabase(object):
	def __init__(self, noUseDatabase=False):
		kwargs = {
			k: Config.database.__dict__[k]
			for k in 'charset host port user passwd'.split()
		}
		if not noUseDatabase and Config.database.db_name is not None:
			kwargs['db'] = Config.database.db_name
		self._db = MySQLdb.connect(**kwargs)
		self._cursor = self._db.cursor()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if exc_type is None:
			self.commit()
		else:
			self.rollback()
		self.close()

	def execute(self, sql, *args):
		return self._cursor.execute(sql, args)

	def getData(self):
		return self._cursor.fetchall()

	def query(self, sql, *args):
		self.execute(sql, *args)
		return self.getData()

	def commit(self):
		self._db.commit()

	def rollback(self):
		self._db.rollback()

	def close(self):
		if self._db is not None:
			self._cursor.close()
			self._db.close()
			self._db = self._cursor = None
