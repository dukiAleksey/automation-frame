import pytest

from utils.asserts import (
    assert_account_creation_modification,
    assert_error_message,
    assert_equals
)
from factories.api.abc_api import AbcFactory
from constants.http import StatusCode as Code
from constants.api.message import ErrorDictAbc


class TestModifyAccount:

    def test_nominal_modify_account(self, customer, db_conn, ids):
        customer_id = ids(without_bad_customer_id=True).customer_id
        client = AbcFactory(customer).payload_modify().modify_account(customer_id)
        assert_account_creation_modification(customer, db_conn, client, customer_id)

    @pytest.mark.parametrize(("login", "email", "delete_empty_fields"), [
        ("", None, False),
        ("!@#$%^&*()>?{}[]<>", None, True),
        (None, "", False),
        (None, "test@gmail", True)
    ], ids=["empty login", "invalid login", "empty email", "invalid email"])
    def test_modify_account_with_invalid_data(self, login, email, delete_empty_fields, customer, db_conn, ids):
        customer_id = ids(without_bad_customer_id=True).customer_id
        resp = AbcFactory(customer).payload_modify(login=login, email=email).modify_account(
            customer_id, Code.BAD_REQUEST, delete_empty_fields=delete_empty_fields).resp
        assert_equals(customer, "Error reason", "INVALID_PARAMETER", resp.ErrorReason)

    def test_modify_account_unauthorized(self, customer, db_conn, ids):
        customer_id = ids(without_bad_customer_id=True).customer_id
        assert_error_message(customer, AbcFactory(customer).payload_modify().modify_account(
            customer_id, Code.UNAUTHORIZED, unauthorised=True).resp, ErrorDictAbc.UNAUTHORIZED)
