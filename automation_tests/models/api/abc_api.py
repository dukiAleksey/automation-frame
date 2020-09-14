class Ids:
    def __init__(self,
                 customer_id: int = None,
                 rlsid: int = None,
                 soc_id: int = None):
        self.customer_id = customer_id
        self.rlsid = rlsid
        self.soc_id = soc_id


class AccountInfoResponse:
    def __init__(self,
                 login: str,
                 iccid: str,
                 rlsid: int,
                 customer_id: str,
                 language: str,
                 email: str = None,
                 brandRef: str = None,
                 countryOfResidence: str = None,
                 customerRef: str = None):
        self.login = login
        self.iccid = iccid
        self.rlsid = rlsid
        self.customer_id = customer_id
        self.language = language
        self.email = email
        self.brandRef = brandRef
        self.countryOfResidence = countryOfResidence
        self.customerRef = customerRef


class AccountModificationRequest:
    def __init__(self,
                 login: str,
                 email: str,
                 language: str):
        self.login = login
        self.email = email
        self.language = language


class AccountModificationResponse:
    def __init__(self,
                 login: str,
                 iccid: str,
                 rlsid: int,
                 customer_id: str,
                 email: str,
                 language: str,
                 brandRef=None,
                 countryOfResidence: str = None,
                 customerRef: str = None):
        self.login = login
        self.iccid = iccid
        self.rlsid = rlsid
        self.customer_id = customer_id
        self.email = email
        self.language = language
        self.brandRef = brandRef
        self.countryOfResidence = countryOfResidence
        self.customerRef = customerRef


class AccountCreationRequest:
    def __init__(self,
                 login: str,
                 password: str,
                 email: str,
                 firstName: str,
                 lastName: str,
                 countryOfResidence: str,
                 language: str = None,
                 source: str = None):
        self.login = login
        self.password = password
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.countryOfResidence = countryOfResidence
        self.language = language
        self.source = source


class SubscriptionsParams:
    def __init__(self,
                 status: str = None):
        self.status = status


class PostVoucherRequest:
    def __init__(self,
                 code: str,
                 requestSource: str):
        self.code = code
        self.requestSource = requestSource


class PostVoucherResponse:
    def __init__(self,
                 creditAdded: float,
                 bonus: float,
                 totalCredit: float):
        self.creditAdded = creditAdded
        self.bonus = bonus
        self.totalCredit = totalCredit


class Template:
    def __init__(self,
                 reference: str = None,
                 locale: str = None):
        self.reference = reference
        self.locale = locale


class PostSubscriptionRequest:
    def __init__(self,
                 productId: str,
                 source: str,
                 paymentType: str,
                 shopperPaymentMethodRef: str = None,
                 parentSubscriptionId: str = None,
                 paymentMethod: str = None,
                 template: Template = None):
        self.productId = productId
        self.parentSubscriptionId = parentSubscriptionId
        self.source = source
        self.paymentType = paymentType
        self.paymentMethod = paymentMethod
        self.shopperPaymentMethodRef = shopperPaymentMethodRef
        self.template = template


class LogoutRequest:
    def __init__(self,
                 deviceToken: str):
        self.deviceToken = deviceToken


class ProductsParams:
    def __init__(self,
                 pc: str = None,
                 pp: str = None,
                 channel: str = None):
        self.pc = pc
        self.pp = pp
        self.channel = channel


class GenerateCodeRequest:
    def __init__(self,
                 customer_id: str = None,
                 language: str = None):
        self.customer_id = customer_id
        self.language = language


class ValidateCodeRequest:
    def __init__(self,
                 customer_id: str,
                 code: str):
        self.customer_id = customer_id
        self.code = code


class Application:
    def __init__(self,
                 version: str,
                 platform: str,
                 applicationName: str,
                 packageName: str):
        self.version = version
        self.platform = platform
        self.applicationName = applicationName
        self.packageName = packageName


class NotificationRequest:
    def __init__(self,
                 deviceToken: str,
                 application: Application):
        self.deviceToken = deviceToken
        self.application = application


class UserData:
    def __init__(self,
                 login: str = None,
                 password: str = None):
        self.login = login
        self.password = password
