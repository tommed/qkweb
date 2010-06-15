import cgi
import os
import cgitb
import sys
sys.path.append(os.path.dirname(__file__))
from jinja2 import Template, Environment, FileSystemLoader

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
		else:
			print "unsupported request method of %s" % method

	def GET(self, form):
		"""virtual method for handling GET requests"""
		print "GET: not yet implemented"

	def POST(self, form):
		"""virtual method for handling POST requests"""
		print "POST: not yet implemented"

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


