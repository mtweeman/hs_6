import threading
import hashlib
import xml.etree.ElementTree
import xml.etree.ElementTree as element_tree


class RecipeMonitor(threading.Thread):
    def __init__(self, recipe_processor, gui_element, queue):
        threading.Thread.__init__(self, daemon=True)
        self.__recipe_processor = recipe_processor
        self.__gui_element = gui_element
        self.__queue = queue

        self.__recipe_path = r'recipe\recipe.xml'
        self.__previous_md5 = None

        self.start()

    def run(self):
        while True:
            self.__detect_file()

    def __detect_file(self):
        imported_recipe = self.__open_recipe_file()

        if imported_recipe:
            new_md5 = self.__calculate_checksum(imported_recipe)

            if new_md5 != self.__previous_md5:
                self.__previous_md5 = new_md5

                self.__process_file()

    def __open_recipe_file(self):
        try:
            with open(self.__recipe_path, 'rb') as recipe_file:
                imported_recipe = recipe_file.read()
        except:
            pass
        else:
            return imported_recipe

    def __calculate_checksum(self, imported_recipe):
        md5 = hashlib.md5(imported_recipe).hexdigest()
        return md5

    def __process_file(self):
        root = self.__get_tree_root()

        if root:
            self.__recipe_processor.import_file(root)
            recipe = self.__recipe_processor.get_recipe()
            additional_parameters = self.__recipe_processor.get_additional_parameters()
            self.__queue.put(recipe)
            self.__queue.put(additional_parameters)
            self.__gui_element.event_generate('<<processed_recipe>>')

    def __get_tree_root(self):
        try:
            root = element_tree.parse(self.__recipe_path).getroot()
        except xml.etree.ElementTree.ParseError:
            pass
        else:
            return root
