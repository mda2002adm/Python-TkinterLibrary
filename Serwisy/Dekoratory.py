import functools
#Komunikaty operacyjne

def wykonywanie_operacji(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Początek wykonywania operacji: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            print(f"Operacja {func.__name__} zostałą pomyślnie ukończona.")
            return result
        except Exception as e:
            print(f"Błąd w operacji {func.__name__}: {e}")
            raise e
    return wrapper