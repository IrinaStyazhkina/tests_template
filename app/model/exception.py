class EmailAlreadyExistsException(Exception):
    """Exception raised for email that already exists in system"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f'{self.message}'

class UserNotFoundException(Exception):
    """Exception raised if user is not found in system"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f'{self.message}'

class NotEnoughBalanceException(Exception):
    """Exception raised if user has not enough balance"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f'{self.message}'

class MLResponseTimeoutException(Exception):
    """Exception raised if ml service don't answer too long"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f'{self.message}'