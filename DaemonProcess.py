# -*- coding: utf-8 -*-
# DaemonProcess.py
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
import platform
import sys, os, signal
from subprocess import Popen

class DaemonProcess:
	def __init__(self, custom_args, entry_function, func_help_msg, kill_with_signal=signal.SIGINT):
		if len(sys.argv) == 2:
			if sys.argv[1] in custom_args:
				Popen(['python', sys.argv[0], '--daemon-start'])
			elif sys.argv[1] == '--daemon-start':
				# Redirect stdout to null
				sys.stdout = open('/dev/null' if platform.system() != 'Windows' else 'nul', 'w')
				with open('pid', 'w') as fout:
					fout.write(str(os.getpid()))
				entry_function()
			elif sys.argv[1] == '-kill':
				with open('pid') as fin:
					os.kill(int(fin.read()), kill_with_signal)
			else:
				func_help_msg()
		else:
			func_help_msg()
