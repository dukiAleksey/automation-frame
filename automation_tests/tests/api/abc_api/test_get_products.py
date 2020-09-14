import pytest

from utils.asserts import assert_for_get_products_tests, assert_error_message
from factories.api.abc_api import AbcFactory
from services.data import get_random_product_category, get_random_channel
from constants.http import StatusCode as Code
from constants.api.message import ErrorDictAbc


class TestGetProducts:

    @pytest.mark.parametrize(("by_rlsid", "by_category", "by_parent_product", "by_channel"), [
        (True, False, False, False),
        (False, True, False, False),
        (False, False, True, False),
        (False, False, False, True)
    ], ids=["by rlsid", "by category", "by parent product", "by channel"])
    def test_nominal_get_products(
            self, by_rlsid, by_category, by_parent_product, by_channel, customer, db_conn, ids, category=None,
            parent_product=None, channel=None, channel_dict=None, category_dict=None
    ):
        ids = ids(with_rlsid=True)

        if by_category:
            category_dict = get_random_product_category()
            category = category_dict["name"]
        elif by_parent_product:
            category_dict = {"name": "Add-on", "category_id": 7}
            category = category_dict["name"]
            parent_product = db_conn.rls_my_sql.get_random_external_id_for_parent_product(
                ids.customer_id, category_dict["category_id"]
            )
        elif by_channel:
            channel_dict = get_random_channel()
            channel = channel_dict["value"]

        resp = AbcFactory(customer).products_params(category, parent_product, channel).get_products(
            ids.rlsid, ids.customer_id).resp

        assert_for_get_products_tests(
            customer, db_conn, ids.customer_id, resp, category_dict, parent_product, channel_dict, by_rlsid, by_category,
            by_parent_product
        )

    def test_get_products_unauthorized(self, customer, ids):
        ids = ids(with_rlsid=True)
        assert_error_message(customer, AbcFactory(customer).products_params().get_products(
            ids.rlsid, ids.customer_id, Code.UNAUTHORIZED, unauthorised=True).resp, ErrorDictAbc.UNAUTHORIZED)
