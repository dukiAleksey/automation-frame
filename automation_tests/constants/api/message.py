from models.api.error import ErrorDetailsAbc


class ErrorDictBobo:

    PASSWORD_UNCHANGED = ErrorDetailsAbc(
        ErrorReason="PASSWORD_UNCHANGED",
        ErrorDetails="New password must be different.",
        UserMessage="New password must be different."
    )

    UNAUTHORIZED = ErrorDetailsAbc(
        ErrorReason="AUTHENTICATION_FAILURE",
        ErrorDetails="Authentication failure",
        UserMessage="No authentication data provided."
    )

    CLIENTID_NOT_FOUND = ErrorDetailsAbc(
        ErrorReason="NO_CLIENTID",
        ErrorDetails="ClientId does not exist.",
        UserMessage="ClientId does not exist."
    )

    INVALID_AUTH_CODE = ErrorDetailsAbc(
        ErrorReason="INVALID_AUTH_CODE",
        ErrorDetails="Wrong authentication code",
        UserMessage=""
    )

    VOUCHER_WRONG_CODE = ErrorDetailsAbc(
        ErrorReason="VOUCHER_WRONG_CODE",
        ErrorDetails="Wrong voucher code",
        UserMessage=""
    )
