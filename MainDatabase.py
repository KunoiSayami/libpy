# -*- coding: utf-8 -*-
# MainDatabase.py
# Copyright (C) 2017-2018 Too-Naive and contributors
#
# This module is part of libpy and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
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
