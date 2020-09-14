from utils.asserts import assert_error_message
from factories.api.abc_api import BoboFactory
from constants.api.message import ErrorDictBobo
from constants.api.http import StatusCode as Code
from tests.api.abc_api.conftest import get_validation_code


class TestPostValidationCode:

    def test_nominal_validate_generated_code(self, customer, db_conn, ids):
        clientid = ids(without_login=True).clientid
        validation_code = get_validation_code(customer, db_conn, clientid)

        BoboFactory(customer).payload_code_validate(customer_id, validation_code).validate_code()

    def test_validate_generated_code_with_invalid_code(self, customer, db_conn, ids):
        customer_id = ids(without_login=True).customer_id
        assert_error_message(customer, BoboFactory(customer).payload_code_validate(customer_id, "12345").validate_code(
            Code.BAD_REQUEST).resp, ErrorDictBobo.INVALID_AUTH_CODE)
