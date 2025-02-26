import random

def generate_matrix(level):
    max_num = level ** 2
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上、下、左、右

    while True:
        matrix = [[0 for _ in range(level)] for _ in range(level)]
        # 随机选择起始位置
        start_row, start_col = random.randint(0, level-1), random.randint(0, level-1)
        matrix[start_row][start_col] = 1
        current_pos = (start_row, start_col)
        current_num = 2

        for _ in range(max_num-1):  # 剩余63个数字需要填入
            # 寻找所有可能的下一步位置及其自由度
            neighbors = []
            for d in directions:
                next_row = current_pos[0] + d[0]
                next_col = current_pos[1] + d[1]
                # 检查是否在矩阵范围内且未被访问过
                if 0 <= next_row < level and 0 <= next_col < level and matrix[next_row][next_col] == 0:
                    # 计算该位置周围未访问的格子数（自由度）
                    freedom = 0
                    for d2 in directions:
                        rr = next_row + d2[0]
                        cc = next_col + d2[1]
                        if 0 <= rr < level and 0 <= cc < level and matrix[rr][cc] == 0:
                            freedom += 1
                    neighbors.append((next_row, next_col, freedom))

            if not neighbors:
                break  # 无路可走，重新生成

            # 选择自由度最小的邻居，若有多个则随机选择
            min_freedom = min(n[2] for n in neighbors)
            candidates = [n for n in neighbors if n[2] == min_freedom]
            next_row, next_col, _ = random.choice(candidates)

            # 填入下一个数字
            matrix[next_row][next_col] = current_num
            current_num += 1
            current_pos = (next_row, next_col)

        # 检查是否成功填满所有数字
        if current_num == max_num+1:
            return matrix

# # 生成矩阵并打印
# matrix = generate_matrix(8)
# for row in matrix:
#     print(row)