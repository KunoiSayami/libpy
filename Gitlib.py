# -*- coding: utf-8 -*-
# Gitlib.py
# Copyright (C) 2017-2018 Too-Naive and contributors
#
# This module is part of libpy and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
from libpy.Config import Config
from git import Repo,Git
import libpy.Log as Log
import shutil,os
import re,time
import libpy.util as util

wkdir = 'workingdir'

class source_not_found:
	pass

class pygitlib:
	def __init__(self,target=wkdir,init=False):
		Log.debug(2,'Entering pygitlib.__init__(), init mode is {}',Log.tfget(init))
		Log.info('Initializing pygitlib...')
		self.ssh_locate = os.path.join(os.path.join(os.path.expanduser('~'),'.ssh'))
		self.__initGitlib(self.ssh_locate)
		self.lockfile = os.path.join(self.ssh_locate,'libpy.lock')
		self.git_ssh_addr = self.__get_source_address()
		self.repo = None
		if not init:
			self.load_git_dir(target)
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
		Log.debug(3,'now at {}',os.getcwd())
		self.configure_create()
		#self.repo = Repo.clone_from(Config.git.source,wkdir,branch=branch)
		self.repo = Repo.clone_from('git@{}:{}'.format(
				'rf_def',self.__get_source_address()[1])
			,wkdir,branch=branch)
		self.revert_configure()
		Log.debug(2,'Exiting pygitlib.clone()')

	def load_git_dir(self,target=wkdir):
		Log.debug(2,'Entering pygitlib.load_git_dir()')
		if not self.repo:
			self.repo = Repo(wkdir)
			assert self.repo.remotes.origin.exists()
		Log.debug(2,'Exiting pygitlib.load_git_dir()')

	def fetch(self):
		Log.debug(2,'Entering pygitlib.fetch()')
		self.repo.remotes.origin.fetch()
		Log.debug(2,'Exiting pygitlib.fetch()')

	def pull(self):
		Log.debug(2,'Entering pygitlib.pull()')
		self.repo.remotes.origin.pull()
		Log.debug(2,'Exiting pygitlib.pull()')

	def commit(self,commitmsg):
		Log.debug(2,'Entering pygitlib.commit()')
		self.repo.git.commit('-m',"{}".format(commitmsg))
		Log.debug(2,'Exiting pygitlib.commit()')

	def add(self,__list):
		Log.debug(2,'Entering pygitlib.addall()')
		self.repo.index.add(__list)
		Log.debug(2,'Exiting pygitlib.addall()')

	def push(self):
		Log.debug(2,'Entering pygitlib.push()')
		self.repo.remotes.origin.push()
		Log.debug(2,'Exiting pygitlib.push()')

	def __get_source_address(self):
		Log.debug(2,'Entering pygitlib.__get_source_address()')
		r = re.match(r'^git@(.*):(.*\/.*\.git)$',Config.git.source)
		if not r:
			raise source_not_found()
		Log.debug(2,'Exiting pygitlib.__get_source_address()')
		return (r.group(1),r.group(2))

	def __aquire_lock(self):
		Log.debug(2,'Entering pygitlib.__aquire_lock()')
		while os.path.isfile(self.lockfile):
			time.sleep(0.1)
		with open(self.lockfile,'w'):
			pass
		Log.debug(2,'Exiting pygitlib.__aquire_lock()')

	def __release_lock(self):
		Log.debug(2,'Entering pygitlib.__release_lock()')
		os.remove(self.lockfile)
		Log.debug(2,'Exiting pygitlib.__release_lock()')

	def configure_create(self):
		Log.debug(2,'Entering pygitlib.configure_create()')
		self.__aquire_lock()
		try:
			if not os.path.isfile(util.parse_file_ssh_path('config')):
				with open(util.parse_file_ssh_path('config'),'w'):
					pass
			shutil.copy(util.parse_file_ssh_path('config'),
				util.parse_file_ssh_path('config_backup'))
			with open(util.parse_file_ssh_path('config'),'w') as fout:
				fout.write('Host rf_def\n\tHostName {}\n\tIdentityFile {}'.format(
					self.__get_source_address()[0],
					os.path.join(os.getcwd(),Config.git.ssh_key)))
		except source_not_found as e:
			self.__release_lock()
			Log.debug(2,'Exiting pygitlib.configure_create() (exception exit)')
			raise e
		Log.debug(2,'Exiting pygitlib.configure_create()')

	def revert_configure(self):
		Log.debug(2,'Entering pygitlib.revert_configure()')
		shutil.copy(util.parse_file_ssh_path('config_backup'),
			util.parse_file_ssh_path('config'))
		os.remove(util.parse_file_ssh_path('config_backup'))
		self.__release_lock()
		Log.debug(2,'Exiting pygitlib.revert_configure()')

	@staticmethod
	def __initGitlib(ssh_path):
		if not os.path.isfile(os.path.join(ssh_path,'.gitlib.bak')):
			if os.path.isfile(os.path.join(ssh_path,'config')):
				with open(os.path.join(ssh_path,'config')) as fin:
					with open(os.path.join(ssh_path,'.gitlib.bak'), 'w') as fout:
						fout.write(fin.read())
			else:
				with open(os.path.join(ssh_path,'.gitlib.bak'), 'w') as fout:
					pass
