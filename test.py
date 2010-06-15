import os
import cgi
import sys
import unittest
sys.path.append('../')
from qkweb.db import DbAdapter, Persistent
from qkweb import Runner
from qkweb.models import BaseHandler

db = DbAdapter(path="/tmp/test.db")
model = db.connect()

def set_cgi(method, qs):
	"""convenience method for quickly setting cgi method and querystring"""
	os.environ['REQUEST_METHOD'] = method
	if method == "GET":
		os.environ['QUERY_STRING'] = qs
	else:
		os.environ['QUERY_STRING'] = ''
		sys.stdin = MyStdin(qs)

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

class MyStdin:
	def __init__(self, string):
		self.string = string

	def read(self, arg1):
		return self.string


class BaseCase(unittest.TestCase):
	"""derrive all testcases from this class"""

	def reset_stdout(self):
		sys.stdout = sys.__stdout__

	def tearDown(self):
		sys.stdin = sys.__stdin__

	def capture_stdout(self, io):
 		sys.stdout = io

	def assertMime(self, mime, io):
		header = io.content[0]
		self.assertEqual(header, 'Content-Type: %s\n' % mime, 'mime type not correct:\n' + header)


####### Scaffold Tests ###########

class TestScaffold(BaseCase):
	"""test scaffold handler"""

	def test_create(self):
		set_cgi('GET', 'a=create')
		out = MyStdout()
		self.capture_stdout(out)
		Runner.scaffold(MockPersistentObject, db, model)
		self.reset_stdout()
		self.assertMime('text/html', out)
		html = '\n'.join(out.content)
		self.assertTrue(html.find('TODO! draw create form') != -1, 'TODO statement not found')

	def test_listall(self):
		set_cgi('GET', '')
		out = MyStdout()
		self.capture_stdout(out)
		Runner.scaffold(MockPersistentObject, db, model)
		self.reset_stdout()
		self.assertMime('text/html', out)
		html = '\n'.join(out.content)
		self.assertTrue(html.find('TODO! list all items') != -1)

	def test_postCreate1(self):
		set_cgi('POST', '')
		out = MyStdout()
		self.capture_stdout(out)
		Runner.scaffold(MockPersistentObject, db, model)
		self.reset_stdout()
		self.assertMime('text/html', out)
		html = '\n'.join(out.content)
		self.assertTrue(html.find('TODO! create new item') != -1)

	def test_showItem1(self):
		set_cgi('GET', 'id=123')
		out = MyStdout()
		self.capture_stdout(out)
		Runner.scaffold(MockPersistentObject, db, model)
		self.reset_stdout()
		self.assertMime('text/html', out)
		html = '\n'.join(out.content)
		self.assertTrue(html.find('TODO! read item 123') != -1)

	def test_editItem1(self):
		set_cgi('POST', 'id=123')
		out = MyStdout()
		self.capture_stdout(out)
		Runner.scaffold(MockPersistentObject, db, model)
		self.reset_stdout()
		self.assertMime('text/html', out)
		html = '\n'.join(out.content)
		self.assertTrue(html.find('TODO! update item 123') != -1)

	def test_showUpdate1(self):
		set_cgi('GET', 'id=123&a=update')
		out = MyStdout()
		self.capture_stdout(out)
		Runner.scaffold(MockPersistentObject, db, model)
		self.reset_stdout()
		self.assertMime('text/html', out)
		html = '\n'.join(out.content)
		self.assertTrue(html.find('TODO! draw update form item 123') != -1)

	def test_editItem2(self):
		set_cgi('POST', 'id=123&a=update')
		out = MyStdout()
		self.capture_stdout(out)
		Runner.scaffold(MockPersistentObject, db, model)
		self.reset_stdout()
		self.assertMime('text/html', out)
		html = '\n'.join(out.content)
		self.assertTrue(html.find('TODO! update item 123') != -1)

	def test_noGETDelete(self):
		set_cgi('GET', 'a=delete')
		out = MyStdout()
		self.capture_stdout(out)
		Runner.scaffold(MockPersistentObject, db, model)
		self.reset_stdout()
		self.assertMime('text/html', out)
		html = '\n'.join(out.content)
		self.assertTrue(html.find('NOT IMPLEMENTED') != -1)

	def test_deleteItem(self):
		set_cgi('POST', 'id=123&a=delete')
		out = MyStdout()
		self.capture_stdout(out)
		Runner.scaffold(MockPersistentObject, db, model)
		self.reset_stdout()
		self.assertMime('text/html', out)
		html = '\n'.join(out.content)
		self.assertTrue(html.find('TODO! delete item 123') != -1)

	def test_create2(self):
		set_cgi('POST', 'id=123&a=create')
		out = MyStdout()
		self.capture_stdout(out)
		Runner.scaffold(MockPersistentObject, db, model)
		self.reset_stdout()
		self.assertMime('text/html', out)
		html = '\n'.join(out.content)
		self.assertTrue(html.find('TODO! create new item') != -1, html)


####### Custom Handlers ###########

class TestHandler(BaseHandler):
	"""a test handler"""
	def GET(self, qs):
		self.set_mime('text/plain')
		print "TEST_GET"

	def POST(self, qs):
		self.set_mime('text/plain')
		print "TEST_POST"


class TestCustomHandler(BaseCase):
	""" test a custom handler"""
	
	def test_get(self):
		set_cgi('GET', '')
		out = MyStdout()
		self.capture_stdout(out)
		Runner.run(TestHandler())
		self.reset_stdout()
		self.assertMime('text/plain', out)
		html = '\n'.join(out.content)
		self.assertEqual(html, "Content-Type: text/plain\n\n\n\nTEST_GET\n\n")

	def test_post(self):
		set_cgi('POST', '')
		out = MyStdout()
		self.capture_stdout(out)
		Runner.run(TestHandler())
		self.reset_stdout()
		self.assertMime('text/plain', out)
		html = '\n'.join(out.content)
		self.assertEqual(html, "Content-Type: text/plain\n\n\n\nTEST_POST\n\n")


if __name__ == "__main__":
	unittest.main()
	db.disconnect()
