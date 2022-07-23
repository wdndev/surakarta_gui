# -*- coding: utf-8 -*-
#  @file        - chess_state.py
#  @author      - dongnian.wang(dongnian.wang@outlook.com)
#  @brief       - 棋子状态类
#  @version     - 0.0
#  @date        - 2022.07.06
#  @copyright   - Copyright (c) 2021 

import copy

class ChessType(enumerate):
    """ 棋子状态类
    """
    GOON = -1,                  # 未赢，继续下棋
    EMPTY = 0,      # 没有任何棋子
    RED   = 1,      # 红色棋子
    BLACK = 2       # 白色棋子

class ChessPoint(object):
    """
        棋子坐标
    """
    def __init__(self, x, y, type) -> None:
        self.x = x
        self.y = y
        self.type = type

    def copy(self):
        """ 深拷贝
        """
        return copy.deepcopy(self)

    def __eq__(self, other) -> bool:
        """ 重载等号
        """
        if self.x == other.x and self.y == other.y and self.type == other.type :
            return True
        return False

class ChessState(object):
    """ 棋子类
    """
    def __init__(self, size:int) -> None:
        self.chess_size = size
        # 所有棋子状态列表
        self.chess_state = [[ChessType.EMPTY for n in range(int(self.chess_size))] for m in range(self.chess_size)]
        # 棋子数量 [红棋，红棋可移动数，黑棋，黑色棋子可移动数]
        self.chess_counts = [0] * 4 

    def size(self) -> int:
        return self.chess_size

    def counts(self):
        """ 返回不同类型棋子的数量，包括空棋
        """
        return self.chess_counts
    
    def clear_chess_counts(self):
        """ 清除所有棋子的数量
        """
        self.chess_counts.clear()
        self.chess_counts = [0] * 4
    
    def copy(self):
        """ 深拷贝
        """
        return copy.deepcopy(self)
    
    def at(self, i:int, j:int):
        """ 返回点的属性
        """
        return self.chess_state[i][j]

    def color(self, i:int, j:int):
        """ 返回棋子颜色
        """
        if self.at(i, j) == ChessType.RED :
            return ChessType.RED
        if self.at(i, j) == ChessType.BLACK :
            return ChessType.BLACK
        return ChessType.EMPTY

    def is_white(self, i:int, j:int):
        """ 是否为红色棋子
        """
        if self.at(i, j) == ChessType.RED :
            return True
        return False

    def is_black(self, i:int, j:int):
        """ 是否为黑色棋子
        """
        if self.at(i, j) == ChessType.BLACK :
            return True
        return False

    def is_empty(self, i:int, j:int):
        """ 是否存在棋子
        """
        if self.at(i, j) == ChessType.EMPTY:
            return True
        return False

