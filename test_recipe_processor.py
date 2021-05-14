import recipe_processor
import unittest
from xml.etree import ElementTree
import datetime


class Test(unittest.TestCase):
    def setUp(self):
        self.set_testing_arguments()
        self.set_tested_objects()
        self.set_test_expected_results()

    def set_testing_arguments(self):
        xml_recipe_path = r'test/xml_recipe_processor.xml'
        self.test_recipe = ElementTree.parse(xml_recipe_path).getroot()

    def set_tested_objects(self):
        self.xml_recipe = recipe_processor.XMLRecipeProcessor()

    def set_test_expected_results(self):
        recipe_path = r'test/xml_recipe_processor_result.txt'
        with open(recipe_path, 'r', encoding='utf-8') as xml_recipe_result:
            self.recipe_result = eval(xml_recipe_result.read())

    def test_import_file(self):
        self.xml_recipe.import_file(self.test_recipe)
        self.assertEqual(self.xml_recipe.get_recipe(), self.recipe_result)


unittest.main()
