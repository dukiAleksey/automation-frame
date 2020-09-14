import pytest

from utils.asserts import assert_registration_process, assert_error_message
from factories.api.abc_api import AbcFactory
from constants.http import StatusCode as Code
from constants.api.message import ErrorDictAbc


class TestGetRegistrationProcess:

    @pytest.mark.parametrize("country", ["BE", "GB", "QQ"],
                             ids=["country is 'BE'", "country is 'GB'", "country isn't in db"])
    def test_nominal_get_registration_process(self, country, customer, db_conn, ids, old_marketing_country=None):
        ids = ids(with_registration=True)
        marketing_country = db_conn.ms_sql.get_marketing_country(ids.rlsid)
        if marketing_country:
            old_marketing_country = marketing_country
            db_conn.ms_sql.update_marketing_country("NULL", ids.rlsid)

        resp = AbcFactory(customer).get_registration_process(ids.rlsid, country, ids.customer_id).resp
        assert_registration_process(
            customer, db_conn, resp, ids.rlsid, country=country, old_marketing_country=old_marketing_country
        )

    def test_get_registration_process_by_marketing_country(self, customer, db_conn, ids, country="QQ"):
        ids = ids(with_registration=True)
        m_country = db_conn.ms_sql.get_marketing_country(ids.rlsid)

        resp = AbcFactory(customer).get_registration_process(ids.rlsid, country, ids.customer_id).resp
        assert_registration_process(customer, db_conn, resp, ids.rlsid, country=country, m_country=m_country)

    def test_get_registration_process_unauthorized(self, customer, db_conn, ids, country="QQ"):
        ids = ids(with_rlsid=True)
        assert_error_message(customer, AbcFactory(customer).get_registration_process(
            ids.rlsid, country, ids.customer_id, Code.UNAUTHORIZED, unauthorised=True).resp, ErrorDictAbc.UNAUTHORIZED)
