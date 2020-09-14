from utils.asserts import assert_error_message, assert_equals
from factories.api.abc_api import AbcFactory
from constants.api.message import ErrorDictAbc
from constants.http import StatusCode as Code


class TestPostNotificationRegistration:

    def test_nominal_post_notifications_registration(self, customer, db_conn, ids):
        customer_id = ids().customer_id
        AbcFactory(customer).payload_notifications(db_conn).notification_registration(customer_id)

    def test_post_notifications_registration_without_token(self, customer, db_conn, ids):
        customer_id = ids().customer_id
        resp = AbcFactory(customer).payload_notifications(db_conn, token="").notification_registration(
            customer_id, Code.BAD_REQUEST).resp
        assert_equals(customer, "Error reason", "INVALID_PARAMETER", resp.ErrorReason)

    def test_post_notifications_registration_unauthorized(self, customer, db_conn, ids):
        customer_id = ids().customer_id
        assert_error_message(customer, AbcFactory(customer).payload_notifications(db_conn).notification_registration(
            customer_id, Code.UNAUTHORIZED, unauthorised=True).resp, ErrorDictAbc.UNAUTHORIZED)
