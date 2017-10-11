# -*- coding: utf-8 -*-
# Log.py
# Copyright (C) 2017 Too-Naive and contributors
#
# This module is part of gu-cycle-bot and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
from __future__ import print_function, division
import sys
import time
from threading import Lock
from libpy.Config import Config
import inspect

printLock = Lock()
logFile = Config.log.logfile and open(Config.log.logfile, 'a')

if Config.log.log_debug:
	assert(Config.log.debug_lvl>=1)

def get_name():
	return inspect.getouterframes(inspect.currentframe())[3]

def info(fmt, *args, **kwargs):
	log('INFO', Config.log.log_info, Config.log.print_info, fmt.format(*args), **kwargs)

def error(fmt, *args, **kwargs):
	log('ERROR', Config.log.log_err, Config.log.print_err, fmt.format(*args), **kwargs)

def get_debug_info():
	if Config.log.log_debug:
		return (True,Config.log.debug_lvl)

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

def log(lvl, bLog, prtTarget, s, start='', end='\n'):
	s = '{}[{}][{}] {}{}'.format(start, time.strftime('%Y-%m-%d %H:%M:%S'), lvl, s, end)
	f = {'stdout': sys.stdout, 'stderr': sys.stderr}.get(prtTarget)
	printLock.acquire()
	try:
		if f:
			f.write(s)
			f.flush()
		if bLog and logFile:
			logFile.write(s)
			logFile.flush()
	finally:
		printLock.release()
