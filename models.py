import cgi
from datetime import datetime
import os
import cgitb
import sys
import re
sys.path.append(os.path.dirname(__file__))
from jinja2 import Template, Environment, FileSystemLoader

t_minute = 1 * 60
t_hour = t_minute * 60
t_day = t_hour * 24

def datetimeformat(date, format="%Y-%m-%d %H:%M"):
	now = datetime.utcnow()
	days = (now - date).days
	if days == 1:
		return "yesterday"
	if days > 1 and days < 5:
		return "%d days ago" % (days)
	elif date.year == now.year and date.month == now.month and date.day == now.day:
		secs = (now - date).seconds
		if secs > t_hour:
			return "%d hours ago" % (secs / 60 / 60)
		elif secs > t_minute:
			return "%d mins ago" % (secs / 60)
		else:
			return "%d seconds ago" % secs
	else:
		return date.strftime(format)

def htmlescape(value):
	return value.replace('<','&lt;').replace('>','&gt;').replace('\n', '<br/>\r')

def linkify(value):
	return re.sub(r'(http(s)?://([^\s]+))', r'<a href="\1">\1</a>', value)

def option(value, compareTo, trueResult='selected', falseResult=''):
	if str(value) == str(compareTo):
		return trueResult
	else:
		return falseResult

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
		print "Content-Type: %s; charset=UTF-8\n" % mimeType
		self.mime_set = True

	def render_template(self, viewfile, context, mime="text/html"):
		"""render a response based on a template"""
		if not self.mime_set:
			self.set_mime(mime)
		env = Environment(loader=FileSystemLoader(self.view_dir))
		env.filters['datetimeformat'] = datetimeformat
		env.filters['option'] = option
		env.filters['escape'] = htmlescape
		env.filters['linkify'] = linkify
		template = env.get_template(viewfile)
		print template.render(context).encode('utf-8')

	def redirect(self, url):
		"""redirect to another url. Doesn't work if set_mime is already called"""
		print "Status: 302 Found"
		print "Location: %s\n" % url


