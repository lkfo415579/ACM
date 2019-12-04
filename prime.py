import time

before = time.time()


def primes(kmax):
    result = []
    p = [0 for i in range(kmax)]

    # if kmax > 1000:
    #     kmax = 1000
    k = 0
    n = 2
    while k < kmax:
        i = 0
        while i < k and n % p[i] != 0:
            i = i + 1
        if i == k:
            p[k] = n
            k = k + 1
            result.append(n)
        n = n + 1
    return result


test = primes(10000)
print (len(test))
after = time.time()

# print test
print ("time: This is python\n", after - before, 's')
print ((after - before) * 1000, 'ms')