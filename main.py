import hashlib
import secrets

from scipy.stats import uniform, t, norm, randint

import matplotlib.pyplot as plt
import numpy as np
from statistics import stdev, mean
import random


def h(data: str, n):
    sha224 = hashlib.sha224()

    sha224.update(bytes.fromhex(str))

    hashed_data = sha224.hexdigest()

    return hashed_data[-int(n/4):]


def genereteVector(bits):
    strBits = str(bin(secrets.randbits(bits)))[2:]
    lenStr = len(strBits)
    strBits = "0" * (bits - lenStr) + strBits
    return strBits


def R(x, n=16):
    r = genereteVector(128 - n)

    s = r + x
    return str(s)

def convertHexToBin(hex, n):
    binStr = str(bin(int(hex, 16)))[2:]
    k = int(len(hex)*n/4)
    return "0"*(k - len(binStr)) + binStr


#0cc7f5ed
def buildTablePrecalculation(K, L, n=16):
    arr = np.array([("", "")]*K, dtype=object)

    for i in range(0, K):
        xi0 = genereteVector(n)
        xij = xi0
        xij1 = ""

        for j in range(0, L):
            xij1 = h(R(xij),n)
            xij = xij1
        arr[i] = (xi0, xij)
    return arr

def buildAttack(table, ha, L, K,n = 16):
    y = ha
    b = False
    x = ""
    for j in range(L):
        for i in range(K):
            if table[i][1] == y:
                x = table[i][0]
                for m in range(L):
                    x = convertHexToBin(h(R(x),n), n)
                    k = convertHexToBin(h(R(x),n),n)
                    if( k== ha):
                        print("PEREMOHA")
                return R(x)
        y = convertHexToBin(h(R(y),n),n)
    return "PROBLEMS"
#buildTablePrecalculation(100,100)



k = 2**10
l = 2**5

n = 16
while True:
    has = h(genereteVector(256),n)
    x = buildAttack(buildTablePrecalculation(k,l,n),convertHexToBin(has,n),l,k)
    if x != "PROBLEMS":
        print(f"h(x_1) = {has}")
        # x = int(x,2)
        print(f"h(x_1)_2 = {convertHexToBin(has,n)}")
        print(f"x = {x}")
        print(f"h_16(x) = {h(x,n)}")
        print(convertHexToBin(h(x,n),n))
        if has == h(x, n):
            print("peremoh")
            break