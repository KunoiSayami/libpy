# -*- coding: utf-8 -*-
# Config.py
# Copyright (C) 2017 Too-Naive and contributors
#
# This module is part of gu-cycle-bot and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
from ConfigParser import RawConfigParser

def struct(name, kvs):
	return type(name, (object,), kvs)

def preprocess(v):
	if v == '':
		return None
	elif v == 'true':
		return True
	elif v == 'false':
		return False
	elif v[0] == v[-1] and v[0] in '"\'': # quoted string
		return v[1:-1]
	elif v.isdigit():
		return int(v)
	try:
		return float(v)
	except ValueError:
		return v

cfg = RawConfigParser()
cfg.read('data/config.ini')
Config = struct('Config', {
	sec: struct('Config_' + sec, {
		str(k): preprocess(str(v)) # unicode to str
		for k, v in cfg.items(sec)
	})
	for sec in map(str, cfg.sections()) # unicode to str
})
