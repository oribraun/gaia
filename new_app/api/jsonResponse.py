
class baseHttpResponse:
    err: int
    errMessage: str
    message: str
    data: dict

    def __init__(self):
        self.err = 0
        self.errMessage = ''
        self.message = ''
        self.data = {}
        pass

    def dict(self):
        return self.__dict__
