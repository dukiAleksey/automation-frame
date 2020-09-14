from utils.asserts import assert_password_change, assert_error_message
from factories.api.abc_api import AbcFactory
from constants.http import StatusCode as Code
from constants.api.message import ErrorDictAbc
from tests.api.abc_api.conftest import get_session_id, get_login_and_pass
from services.data import get_md5_password


class TestChangePassword:

    def test_nominal_change_password(self, customer, db_conn, ids):
        customer_id = ids().customer_id
        user_data = get_login_and_pass(db_conn, customer_id)

        AbcFactory(customer).payload_change_password(get_md5_password()).change_password(
            customer_id, cookies=get_session_id(customer, customer_id))

        assert_password_change(customer, db_conn, user_data)

    def test_change_password_to_the_same(self, customer, db_conn, ids):
        factory = AbcFactory(customer)
        customer_id = ids().customer_id
        new_pass = get_md5_password()
        cookie = get_session_id(customer, customer_id)

        factory.payload_change_password(new_pass).change_password(customer_id, cookies=cookie)
        resp = factory.payload_change_password(new_pass).change_password(customer_id, Code.BAD_REQUEST, cookies=cookie).resp

        assert_error_message(customer, resp, ErrorDictAbc.PASSWORD_UNCHANGED)

    def test_change_password_unauthorized(self, customer, db_conn, ids):
        customer_id = ids().customer_id
        assert_error_message(customer, AbcFactory(customer).payload_change_password(get_md5_password()).change_password(
            customer_id, Code.UNAUTHORIZED, unauthorised=True).resp, ErrorDictAbc.UNAUTHORIZED)
