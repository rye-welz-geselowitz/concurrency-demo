from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import requests

from timer import timed


def slow_request(x):
    # I/O bound - input/output
    r = requests.get('http://httpbin.org/delay/3')
    return f'Status code: {r.status_code}'


def slow_computation(num):
    # CPU-bound
    for i in range(50_000_000):
        num += 1 
    return num

# Global Interpret Lock

# CPU-bound - use ProcessPoolExecutor
# I/O-bound - can use ThreadPoolExecutor 

@timed
def main():
    nums = list(range(0, 10))
    # for num in nums:
    #     res = slow_computation(num)
    #     print(res)

    with ProcessPoolExecutor(max_workers=5) as executor:
        res = executor.map(slow_computation, nums)
        print('res', list(res))

if __name__ == '__main__':
    main()


