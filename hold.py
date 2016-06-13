@ddt
class TestUserModelMethods(unittest.TestCase):
	"""
	This is a preliminary documentation
		lol but here is more with an endline
	"""

	def startUp(self, expected_output=None):
		"""
		 printer: a pretty_printer 
		"""
		self.printer = pprint.PrettyPrinter(indent=1).pprint

	def tearDown(self, expected_output=None):
		"""
		"""
		pass

	def test_convert_from_dict(self, user_dict, holder, expected_output=None):
		"""
		convert from User Dictionary format into User object
		"""
		pass



""" end of file """


