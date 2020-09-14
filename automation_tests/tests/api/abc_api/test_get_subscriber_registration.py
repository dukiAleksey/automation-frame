from utils.asserts import assert_subscriber_registration, assert_error_message
from factories.api.abc_api import AbcFactory
from constants.http import StatusCode as Code
from constants.api.message import ErrorDictAbc


class TestGetSubscriberRegistration:

    def test_nominal_get_subscriber_registration(self, customer, db_conn, ids):
        ids = ids(with_registration=True)
        resp = AbcFactory(customer).get_subscriber_registration(ids.rlsid, ids.customer_id).resp
        assert_subscriber_registration(customer, db_conn, resp, ids.rlsid)

    def test_get_subscriber_registration_for_rlsid_without_registration(self, customer, db_conn, ids):
        customer_id = db_conn.rls_my_sql.self_care_customer_id()
        customer_id_with_plus = f"+{customer_id}"
        list_of_customer_id = [el[0] for el in db_conn.ms_sql.customer_id_with_registration()]
        while customer_id_with_plus in list_of_customer_id:
            customer_id = db_conn.rls_my_sql.self_care_customer_id()
            customer_id_with_plus = f"+{customer_id}"
        rlsid = db_conn.rls_my_sql.get_slr_id_by_customer_id(customer_id)

        AbcFactory(customer).get_subscriber_registration(rlsid, customer_id, Code.NOT_FOUND)

    def test_get_subscriber_registration_unauthorized(self, customer, db_conn, ids):
        ids = ids(with_registration=True)
        assert_error_message(customer, AbcFactory(customer).get_subscriber_registration(
            ids.rlsid, ids.customer_id, Code.UNAUTHORIZED, unauthorised=True).resp, ErrorDictAbc.UNAUTHORIZED)
