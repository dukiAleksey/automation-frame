import pytest

from utils.asserts import assert_error_message
from factories.api.abc_api import AbcFactory
from constants.http import StatusCode as Code
from constants.api.message import ErrorDictAbc


class TestLogout:

    @pytest.mark.parametrize("empty_token", [True, False], ids=["without token", "with token"])
    def test_nominal_logout(self, empty_token, customer, db_conn, ids):
        customer_id = ids().customer_id
        AbcFactory(customer).payload_logout(db_conn.ms_sql.get_device_token(), empty_token).logout(customer_id)

    def test_logout_unauthorized(self, customer, db_conn, ids):
        customer_id = ids().customer_id
        assert_error_message(customer, AbcFactory(customer).payload_logout().logout(
            customer_id, Code.UNAUTHORIZED, unauthorised=True).resp, ErrorDictAbc.UNAUTHORIZED)
