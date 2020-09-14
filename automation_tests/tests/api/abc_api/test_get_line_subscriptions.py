import pytest

from utils.asserts import assert_tracking, assert_for_get_subscriptions_tests, assert_error_message
from factories.api.abc_api import AbcFactory
from constants.http import StatusCode as Code
from constants.http import HttpMethod as Method
from constants.api.abc_api import MethodUrl as Url
from constants.api.message import ErrorDictAbc


class TestGetLineSubscription:

    @pytest.mark.parametrize(("by_status", "all_lines"), [(True, False), (False, True)],
                             ids=["by status", "without filtration by status"])
    def test_nominal_get_line_subscriptions(self, all_lines, by_status, customer, db_conn, ids):
        ids = ids(with_rlsid=True)

        client = AbcFactory(customer).subscriptions_params(by_status).get_subscriptions(ids.rlsid, ids.customer_id)

        assert_tracking(
            customer, db_conn, ids.customer_id, Code.OK, Method.GET, Url.SUBSCRIPTIONS.format(ids.rlsid),
            param=client.params.status if by_status else None
        )
        assert_for_get_subscriptions_tests(customer, db_conn, client, ids.customer_id, all_lines, by_status)

    def test_get_line_subscriptions_unauthorized(self, customer, db_conn, ids):
        ids = ids(with_rlsid=True)
        assert_error_message(customer, AbcFactory(customer).subscriptions_params().get_subscriptions(
            ids.rlsid, ids.customer_id, Code.UNAUTHORIZED, unauthorised=True).resp, ErrorDictAbc.UNAUTHORIZED)
