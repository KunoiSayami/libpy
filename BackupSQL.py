# -*- coding: utf-8 -*-
# backupSQL.py
# Copyright (C) 2017 Too-Naive and contributors
#
# This module is part of gu-cycle-bot and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt

import libpy.Config as Config
from libpy.MainDatabase import MainDatabase
from base64 import b64encode,b64decode
from libpy.Encrypt import b64encrypt,b64decrypt
import libpy.Log as Log
from libpy.SQLbackup import func_backup_sql
from libpy.util import current_join_path

def backup_and_encrypt(target_database_name=Config.database.db_name,
		workingdir='workingdir',sub_folder_name='sqlbkup'):
	Log.debug(2,'Entering backup_and_encrypt()')
	func_backup_sql(target_database_name)
	with open(current_join_path(sub_folder_name,target_database_name+'.sql')) as  fin:
		raw = fin.read()
	with open(current_join_path(workingdir,Config.github.filename),'w') as fout:
		a,b,c=b64encrypt(raw)
		fout.write(a+'\\\\n'+b+'\\\\n'+c)
	Log.debug(2,'Exiting backup_and_encrypt()')

def restore_sql():
	Log.debug(2,'Entering restore_sql()')
	
	Log.debug(2,'Exiting restore_sql()')


def __execute_sql(sql_filename='temp.sql'):
	with open(os.path.join('.',sql_filename)) as fin:
		with MainDatabase() as db:
			for x in fin.read().split(';'):
				db.execute(x)
