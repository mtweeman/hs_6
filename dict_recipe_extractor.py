import datetime
from abc import ABC, abstractmethod


class DictRecipeExtractor(ABC):
    def __init__(self, recipe_dict):
        self._recipe = recipe_dict
        self._category = None
        self._entries = None
        self._extracted_records = []
        self._additional_parameter = None
        self._usage_ordered = None

    def extract(self):
        if self._category in self._recipe:
            self.__format_recipe()
            self.__extract_entries()
            self._sort_entries()
            self._calculate_additional_parameter()

    def get_extracted_records(self):
        return self._extracted_records

    def get_additional_parameter(self):
        return self._additional_parameter

    def get_category(self):
        return self._category

    def __format_recipe(self):
        single_entry = self.__check_entry_quantity(self._category, self._entries)
        if single_entry:
            self.__convert_single_entry_to_list(self._category, self._entries)

    def __check_presence(self, category):
        if category in self._recipe:
            return True

    def __check_entry_quantity(self, category, entry):
        single_entry = isinstance(self._recipe[category][entry], dict)
        return single_entry

    def __convert_single_entry_to_list(self, category, entry):
        self._recipe[category][entry] = list([self._recipe[category][entry]])

    def __extract_entries(self):
        if self._category in self._recipe:
            for entry in self._recipe[self._category][self._entries]:
                new_record = self._extract(entry)
                self.__add_to_extracted_records(new_record)

    @abstractmethod
    def _extract(self, entry):
        pass

    def __add_to_extracted_records(self, new_record):
        if new_record:
            self._extracted_records.append(new_record)

    def _sort_entries(self):
        if self._usage_ordered:
            self._extracted_records.sort(key=lambda k: (self._usage_ordered[k['USE']], -k['TIME']))

    def _calculate_additional_parameter(self):
        pass


class HopsExtractor(DictRecipeExtractor):
    def __init__(self, recipe_dict):
        DictRecipeExtractor.__init__(self, recipe_dict)
        self._category = 'HOPS'
        self._entries = 'HOP'
        self._usage_ordered = {'Mash': 0, 'First Wort': 1, 'Boil': 2, 'Aroma': 3}

    def _extract(self, entry):
        if entry['USE'] in self._usage_ordered:
            new_record = {'NAME': entry['NAME'],
                          'USE': entry['USE'],
                          'AMOUNT': int(round(1e3 * float(entry['AMOUNT']), 0)),
                          'TIME': datetime.timedelta(minutes=int(round(float(entry['TIME']), 0)))}
            return new_record

    def _calculate_additional_parameter(self):
        hops_weight = 0
        for record in self._extracted_records:
            hops_weight += record['AMOUNT']

        self._additional_parameter = hops_weight


class MiscellaneousExtractor(DictRecipeExtractor):
    def __init__(self, recipe_dict):
        DictRecipeExtractor.__init__(self, recipe_dict)
        self._category = 'MISCS'
        self._entries = 'MISC'
        self._usage_ordered = {'Mash': 0, 'Sparge': 1, 'Boil': 2, 'Primary': 3, 'Secondary': 4, 'Bottling': 5}

    def _extract(self, entry):
        self.__set_use_key(entry)

        new_record = {'NAME': entry['NAME'],
                      'USE': entry['USE'],
                      'AMOUNT': round(1e3 * float(entry['AMOUNT']), 2),
                      'TIME': datetime.timedelta(minutes=int(round(float(entry['TIME']), 0)))}
        return new_record

    def __set_use_key(self, entry):
        if not entry['USE']:
            entry['USE'] = 'Sparge'

    def _calculate_additional_parameter(self):
        for record in self._extracted_records:
            if record['NAME'] == "Baker's Dry Yeast":
                self._additional_parameter = True
                break


class FermentablesExtractor(DictRecipeExtractor):
    def __init__(self, recipe_dict):
        DictRecipeExtractor.__init__(self, recipe_dict)
        self._category = 'FERMENTABLES'
        self._entries = 'FERMENTABLE'

    def _extract(self, entry):
        new_record = {'NAME': entry['NAME'],
                      'AMOUNT': round(float(entry['AMOUNT']), 2)}
        return new_record

    def _calculate_additional_parameter(self):
        fermentables_weight = 0
        for record in self._extracted_records:
            fermentables_weight += record['AMOUNT']

        self._additional_parameter = round(fermentables_weight, 2)


class MashStepsExtractor(DictRecipeExtractor):
    def __init__(self, recipe_dict):
        DictRecipeExtractor.__init__(self, recipe_dict)
        self._category = 'MASH_STEPS'
        self._entries = 'MASH_STEP'
        self._usage_ordered = {'Mash In': 0, 'Beta 1': 1, 'Beta 2': 2, 'Alpha': 3, 'Mash Out': 4}

    def _extract(self, entry):
        new_record = {'NAME': entry['NAME'],
                      'STEP_TIME': datetime.timedelta(minutes=int(round(float(entry['STEP_TIME']), 0))),
                      'STEP_TEMP': int(round(float(entry['STEP_TEMP']), 0))}
        return new_record

    def _calculate_additional_parameter(self):
        self._additional_parameter = self._recipe['MASH']['NAME']

    def _sort_entries(self):
        if self._usage_ordered:
            self._extracted_records.sort(key=lambda k: (self._usage_ordered[k['NAME']]))


class ParametersExtractor(DictRecipeExtractor):
    def __init__(self, recipe_dict):
        DictRecipeExtractor.__init__(self, recipe_dict)
        self._extracted_records = {}
        self._category = 'PARAMETERS'
        self._entries = 'PARAMETER'

    def extract(self):
        self._extracted_records['GRAIN_TEMP'] = round(float(self._recipe['MASH']['GRAIN_TEMP']), 2)
        self._extracted_records['WATER_GRAIN_RATIO'] = round(
            float(self._recipe['MASH_STEPS']['MASH_STEP'][0]['WATER_GRAIN_RATIO'].
                  split()[0].replace(',', '.')), 1)
        self._extracted_records['INFUSE_VOLUME'] = round(
            float(self._recipe['MASH_STEPS']['MASH_STEP'][0]['DISPLAY_INFUSE_AMT'].split()[0]), 2)
        self._extracted_records['INFUSE_TEMP'] = round(
            float(self._recipe['MASH_STEPS']['MASH_STEP'][0]['INFUSE_TEMP'].split()[0]), 1)
        self._extracted_records['MLT_DEADSPACE_VOLUME'] = round(float(self._recipe['EQUIPMENT.LAUTER_DEADSPACE']), 2)
        self._extracted_records['SPARGE_VOLUME'] = round(float(self._recipe['SPARGE_VOLUME'].split()[0]), 2)
        self._extracted_records['BOIL_VOLUME'] = round(float(self._recipe['BOIL_SIZE']), 2)
        self._extracted_records['PRE_BOIL_OG'] = round(float(self._recipe['PRE_BOIL_OG'].split()[0]), 3)
        self._extracted_records['BOIL_TIME'] = datetime.timedelta(
            minutes=int(round(float(self._recipe['BOIL_TIME']), 0)))
        self._extracted_records['TRUB_CHILLER_VOLUME'] = round(float(self._recipe['EQUIPMENT.TRUB_CHILLER_LOSS']), 2)
        self._extracted_records['COOLING_SHRINKAGE_PERCENTAGE'] = round(
            float(self._recipe['EQUIPMENT.COOLING_LOSS_PCT']), 2)
        self._extracted_records['EVAPORATION_PERCENTAGE'] = round(float(self._recipe['EVAP_RATE']), 2)
        self._extracted_records['POST_BOIL_VOLUME'] = round(self._extracted_records['BOIL_VOLUME'] -
                                                            (self._extracted_records['EVAPORATION_PERCENTAGE'] / 100 *
                                                             self._extracted_records['BOIL_VOLUME'] *
                                                             int(round(float(self._recipe['BOIL_TIME']), 0)) / 60.0), 2)
        self._extracted_records['KNOCKOUT_VOLUME'] = round(self._extracted_records['POST_BOIL_VOLUME'] *
                                                           (1 - self._extracted_records[
                                                               'COOLING_SHRINKAGE_PERCENTAGE'] / 100), 2)
        self._extracted_records['BATCH_VOLUME'] = round(float(self._recipe['BATCH_SIZE']), 2)
        self._extracted_records['FERMENTATION_TEMP'] = round(float(self._recipe['PRIMARY_TEMP']), 1)
        self._extracted_records['OG'] = round(float(self._recipe['EST_OG'].split()[0]), 3)
        self._extracted_records['IBU'] = round(float(self._recipe['IBU'].split()[0]), 1)
        self._extracted_records['RECIPE_NAME'] = self._recipe['NAME']
        self._extracted_records['BATCH_NUMBER'] = int(self._recipe['NAME'].split()[0][1:])
        self._extracted_records['BATCH_NAME'] = self._recipe['NAME'].strip(self._recipe['NAME'].split()[0] + ' ')

        self._calculate_additional_parameter()

    def _extract(self, entry):
        pass

    def _calculate_additional_parameter(self):
        self._additional_parameter = self._recipe['EQUIPMENT.NAME']


class RecipeNameExtractor(DictRecipeExtractor):
    def __init__(self, recipe_dict):
        DictRecipeExtractor.__init__(self, recipe_dict)
        self._category = 'USER_SETTINGS'
        self._entries = 'USER_SETTINGS'

    def extract(self):
        self._calculate_additional_parameter()

    def _extract(self, entry):
        pass

    def _calculate_additional_parameter(self):
        self._additional_parameter = self._recipe['NAME']
