# QkWeb

* Project: QkWeb
* Author: Tom <tom.medhurst@gmail.com>
* License: GPL v3
* Description: Yet another rapid application development library for Python web developers.

## Components

 * Jinja2 template system
 * CGI interface (for now!)
 * ZODB storage (no more relational tables to create yippee!)
 * Routing and general 'glue' code is my own creation

## Quick Start

The best way to describe how quickly you can write a web application with qkweb, is to show you
a demo. This demo takes a first name and surname and posts it to a new view. It shows you the 
following:

 * How to load templates
 * How to derrive from a base template
 * How to handle form data from the controller and the view
 * How to handle GET and POST requests

### index.cgi

<pre><code>
#!/usr/bin/env python
from qkweb.models import BaseHandler, Runner

class IndexHandler(BaseHandler):
	def GET(self, form):
		self.render_template('index.get.html', vars())

	def POST(self, form):
		name = form.getvalue('name')
		self.render_template('index.post.html', vars())

if __name__ == "__main__":
	Runner.run(IndexHandler())
</code></pre>

### index.get.html

<pre><code>
{% extends "_base.html" %}
{% block title %}Index Page{% endblock %}
{% block body %}
	<h1>Welcome!</h1>
	<p>This site uses jinja2 templates!</p>
	<form method="post" action="index.cgi">
		<input type="text" name="name" placeholder="Enter your Name"/>
		<input type="text" name="lastname" placeholder="Enter you Surname"/>
		<input type="submit" value="send..."/>
	</form>
{% endblock %}
</code></pre>

### index.post.html

<pre><code>
{% extends "_base.html" %}
{% block title %}Index Page{% endblock %}
{% block body %}
	<h1>Welcome {{ name }}!</h1>
	<p>Your surname is {{ form.getvalue('lastname') }}</p>
{% endblock %}
</code></pre>

### _base.html

<pre><code>
<!doctype html>
<html lang="en">
	<head>
		<title>{% block title %}Jinja2 Templatei{% endblock %}</title>
	</head>
	<body>
		{% block body %}Hello World!{% endblock %}
	</body>
</html>
</code></pre>

