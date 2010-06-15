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
		print "TODO! list all items"

	def read_(self, id):
		print "TODO! read item %d" % id

	def update_form_(self, id):
		print "TODO! draw update form item %d" % id

	def create_form_(self):
		print "TODO! draw create form"

	def update_(self, form):
		id = int(form.getvalue('id'))
		print "TODO! update item %d" % id

	def create_(self, form):
		print "TODO! create new item"

	def delete_(self, id):
		print "TODO! delete item %d" % id

	def GET(self, form):
		self.set_mime("text/html")
		if 'id' not in form and 'a' not in form:
			self.index_(form)
		elif 'a' not in form:
			self.read_(int(form.getvalue('id')))
		elif form.getvalue('a') == 'update':
			self.update_form_(int(form.getvalue('id')))
		elif form.getvalue('a') == 'create':
			self.create_form_()
		else:
			print "SCAFFOLD GET ACTION NOT IMPLEMENTED %s" % form.getvalue('a')

	def POST(self, form):
		self.set_mime("text/html")
		if 'id' not in form and 'a' not in form:
			self.create_(form)
		elif 'a' not in form:
			self.update_(form)
		elif form.getvalue('a') == 'update':
			self.update_(form)
		elif form.getvalue('a') == 'create':
			self.create_(form)
		elif form.getvalue('a') == 'delete':
			self.delete_(int(form.getvalue('id')))
		else:
			print "SCAFFOLD POST ACTION NOT IMPLEMENTED %s" % form.getvalue('a')


