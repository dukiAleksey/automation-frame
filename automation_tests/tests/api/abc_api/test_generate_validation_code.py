from factories.api.abc_api import AbcFactory
from constants.http import StatusCode as Code
from constants.api.abc_api import INVALID_CLIENTID
from constants.api.message import ErrorDictAbc
from utils.asserts import assert_error_message


class TestGenerateValidationCode:

    def test_nominal_generate_validation_code(self, customer, ids):
        ids = ids(without_login=True)
        AbcFactory(customer).payload_code_generate(ids.customer_id).generate_code()

    def test_generate_validation_code_with_invalid_customer_id(self, customer):
        assert_error_message(customer, AbcFactory(customer).payload_code_generate(INVALID_CLIENTID).generate_code(
            Code.NOT_FOUND).resp, ErrorDictAbc.CLIENTID_NOT_FOUND)
