class QueryFailedException(Exception):
    """Raised when the query status is not 'success'"""

    def __init__(self, message="Query failed"):
        self.message = message
        super().__init__(self.message)


class BadStatusCodeException(Exception):
    """Raised when the response status code is not 200"""

    def __init__(self, message="Bad status code"):
        self.message = message
        super().__init__(self.message)
