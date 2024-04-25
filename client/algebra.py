import random
from primefac import primefac


def ctz(v):
    """
    Returns number of trailing zeros from binary representation of v.
    :param v: Number to be processed.
    """
    return (v & -v).bit_length() - 1


def fast_gcd(u, v):
    """
    Returns the greatest common divisor of u and v.
    :param u: First number.
    :param v: Second number.
    """
    if u == 0:
        return v
    if v == 0:
        return u
    uz = ctz(u)
    vz = ctz(v)
    shift = uz if vz > uz else vz
    u >>= uz
    while True:
        v >>= vz
        diff = v - u
        vz = ctz(diff)
        if diff == 0:
            break
        if v < u:
            u = v
        v = abs(diff)
    return u << shift


def fast_exp(base, exp, mod):
    """
    Returns based raised to the power of exponent modulo exp.
    :param base: The base of the exponent.
    :param exp: The exponent.
    :param mod: The modulus.
    """
    # If mod is a composite number, we can improve efficiency
    if mod & 1 == 0:
        exp = exp % totient(mod)

    base = base % mod
    result = 1
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp = exp >> 1
    return result


def miller_rabin_primality_test(number, rounds=20) -> bool:
    """
    Tests if a number is prime or not.
    :param number: Number to be cheked.
    :param rounds: Total number of rounds.
    """
    if number & 1 == 0:
        return False
    if number in [0, 1, 4, 6, 8, 9]:
        return False
    if number in [2, 3, 5, 7]:
        return True
    d = number - 1
    # Compute number - 1 = 2^s * d
    s = 1
    while d % 2 == 0:
        s += 1
        d = d // 2

    # Now we have s and d
    def trial_composite(a):
        if fast_exp(a, d, number) == 1:
            return False
        for i in range(s):
            if fast_exp(a, 2 ** i * d, number) == number - 1:
                return False
        return True

    for _ in range(rounds):
        a = random.randint(2, number)
        if trial_composite(a):
            return False
    return True


def totient(number):
    """
    Returns the totient function (Euler indicator) of the number.
    :param number: Number to be chcked.
    """
    result = number
    factors = set(primefac(number))
    for factor in factors:
        result -= result // factor
    return result


def random_big_prime(bits_num):
    """
    Generates a random big prime number with the given bits_num number of bits.
    :param bits_num: Number of bits for the generated prime number.
    """
    while True:
        rand_number = random.randrange(2 ** (bits_num - 1) + 1, 2 ** bits_num - 1)
        if miller_rabin_primality_test(rand_number):
            return rand_number


def multiplicative_inverse(e, phi):
    """
    Returns the multiplicative inverse.
    :param e:
    :param phi:
    :return:
    """
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi
