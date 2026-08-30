import sys
input = lambda: sys.stdin.buffer.readline().decode().strip()
from math import isqrt
from bisect import bisect_right

# d4 = [(0, 1), (-1, 0), (0, -1), (1, 0)]
# d8 = [(0, 1), (-1, 0), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

def read_int(): return(int(input()))
def read_ints(): return(map(int,input().split()))
def read_list(): return(list(map(int,input().split())))
def read_matrix(m,n):
    ans = []
    for _ in range(m):
        ans.append(read_list())
    return ans

def read_graph(n, edges):
    graph = [[] for _ in range(n+1)]
    for _ in range(edges):
        u,v = read_ints()
        graph[u].append(v)
        graph[v].append(u)
    return graph

"""
Yes my answer is wrong right now and I know why. It fails [1,2,3,4,4,4]. For k=1 the answer should be 8 because the 2nd and 3rd element contributes freq 1 while the 4th-6th contribute freq 2 each. My program outputs 7 because it assumes a divide by 2 is necessary.

I noticed VERY EARLY that in at most 18 iterations the answer will be sum(arr) because it would be possible to make every element go to 1. At each round (or k), the max freq an element can contribute is 2 ** round and it can only do so if arr[I] == (2 ** round) * element. If arr[I] > (2 ** round) * element, it can always contribute (2 ** round - 1). Else, if arr[I] < (2 ** round) * element, then it can only contribute (arr[I] // element)
"""

def solve():

    n, k = read_ints()
    arr = sorted(read_list())
    MAX = max(arr)
    SUM = sum(arr)

    ans = [-1]*k

    suffix = [0] * (MAX + 2)

    r = n-1
    for num in range(MAX, 0, -1):
        suffix[num] = suffix[num + 1]
        while r >= 0 and arr[r] >= num:
            suffix[num] += 1
            r -= 1

    # AT MOST 17 attempts will make the answer always 1 and we can stop
    for base in range(1, MAX+1):
        prev_suffix_num = n
        sum_below = 0
        round = 1
        for num in range(base, MAX+1, base):
            count_cleared = prev_suffix_num - suffix[num]
            sum_below += (num // base - 1) * count_cleared
            count_same = suffix[num] - suffix[num + 1]

            if num // base == 2 ** round:
                sum_above = (suffix[num] * (2 ** round - 1)) + count_same # count_same elements are 2 ** round not 2 ** round - 1
                ans[round - 1] = max(ans[round - 1], sum_below + sum_above)
                round += 1
                
            prev_suffix_num = suffix[num]

    for i in range(k):
        if ans[i] == -1: ans[i] = SUM

    print(*ans)

t = read_int()

for _ in range(t):
    solve()
