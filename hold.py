import unittest
from unittest.mock import patch, Mock, MagicMock
from deepdiff import DeepDiff
import logging
import sys
import locale
import os
import json
from bigml.api import FINISHED
from bigml.api import (get_status, BigML, get_model_id,
from ddt import ddt, data, unpack
import pprint

@ddt
class TestcomplexMethods(unittest.TestCase):

	def teardown(self, expected_output=None):
		pass

	def startup(self, expected_output=None):
		"""
		 printer: a pretty_printer 
		"""
		self.printer = pprint.PrettyPrinter(indent=2).pprint

	@data(

	)
	@unpack
	def test_retrieve_resource(self, api, resource_id, query_string='', expected_output=None):
		"""
		 Retrieves resource info either from a local repo orfrom the remote server
		"""
		pass

	@data(

	)
	@unpack
	def test_basemodel_resource(self, expected_output=None):
		"""
		Returns the model resource ID
		"""
		pass

	@data(

	)
	@unpack
	def test_basemodel___init__(self, model, api=None, expected_output=None):
		pass

	@data(

	)
	@unpack
	def test_print_importance(self, instance, out=sys.stdout, expected_output=None):
		"""
		Print a field importance structure
		"""
		pass

	@data(

	)
	@unpack
	def test_basemodel_field_importance_data(self, expected_output=None):
		"""
		Returns field importance related info
		"""
		pass

	@data(

	)
	@unpack
	def test_extract_objective(self, objective_field, expected_output=None):
		"""
		Extract the objective field id from the model structure
		"""
		pass

	@data(

	)
	@unpack
	def test_basemodel_print_importance(self, out=sys.stdout, expected_output=None):
		"""
		Prints the importance data
		"""
		pass

""" end of file """
