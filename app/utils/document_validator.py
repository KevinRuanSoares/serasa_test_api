import re
from django.core.exceptions import ValidationError


def validate_cpf_cnpj(value):
    """
    Validate whether the provided value is a valid CPF or CNPJ.
    """
    cpf_cnpj = re.sub(r"[^0-9]", "", value)  # Remove non-numeric characters

    if len(cpf_cnpj) == 11:
        if not validate_cpf(cpf_cnpj):
            raise ValidationError("CPF inválido.")
    elif len(cpf_cnpj) == 14:
        if not validate_cnpj(cpf_cnpj):
            raise ValidationError("CNPJ inválido.")
    else:
        raise ValidationError("O valor informado não é um CPF ou CNPJ válido.")


def validate_cpf(cpf):
    """
    Validate CPF (Cadastro de Pessoas Físicas).
    """
    if len(cpf) != 11 or cpf in ("00000000000", "11111111111", "22222222222", "33333333333",
                                 "44444444444", "55555555555", "66666666666", "77777777777",
                                 "88888888888", "99999999999"):
        return False

    # Calculate first verification digit
    sum_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digit_1 = (sum_1 * 10 % 11) % 10

    # Calculate second verification digit
    sum_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digit_2 = (sum_2 * 10 % 11) % 10

    return cpf[-2:] == f"{digit_1}{digit_2}"


def validate_cnpj(cnpj):
    """
    Validate CNPJ (Cadastro Nacional da Pessoa Jurídica).
    """
    if len(cnpj) != 14 or cnpj in ("00000000000000", "11111111111111", "22222222222222",
                                   "33333333333333", "44444444444444", "55555555555555",
                                   "66666666666666", "77777777777777", "88888888888888",
                                   "99999999999999"):
        return False

    # Calculate first verification digit
    weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_1 = sum(int(cnpj[i]) * weights_1[i] for i in range(12))
    digit_1 = (sum_1 % 11)
    digit_1 = 0 if digit_1 < 2 else 11 - digit_1

    # Calculate second verification digit
    weights_2 = [6] + weights_1
    sum_2 = sum(int(cnpj[i]) * weights_2[i] for i in range(13))
    digit_2 = (sum_2 % 11)
    digit_2 = 0 if digit_2 < 2 else 11 - digit_2

    return cnpj[-2:] == f"{digit_1}{digit_2}"
