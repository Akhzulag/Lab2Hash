import hashlib
import secrets
import time
from scipy.stats import uniform, t, norm, randint

import matplotlib.pyplot as plt
import numpy as np
from statistics import stdev, mean
import random
import pickle


def h(data: bytes, n):
    sha224 = hashlib.sha224()

    sha224.update(data)

    hashed_data = sha224.hexdigest()

    return hashed_data[-int(n / 4):]


def toBytes(strHex):
    return bytes.fromhex(strHex)


def generateHex(bits):
    strBits = hex(secrets.randbits(bits))[2:]
    lenStr = len(strBits)
    kT = int(bits / 4)
    strBits = "0" * (kT - lenStr) + strBits
    return strBits


gen = False
r: str = ""

def R(x, n):
    global gen
    global r
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
def buildTablePrecalculation(K, L, n):
    arr = np.array([("", "")] * K, dtype=object)

    for i in range(0, K):
        xi0 = generateHex(n)
        xij = xi0
        for j in range(0, L):
            xij = h(toBytes(R(xij, n)), n)
        arr[i] = (xi0, xij)
        if i % 100000 == 0:
            print(i, K)
    return arr


# def buildAttack(table, ha, L, K, n):
#     y = ha
#     b = False
#     x = ""
#     for j in range(L):
#         for i in range(K):
#             if table[i][1] == y:
#                 x = table[i][0]
#                 for m in range(L - j - 1):
#                     x1 = x
#                     x = h(toBytes(R(x, n)), n)
#                     k = h(toBytes(R(x1, n)), n)
#                     if (h(toBytes(R(x, n)), n) == ha):
#                         print(L - j, m)
#                         print("PEREMOHA", k, x)
#                 return R(x, n)
#         y = h(toBytes(R(y, n)), n)
#     return "PROBLEMS"

def buildAttack(table, index_dict, ha, L, K, n):
    y = ha

    for j in range(L):
        if y in index_dict:
            i = index_dict[y]
            x = table[i][0]
            for m in range(L - j - 1):
                x1 = x
                x = h(toBytes(R(x, n)), n)
                k = h(toBytes(R(x1, n)), n)
                if h(toBytes(R(x, n)), n) == ha:
                    print(L - j, m)
                    print("PEREMOHA", k, x)
                    return R(x, n)
            return "PROBLEMS"

        y = h(toBytes(R(y, n)), n)
    return "PROBLEMS"


n = 32


def save_table_to_file(table1, filename):
    with open(filename, 'wb') as file:
        pickle.dump(table1, file)


def load_table_from_file(filename):
    with open(filename, 'rb') as file:
        table1 = pickle.load(file)
    return table1


def buildAndSave(K, L, n, filename1):
    start_time = time.time()
    table = buildTablePrecalculation(K, L, n)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Час побудови таблиці: {execution_time} секунд:", filename1)
    save_table_to_file(table, filename1)
    print(table)
    return table


def results(table, K, L):
    index_dict = {table[i][1]: i for i in range(K)}
    s = 0
    for _ in range(10_000):
        has = h(toBytes(generateHex(256)), n)
        x = buildAttack(table, index_dict, has, L, K, n)
        if x != "PROBLEMS":
            print("NOT PROBLEMS")
            print(f"h(x_1) = {has}")
            # x = int(x,2)
            print(f"x = {x}")
            print(f"h_16(x) = {h(toBytes(x), n)}")
            print(h(toBytes(x), n))
            if has == h(toBytes(x), n):
                s += 1
                print("peremoh")
                break
    print(f"кількість успіхів: {s}, Pr:{s / 10000}")
    print(f"кількість невдач: {10000 - s}")


# K00 = 2 ** 20
# L00 = 2 ** 10
# tab00 = buildAndSave(K00, L00, 32, "tab00.pkl")
print("1")
print(load_table_from_file("tab00.pkl"))
K01 = 2 ** 20
L01 = 2 ** 11
tab01 = buildAndSave(K01, L01, 32, "tab01.pkl")

print("4")
K02 = 2 ** 20
L02 = 2 ** 12
tab02 = buildAndSave(K02, L02, 32, "tab02.pkl")
print("7")

K11 = 2 ** 22
L11 = 2 ** 11
tab11 = buildAndSave(K11, L11, 32, "tab11.pkl")
print("5")

K10 = 2 ** 22
L10 = 2 ** 10
tab10 = buildAndSave(K10, L10, 32, "tab10.pkl")
print("2")

K12 = 2 ** 22
L12 = 2 ** 12
tab12 = buildAndSave(K12, L12, 32, "tab12.pkl")
print("8")

K20 = 2 ** 24
L20 = 2 ** 10
tab20 = buildAndSave(K20, L20, 32, "tab20.pkl")
print("3")

K21 = 2 ** 24
L21 = 2 ** 11
tab21 = buildAndSave(K21, L21, 32, "tab21.pkl")
print("6")

K22 = 2 ** 24
L22 = 2 ** 12
tab22 = buildAndSave(K22, L22, 32, "tab22.pkl")

# print(f"K = {K00}, L = {L00}")
# results(tab00, K00, L00)
#
# print(f"K = {K10}, L = {L10}")
# results(tab10, K10, L10)
#
# print(f"K = {K20}, L = {L20}")
# results(tab20, K20, L20)
#
# print(f"K = {K01}, L = {L01}")
# results(tab01, K01, L01)
#
# print(f"K = {K11}, L = {L11}")
# results(tab11, K11, L11)
#
# print(f"K = {K21}, L = {L21}")
# results(tab21, K21, L21)
#
# print(f"K = {K02}, L = {L02}")
# results(tab02, K02, L02)
#
# print(f"K = {K12}, L = {L12}")
# results(tab12, K12, L12)
#
# print(f"K = {K22}, L = {L22}")
# results(tab22, K22, L22)
