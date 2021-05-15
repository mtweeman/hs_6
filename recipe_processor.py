from abc import ABC, abstractmethod
from dict_recipe_extractor import DictRecipeExtractor
import xmltodict


class RecipeProcessor(ABC):
    @abstractmethod
    def import_file(self, file):
        pass


class XMLRecipeProcessor(RecipeProcessor):
    def __init__(self):
        self.__recipe_dict = None
        self.__extractors = []
        self.__recipe = {}
        self.__additional_parameters = {}

    def import_file(self, xml):
        self.__create_dict(xml)
        self.__create_extractors_for_categories()
        self.__extract_categories_to_records()
        self.__add_records_to_recipe()

    def get_recipe(self):
        return self.__recipe

    def get_additional_parameters(self):
        return self.__additional_parameters

    def __create_dict(self, xml):
        xml = xmltodict.parse(xml)
        self.__recipe_dict = xml['RECIPES']['RECIPE']

    def __create_extractors_for_categories(self):
        for subclass in DictRecipeExtractor.__subclasses__():
            self.__extractors.append(subclass(self.__recipe_dict))

    def __extract_categories_to_records(self):
        for extractor in self.__extractors:
            extractor.extract()

    def __add_records_to_recipe(self):
        for extractor in self.__extractors:
            self.__recipe[extractor.get_category()] = extractor.get_extracted_records()
            self.__additional_parameters[extractor.get_category()] = extractor.get_additional_parameter()
