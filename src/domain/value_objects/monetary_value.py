from decimal import Decimal

class MonetaryValue:

    def __init__(self, value: float | int | Decimal) -> None:
        self.__validate(value)
        self.__value = Decimal(value)

    @property
    def value(self) -> Decimal:
        return self.__value

    def __str__(self) -> str:
        return f"${self.__value:.2f}"

    def __repr__(self) -> str:
        return f"MonetaryValue({str(self)})"

    def __add__(self, other) -> "MonetaryValue":
        if isinstance(other, MonetaryValue):
            return MonetaryValue(self.__value + other.value)
        raise TypeError(
            f"{self.__class__.__name__} only accepts sum operations with objects of the same type and you are trying to pass a {type(other)}"
        )

    def __sub__(self, other) -> "MonetaryValue":
        if isinstance(other, MonetaryValue):
            return MonetaryValue(self.__value - other.value)
        raise TypeError(
            f"{self.__class__.__name__} only accepts subtraction operations with objects of the same type and you are trying to pass a {type(other)}"
        )

    def __mul__(self, other) -> "MonetaryValue":
        if isinstance(other, (float, int, Decimal)):
            return MonetaryValue(self.__value * Decimal(other))
        raise TypeError(
            f"{self.__class__.__name__} only accepts multiplication operations with float, int and Decimal and you are trying to pass a {type(other)}"
        )

    def __truediv__(self, other) -> "MonetaryValue":
        if not isinstance(other, (float, int, Decimal)):
            raise TypeError(
                f"{self.__class__.__name__} only accepts division operations with float, int and Decimal and you are trying to pass a {type(other)}"
            )
        if other == 0:
            raise ZeroDivisionError('Division by zero is not allowed')
        return MonetaryValue(self.__value / Decimal(other))

    def __rtruediv__(self, other) -> None:
        raise ValueError(
            f"Division operation not supported, {self.__class__.__name__} cannot be a divisor"
        )

    @staticmethod
    def __validate_value_entry(value: float | int | Decimal) -> None:
        if not isinstance(value, (float, int, Decimal)):
            raise TypeError("Value must be a number")

    def __validate(self, value: float | int | Decimal) -> None:
        self.__validate_value_entry(value)