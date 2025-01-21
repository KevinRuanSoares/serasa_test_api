from django.core.exceptions import ValidationError


def calculate_digit(digits):
    weight = len(digits) + 1
    total = sum(
        int(digit) * weight for digit, weight in zip(
            digits, range(weight, 1, -1)
        )
    )
    remainder = total % 11
    return '0' if remainder < 2 else str(11 - remainder)


def validate_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        raise ValidationError("Invalid CPF.")
    if cpf == cpf[0] * len(cpf):
        raise ValidationError("Invalid CPF.")
    first_digit = calculate_digit(cpf[:-2])
    if first_digit != cpf[9]:
        raise ValidationError("Invalid CPF.")
    second_digit = calculate_digit(cpf[:-1])
    if second_digit != cpf[10]:
        raise ValidationError("Invalid CPF.")
    return True
