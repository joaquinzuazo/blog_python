def suma(a: int, b: int):
    return a + b

def dividir(a: int, b: int):
    if b == 0:
        raise ZeroDivisionError("El divisor no puede ser cero.")
    return a / b