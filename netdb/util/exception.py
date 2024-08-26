class NetDBException(Exception):
    def __init__(self, code=422, message='An exception has occurred.', out=None):
        self.code = code
        self.message = message
        self.out = out
