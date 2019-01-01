# -*- coding: utf-8 -*-
# util.py
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
from __future__ import unicode_literals
import datetime
import os
import libpy.Log as Log

def current_join_path(subfolder,targetfile):
	return os.path.join('.',os.path.join(subfolder,targetfile))

def get_ssh_directory():
	return os.path.join(os.path.join(os.path.expanduser('~'),'.ssh'))

def parse_file_ssh_path(targetfile):
	return os.path.join(os.path.join(os.path.join(os.path.expanduser('~'),'.ssh')),
		targetfile)

def datetime_sub_datetime(timestampnow,timestamp):
	return (timestampnow.replace(microsecond=0) - timestamp.replace(microsecond=0)
		).total_seconds()

def datetime_sub_day(datetimein,days):
	return datetimein - datetime.timedelta(days=days)

def sql_clear_comment(sql_file_path):
	with open(sql_file_path) as fin:
		r = fin.readlines()
	with open(sql_file_path,'w') as fout:
		for x in r:
			if x[:2] != '--':
				#content.append(x)
				fout.write(x)
				Log.debug(5, '[x = {}]',x[:-1])

def split_list(l, split_count, Fill_with_None=False):
	assert isinstance(l, list) or l is None
	Count = len(l)//split_count
	Log.debug(3, 'Count:{}', Count)
	if Count == 0:
		tmp = [[x] for x in l]
		if Fill_with_None:
			for x in xrange(len(tmp), split_count):
				tmp.append(None)
		return tmp
	if len(l)%split_count:
		Count += 1
	tmp = [l[Count*x:Count*(x+1)] for x in xrange(0, split_count)]
	for x in tmp:
		if x == []:
			tmp.remove(x)
	if Fill_with_None:
		for x in xrange(len(tmp), split_count):
			tmp.append(None)
	return tmp

def custom_diff(diff1,diff2):
	d1 = []
	d2 = []
	with open(diff1) as fin:
		r = fin.readlines()
	for x in r:
		if x[:2] != '--':
			d1.append(x)
	with open(diff2) as fin:
		r = fin.readlines()
	for x in r:
		if x[:2] != '--':
			d2.append(x)
	#Log.debug(3, '[d1 == d2 = {}]', d1 == d2)
	#Log.debug(3, '[d1 = {}]', d1)
	#Log.debug(3, '[d2 = {}]', d2)
	return d1 == d2