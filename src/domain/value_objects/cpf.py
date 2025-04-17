import re

class CPF:

    def __init__(self, value:str) -> None:
        self.__value = value
        self.__value_formated = self.__cpf_format()
        self.__valid()
    
    @property
    def value(self) -> str:
        return self.__value_formated
    
    def __cpf_format(self) -> str:
        return re.sub(r'\D', '', self.__value )

    def __valid_cpf_length(self) -> None:

        if len(self.__value_formated) != 11:
            raise ValueError('The number of digits is different from 11')
        
    def __valid_all_numbers_are_the_same(self) -> None:
        if self.__value_formated == self.__value_formated[0]*11:
            raise ValueError('All numbers are the same')


    def __valid_cpf(self) -> None:
        
        for i in range(9, 11):
            soma = sum(int(self.__value_formated[j]) * ((i + 1) - j) for j in range(i))
            digito = (soma * 10 % 11) % 10
            if digito != int(self.__value_formated[i]):
                raise ValueError('Check digits are invalid!')
    
    def __valid(self) -> None:
        self.__valid_cpf_length()
        self.__valid_all_numbers_are_the_same()
        self.__valid_cpf()