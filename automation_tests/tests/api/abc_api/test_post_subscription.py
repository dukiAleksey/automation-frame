import pytest

from utils.asserts import (
    assert_post_subscription,
    assert_tracking,
    assert_equals,
    assert_error_message
)
from factories.api.abc_api import AbcFactory
from constants.http import StatusCode as Code, HttpMethod as Method
from constants.api.message import ErrorDictAbc
from constants.api.abc_api import PaymentType as PType, MethodUrl as Url
from tests.api.abc_api.conftest import (
    create_account,
    get_session_id,
    get_product_id,
    finish_bancontact_payment
)
from tests.api.tsm.conftest import add_balance


class TestPostSubscription:

    def test_nominal_post_subscription_by_main_credit(self, customer, db_conn, ids, payment_type=PType.MAIN_CREDIT):
        ids = ids(with_balance=True, with_rlsid=True)
        add_balance(db_conn, ids.rlsid)
        product_id = get_product_id(customer, db_conn, ids.customer_id, payment_type)

        resp = AbcFactory(customer).payload_post_subscription(product_id, payment_type).post_subscriptions(
            ids.rlsid, ids.customer_id, cookies=get_session_id(customer, ids.customer_id)).resp

        assert_tracking(customer, db_conn, ids.customer_id, Code.OK, Method.POST, Url.SUBSCRIPTIONS.format(ids.rlsid))
        assert_post_subscription(customer, resp, payment_type)

    def test_nominal_post_subscription_by_external_payment(
            self, customer, db_conn, ids, payment_type=PType.EXTERNAL_PAYMENT
    ):
        ids = ids(without_login=True, check_customer=True, with_rlsid=True)
        create_account(customer, db_conn, ids.customer_id)
        product_id = get_product_id(customer, db_conn, ids.customer_id, payment_type)

        resp = AbcFactory(customer).payload_post_subscription(product_id, payment_type).post_subscriptions(
            ids.rlsid, ids.customer_id, cookies=get_session_id(customer, ids.customer_id)).resp

        assert_tracking(customer, db_conn, ids.customer_id, Code.OK, Method.POST, Url.SUBSCRIPTIONS.format(ids.rlsid))
        assert_post_subscription(customer, resp, payment_type)

    def test_nominal_post_subscription_using_bancontact_method(
            self, customer, db_conn, ids, payment_type=PType.EXTERNAL_PAYMENT
    ):
        ids = ids(without_login=True, check_customer=True, with_rlsid=True)
        create_account(customer, db_conn, ids.customer_id)
        product_id = get_product_id(customer, db_conn, ids.customer_id, payment_type)

        resp = AbcFactory(customer).payload_post_subscription(product_id, payment_type, payment_method="BANCONTACT").\
            post_subscriptions(ids.rlsid, ids.customer_id, cookies=get_session_id(customer, ids.customer_id)).resp

        assert_tracking(customer, db_conn, ids.customer_id, Code.OK, Method.POST, Url.SUBSCRIPTIONS.format(ids.rlsid))
        assert_post_subscription(customer, resp, payment_type)

        # Finish payment using UI
        finish_bancontact_payment(customer, resp["paymentForm"]["url"])
        query = db_conn.ms_sql.get_registration_process_type(f"+{ids.customer_id}")
        customer.logger.assert_fail(query, "No registration process in db", db_conn.ms_sql.last_query)
        assert_equals(customer, "state", "TEMPORARY_REGISTERED", query["State"])

    @pytest.mark.parametrize(("product_id", "source", "payment_type"), [
        ("", None, PType.MAIN_CREDIT),
        (None, "", PType.MAIN_CREDIT),
        (None, None, "")
    ], ids=["without product id", "without source", "without payment type"])
    def test_post_subscription_with_wrong_data(self, product_id, source, customer, payment_type, db_conn, ids):
        ids = ids(with_balance=True, with_rlsid=True)
        add_balance(db_conn, ids.rlsid)
        product_id = product_id if product_id or product_id == "" else \
            get_product_id(customer, db_conn, ids.customer_id, payment_type)

        resp = AbcFactory(customer).payload_post_subscription(product_id, payment_type, source=source).\
            post_subscriptions(ids.rlsid, ids.customer_id, Code.BAD_REQUEST, cookies=get_session_id(customer, ids.customer_id)).resp

        assert_tracking(
            customer, db_conn, ids.customer_id, Code.BAD_REQUEST, Method.POST, Url.SUBSCRIPTIONS.format(ids.rlsid), by_url=True)
        assert_equals(customer, "Error reason", "INVALID_PARAMETER", resp.ErrorReason)

    def test_post_subscription_unauthorized(self, customer, db_conn, ids, payment_type=PType.MAIN_CREDIT):
        ids = ids(with_balance=True, with_rlsid=True)
        add_balance(db_conn, ids.rlsid)
        product_id = get_product_id(customer, db_conn, ids.customer_id, payment_type)

        resp = AbcFactory(customer).payload_post_subscription(product_id, payment_type).\
            post_subscriptions(ids.rlsid, ids.customer_id, Code.UNAUTHORIZED, unauthorised=True).resp

        assert_error_message(customer, resp, ErrorDictAbc.UNAUTHORIZED)
