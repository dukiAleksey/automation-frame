import pytest
import json

from time import sleep

from constants.commands import Interface
from constants.api.abc_api import MethodUrl as Url, Locators
from constants.http import HttpMethod as Method, StatusCode
from tests.api.conftest import not_found, run_wfe_webdriver
from services.data import get_customerids_as_str, get_host_by_customer
from steps.rest_client import CommonSession
from models.api.abc_api import UserData, Ids
from factories.api.abc_api import AbcFactory


@pytest.fixture(scope='session', autouse=True)
def interface():
    return Interface.ABC


@pytest.fixture
def ids(customer, db_conn):
    def _ids(
            without_products: bool = False, without_bad_customerid: bool = False, without_login: bool = False,
            with_rlsid: bool = False, check_customer: bool = False, with_balance: bool = False, with_products: bool = False,
            with_registration: bool = False, rlsid=None, soc_id=None
    ):
        if without_bad_customerid:
            bad_customerid = get_customerids_as_str(db_conn.ms_sql.get_bad_customerid())
            customerid = db_conn.rls_my_sql.self_care_customerid_without_bad(bad_customerid)
        elif without_login:
            customerid = db_conn.rls_my_sql.self_care_customerid_without_login(check_customer=check_customer)
        elif with_balance:
            query = db_conn.rls_my_sql.self_care_customerid_with_balance(with_products=with_products)
            if not query:
                return not_found(customer, db_conn)
            customerid = query["CUSTOMERID"]
            soc_id = query["SOC_ID"]
        elif with_registration:
            possible_customerids = get_customerids_as_str(db_conn.ms_sql.customerid_with_registration())
            customerid = db_conn.rls_my_sql.self_care_customerid_with_registration(possible_customerids)
            rlsid = db_conn.ms_sql.get_rlsid_with_registration(f"+{customerid}")
        else:
            customerid = db_conn.rls_my_sql.self_care_customerid(without_products=without_products)
        if not customerid:
            return not_found(customer, db_conn)
        if with_rlsid:
            rlsid = db_conn.rls_my_sql.get_slr_id_by_customerid(customerid)
        return Ids(
            customerid=customerid,
            rlsid=rlsid,
            soc_id=soc_id
        )
    return _ids


def get_session_id(customer, customerid):
    rs = CommonSession(get_host_by_customer(customer.name), Url.ACCOUNTS_INFO, customer.logger, "https://")
    rs.headers_self_care(customerid)
    r = rs.send_request(req_type=Method.GET)
    customer.logger.assert_fail(r.status_code == StatusCode.OK, "No cookies received", f"{r.status_code}\n{r.text}")
    return dict(sessionId=r.cookies['sessionId'])


def get_login_and_pass(db_conn, customerid):
    login = db_conn.rls_my_sql.get_account_login(customerid)
    return UserData(
        login=login,
        password=db_conn.rls_my_sql.get_user_password(login)
    )


def create_account(customer, db_conn, customerid):
    user_info = db_conn.ms_sql.get_user_info_by_customerid(customerid)
    customer.logger.assert_fail(len(user_info) != 0, "User info didn't found", f"CustomerId: {customerid}")
    AbcFactory(customer).payload_creation(user_info).create_account(customerid)


def get_product_id(customer, db_conn, customerid, payment_type):
    bad_products = get_customerids_as_str(db_conn.rls_my_sql.get_bad_products(customerid))
    product_id = db_conn.rls_my_sql.get_product_id_by_customerid(customerid, payment_type, bad_products)
    if not product_id:
        return not_found(customer, db_conn)
    return product_id


def get_validation_code(customer, db_conn, customerid):
    AbcFactory(customer).payload_code_generate(customerid).generate_code()
    sleep(4)
    query = db_conn.ms_sql.get_last_notification_event(event_type=50)
    if not query:
        return not_found(customer, db_conn, slr=False)
    code = query[0][1]
    return json.loads(code)["body"]["code"]


def get_voucher_code(customer, db_conn, soc_id):
    voucher_code = db_conn.rls_my_sql.get_voucher_code(soc_id)
    if not voucher_code:
        return not_found(customer, db_conn)
    return voucher_code["serial"], voucher_code["CreditValue"]
