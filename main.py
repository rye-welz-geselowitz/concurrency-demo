import concurrent.futures
from datetime import datetime

import requests

DO_CONCURRENTLY = True 
CPU_BOUND = False # Alternative: i/o bound
USE_PROCESS_POOL_EXECUTOR = True # Alernative: thread pool executor
MAX_WORKERS = 4

inputs = range(0, 10)


# TIMER UTILITY
def timed(f):
    def inner(*args, **kwargs):
        print(f'Starting function {f.__name__}!')
        start_dt = datetime.now()
        res = f(*args, **kwargs)
        end_dt = datetime.now()
        print(f'Function {f.__name__} took {end_dt - start_dt}')
        return res 
    return inner


# CHUNKS OF WORK
def slow_work_cpu_bound(num):
    for i in range(50_000_000):
        num = num + 1
    return num

def slow_work_io_bound(num):
    r = requests.get('http://httpbin.org/delay/3')
    return f'Status code: {r.status_code}'

# FUNCTIONS THAT COORDINATE MULTIPLE CHUNKS OF WORK
def do_normally(inputs, func):
    return [func(input) for input in inputs]

def do_concurrently(inputs, func):
    executor_class = concurrent.futures.ProcessPoolExecutor if USE_PROCESS_POOL_EXECUTOR else  concurrent.futures.ThreadPoolExecutor
    with executor_class(max_workers=MAX_WORKERS) as executor:
        return executor.map(func, inputs)

# MAIN FUNCTION
@timed
def main():

    print(f'Processing {"concurrently with " + ("ProcessPoolExecutor" if USE_PROCESS_POOL_EXECUTOR else "ThreadPoolExecutor") if DO_CONCURRENTLY else "normally"}')
    if DO_CONCURRENTLY:
        print(f'Max workers: {MAX_WORKERS}')
    print(f'Work is {"cpu bound" if CPU_BOUND else "i/o bound"}')

    handler = do_concurrently if DO_CONCURRENTLY else do_normally

    func = slow_work_cpu_bound if CPU_BOUND else slow_work_io_bound

    outputs = handler(inputs, func)

    for (input, output) in zip(inputs, outputs):
        print(f'{input} -> {output}')


if __name__ == '__main__':
    main()