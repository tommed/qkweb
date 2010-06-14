"""
QKWEB - SCAFFOLD

This file declares the handler required for creating CRUD pages
"""
from qkweb.models import BaseHandler

class ScaffoldHandler(BaseHandler):
	def __init__(self, klass, db, model, view_dir='.'):
		BaseHandler.__init__(self, view_dir=view_dir)
		self.db = db
		self.model = model
		self.klass = klass

	def index_(self, form):
		self.set_mime('text/html')
		print "TODO! list all items"

	def read_(self, id):
		self.set_mime('text/html')
		print "TODO! read item %d" % id

	def update_form_(self, id):
		self.set_mime('text/html')
		print "TODO! draw update form item %d" % id

	def create_form_(self):
		self.set_mime('text/html')
		print "TODO! draw create form"

	def update_(self, form):
		self.set_mime('text/html')
		id = int(form.getvalue('id'))
		print "TODO! update item %d" % id

	def create_(self, form):
		self.set_mime('text/html')
		print "TODO! create new item"

	def delete_(self, id):
		self.set_mime('text/html')
		print "TODO! delete item %d" % id

	def GET(self, form):
		if 'id' not in form and 'a' not in form:
			index_(self, form)
		elif 'a' not in form:
			read_(self, int(form.getvalue('id')))
		elif form.getvalue('a') == 'update':
			update_form_(self, int(form.getvalue('id')))
		elif form.getvalue('a') == 'create':
			create_form_(self)

	def POST(self, form):
		if 'id' not in form and 'a' not in form:
			create_(self, form)
		elif 'a' not in form:
			update_(self, form)
		elif form.getvalue('a') == 'update':
			update_(self, form)
		elif form.getvalue('a') == 'create':
			create_(self, form)
		elif form.getvalue('a') == 'delete':
			delete_(self, int(form.getvalue('id')))


