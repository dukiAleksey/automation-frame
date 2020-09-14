from constants.customer import CustomerId

INVALID_CLIENTID = "12345"

CUSTOMER = (
    CustomerId.Customer_BOBO
)


class Host:
    from steps.configurator import Configurator
    configurator = Configurator()
    utl = configurator.get_customer_url()


class MethodUrl:
    ACCOUNTS = "accounts"
    ACCOUNTS_INFO = "accounts/me"
    ACCOUNTS_PASSWORD = "accounts/me/password"
    SUBSCRIPTIONS = "lines/{}/subscriptions"
    LOGOUT = "accounts/me/logout"
    PRODUCTS = "lines/{}/products"
    CODE_GENERATE = "codes/generate"
    CODE_VALIDATE = "codes/validate"
    NOTIFICATIONS = "accounts/me/notifications/registrations"
    VOUCHERS = "lines/{}/vouchers"
    SUBSCRIBER_REGISTRATION = "registrations/{}"
    REGISTRATION_PROCESS = "registrations/process/{}/{}"


class SubscriptionStatus:
    ALIVE = "ALIVE"
    HISTORY = "HISTORY"

    ALIVE_STATUSES = (
        "ACTIVE", "PENDING FOR FIRST USE", "SCHEDULED", "WAITING_FOR_PAYMENT", "WAITING_FOR_ACTIVATION_ORDER"
    )
    HISTORY_STATUSES = (
        "SUSPENDED", "TERMINATED", "DONE", "EFFECTIVE", "VOIDED", "END_OF_PRODUCT_LIFE", "EXPIRED", "REMOVED"
    )
    ALL_STATUSES = (
        'ACTIVE', 'PENDING FOR FIRST USE', 'SCHEDULED', 'WAITING_FOR_PAYMENT', 'SUSPENDED', 'DONE', 'EFFECTIVE',
        'VOIDED', 'END_OF_PRODUCT_LIFE', 'EXPIRED', 'REMOVED', 'WAITING_FOR_ACTIVATION_ORDER', 'TERMINATED'
    )


class PaymentType:
    EXTERNAL_PAYMENT = "EXTERNAL_PAYMENT"
    MAIN_CREDIT = "MAIN_CREDIT"


class Locators:
    XPATH_MONTH = "//select[@id='Ecom_Payment_Card_ExpDate_Month']/option[text()='01']"
    XPATH_YEAR = "//select[@id='Ecom_Payment_Card_ExpDate_Year']/option[text()='2023']"
    ID_CARD_NAME = "Ecom_Payment_Card_Name"
    ID_CARD_NUMBER = "Ecom_Payment_Card_Number"
    ID_BTN_SEND_DATA = "btn_sendCardData"
    ID_BTN_SUBMIT = "Submit"
