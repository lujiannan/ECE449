import sys
import logging

FILE_NAME = 'chromosomes.log'

def singleton(cls):
	instances = {}
	def get_instance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return get_instance()

@singleton
class Logger():
	def __init__(self):
		# logging.basicConfig(stream=sys.stdout, format='[%(levelname)s] %(message)s', level=logging.INFO)
		logging.basicConfig(
			filename=FILE_NAME,
			format='[%(asctime)s]:[%(levelname)s] %(message)s',
			level=logging.INFO,
			datefmt='%H:%M:%S')
		self.log = logging.getLogger('root')