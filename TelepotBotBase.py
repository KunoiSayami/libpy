# -*- coding: utf-8 -*-
# TelepotBotBase.py
# Copyright (C) 2017 Too-Naive and contributors
#
# This module is part of gu-cycle-bot and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
import telepot
import sys
import io
import time
import json
import threading
import traceback
import collections
import bisect
import libpy.Log as Log
import telepot.exception
import urllib3

try:
    import Queue as queue
except ImportError:
    import queue


class Bot(telepot.Bot):
	def message_loop(self, callback=None, relax=0.1,
					 timeout=20, allowed_updates=None,
					 source=None, ordered=True, maxhold=3,
					 run_forever=False):
		if callback is None:
			callback = self.handle
		elif isinstance(callback, dict):
			callback = flavor_router(callback)

		collect_queue = queue.Queue()

		def collector():
			while 1:
				try:
					item = collect_queue.get(block=True)
					callback(item)
				except:
					traceback.print_exc()

		def relay_to_collector(update):
			key = _find_first_key(update, ['message',
										   'edited_message',
										   'channel_post',
										   'edited_channel_post',
										   'callback_query',
										   'inline_query',
										   'chosen_inline_result',
										   'shipping_query',
										   'pre_checkout_query'])
			collect_queue.put(update[key])
			return update['update_id']

		def get_from_telegram_server():
			offset = None  # running offset
			allowed_upd = allowed_updates
			while 1:
				try:
					result = self.getUpdates(offset=offset,
											 timeout=timeout,
											 allowed_updates=allowed_upd)

					allowed_upd = None

					if len(result) > 0:
						offset = max([relay_to_collector(update) for update in result]) + 1

				except telepot.exception.BadHTTPResponse as e:
					traceback.print_exc()
					Log.error('Catched telepot.exception.BadHTTPResponse')
					if e.status == 502:
						time.sleep(30)
				except urllib3.exceptions.ReadTimeoutError:
					Log.error('Catched requests.exceptions.ReadTimeoutError')
					pass
				except:
					traceback.print_exc()
				finally:
					time.sleep(relax)

		def dictify3(data):
			if type(data) is bytes:
				return json.loads(data.decode('utf-8'))
			elif type(data) is str:
				return json.loads(data)
			elif type(data) is dict:
				return data
			else:
				raise ValueError()

		def dictify27(data):
			if type(data) in [str, unicode]:
				return json.loads(data)
			elif type(data) is dict:
				return data
			else:
				raise ValueError()

		def get_from_queue_unordered(qu):
			dictify = dictify3 if sys.version_info >= (3,) else dictify27
			while 1:
				try:
					data = qu.get(block=True)
					update = dictify(data)
					relay_to_collector(update)
				except:
					traceback.print_exc()

		def get_from_queue(qu):
			dictify = dictify3 if sys.version_info >= (3,) else dictify27

			max_id = None
			buffer = collections.deque()
			qwait = None
										 
			while 1:
				try:
					data = qu.get(block=True, timeout=qwait)
					update = dictify(data)

					if max_id is None:
						max_id = relay_to_collector(update)

					elif update['update_id'] == max_id + 1:
						max_id = relay_to_collector(update)

						if len(buffer) > 0:
							buffer.popleft()
							while 1:
								try:
									if type(buffer[0]) is dict:
										max_id = relay_to_collector(buffer.popleft())
									else:
										break
								except IndexError:
									break

					elif update['update_id'] > max_id + 1:
						nbuf = len(buffer)
						if update['update_id'] <= max_id + nbuf:
							buffer[update['update_id'] - max_id - 1] = update
						else:
							expire = time.time() + maxhold
							for a in range(nbuf, update['update_id']-max_id-1):
								buffer.append(expire)
							buffer.append(update)

					else:
						pass

				except queue.Empty:
					while 1:
						try:
							if type(buffer[0]) is dict:
								max_id = relay_to_collector(buffer.popleft())
							else:
								expire = buffer[0]
								if expire <= time.time():
									max_id += 1
									buffer.popleft()
								else:
									break  # non-expired
						except IndexError:
							break  # buffer empty
				except:
					traceback.print_exc()
				finally:
					try:
						qwait = buffer[0] - time.time()
						if qwait < 0:
							qwait = 0
					except IndexError:
						qwait = None

		collector_thread = threading.Thread(target=collector)
		collector_thread.daemon = True
		collector_thread.start()

		if source is None:
			message_thread = threading.Thread(target=get_from_telegram_server)
		elif isinstance(source, queue.Queue):
			if ordered:
				message_thread = threading.Thread(target=get_from_queue, args=(source,))
			else:
				message_thread = threading.Thread(target=get_from_queue_unordered, args=(source,))
		else:
			raise ValueError('Invalid source')

		message_thread.daemon = True
		message_thread.start()

		self._scheduler.on_event(collect_queue.put)
		self._scheduler.run_as_thread()

		if run_forever:
			if _isstring(run_forever):
				print(run_forever)
			while 1:
				time.sleep(10)

