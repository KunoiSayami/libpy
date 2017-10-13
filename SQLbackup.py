# -*- coding: utf-8 -*-
# SQLbackup.py
# Copyright (C) 2017 Too-Naive and contributors
#
# This module is part of gu-cycle-bot and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
#
# This python file download from https://goo.gl/9QWqZR
# On the basis of the original made a few modifications
###########################################################
#
# This python script is used for mysql database backup
# using mysqldump utility.
#
# Written by : Rahul Kumar
# Website: http://tecadmin.net
# Created date: Dec 03, 2013
# Last modified: Dec 03, 2013
# Tested with : Python 2.6.6
# Script Revision: 1.1
#
##########################################################
# Import required python libraries
import os
import time
import datetime

import libpy.Log
import libpy.Config
# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup. 
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databses names one on each line and assignd to DB_NAME variable.

def func_backup_sql(
		DB_NAME=Config.database.db_name,
		BACKUP_PATH = os.getcwd(),
		DATETIME=time.strftime('%m%d%Y-%H%M%S')):
	Log.debug(2,'Entering func_backup_sql()')
	DB_HOST = Config.database.host
	DB_USER = Config.database.user
	DB_USER_PASSWORD = Config.database.passwd
	#DB_NAME = '/backup/dbnames.txt'

	# Getting current datetime to create seprate backup folder like "12012013-071334".
	#DATETIME=time.strftime('%m%d%Y-%H%M%S')

	TODAYBACKUPPATH = BACKUP_PATH + DATETIME

	# Checking if backup folder already exists or not. If not exists will create it.
	Log.debug(3,"creating backup folder")
	if not os.path.exists(TODAYBACKUPPATH):
			os.makedirs(TODAYBACKUPPATH)

	# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
	Log.debug(3,"checking for databases names file.")
	if os.path.exists(DB_NAME):
			file1 = open(DB_NAME)
			multi = True
			Log.debug(3,"Databases file found...")
			Log.debug(3,"Starting backup of all dbs listed in file {}", DB_NAME)
	else:
			Log.debug(3,"Databases file not found...")
			Log.debug(3,"Starting backup of database {}", DB_NAME)
			multi = False

	# Starting actual database backup process.
	if multi:
		in_file = open(DB_NAME,"r")
		flength = len(in_file.readlines())
		in_file.close()
		p = 1
		dbfile = open(DB_NAME,"r")

		while p <= flength:
				db = dbfile.readline()   # reading database name from file
				db = db[:-1]         # deletes extra line
				dumpcmd = 'mysqldump -u {} -p{} {} > {}.sql'.format(DB_USER,DB_USER_PASSWORD,db,os.path.join(TODAYBACKUPPATH,db))
				os.system(dumpcmd)
				p = p + 1
		dbfile.close()
	else:
		db = DB_NAME
		dumpcmd = 'mysqldump -u {} -p{} {} > {}.sql'.format(DB_USER,DB_USER_PASSWORD,db,os.path.join(TODAYBACKUPPATH,db))
		os.system(dumpcmd)
	Log.debug(3,"Backup script completed")
	Log.debug(3,"Your backups has been created in '{}' directory",TODAYBACKUPPATH)
	Log.info('[{}] SQL backup successful',Log.get_name())
	Log.debug(3,'Exiting func_backup_sql()')
