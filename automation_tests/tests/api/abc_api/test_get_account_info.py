from utils.asserts import assert_tracking, assert_not_none, assert_error_message
from factories.api.abc_api import AbcFactory
from constants.http import StatusCode as Code
from constants.http import HttpMethod as Method
from constants.api.abc_api import MethodUrl as Url
from constants.api.message import ErrorDictAbc


class TestGetAccountInfo:

    def test_nominal_get_account_info(self, customer, db_conn, ids):
        customer_id = ids().customer_id
        resp = AbcFactory(customer).get_account_info(customer_id).resp
        assert_tracking(customer, db_conn, customer_id, Code.OK, Method.GET, Url.ACCOUNTS_INFO)
        assert_not_none(customer, "iccid", resp.iccid)

    def test_get_account_info_unauthorized(self, customer, db_conn, ids):
        customer_id = ids().customer_id
        assert_error_message(customer, AbcFactory(customer).get_account_info(
            customer_id, Code.UNAUTHORIZED, unauthorised=True).resp, ErrorDictAbc.UNAUTHORIZED)
