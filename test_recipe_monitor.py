import recipe_monitor
import unittest
from recipe_processor import XMLRecipeProcessor
from queue import Queue


class MockGUIElement:
    def __init__(self):
        self.processed_event = False

    def event_generate(self, event_name):
        self.processed_event = True


class Test(unittest.TestCase):
    def setUp(self):
        self.set_testing_arguments()
        self.set_tested_objects()
        self.set_test_expected_results()

    def set_testing_arguments(self):
        self.mock_gui_element = MockGUIElement()
        self.queue = Queue()

    def set_tested_objects(self):
        self.recipe_monitor = recipe_monitor.RecipeMonitor(XMLRecipeProcessor(), self.mock_gui_element, self.queue)

    def set_test_expected_results(self):
        self.recipe_processed = False

    def test_run(self):
        while not self.mock_gui_element.processed_event:
            pass

        self.assertEqual(False, self.queue.empty())
        self.assertEqual(2, self.queue.qsize())


unittest.main()
