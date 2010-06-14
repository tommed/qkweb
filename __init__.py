import cgitb
from qkweb.scaffold import ScaffoldHandler

class Runner:
	"""used to start a derrivative of BaseHandler"""
	@staticmethod
	def run(handler):
		"""run the given handler (derrives from BaseHandler)"""
		cgitb.enable()
		handler.run()

	@staticmethod
	def scaffold(klass, db, model, base_template=None, view_dir='.'):
		cgitb.enable()
		ScaffoldHandler(klass, db, model, view_dir=view_dir).run()

