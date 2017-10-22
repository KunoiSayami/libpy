# -*- coding: utf-8 -*-
# util.py
# Copyright (C) 2017 Too-Naive and contributors
#
# This module is part of gu-cycle-bot and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
import os

def current_join_path(subfolder,targetfile):
	return os.path.join('.',os.path.join(subfolder,targetfile))

def get_ssh_directory():
	return os.path.join(os.path.join(os.path.expanduser('~'),'.ssh'))

def parse_file_ssh_path(targetfile):
	return os.path.join(os.path.join(os.path.join(os.path.expanduser('~'),'.ssh')),
		targetfile)
