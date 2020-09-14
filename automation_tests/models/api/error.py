class ErrorDetailsAbc:
    def __init__(self,
                 ErrorReason: str,
                 ErrorDetails: str,
                 UserMessage: str,
                 AdditionalDetails: str = None):
        self.ErrorReason = ErrorReason
        self.ErrorDetails = ErrorDetails
        self.UserMessage = UserMessage
        self.AdditionalDetails = AdditionalDetails

    def __eq__(self, other):
        return self.ErrorReason == other.ErrorReason and self.ErrorDetails == other.ErrorDetails and \
            self.UserMessage == other.UserMessage and self.AdditionalDetails == other.AdditionalDetails
