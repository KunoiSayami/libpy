# -*- coding: utf-8 -*-
# Config.py
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
