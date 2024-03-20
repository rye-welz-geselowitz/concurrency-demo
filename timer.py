from datetime import datetime


def timed(f):
    def inner(*args, **kwargs):
        print(f'Starting function {f.__name__}!')
        start_dt = datetime.now()
        res = f(*args, **kwargs)
        end_dt = datetime.now()
        print(f'Function {f.__name__} took {end_dt - start_dt}')
        return res 
    return inner