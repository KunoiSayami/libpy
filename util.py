# -*- coding: utf-8 -*-
# util.py
# Copyright (C) 2017-2018 Too-Naive and contributors
#
# This module is part of libpy and is released under
# the AGPL v3 License: https://www.gnu.org/licenses/agpl-3.0.txt
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
