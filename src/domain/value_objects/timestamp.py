from src.domain.value_objects.date import Date
from datetime import datetime, timezone


class Timestamp:

    def __init__(self, value: float) -> None:
        self.__value = value
        self.__validate_type()
        self.__validate_positive()
        self.__validate_reasonable_range()

    def to_datetime(self) -> datetime:
        value = self.__value
        if value > 1e12:
            value = value / 1000
        return datetime.fromtimestamp(value, tz=timezone.utc)

    def to_date(self) -> Date:
        dt = self.to_datetime()
        return Date(f"{dt.day:02d}/{dt.month:02d}/{dt.year}")

    def __validate_type(self) -> None:
        if not isinstance(self.__value, (int, float)):
            raise TypeError(f"Timestamp must be int or float. Got: {type(self.__value).__name__}")

    def __validate_positive(self) -> None:
        if self.__value < 0:
            raise ValueError("Timestamp must be a positive number.")

    def __validate_reasonable_range(self) -> None:
        if self.__value > 32503680000 * 1000:
            raise ValueError("Timestamp is unreasonably far in the future.")
        if self.__value < 0:
            raise ValueError("Timestamp cannot be negative.")
