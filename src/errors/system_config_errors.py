class SystemConfigNotFound(Exception):
    """Exception raised when system config is not found"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ErrorOnFindSystemConfig(Exception):
    """Exception raised when error occurs finding system config"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ErrorOnUpdateSystemConfig(Exception):
    """Exception raised when error occurs updating system config"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ErrorOnCreateSystemConfig(Exception):
    """Exception raised when error occurs creating system config"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

