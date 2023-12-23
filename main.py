import hashlib
import secrets

from scipy.stats import uniform, t, norm, randint

import matplotlib.pyplot as plt
import numpy as np
from statistics import stdev, mean
import random


def h(data: bytes, n):
    sha224 = hashlib.sha224()

    sha224.update(data)

    hashed_data = sha224.hexdigest()

    return hashed_data[-int(n / 4):]


def toBytes(a):
    return bytes.fromhex(a)


def generateHex(bits):
    strBits = hex(secrets.randbits(bits))[2:]
    lenStr = len(strBits)
    kT = int(bits / 4)
    strBits = "0" * (kT - lenStr) + strBits
    return strBits

gen = False
def R(x, n=16):
    global gen
    r: str = ""
    if gen == False:
        r = generateHex(128 - n)
        gen = True
    s = r + x
    return str(s)


def convertHexToBin(hex, n):
    binStr = str(bin(int(hex, 16)))[2:]
    k = int(len(hex) * n / 4)
    return "0" * (k - len(binStr)) + binStr


# 0cc7f5ed
def buildTablePrecalculation(K, L, n=16):
    arr = np.array([("", "")] * K, dtype=object)

    for i in range(0, K):
        xi0 = generateHex(n)
        xij = xi0
        xij1 = ""
        for j in range(0, L):
            xij1 = h(toBytes(R(xij, n)), n)
            xij = xij1
        arr[i] = (xi0, xij)
    return arr


def buildAttack(table, ha, L, K, n=16):
    y = ha
    b = False
    x = ""
    for j in range(L):
        for i in range(K):
            if table[i][1] == y:
                x = table[i][0]
                for m in range(L - j - 1):
                    x1 = x
                    x = h(toBytes(R(x, n)), n)
                    k = h(toBytes(R(x1, n)), n)
                    if (h(toBytes(R(x, n)), n) == ha):
                        print(L - j, m)
                        print("PEREMOHA", k, x)
                return R(x,n)
        y = h(toBytes(R(y, n)), n)
    return "PROBLEMS"


# buildTablePrecalculation(100,100)

def converttohex(byte_data):
    hex_string = ''.join([hex(b)[2:].zfill(2) for b in byte_data])
    return hex_string


for _ in range(1000):
    a = generateHex(16)
    print(a, bytes.fromhex(a), converttohex(bytes.fromhex(a)))

k = 2 ** 10
l = 2 ** 5

n = 16
while True:
    has = h(toBytes(generateHex(256)), n)
    x = buildAttack(buildTablePrecalculation(k, l, n), has, l, k)
    if x != "PROBLEMS":
        print("NOT PROBLEMS")
        print(f"h(x_1) = {has}")
        # x = int(x,2)
        print(f"x = {x}")
        print(f"h_16(x) = {h(toBytes(x), n)}")
        print(h(toBytes(x), n))
        if has == h(toBytes(x), n):
            print("peremoh")
            break
        print()