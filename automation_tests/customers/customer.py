import collections
import copy
import datetime
import json
import os
import re
import string
import pytest

from random import randrange, choices
from time import strftime

from steps.configurator import Configurator
from constants.customer import ValidationProfiles as Vp
from constants.line import Statusses as St
from services.test_selection import get_test_by_interface_and_suit
from utils.datetime_utils import get_current_datetime, timestamp
from services.data import get_folder_by_interface


class Customer(object):
    def __init__(self, name, logger, env=None):
        self.name = name
        self.country = str
        self.logger = logger
        self.bugs_dict = dict()
        self.expected_termination_reason = None
        self.payg_offer_name = ''
        self.paym_offer_name = ''
        self.default_offer_name = ''
        self.test_mode_offer_name = ''
        self.summa_offer_name = ''
        self.not_test_mode_offer_name = ''
        self.current_offer = ''
        self.bapi_transaction_id = ''
        self.option_mapping = None
        self.init_option_mapping()
        self.connections = ConnectionsManager(self.logger)
        self.configurator = Configurator(env=env)

    def run_tests(self, to_run_data):
        self.logger.name = self.name
        self.country = to_run_data.get('country')
        suit = copy.deepcopy(to_run_data["cases"])
        pytest_tests_names = []
        new_suit = copy.deepcopy(suit)
        db_conn = DbConnector(self.configurator, self)

        tests_string = ' or '.join(pytest_tests_names)
        pytest.main(self._get_pytest_run_options(
            tests_string, to_run_data['name'], to_run_data['ident'], to_run_data.get('customerid_to_run'),
            interface, to_run_data.get('env'), to_run_data.get('is_mbapi_run'))
        )
        self.clear_temp_folders()

    def clear_temp_folders(self):
        precondition_folder = os.path.join("results", "preconditions", self.name)

        for f in os.listdir(precondition_folder):
            os.remove(os.path.join(precondition_folder,f))

    @staticmethod
    def _get_pytest_run_options(tests_string, var_file_name, ident, interface, env, is_mbapi_run):
        folder = get_folder_by_interface(interface)
        options = ['-v']
        options.extend(['-k', tests_string])
        options.extend((['--variables', f'test_cases/{folder}/{var_file_name}.json']))
        options.extend(['--ident', ident])
        options.extend(['--jira'])
        if env:
            options.extend(['--env', env])
        if is_mbapi_run:
            options.extend(['--is_mbapi_run', str(is_mbapi_run)])
        return options

    def test_suit(self):
        with open(os.path.join('test_cases', 'to_run', self.name + '.json')) as file_body:
            file_body = file_body.read()
            json_data = json.loads(file_body, object_pairs_hook=collections.OrderedDict)
            cases = json_data['cases']
        return cases

    def get_customer_name(self, target=''):
        return self.name


    def __generate_test_params_file(self, json_path, interface, command_name, test_name, params_dict):
        json_dict = {"cases": {interface: {command_name: {test_name: params_dict}}}}
        json_dict.update({"name": self.test_case_file_name()})
        json_dict.update({"country": self.country})
        with open(json_path, 'w') as f:
            json.dump(json_dict, f)
        f.close()
