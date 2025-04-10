from datetime import date

class Date:

    def __init__(self, date_string: str) -> None:
        self.__date_string = date_string
        self.__valid_date_string_entry()
        self.__date = self.__parse_date()
    
    def year(self) -> int:
        return self.__date.year
    
    def day(self) -> int:
        return self.__date.day
    
    def month(self) -> int:
        return self.__date.month

    def __date_format(self) -> str:
        return 'DD/MM/YYYY'

    def __valid_date_string_entry(self) -> None:
        n_bars = self.__date_string.count('/')
        if n_bars != 2:
            raise ValueError(f'date_string entry is invalid! Expected format: {self.__date_format()}')
        day, month, year = self.__date_string.split('/')
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            raise ValueError(f'date_string must contain only digits. Expected format: {self.__date_format()}')
        if len(year) != 4:
            raise ValueError(f'Year must be 4 digits. Got: {year}')

    def __parse_date(self) -> date:
        day, month, year = map(int, self.__date_string.split('/'))
        try:
            return date(year, month, day)
        except ValueError as e:
            raise ValueError(f'Invalid date: {e}') from e

    def to_date(self) -> date:
        return self.__date

    def __str__(self) -> str:
        return self.__date_string

    def __repr__(self) -> str:
        return f"Date('{self.__date_string}')"

    def __eq__(self, other) -> bool:
        if isinstance(other, Date):
            return self.to_date() == other.to_date()
        return False