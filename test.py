import os
import cgi
import sys
import unittest
sys.path.append('../')
from qkweb.db import DbAdapter, Persistent
from qkweb import Runner

db = DbAdapter(path="/tmp/test.db")

def set_cgi(method, qs):
	"""convenience method for quickly setting cgi method and querystring"""
	os.environ['REQUEST_METHOD'] = method
	os.environ['QUERY_STRING'] = qs

class MockPersistentObject(Persistent):
	"""class we can test scaffold with"""
	def __init__(self, prop1, prop2):
		self.id = 0
		self.prop1 = prop1
		self.prop2 = prop2


class MyStdout:
	"""we'll be redirecting stdout to an instance of this class for testing"""
	def __init__(self):
		self.content = []

	def write(self, string):
		self.content.append(string)


class TestScaffold(unittest.TestCase):
	def reset_stdout_(self):
		sys.stdout = sys.__stdout__

	def capture_stdout_(self):
 		sys.stdout = self.stdout

	def assertMime(self, mime):
		header = self.stdout.content[0]
		self.assertEqual(header, 'Content-Type: %s\n' % mime, 'mime type not correct:\n' + header)

	def setUp(self):
		self.model = db.connect()
		self.stdout = MyStdout()

	def test_create(self):
		try:
			set_cgi('GET', 'a=create')
			self.capture_stdout_()
			Runner.scaffold(MockPersistentObject, db, self.model)
			self.reset_stdout_()
			self.assertMime('text/html')
			html = '\n'.join(self.stdout.content)
			self.assertTrue(html.find('TODO! draw create form') != -1, 'TODO statement not found')
		except Exception as ex:
			self.reset_stdout_()
			self.fail(str(ex))

	def test_listall(self):
		try:
			set_cgi('GET', '')
			self.capture_stdout_()
			Runner.scaffold(MockPersistentObject, db, self.model)
			self.reset_stdout_()
			html = '\n'.join(self.stdout.content)
			self.assertTrue(html.find('TODO! list all items') != -1)
		except Exception as ex:
			self.reset_stdout_()
			self.fail(str(ex))

	def test_postCreate1(self):
		try:
			set_cgi('POST', '')
			self.capture_stdout_()
			Runner.scaffold(MockPersistentObject, db, self.model)
			self.reset_stdout_()
			html = '\n'.join(self.stdout.content)
			self.assertTrue(html.find('TODO! create new item') != -1)
		except Exception as ex:
			self.reset_stdout_()
			self.fail(str(ex))

	def test_showItem1(self):
		try:
			set_cgi('GET', 'id=123')
			self.capture_stdout_()
			Runner.scaffold(MockPersistentObject, db, self.model)
			self.reset_stdout_()
			html = '\n'.join(self.stdout.content)
			self.assertTrue(html.find('TODO! read item 123') != -1)
		except Exception as ex:
			self.reset_stdout_()
			self.fail(str(ex))

	def test_editItem1(self):
		try:
			set_cgi('POST', 'id=123')
			self.capture_stdout_()
			Runner.scaffold(MockPersistentObject, db, self.model)
			self.reset_stdout_()
			html = '\n'.join(self.stdout.content)
			self.assertTrue(html.find('TODO! update item 123') != -1)
		except Exception as ex:
			self.reset_stdout_()
			self.fail(str(ex))

	def test_showUpdate1(self):
		try:
			set_cgi('GET', 'id=123&a=update')
			self.capture_stdout_()
			Runner.scaffold(MockPersistentObject, db, self.model)
			self.reset_stdout_()
			html = '\n'.join(self.stdout.content)
			self.assertTrue(html.find('TODO! draw update form item 123') != -1)
		except Exception as ex:
			self.reset_stdout_()
			self.fail(str(ex))

	def test_editItem2(self):
		try:
			set_cgi('POST', 'id=123&a=update')
			self.capture_stdout_()
			Runner.scaffold(MockPersistentObject, db, self.model)
			self.reset_stdout_()
			html = '\n'.join(self.stdout.content)
			self.assertTrue(html.find('TODO! update item 123') != -1)
		except Exception as ex:
			self.reset_stdout_()
			self.fail(str(ex))

	def test_noGETDelete(self):
		try:
			set_cgi('GET', 'a=delete')
			self.capture_stdout_()
			Runner.scaffold(MockPersistentObject, db, self.model)
			self.reset_stdout_()
			html = '\n'.join(self.stdout.content)
			self.assertFalse(html.find('TODO! delete item 123') != -1)
			print 'actual:', html
		except Exception as ex:
			self.reset_stdout_()
			self.fail(str(ex))

	def test_deleteItem(self):
		try:
			set_cgi('POST', 'id=123&a=delete')
			self.capture_stdout_()
			Runner.scaffold(MockPersistentObject, db, self.model)
			self.reset_stdout_()
			html = '\n'.join(self.stdout.content)
			self.assertTrue(html.find('TODO! delete item 123') != -1)
		except Exception as ex:
			self.reset_stdout_()
			self.fail(str(ex))

	def test_create2(self):
		try:
			set_cgi('POST', 'id=123&a=create')
			self.capture_stdout_()
			Runner.scaffold(MockPersistentObject, db, self.model)
			self.reset_stdout_()
			html = '\n'.join(self.stdout.content)
			self.assertTrue(html.find('TODO! create item 123') != -1)
		except Exception as ex:
			self.reset_stdout_()
			self.fail(str(ex))


if __name__ == "__main__":
	unittest.main()
	db.disconnect()
