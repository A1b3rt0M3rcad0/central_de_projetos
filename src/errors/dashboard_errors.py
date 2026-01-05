"""Dashboard errors"""


class ErrorOnGetDashboardData(Exception):
    """Exception raised when error occurs getting dashboard data"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

