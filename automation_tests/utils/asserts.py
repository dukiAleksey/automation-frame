import re
import requests
import json

from datetime import datetime, timedelta

from models.api.error import ErrorDetailsAbc as AbcError


def assert_equals(customer, name, expected, actual, message=None, second_comment=''):
    message = f"Check equals value for '{name}'" if not message else message
    expected = expected.__dict__ if isinstance(expected, AbcError) else expected
    actual = actual.__dict__ if isinstance(actual, AbcError) else actual
    comment = f"Expected value: \n{name} is '{expected}'\n\nActual value: \n{name} is '{actual}'"
    if expected == actual:
        customer.logger.add_pass(message, comment, second_comment=second_comment)
        return True
    else:
        customer.logger.add_fail(message, comment, second_comment=second_comment)
        return False


def assert_not_equals(customer, name, expected, actual, message=None, second_comment=''):
    message = f"Check not equal value for '{name}'" if not message else message
    comment = f"Expected value: \n{name} is not '{expected}'\n\nActual value: \n{name} is '{actual}'"
    if expected != actual:
        customer.logger.add_pass(message, comment, second_comment=second_comment)
        return True
    else:
        customer.logger.add_fail(message, comment, second_comment=second_comment)
        return False


def assert_specific(customer, req_values: list, resp):
    if not isinstance(resp, dict):
        resp = json.loads(convert_class_obj_to_json_str(resp))
    for item in req_values:
        if hasattr(item, '__dict__'):
            item = json.loads(convert_class_obj_to_json_str(item))
        key = list(resp.keys())[list(resp.values()).index(item)]
        if item in resp.values():
            customer.logger.add_pass(f"Check value for '{key}'", f"Actual: {resp[f'{key}']}\n\nExpected: {item}")
        else:
            customer.logger.add_fail(f"Check value for '{key}'", f"Actual: {resp[f'{key}']}\n\nExpected: {item}")
            return False


def assert_contains(customer, value, text, message=None):
    message = f"Check that '{text}' contains '{value}'" if not message else message
    if re.search(value, text):
        customer.logger.add_pass(message, f"Expected value: \n'{text}' contains '{value}'\n\n"
                                      f"Actual value: \n'{text}' contains '{value}'")
        return True
    else:
        customer.logger.add_fail(message, f"Expected value: \n'{text}' contains '{value}'\n\n"
                                      f"Actual value: \n'{text}' does not contain '{value}'")
        return False


def assert_not_none(customer, name, value, message=None, second_comment=''):
    message = f"Check that '{name}' is not empty" if not message else message
    comment = f"Expected value: \n{name} is not empty\n\nActual value: \n{name} is '{value}'"
    if value:
        customer.logger.add_pass(message, comment, second_comment=second_comment)
        return True
    else:
        customer.logger.add_fail(message, comment, second_comment=second_comment)
        return False


def assert_dict_equals(customer, actual, expected, step=None):
    step = step if step else "Check of data identity"
    invalid_keys = [key for key in expected if key not in actual]
    error_message = str()
    # assert invalid_keys == []
    if invalid_keys:
        error_message += f"Actual response do not contain following parameters:\n{invalid_keys}\n\n"
        for key in invalid_keys:
            expected.pop(key)
    invalid_items = [f"Actual: \n{v[0][0]} = {actual[v[0][0]]}\nExpected: \n{v[0][0]} = {expected[v[0][0]]}\n"
                     for v in zip(expected.items()) if v not in zip(actual.items())]
    # assert invalid_items == []
    if not invalid_items and not invalid_keys:
        customer.logger.add_pass(step, f"Data match:\nActual data: \n{actual}\n\nExpected data: \n{expected}")
    else:
        error_message += "\n".join(invalid_items)
        customer.logger.add_fail(step, error_message)


def assert_list_equals(customer, actual, expected, step=None):
    step = step if step else "Check of list identity"
    if set(actual) == set(expected):
        customer.logger.add_pass(step, f"Lists match:\n\nActual list: {actual}\n\nExpected list: {expected}")
    else:
        customer.logger.add_fail(step, f"Lists don't match:\n\nActual list: {actual}\n\nExpected list: {expected}")


def assert_len_equal(customer, length, resp, _object):
    if length == len(_object):
        customer.logger.add_pass("Comparison is right", f"Response length from api '{length}' same to db '{len(_object)}'")
    else:
        customer.logger.add_fail(
            "Comparison isn't right",
            f"Response length from api: {length} different to db: {len(_object)}",
            f"Response from api: {resp}\n\nResponse from db: {_object}"
        )


def assert_error_message(customer, resp, error):
    assert_equals(customer, "response", error, resp)


def assert_for_get_products_tests(
        customer, db_conn, customer_id, resp, category_dict, parent_product, channel_dict, by_rlsid, by_category,
        by_parent_product
):
    if by_rlsid:
        products = db_conn.rls_my_sql.get_available_products(customer_id)
    elif by_category:
        products = db_conn.rls_my_sql.get_available_products(customer_id, category_id=category_dict["category_id"])
    elif by_parent_product:
        products = db_conn.rls_my_sql.get_available_products(
            customer_id, category_id=category_dict["category_id"], external_id=parent_product)
    else:
        products = db_conn.rls_my_sql.get_available_products(customer_id, product_tag_id=channel_dict["id"])
    length = len(resp["products"])
    assert_len_equal(customer, length, resp, products)


def assert_for_get_subscriptions_tests(customer, db_conn, client, customer_id, all_lines, by_status):
    subscriptions = None
    length = len(client.resp["productSubscriptions"])
    if all_lines:
        subscriptions = db_conn.rls_my_sql.get_subscriptions(customer_id, SubStatus.ALL_STATUSES)
    elif by_status:
        if client.params.status == SubStatus.ALIVE:
            subscriptions = db_conn.rls_my_sql.get_subscriptions(customer_id, SubStatus.ALIVE_STATUSES)
        else:
            subscriptions = db_conn.rls_my_sql.get_subscriptions(customer_id, SubStatus.HISTORY_STATUSES)
    assert_len_equal(customer, length, client.resp, subscriptions)


def assert_password_change(customer, db_conn, user_data):
    new_password = db_conn.rls_my_sql.get_user_password(user_data.login)
    assert_not_equals(customer, name="Password", actual=new_password, expected=user_data.password)


def assert_account_creation_modification(customer, db_conn, client, customer_id):
    account_data = db_conn.rls_my_sql.get_account_info_by_customer_id(customer_id)
    expected = {"login": client.req.login, "email": client.req.email, "locale": client.req.language}
    assert_dict_equals(customer, account_data, expected)


def assert_tracking(customer, db_conn, customer_id, expected_code, http_method, method_url, by_url=False, param=None):
    sleep(1)
    params = f"?status={param}" if param else ""
    url = f"http://{customer.abc_api_rs_host()}{method_url}{params}"
    rlsid = db_conn.rls_my_sql.slr_get_slr_id(customer_id)

    tracking_info = db_conn.ms_sql.get_tracking_info(rlsid, url=url if by_url else None)
    customer.logger.assert_fail(tracking_info, "Check 'Tracking' db", "There is no record in db")

    expected = {"StatusCode": expected_code, "HttpMethod": http_method, "Url": url}
    assert_dict_equals(customer, tracking_info, expected, "Check new record in 'Tracking' db")


def assert_post_subscription(customer, resp, payment_type):
    if payment_type == PaymentType.MAIN_CREDIT:
        customer.logger.assert_fail(
            any(field in resp for field in ["productSubscriptionId", "PRODUCTSUBSCRIPTIONID"]),
            "Response Error", f"{resp}"
        )
    else:
        customer.logger.assert_fail(resp["paymentForm"], "Response Error", f"{resp}")


def assert_subscriber_registration(customer, db_conn, resp, rlsid):
    subscriber_number = db_conn.ms_sql.get_subscriber_number(rlsid)
    assert_equals(customer, "SubscriberNumber", subscriber_number, resp["subscriberNumber"])
