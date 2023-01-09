from enum import Enum


class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'
    TRANSGENDER = 'transgender'


class TransactionStatus(Enum):
    Successful = 1
    Failed = 2
