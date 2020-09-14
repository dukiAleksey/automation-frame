import names

from services.api.abc_api import AbcService
from services.data import (
    get_random_string,
    get_random_email,
    get_random_lang,
    get_md5_password,
    get_random_country,
    get_random_status,
    get_random_source,
    get_ref_by_customer
)
from models.api.abc_api import (
    AccountModificationRequest,
    AccountCreationRequest,
    SubscriptionsParams,
    PostVoucherRequest,
    PostSubscriptionRequest,
    LogoutRequest,
    ProductsParams,
    GenerateCodeRequest,
    ValidateCodeRequest,
    NotificationRequest,
    Application,
    Template
)
from constants.api.abc_api import PaymentType as PType


class AbcFactory(AbcService):

    def __init__(self, customer, params=None, req=None):
        super().__init__(customer=customer, params=params, req=req)

    def payload_modify(self, login=None, email=None, lang=None):
        self.req = AccountModificationRequest(
            login=login if login or login == "" else get_random_string(),
            email=email if email or email == "" else get_random_email(),
            language=lang if lang else get_random_lang()
        )
        return self

    def payload_change_password(self, password=None):
        self.req = password if password else get_md5_password()
        return self

    def payload_creation(
            self, user_data, login=None, password=None, email=None, first_name=None, last_name=None, country=None,
            lang=None
    ):
        email = email if email or email == "" else "{}".format(
            get_random_email() if user_data["Email"] in ("-", "", "NULL", None) else "customer.dev@gmail.com"
        )
        first_name = first_name if first_name or first_name == "" else "{}".format(
            names.get_first_name() if user_data["FirstName"] in ("-", "", "NULL", None) else user_data["FirstName"]
        )
        last_name = last_name if last_name or last_name == "" else "{}".format(
            names.get_last_name() if user_data["LastName"] in ("-", "", "NULL", None) else user_data["LastName"]
        )
        password = password if password or password == "" else \
            f"{password if password else get_md5_password(passw='abc@123')}"
        self.req = AccountCreationRequest(
            login=login if login or login == "" else f"AutoTest{get_random_string()}",
            email=email,
            password=password,
            language=lang if lang else get_random_lang(),
            firstName=first_name,
            lastName=last_name,
            countryOfResidence=country if country or country == "" else get_random_country(),
            source="SFC_APP"
        )
        return self

    def subscriptions_params(self, by_status=None):
        self.params = SubscriptionsParams(status=get_random_status()) if by_status else None
        return self

    def payload_post_voucher(self, code=None):
        self.req = PostVoucherRequest(
            code=code if code or code == "" else None,
            requestSource="SFC_APP"
        )
        return self

    def payload_post_subscription(
            self, product_id, payment_type, parent_id=None, payment_method=None, source=None,
            shopper_payment_method=None
    ):
        self.req = PostSubscriptionRequest(
            productId=product_id if product_id or product_id == "" else None,
            parentSubscriptionId=parent_id if parent_id else None,
            source=source if source or source == "" else get_random_source(),
            paymentType=payment_type if payment_type or payment_type == "" else None,
            paymentMethod=payment_method,
            shopperPaymentMethodRef=shopper_payment_method,
            template=Template(
                reference=get_ref_by_customer(self.customer.name),
                locale="en_US"
            ) if payment_type == PType.EXTERNAL_PAYMENT else None
        )
        return self

    def payload_logout(self, token=None, empty_token=True):
        self.req = "{}" if empty_token else LogoutRequest(deviceToken=token)
        return self

    def products_params(self, product_category=None, parent_product=None, channel=None):
        self.params = ProductsParams(
            pc=product_category,
            pp=parent_product,
            channel=channel
        )
        return self

    def payload_code_generate(self, customer_id):
        self.req = GenerateCodeRequest(
            customer_id=customer_id,
            language=get_random_lang()
        )
        return self

    def payload_code_validate(self, customer_id, code):
        self.req = ValidateCodeRequest(
            customer_id=customer_id,
            code=code
        )
        return self

    def payload_notifications(self, db_conn, version=None, platform=None, app_name=None, package_name=None, token=None):
        app_info = db_conn.ms_sql.get_application_info()
        self.req = NotificationRequest(
            deviceToken=token if token or token == "" else get_random_string(size=256),
            application=Application(
                version=version if version else app_info["Version"],
                platform=platform if platform else app_info["Platform"],
                applicationName=app_name if app_name else app_info["ApplicationName"],
                packageName=package_name if package_name else app_info["PackageName"]
            )
        )
        return self
