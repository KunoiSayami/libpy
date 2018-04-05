# -*- coding: utf-8 -*-
# Log.py
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
from __future__ import print_function, division, unicode_literals
import sys
import time
import datetime
import inspect,os
from Queue import Queue
import traceback,tempfile
from threading import Lock
from libpy.Config import Config

printLock = Lock()
logFile = Config.log.logfile and open(Config.log.logfile, 'a')

loaddatetime = datetime.datetime.now().replace(microsecond=0)

__currentcwdlen = len(os.getcwd())+1

error_queue = Queue()

if Config.log.log_debug:
	assert(Config.log.debug_lvl>=1)

def get_runtime():
	return str(datetime.datetime.now().replace(microsecond=0)-loaddatetime)

def print_call_backfunc():
	'''
		This func can print stack track
	'''
	t = inspect.currentframe()
	r = inspect.getouterframes(t)
	s = 'Stack track:\n'
	for x in r[1:]:
		s += '\t\t\t\t\t\tIn {}:{} function:{}\n'.format(x[1],x[2],x[3])
	debug(3,'{}'.format(s))
	del r
	del t
	del s

def get_name():
	t = inspect.currentframe()
	r = inspect.getouterframes(t)
	s = '{}.{}][{}'.format(r[3][1][__currentcwdlen:-3].replace('\\','.').replace('/','.'),
		r[3][3],r[3][2])
	del r
	del t
	return s[1:] if s[0] == '.' else s

def info(fmt, *args, **kwargs):
	log('INFO', Config.log.log_info, Config.log.print_info, fmt.format(*args), **kwargs)

def error(fmt, *args, **kwargs):
	log('ERROR', Config.log.log_err, Config.log.print_err, fmt.format(*args), **kwargs)

def warn(fmt, *args, **kwargs):
	log('WARN', Config.log.log_warn, Config.log.print_warn, fmt.format(*args), **kwargs)

def get_debug_info():
	return (True,Config.log.debug_lvl) if Config.log.log_debug else (False,-0x7ffffff)

def custom_info(custom_head, fmt, *args, **kwargs):
	log(custom_head, Config.log.log_info, Config.log.print_info, fmt.format(*args), **kwargs)

def debug(level ,fmt, *args, **kwargs):
	assert isinstance(level,int)
	if level <= Config.log.debug_lvl:
		log('DEBUG', Config.log.log_debug, Config.log.print_debug, fmt.format(*args), **kwargs)

def reopen(path):
	global logFile
	if logFile:
		logFile.close()
	logFile = open(path, 'a')

def tfget(value):
	return 'On' if value else 'Off'

def write_traceback_error(error_msg, *args, **kwargs):
	error(error_msg, pre_print=False, *args, **kwargs)
	printLock.acquire()
	try:
		tmpfile = tempfile.SpooledTemporaryFile(mode='w')
		traceback.print_exc(file=tmpfile)
		tmpfile.seek(0)
		s = tmpfile.read()
		tmpfile.close()
		del tmpfile
		if Config.log.log_err and logFile:
			logFile.write(s)
			logFile.flush()
	finally:
		printLock.release()

def log(lvl, bLog, prtTarget, s, start='', end='\n', pre_print=True):
	s = '{}[{}] [{}]\t[{}] {}{}'.format(start, time.strftime('%Y-%m-%d %H:%M:%S'), lvl, get_name(), s, end)
	f = {'stdout': sys.stdout, 'stderr': sys.stderr}.get(prtTarget)
	printLock.acquire()
	if lvl in ('ERROR','WARN'):
		error_queue.put(s)
	try:
		if pre_print and f:
			f.write(s)
			f.flush()
		if bLog and logFile:
			logFile.write(s)
			logFile.flush()
	finally:
		printLock.release()
