from typing import Union

from steps.rest_client import CommonSession
from services.data import get_host_by_customer
from constants.http import (
    HttpMethod as Method,
    StatusCode
)
from constants.api.abc_api import MethodUrl as Url
from models.api.abc_api import (
    AccountInfoResponse,
    AccountModificationRequest,
    AccountModificationResponse,
    AccountCreationRequest,
    SubscriptionsParams,
    PostVoucherRequest,
    PostVoucherResponse,
    PostSubscriptionRequest,
    LogoutRequest,
    ProductsParams,
    GenerateCodeRequest,
    ValidateCodeRequest,
    NotificationRequest
)
from models.api.error import ErrorDetailsAbc


class AbcService:

    def __init__(self, customer, params=None, req=None):
        self.customer = customer
        self.params: Union[SubscriptionsParams, ProductsParams, None] = params
        self.req: Union[AccountModificationRequest, AccountCreationRequest, PostVoucherRequest, PostSubscriptionRequest,
                        LogoutRequest, GenerateCodeRequest, ValidateCodeRequest, NotificationRequest, str] = req
        self.resp: Union[AccountInfoResponse, AccountModificationResponse, PostVoucherResponse, ErrorDetailsAbc,
                         dict, None] = None

    def send_request(
            self, req_type, method_url, payload=None, params=None, expected_code=None, delete_empty_fields=False,
            deserialize=True, deserialize_to=None, unauthorised=False, lang=False, customer_id=None, content_type=False,
            cookies=None
    ):
        rs = CommonSession(get_host_by_customer(self.customer.name), method_url, self.customer.logger, "https://")
        if content_type:
            rs.headers_content_type("text/plain")
        if not unauthorised and not cookies:
            rs.headers_self_care(customer_id, lang)
        resp = rs.send_request(
            req_type, params=params, _json=payload, delete_empty_fields=delete_empty_fields, deserialize=deserialize,
            deserialize_to=deserialize_to, expected_code=expected_code, log_response=False, simple_log_response=True,
            cookies=cookies
        )
        return resp

    def get_account_info(self, customer_id, expected_code=StatusCode.OK, unauthorised=False):
        self.resp = self.send_request(
            req_type=Method.GET,
            method_url=Url.ACCOUNTS_INFO,
            unauthorised=unauthorised,
            customer_id=customer_id,
            deserialize_to=ErrorDetailsBobo if expected_code != StatusCode.OK else AccountInfoResponse,
            expected_code=expected_code
        )
        return self

    def modify_account(self, customer_id, expected_code=StatusCode.OK, unauthorised=False, delete_empty_fields=True):
        self.resp = self.send_request(
            req_type=Method.PATCH,
            method_url=Url.ACCOUNTS_INFO,
            unauthorised=unauthorised,
            payload=self.req,
            customer_id=customer_id,
            deserialize_to=ErrorDetailsAbc if expected_code != StatusCode.OK else AccountModificationResponse,
            expected_code=expected_code,
            delete_empty_fields=delete_empty_fields
        )
        return self

    def change_password(self, customer_id, expected_code=StatusCode.NO_CONTENT, unauthorised=False, cookies=None):
        self.resp = self.send_request(
            req_type=Method.PUT,
            method_url=Url.ACCOUNTS_PASSWORD,
            unauthorised=unauthorised,
            payload=self.req,
            customer_id=customer_id,
            deserialize=True if expected_code != StatusCode.NO_CONTENT else False,
            deserialize_to=ErrorDetailsAbc,
            content_type=True,
            cookies=None if unauthorised else cookies,
            expected_code=expected_code
        )
        return self

    def create_account(self, customer_id, expected_code=StatusCode.CREATED, unauthorised=False, delete_empty_fields=True):
        self.resp = self.send_request(
            req_type=Method.POST,
            method_url=Url.ACCOUNTS,
            unauthorised=unauthorised,
            payload=self.req,
            customer_id=customer_id,
            deserialize_to=ErrorDetailsAbc if expected_code != StatusCode.CREATED else AccountInfoResponse,
            expected_code=expected_code,
            delete_empty_fields=delete_empty_fields
        )
        return self

    def get_subscriptions(self, rlsid, customer_id, expected_code=StatusCode.OK, unauthorised=False):
        self.resp = self.send_request(
            req_type=Method.GET,
            method_url=Url.SUBSCRIPTIONS.format(rlsid),
            unauthorised=unauthorised,
            params=self.params,
            customer_id=customer_id,
            lang=True,
            deserialize_to=dict,
            expected_code=expected_code,
            delete_empty_fields=True
        )
        return self

    def post_subscriptions(
            self, rlsid, customer_id, expected_code=StatusCode.OK, unauthorised=False, delete_empty_fields=True, cookies=None
    ):
        self.resp = self.send_request(
            req_type=Method.POST,
            method_url=Url.SUBSCRIPTIONS.format(rlsid),
            unauthorised=unauthorised,
            payload=self.req,
            customer_id=customer_id,
            deserialize_to=ErrorDetailsAbc if expected_code != StatusCode.OK else dict,
            cookies=None if unauthorised else cookies,
            expected_code=expected_code,
            delete_empty_fields=delete_empty_fields
        )
        return self

    def post_voucher(
            self, rlsid, customer_id, expected_code=StatusCode.CREATED, unauthorised=False, delete_empty_fields=True,
            cookies=None
    ):
        self.resp = self.send_request(
            req_type=Method.POST,
            method_url=Url.VOUCHERS.format(rlsid),
            unauthorised=unauthorised,
            payload=self.req,
            customer_id=customer_id,
            cookies=None if unauthorised else cookies,
            deserialize_to=ErrorDetailsAbc if expected_code != StatusCode.CREATED else PostVoucherResponse,
            expected_code=expected_code,
            delete_empty_fields=delete_empty_fields
        )
        return self

    def logout(self, customer_id, expected_code=StatusCode.OK, unauthorised=False):
        self.resp = self.send_request(
            req_type=Method.POST,
            method_url=Url.LOGOUT,
            unauthorised=unauthorised,
            payload=self.req,
            customer_id=customer_id,
            deserialize=False if expected_code == StatusCode.OK else True,
            deserialize_to=dict,
            expected_code=expected_code
        )
        return self

    def get_products(self, rlsid, customer_id, expected_code=StatusCode.OK, unauthorised=False):
        self.resp = self.send_request(
            req_type=Method.GET,
            method_url=Url.PRODUCTS.format(rlsid),
            unauthorised=unauthorised,
            lang=True,
            params=self.params,
            customer_id=customer_id,
            deserialize_to=ErrorDetailsAbc if expected_code != StatusCode.OK else dict,
            expected_code=expected_code,
            delete_empty_fields=True
        )
        return self

    def generate_code(self, expected_code=StatusCode.CREATED):
        self.resp = self.send_request(
            req_type=Method.POST,
            method_url=Url.CODE_GENERATE,
            unauthorised=True,
            payload=self.req,
            deserialize=False if expected_code == StatusCode.CREATED else True,
            deserialize_to=ErrorDetailsAbc,
            expected_code=expected_code,
            delete_empty_fields=True
        )
        return self

    def validate_code(self, expected_code=StatusCode.OK):
        self.resp = self.send_request(
            req_type=Method.POST,
            method_url=Url.CODE_VALIDATE,
            unauthorised=True,
            payload=self.req,
            deserialize=True if expected_code != StatusCode.OK else False,
            deserialize_to=ErrorDetailsAbc,
            expected_code=expected_code,
            delete_empty_fields=True
        )
        return self

    def notification_registration(self, customer_id, expected_code=StatusCode.OK, unauthorised=False):
        self.resp = self.send_request(
            req_type=Method.POST,
            method_url=Url.NOTIFICATIONS,
            unauthorised=unauthorised,
            payload=self.req,
            customer_id=customer_id,
            deserialize=True if expected_code != StatusCode.OK else False,
            deserialize_to=ErrorDetailsAbc,
            expected_code=expected_code,
            delete_empty_fields=True
        )
        return self

    def get_subscriber_registration(self, rlsid, customer_id, expected_code=StatusCode.OK, unauthorised=False):
        self.resp = self.send_request(
            req_type=Method.GET,
            method_url=Url.SUBSCRIBER_REGISTRATION.format(rlsid),
            unauthorised=unauthorised,
            customer_id=customer_id,
            deserialize=False if expected_code == StatusCode.NOT_FOUND else True,
            deserialize_to=ErrorDetailsAbc if expected_code == StatusCode.UNAUTHORIZED else dict,
            expected_code=expected_code
        )
        return self

    def get_registration_process(self, rlsid, country, customer_id, expected_code=StatusCode.OK, unauthorised=False):
        self.resp = self.send_request(
            req_type=Method.GET,
            method_url=Url.REGISTRATION_PROCESS.format(rlsid, country),
            unauthorised=unauthorised,
            customer_id=customer_id,
            deserialize_to=ErrorDetailsAbc if expected_code != StatusCode.OK else dict,
            expected_code=expected_code
        )
        return self
