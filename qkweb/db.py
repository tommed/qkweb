import ZODB
import transaction
from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
from persistent import Persistent
import os

class DbAdapter:
	def __init__(self, path="data.db"):
		self.path = path
		
	def connect(self):
		self.storage = FileStorage(self.path)
		self.db = DB(self.storage)
		self.conn = self.db.open()
		return self.conn.root()

	def begin_transaction(self):
		transaction.begin()

	def commit(self):
		transaction.commit()

	def rollback(self):
		transaction.abort()

	def disconnect(self):
		self.conn.close()
		self.db.close()
		self.storage.close()
		if os.path.exists(self.path+'.lock'):
			os.remove(self.path+'.lock')


__all__ = ["DbAdapter", "Persistent"]
