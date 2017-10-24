# -*- coding: utf-8 -*-
# backupSQL.py
# Copyright (C) 2017 Too-Naive and contributors
#
# This module is part of gu-cycle-bot and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
import time
import os,shutil
import libpy.Log as Log
from threading import Thread
from libpy.Config import Config
from libpy.Gitlib import pygitlib
from base64 import b64encode,b64decode
from libpy.util import current_join_path
from libpy.MainDatabase import MainDatabase
from libpy.SQLexport import func_backup_sql
from libpy.Encrypt import b64encrypt,b64decrypt

def backup_and_encrypt(target_database_name=Config.database.db_name,
		workingdir='workingdir',sub_folder_name='sqlbkup'):
	Log.debug(2,'Entering backup_and_encrypt()')
	func_backup_sql(target_database_name,DATETIME=sub_folder_name)
	with open(current_join_path(sub_folder_name,target_database_name+'.sql')) as  fin:
		raw = fin.read()
	with open(current_join_path(workingdir,Config.git.filename),'w') as fout:
		a,b,c=b64encrypt(raw)
		fout.write(a+'\\\\n'+b+'\\\\n'+c)
	if os.path.isdir(sub_folder_name):
		shutil.rmtree(sub_folder_name)
	Log.debug(2,'Exiting backup_and_encrypt()')

def restore_sql(
		target_database_name=Config.database.db_name,
		workingdir='workingdir'):
	Log.debug(2,'Entering restore_sql()')
	git = pygitlib(workingdir,init=True)
	with open(current_join_path(workingdir,Config.git.filename)) as fin:
		raw = fin.read()
	with open(os.path.join('.','temp.sql'),'w') as fout:
		r = raw.split('\\\\n')
		fout.write(b64decrypt(r[0],r[1],r[2]))
	__execute_sql()
	os.remove(os.path.join('.','temp.sql'))
	Log.debug(2,'Exiting restore_sql()')

def __execute_sql(sql_filename='temp.sql'):
	with open(os.path.join('.',sql_filename)) as fin:
		with MainDatabase() as db:
			for x in fin.read().split(';'):
				db.execute(x)

class sql_backup_daemon(Thread):
	def __init__(
		self,
		target_dir='workingdir',
		DB_NAME=Config.database.db_name,
		sub_folder_name='sqlbkup'):
		Log.debug(2,'Entering sql_backup_daemon.__init__()')
		Thread.__init__(self)
		if os.path.isdir(target_dir):
			self.git = pygitlib(target_dir,init=True)
			self.git.configure_create()
			self.git.fetch()
			self.git.pull()
			self.git.revert_configure()
		else:
			self.git = pygitlib(target_dir,True)
		self.target_dir = target_dir
		self.DB_NAME = DB_NAME
		self.daemon = True
		self.sub_folder_name = sub_folder_name
		#self.Lock = Lock()
		Log.debug(2,'Exiting sql_backup_daemon.__init__()')

	def run(self):
		Log.debug(2,'Start sql_backup_daemon Thread')
		while True:
			Log.info('[Daemon] Starting backup')
			backup_and_encrypt(self.DB_NAME,self.target_dir,self.sub_folder_name)
			self.git.add([Config.git.filename])
			self.git.commit('Daily backup');
			self.git.configure_create()
			self.git.push()
			self.git.revert_configure()
			Log.info('[Daemon] Backup successful')
			time.sleep(60*60)

