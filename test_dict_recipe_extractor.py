import dict_recipe_extractor
import unittest
import datetime


class Test(unittest.TestCase):
    def setUp(self):
        self.set_testing_arguments()
        self.set_tested_objects()
        self.set_test_expected_results()

    def set_testing_arguments(self):
        dict_recipe_path = r'test/dict_recipe_extractor.txt'
        with open(dict_recipe_path, 'r', encoding='utf-8') as dict_recipe_file:
            self.test_recipe = eval(dict_recipe_file.read())

    def set_tested_objects(self):
        self.hops_extractor = dict_recipe_extractor.HopsExtractor(self.test_recipe)
        self.miscellaneous_extractor = dict_recipe_extractor.MiscellaneousExtractor(self.test_recipe)
        self.fermentables_extractor = dict_recipe_extractor.FermentablesExtractor(self.test_recipe)
        self.mash_steps_extractor = dict_recipe_extractor.MashStepsExtractor(self.test_recipe)
        self.parameters_extractor = dict_recipe_extractor.ParametersExtractor(self.test_recipe)
        self.recipe_name_extractor = dict_recipe_extractor.RecipeNameExtractor(self.test_recipe)

    def set_test_expected_results(self):
        self.hops_result = [
            {'NAME': 'CP Columbus 2017', 'AMOUNT': 3, 'USE': 'Boil', 'TIME': datetime.timedelta(seconds=2700)},
            {'NAME': 'TB Citra 2019', 'AMOUNT': 75, 'USE': 'Aroma', 'TIME': datetime.timedelta(seconds=1800)}]
        self.hops_additional_result = 78
        self.miscellaneous_result = [{'NAME': 'Gypsum (Calcium Sulfate)', 'USE': 'Mash', 'AMOUNT': 5.25,
                                      'TIME': datetime.timedelta(seconds=0)},
                                     {'NAME': "Baker's Dry Yeast", 'USE': 'Sparge', 'AMOUNT': 7.05,
                                      'TIME': datetime.timedelta(seconds=0)}]
        self.miscellaneous_additional_result = True
        self.fermentables_result = [{'NAME': 'Weyermann Słód Barke pilzneński 4 EBC', 'AMOUNT': 3.91},
                                    {'NAME': 'Weyermann Słód wiedeński 7,5 EBC', 'AMOUNT': 0.21}]
        self.fermentables_additional_result = 4.12
        self.mash_steps_result = [{'NAME': 'Mash In', 'STEP_TIME': datetime.timedelta(seconds=0), 'STEP_TEMP': 55},
                                  {'NAME': 'Mash Out', 'STEP_TIME': datetime.timedelta(seconds=1800), 'STEP_TEMP': 75}]
        self.mash_steps_additional_result = 'Lupulus Mash'
        self.parameters_result = {
            'GRAIN_TEMP': 22.2, 'WATER_GRAIN_RATIO': 2.6, 'INFUSE_VOLUME': 13.36, 'INFUSE_TEMP': 59.8,
            'MLT_DEADSPACE_VOLUME': 9.24, 'SPARGE_VOLUME': 20.81, 'BOIL_VOLUME': 20.81, 'PRE_BOIL_OG': 1.046,
            'BOIL_TIME': datetime.timedelta(seconds=3600), 'TRUB_CHILLER_VOLUME': 5.0,
            'COOLING_SHRINKAGE_PERCENTAGE': 4.0, 'EVAPORATION_PERCENTAGE': 2.4, 'POST_BOIL_VOLUME': 20.31,
            'KNOCKOUT_VOLUME': 19.5, 'BATCH_VOLUME': 14.5, 'FERMENTATION_TEMP': 20.0, 'OG': 1.049,
            'IBU': 38.2, 'RECIPE_NAME': '#079 Session IPA', 'BATCH_NUMBER': 79, 'BATCH_NAME': 'Session IPA'}
        self.parameters_additional_result = 'HS_3'
        self.user_settings_result = []
        self.user_settings_additional_result = '#079 Session IPA'

    def test_hops_extract(self):
        self.hops_extractor.extract()
        self.assertEqual(self.hops_extractor.get_extracted_records(), self.hops_result)
        self.assertEqual(self.hops_extractor.get_additional_parameter(), self.hops_additional_result)

    def test_miscellaneous_extract(self):
        self.miscellaneous_extractor.extract()
        self.assertEqual(self.miscellaneous_extractor.get_extracted_records(), self.miscellaneous_result)
        self.assertEqual(self.miscellaneous_extractor.get_additional_parameter(), self.miscellaneous_additional_result)

    def test_fermentables_extract(self):
        self.fermentables_extractor.extract()
        self.assertEqual(self.fermentables_extractor.get_extracted_records(), self.fermentables_result)
        self.assertEqual(self.fermentables_extractor.get_additional_parameter(), self.fermentables_additional_result)

    def test_mash_steps_extract(self):
        self.mash_steps_extractor.extract()
        self.assertEqual(self.mash_steps_extractor.get_extracted_records(), self.mash_steps_result)
        self.assertEqual(self.mash_steps_extractor.get_additional_parameter(), self.mash_steps_additional_result)

    def test_parameters_extract(self):
        self.parameters_extractor.extract()
        self.assertEqual(self.parameters_extractor.get_extracted_records(), self.parameters_result)
        self.assertEqual(self.parameters_extractor.get_additional_parameter(), self.parameters_additional_result)

    def test_recipe_name(self):
        self.recipe_name_extractor.extract()
        self.assertEqual(self.recipe_name_extractor.get_extracted_records(), self.user_settings_result)
        self.assertEqual(self.recipe_name_extractor.get_additional_parameter(), self.user_settings_additional_result)


unittest.main()
