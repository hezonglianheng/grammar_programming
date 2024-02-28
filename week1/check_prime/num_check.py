# encoding: utf8
# usage: 检查一个数是否为偶数; 是否为素数并给出与其绝对值差最小的素数

from functools import lru_cache # 用于缓存已经计算的结果, 减小计算开销
from math import sqrt # 求一个数的平方根, 用于判断素数

def is_even(num: int) -> bool:
    """判断一个数是否为偶数
    num: 待判断的数字"""
    return num % 2 == 0

@lru_cache
def is_prime(num: int) -> bool:
    """判断一个数是否为素数
    num: 待判断的数字"""
    if num < 2:
        # 小于2的数字不符合素数判断的条件
        return False
    elif num == 2:
        # 2是素数
        return True
    else:
        # 大于2的数字, 判断从2至其平方根的整数中是否有其因子
        # 遍历从2至其平方根的整数
        for i in range(2, int(sqrt(num)+1), 1):
            if not is_prime(i):
                # 若遍历到的不是素数就跳过
                continue
            else:
                # 否则判断num能否被i整除, 若能则num不是素数
                if num % i == 0:
                    return False
                else:
                    continue
        return True
    
def find_nearest_prime(num: int) -> list[int]:
    """查找与一个数绝对值差最小的素数列表
    num: 查找的基准数
    return: 与基准数绝对值差最小的素数列表"""
    prime_lst = [] # 待填的素数列表
    if is_prime(num):
        # 若num为素数则返回仅有num的列表
        return [num]
    elif num < 2:
        # 对于小于2的数字而言最接近的素数是2
        return [2]
    else:
        # 否则考虑num-(num-2)~num+(num-2)范围内的数字是否为素数
        for i in range(1, num):
            if prime_lst:
                # 若prime_lst中有数字则跳出循环(找到了)
                break
            else:
                # 否则计算与num绝对值差为i的数字是否为素数
                if is_prime(num-i):
                    prime_lst.append(num-i)
                if is_prime(num+i):
                    prime_lst.append(num+i)
        return prime_lst

if __name__ == "__main__":
    for i in range(3, 20):
        print(f"{i}: {is_prime(i)}, {find_nearest_prime(i)}")
