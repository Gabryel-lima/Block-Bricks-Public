
import threading

def as_thrad(func):
    def wraperr(*args, **kwargs):
        thread = threading.Thread(
            target = func,
            args = args,
            kwargs = kwargs 
        )
        thread.start()
        return thread
    return wraperr

# Exemplo de videoaula:

# def deco(f):
#     def wrapper():
#         return "decorado"
#     return wrapper

# @deco
# def target():
#     return "original"

import time
from functools import wraps

def clock(func):
    """Decorator para medir o tempo de execução de uma função."""
    @wraps(func)
    def clocked(*args):
        t0 = time.perf_counter()  # Inicia a contagem de tempo da CPU
        result = func(*args)
        elapsed = time.perf_counter() - t0  # Mede o tempo decorrido

        # Extrai o nome do módulo e da função
        mod_name = func.__module__
        func_name = func.__name__

        # Formata a string de argumentos
        arg_str = ", ".join(repr(arg) for arg in args)

        # Imprime o resultado formatado
        print("\n[%0.8fs] %s.%s(%s) -> %r\n" % (elapsed, mod_name, func_name, arg_str, result))
            # Exemplo abaixo com f_strings
            # print(f"[{elapsed:0.8f}s] {mod_name}.{func_name}({arg_str}) -> {result}")
        return result

    return clocked

from datetime import datetime

@lambda _: _()
def program_start_time() -> str:
    now = datetime.now()
    return f'{now: %c}'

start_time: str = f'{datetime.now(): %c}'

print(start_time)

# @clock
# def soma(a,b):
#     return a + b

# soma(2,3)

# Decorators descartados:

def bool_game_over(func):
    def wrapper(*args):
        nonlocal game_state

        if game_state:
            game_state = 0
            print(game_state)
            return func(*args)
        else:
            game_state = 1
            print(game_state)
            return func(*args)

    def game_over():
        return game_state

    game_state = 0
    wrapper.bool_game_over = game_over
    return wrapper

