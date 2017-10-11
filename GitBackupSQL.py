# -*- coding: utf-8 -*-
# GitBackupSQL.py
# Copyright (C) 2017 Too-Naive and contributors
#
# This module is part of gu-cycle-bot and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
import libpy.Config as Config
from git import Repo,Git
import libpy.Log as Log
import shutil,os
from libpy.MainDatabase import MainDatabase
from base64 import b64encode,b64decode
from libpy.Encrypt import b64encrypt,b64decrypt

wkdir = 'workingdir'


class pygitlib:
	def __init__(self,init=False):
		Log.debug(2,'Entering pygitlib.__init__(), init mode is {}',Log.tfget(init))
		Log.info('Initializing pygitlib...')
		self.repo = None
		if not init:
			self.load_git_dir()
		else:
			self.clone()
		Log.info('Initialized pygitlib() successful')
		Log.debug(2,'Exiting pygitlib.__init__()')

	def clone(self):
		Log.debug(2,'Entering pygitlib.clone()')
		branch = 'master'
		if Config.git.branch:
			branch = Config.git.branch
		Log.debug(3,'[branch is {}]',branch)
		if os.path.isdir(wkdir):
			Log.debug(3,'Dir is already exist, delete it')
			shutil.rmtree(wkdir)
		ssh_key = os.path.join('.',Config.git.ssh_key)
		Log.debug(3,'[ssh_key is locate \'{}\']',ssh_key)
		with Git().custom_environment(GIT_SSH = ssh_key)
			Log.debug(3,'Set custom environment successful')
			self.repo = Repo.clone_from(Config.git.source,wkdir,branch=branch)
		Log.debug(2,'Exiting pygitlib.clone()')

	def load_git_dir(self,target=wkdir):
		Log.debug(2,'Entering pygitlib.load_git_dir()')
		if not self.repo:
			self.repo = Repo(wkdir)
			assert repo.remotes.origin.exists()
		Log.debug(2,'Exiting pygitlib.load_git_dir()')

	def fetch(self):
		self.repo.remotes.origin.fetch()

	def pull(self):
		self.repo.remotes.origin.pull()

	def commit(self,commitmsg):
		self.repo.git.commit('-m',commitmsg)

	def addall(self):
		self.repo.index.add(u=True)

	def push(self):
		self.repo.origin.push()


class bklib:
	def backup(self,query_sql_statements,a_mode=True):
		Log.debug(2,'Entering bklib.backup(), a mode is {}',Log.tfget(continue_mode))
		Log.debug(3,'[query_sql_statements = \"{}\"]',query_sql_statements)
		write_mode = 'a'
		if not a_mode:
			write_mode = 'w'
		with MainDatabase() as db:
			r = db.query(query_sql_statements)
		finalfile = ''
		for x in r:
			st = ''
			for y in x:
				st += b64encode(str(y)) + '\\n'
			finalfile += st + '\\\\n'
		with open(os.path.join('.',
			os.path.join(wkdir,Config.git.filenmae)),
					write_mode) as fout:
			if write_mode:
				fout.write('\\\\n')
			a,b,c = b64encrypt(finalfile)
			fout.write(a+'\\n'+b+'\\n'+c)
		Log.debug(2,'Exiting bklib.backup()')

	def restore(self,sql_structure_statements):
		Log.debug(2,'Entering bklib.restore()')
		with open(os.path.join('.',
			os.path.join(wkdir,Config.git.filenmae))) as fin:
			raw = fin.read().split('\\\\n')
		
		Log.debug(2,'Exiting bklib.restore()')