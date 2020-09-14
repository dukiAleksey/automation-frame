import pytest

from utils.asserts import assert_equals, assert_error_message
from factories.api.abc_api import AbcFactory
from constants.api.message import ErrorDictAbc
from constants.http import StatusCode as Code
from tests.api.abc_api.conftest import get_voucher_code, get_session_id
from tests.api.tsm.conftest import add_balance


class TestPostVoucher:

    def test_nominal_post_voucher(self, customer, db_conn, ids):
        ids = ids(with_balance=True, with_products=True, with_rlsid=True)
        code = get_voucher_code(customer, db_conn, ids.soc_id)
        cookies = get_session_id(customer, ids.customer_id)

        add_balance(db_conn, ids.rlsid, value=1)

        resp = AbcFactory(customer).payload_post_voucher(code[0]).post_voucher(
            ids.rlsid, ids.customer_id, cookies=cookies).resp

        assert_equals(customer, "CreditValue", float(code[1] / 100), resp.creditAdded)

    @pytest.mark.parametrize("code", ["", "12345"], ids=["without code", "with invalid code"])
    def test_post_voucher_with_invalid_code(self, code, customer, db_conn, ids):
        ids = ids(with_balance=True, with_products=True, with_rlsid=True)
        cookies = get_session_id(customer, ids.customer_id)

        resp = AbcFactory(customer).payload_post_voucher(code).post_voucher(
            ids.rlsid, ids.customer_id, Code.BAD_REQUEST, cookies=cookies).resp

        if code == "":
            assert_equals(customer, "Error reason", "PARAMETER", resp.ErrorReason)
        else:
            assert_error_message(customer, resp, ErrorDictAbc.VOUCHER_WRONG_CODE)

    def test_post_voucher_unauthorized(self, customer, db_conn, ids):
        ids = ids(with_balance=True, with_products=True, with_rlsid=True)
        code = get_voucher_code(customer, db_conn, ids.soc_id)

        assert_error_message(customer, AbcFactory(customer).payload_post_voucher(code[0]).post_voucher(
            ids.rlsid, ids.customer_id, Code.UNAUTHORIZED, unauthorised=True).resp, ErrorDictAbc.UNAUTHORIZED)
