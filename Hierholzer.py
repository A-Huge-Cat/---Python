""" 有向图欧拉路径的求解 """


def dfs(u):
    """Hierholzer算法"""
    for v in range(n):  # 遍历可以走的边
        if graph[u][v]:  # 判断这条边是否可以走
            graph[u][v] -= 1  # 对应的边数减一
            dfs(v)
    # 遇到阻塞了（邻边都走完了），入栈
    stack.append(u)


def has_path():
    """判断图是否有欧拉路径，顺便找到起点"""
    start_count, end_count = 0, 0
    global start
    for i in range(n):
        in_de, out_de = in_degree[i], out_degree[i]
        diff = in_de - out_de
        if diff == -1:
            start_count += 1
            start = i
        elif diff == 1:
            end_count += 1
        elif diff != 0:
            return False
    # 起终点都只有一个或者全部结点出入度差为0才有欧拉路径
    return start_count == 1 and end_count == 1 or start_count == 0 and out_degree == 0


# 图数据（有向图）
edges = [
    [1, 2],
    [1, 3],
    [2, 2],
    [2, 4],
    [2, 4],
    [3, 1],
    [3, 2],
    [3, 5],
    [4, 3],
    [4, 6],
    [5, 6],
    [6, 3],
]

# 点，边个数
n, m = 7, len(edges)

# 邻接矩阵，重边的对应的graph[u][v]和graph[v][u]自增一
graph = [[0] * n for _ in range(n)]

# 每个结点的出入度
in_degree = [0] * n
out_degree = [0] * n

stack = []
start = 0

# 构建图
for u, v in edges:
    graph[u][v] += 1
    out_degree[u] += 1
    in_degree[v] += 1

# 欧拉路径
if has_path():
    print('The graph exist Euler Path')
    dfs(start)
    [print(str(e) + " -> ", end='') for e in stack[::-1]]
else:
    print("The graph do not exist Euler Path.")

