import ZODB
import transaction
from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
from persistent import Persistent

class DbAdapter:
	def __init__(self, path="data.db"):
		self.path = path
		self.storage = FileStorage(path)
		
	def connect(self):
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
		if self.db != None:
			self.db.close()


__all__ = ["DbAdapter", "Persistent"]
