from utils.asserts import assert_equals
from tests.api.conftest import run_wfe_webdriver
from steps.pages.pages_sfc.login_page import LoginPage
from constants.customer import customerId


def assert_account(customer, db_conn, login, locale, account_must_be, password=None, customer_id=None, registration_check=False):
    with run_wfe_webdriver(customer, customer.get_sfc_url()) as wd:
        login_page = LoginPage(wd, customer, customer.configurator, login, password if password else 'tsl@123', locale)
        login_page.log_in(account_must_be=account_must_be)
    if customer.name == CustomerId.MVNE_BE_OBE_LMOBI and registration_check:
        query = db_conn.ms_sql.get_registration_process_type(f"+{customer_id}")
        customer.logger.assert_fail(query, "No registration process in db", f"{db_conn.ms_sql.last_query}")
        assert_equals(customer, "registration_type", "BLOCKED_DEFAULT_BE", query["Type"])
        assert_equals(customer, "state", "NOT_REGISTERED", query["State"])


def assert_delete_account(customer, db_conn, slr_id):
    login = db_conn.rls_my_sql.get_login_by_slr_id(slr_id)
    if login:
        customer.logger.add_fail("Check login", f"Login {login} still exists")
