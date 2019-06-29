import numpy as np




# 未对输入邻接矩阵作有效性检查，如对角线元素应该为0， 邻接矩阵应该是对称矩阵
# N 节点数量， w无向图矩阵嵌套list形式给出[[]]， start路由起点， end路由终点
def Floyd(N, w, start, end):

    M = 1000  # 延迟达到1000ms及以上表示两点之间无法连接

    edge = np.ones((N, N)) * M
    for i in range(N):
        edge[i, i] = 0

    for li in w:
        edge[li[0], li[1]] = li[2]
        edge[li[1], li[0]] = li[2]
    ''' 
        注意A = edge和A = edge[:]的区别：
        A = edge是将edge数组的引用赋给A， A 和 edge指向同一个list,属于浅拷贝,此后对A的改变都是对edge的改变；
        A = edge[:]是将edge的内容完全复制一份，然后将A指向这个复制的内容, 此时A和edge指向不同的list, 属于深拷贝，此后对A的改变不会影响到edge
    '''

    A = edge[:]
    path = np.zeros((N, N))
    # 初始化path将所有可以访问path(i,j)的前驱置为i(两种情况不需要放前驱，一种是i = j, 自己到自己没有前驱；一种是两者之间的连接矩阵系数为M,表示无法连接)
    for i in range(N):
        for j in range(N):
            path[i, j] = j

    # floyd算法更新邻接距离和path矩阵
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if (A[i, j]>A[i, k] + A[k, j]):
                    A[i, j] = A[i, k] + A[k, j]
                    path[i, j] = path[i, k]

    result = []
    i = int(start)
    j = int(end)
    while (int(path[i, j] != i)):
        tmp = [i, int(path[i, j])]
        result.append(tmp)
        i = int(path[i, j])
    # result.append([i, int(end)])

    return result, A[start,end]

if __name__ == "__main__":
    w = [
        [0, 1, 1], [0, 2, 5], [1, 2, 3], [1, 3, 7],
        [3, 4, 2], [1, 4, 5], [2, 4, 1], [4, 5, 3],
        [2, 5, 7], [3, 6, 3], [4, 6, 6], [6, 7, 2],
        [4, 7, 9], [5, 7, 5], [6, 8, 7], [7, 8, 4]
    ]
    print(Floyd(9,w,0,8))

