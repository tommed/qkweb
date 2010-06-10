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

### _base.html

<pre><code>
&lt;doctype html&gt;
&lt;html lang="en"&gt;
	&lt;head&gt;
		&lt;title&gt; block title %}Jinja2 Templatei{% endblock %}&lt;title&gt;
	&lt;head&gt;
	&lt;body&gt;
		{% block body %}Hello World!{% endblock %}
	&lt;body&gt;
&lt;html&gt;
</code></pre>

### index.get.html

<pre><code>
{% extends "_base.html" %}
{% block title %}Index Page{% endblock %}
{% block body %}
	&lt;h1&gt;Welcome!&lt;h1&gt;
	&lt;p&gt;This site uses jinja2 templates!&lt;p&gt;
	&lt;form method="post" action="index.cgi"&gt;
		&lt;input type="text" name="name" placeholder="Enter your Name"/&gt;
		&lt;input type="text" name="lastname" placeholder="Enter you Surname"/&gt;
		&lt;input type="submit" value="send..."/&gt;
	&lt;form&gt;
{% endblock %}
</code></pre>

### index.post.html

<pre><code>
{% extends "_base.html" %}
{% block title %}Index Page{% endblock %}
{% block body %}
	&lt;h1&gt;Welcome {{ name }}!&lt;h1&gt;
	&lt;p&gt;Your surname is {{ form.getvalue('lastname') }}&lt;p&gt;
{% endblock %}
</code></pre>

