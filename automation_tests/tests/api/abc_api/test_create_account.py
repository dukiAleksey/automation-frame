import pytest

from utils.asserts import (
    assert_account_creation_modification,
    assert_tracking,
    assert_equals,
    assert_error_message
)
from factories.api.abc_api import AbcFactory
from constants.http import StatusCode as Code, HttpMethod as Method
from constants.api.abc_api import MethodUrl as Url
from constants.api.message import ErrorDictAbc


class TestCreateAccount:

    def test_nominal_create_account(self, customer, db_conn, ids):
        customer_id = ids(without_login=True).customer_id
        user_info = db_conn.ms_sql.get_user_info_by_customer_id(customer_id)

        client = AbcFactory(customer).payload_creation(user_info).create_account(customer_id)

        assert_tracking(customer, db_conn, customer_id, Code.CREATED, Method.POST, Url.ACCOUNTS)
        assert_account_creation_modification(customer, db_conn, client, customer_id)

    @pytest.mark.parametrize(
        ("login", "password", "email", "first_name", "last_name", "country", "delete_empty_fields"), [
            ("", None, None, None, None, None, True),
            ("", None, None, None, None, None, False),
            ("!@#$%^&*()|\\/<>?", None, None, None, None, None, True),
            (None, "", None, None, None, None, True),
            (None, "", None, None, None, None, False),
            (None, "12345", None, None, None, None, True),
            (None, None, "", None, None, None, True),
            (None, None, "", None, None, None, False),
            (None, None, "test.com", None, None, None, True),
            (None, None, None, "", None, None, True),
            (None, None, None, None, "", None, True),
            (None, None, None, None, None, "", True)
        ], ids=[
            "without login", "empty login", "invalid login", "without password", "empty password", "invalid password",
            "without email", "empty email", "invalid email", "without first name", "without last name",
            "without country"
        ]
    )
    def test_create_account_with_wrong_data(
            self, login, password, email, first_name, last_name, country, delete_empty_fields, customer, db_conn, ids
    ):
        customer_id = ids(without_login=True).customer_id
        user_info = db_conn.ms_sql.get_user_info_by_customer_id(customer_id)

        resp = AbcFactory(customer).payload_creation(user_info, login, password, email, first_name, last_name, country).\
            create_account(customer_id, Code.BAD_REQUEST, delete_empty_fields=delete_empty_fields).resp

        assert_equals(customer, "Error reason", "INVALID_PARAMETER", resp.ErrorReason)
        assert_tracking(customer, db_conn, customer_id, Code.BAD_REQUEST, Method.POST, Url.ACCOUNTS, by_url=True)

    def test_create_account_unauthorized(self, customer, db_conn, ids):
        customer_id = ids(without_login=True).customer_id
        user_info = db_conn.ms_sql.get_user_info_by_customer_id(customer_id)

        assert_error_message(customer, AbcFactory(customer).payload_creation(user_info).create_account(
            customer_id, Code.UNAUTHORIZED, unauthorised=True).resp, ErrorDictAbc.UNAUTHORIZED)
