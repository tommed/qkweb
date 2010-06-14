import cgitb

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

