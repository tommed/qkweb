import cgi
import os
import cgitb
import sys
sys.path.append(os.path.dirname(__file__))
from jinja2 import Template, Environment, FileSystemLoader
from scaffold import ScaffoldHandler

class Runner:
	"""used to start a derrivative of BaseHandler"""
	@staticmethod
	def run(handler):
		"""run the given handler (derrives from BaseHandler)"""
		cgitb.enable()
		handler.run()

	def scaffold(klass, db, model, base_template=None, view_dir='.'):
		cgitb.enable()
		ScaffoldHandler(klass, db, model, view_dir=view_dir).run()

class BaseHandler:
	def __init__(self, view_dir='.'):
		self.mime_set = False
		self.view_dir = view_dir

	"""the abstract base class for all request handlers"""
	def run(self):
		"""the main entry point for the handler"""
		form = cgi.FieldStorage()
		method = os.environ['REQUEST_METHOD']
		if method == "GET":
			self.GET(form)
		elif method == "POST":
			self.POST(form)

	def GET(self, form):
		"""virtual method for handling GET requests"""
		print "GET: not yet implemented"
		pass

	def POST(self, form):
		"""virtual method for handling POST requests"""
		print "POST: not yet implemented"
		pass

	def set_mime(self, mimeType="text/html"):
		print "Content-Type: %s\n" % mimeType
		self.mime_set = True

	def render_template(self, viewfile, context, mime="text/html"):
		"""render a response based on a template"""
		if not self.mime_set:
			self.set_mime(mime)
		env = Environment(loader=FileSystemLoader(self.view_dir))
		template = env.get_template(viewfile)
		print template.render(context)


