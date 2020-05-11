from enum import Enum, unique

@unique
class AllowedHTTPMetohds(Enum):
    POST = "POST"
    GET = "GET"


@unique
class TransactionStatus(Enum):
    NOT_SEND = None  # Transaction wasn't send to the endpoint
    NEW = 'new'  # Nowa, nieobsłużona transakcja
    AUTHORIZED = 'authorized'  # Autoryzacja transakcji (karty)
    PENDING = 'pending'  # Oczekiwanie na status
    SUBMITTED = 'submitted'  # Wysłana do realizacji
    REJECTED = 'rejected'  # Płatność odrzucona
    SETTLED = 'settled'  # Transakcja zrealizowana
    ERROR = 'error'  # Bład podczas realizowania transakcji
    CANCELED = 'canceled'  # Transakcja anulowana


@unique
class PaymentMethod(Enum):
    PAY_BY_LINK = "pbl"
    CREDIT_CARD = "card"
    BLIK = "blik"
    ING = "ing"


@unique
class PayByLinkBank(Enum):
    MTRANSFER = "mtransfer"  # mBank
    BZWBK = "bzwbk"
    PEAKO24 = "peako24"  # Pekao S.A
    INTELIGO = "inteligo"
    IPKO = "ipko"  # PKO BP
    GETIN = "getin"
    NOBLE = "noble"
    IDEABANK = "ideabank"
    CREDITAGRICOLE = "creditagricole"
    T_MOBILE = "tmobile"
    ALIOR = "alior"
    PBS = "pbs"
    MILLENNIUM = "millennium"
    CITI = "citi"  # Citi Handlowy
    BOS = "bos"  # BOŚ
    BNPPARIBAS = "bnpparibas"
    POCZTOWY = "pocztowy"  # Bank Pocztowy24
    PLUS_BANK = "plusbank"
    BS = "bs"  # Bank Spółdzielczy
    BSPB = "bspb"  # Bank Spółdzielczy w Brodnicy
    NEST = "nest"
    ENVELO = "envelo"
    ING = "ing"

@unique
class BlikMethod(Enum):
    BLIK = "blik"


@unique
class PayByCardMethod(Enum):
    SECURE_3D = "ecom3ds"
    ONECLICK = "oneclick"
    RECURRING = "recurring"
