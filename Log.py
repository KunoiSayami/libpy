# -*- coding: utf-8 -*-
# Log.py
# Copyright (C) 2017 Too-Naive and contributors
#
# This module is part of libpy and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
from __future__ import print_function, division, unicode_literals
import sys
import time
import datetime
import inspect,os
import traceback,tempfile
from threading import Lock
from libpy.Config import Config

printLock = Lock()
logFile = Config.log.logfile and open(Config.log.logfile, 'a')

loaddatetime = datetime.datetime.now().replace(microsecond=0)

__currentcwdlen = len(os.getcwd())+1

if Config.log.log_debug:
	assert(Config.log.debug_lvl>=1)

def get_runtime():
	return str(datetime.datetime.now().replace(microsecond=0)-loaddatetime)

def get_name():
	t = inspect.currentframe()
	r = inspect.getouterframes(t)[3]
	s = '{}.{}][{}'.format(r[1][__currentcwdlen:-3].replace('\\','.').replace('/','.'),
		r[3],r[2])
	del r
	del t
	if s[0] == '.':
		s = s[1:]
	return s

def info(fmt, *args, **kwargs):
	log('INFO', Config.log.log_info, Config.log.print_info, fmt.format(*args), **kwargs)

def error(fmt, *args, **kwargs):
	log('ERROR', Config.log.log_err, Config.log.print_err, fmt.format(*args), **kwargs)

def get_debug_info():
	if Config.log.log_debug:
		return (True,Config.log.debug_lvl)
	return (False,-0x7ffffff)

def custom_info(custom_head, fmt, *args, **kwargs):
	log(custom_head, Config.log.log_info, Config.log.print_info, fmt.format(*args), **kwargs)

def debug(level ,fmt, *args, **kwargs):
	assert(type(level) is int)
	if level <= Config.log.debug_lvl:
		log('DEBUG', Config.log.log_debug, Config.log.print_debug, fmt.format(*args), **kwargs)

def reopen(path):
	global logFile
	if logFile:
		logFile.close()
	logFile = open(path, 'a')

def tfget(value):
	return {False:"Off",True:"On"}.get(value)

def write_traceback_error(error_msg,*args,**kwargs):
	error(error_msg,pre_print=False,*args,**kwargs)
	printLock.acquire()
	try:
		tmpfile = tempfile.SpooledTemporaryFile(mode='w')
		traceback.print_exc(file=tmpfile)
		tmpfile.seek(0)
		s = tmpfile.read()
		del tmpfile
		if Config.log.log_err and logFile:
			logFile.write(s)
			logFile.flush()
	finally:
		printLock.release()

def log(lvl, bLog, prtTarget, s, start='', end='\n',pre_print=True):
	s = '{}[{}] [{}]\t[{}] {}{}'.format(start, time.strftime('%Y-%m-%d %H:%M:%S'), lvl, get_name(), s, end)
	f = {'stdout': sys.stdout, 'stderr': sys.stderr}.get(prtTarget)
	printLock.acquire()
	try:
		if pre_print and f:
			f.write(s)
			f.flush()
		if bLog and logFile:
			logFile.write(s)
			logFile.flush()
	finally:
		printLock.release()
