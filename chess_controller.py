# -*- coding: utf-8 -*-
#  @file        - chess_controller.py
#  @author      - dongnian.wang(dongnian.wang@outlook.com)
#  @brief       - 国际跳棋逻辑控制类
#  @version     - 0.0
#  @date        - 2022.07.06
#  @copyright   - Copyright (c) 2021 

from chess_board import ChessBoard
from chess_state import ChessState, ChessPoint, ChessType

from PyQt5.QtCore import QObject, QPoint, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore

from collections import deque

class ChessController(QObject):
    """ 游戏控制类
    """

    """ 信号
    """
    state_change_signal = pyqtSignal(int, ChessState)
    game_end_signal = pyqtSignal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        """ 初始化
        """
        self.chess_size = 6
        self.chess_row = 2

        self.rival_chess_color = ChessType.BLACK    # 对手棋子颜色
        self.my_chess_color = ChessType.RED         # 我方棋子颜色

        self.first_state = None     # 游戏初始状态
        self.curr_state= None       # 当前游戏状态

        self.select_chess = ChessPoint(-1, -1, ChessType.EMPTY)

        self.gamerunning = False

        # player 为 1 代表红色方（自己），-1 代表黑色（对手）
        self._player = 1

        # 是否对手先手标志位
        self._is_rival_first_go = False

        self.game_running_queue = deque()

    def start_game(self, player, rival_chess_color=ChessType.BLACK):
        """ 游戏开始
        """
        self.rival_chess_color = rival_chess_color
        if self.rival_chess_color == ChessType.BLACK:
            self.my_chess_color = ChessType.RED
        else:
            self.my_chess_color = ChessType.BLACK

        self._player = player
        
        self.first_state = ChessState(self.chess_size)
        for i in range(0, self.chess_row):
            for j in range(0, self.chess_size):
                self.first_state.chess_state[i][j] = ChessType.BLACK
        for i in range(self.chess_size - self.chess_row, self.chess_size):
            for j in range(0, self.chess_size):
                self.first_state.chess_state[i][j] = ChessType.RED

        print("first: ", self.first_state.chess_state)
        if self.curr_state is not None:
            self.curr_state = None
        self.curr_state = self.first_state.copy()

        self.state_change_signal.emit(self._player, self.curr_state)
        self.game_running_queue.append((self._player, self.first_state.copy()))

        self.gamerunning = True

        if self._player == 1:
            # 我方走，AI
            pass
        elif self._player == -1:
            # 对手走，
            pass

        # if self._is_rival_first_go:
        #     # 对手先走, 鼠标点击事件
        #     self._player = 1
        #     pass
        # else :
        #     # 我方走, AI
        #     self._player = -1
        #     pass

    def game_over(self):
        """ 游戏结束
        """
        self.gamerunning = False
        if self.curr_state is not None:
            self.curr_state = None
        self.first_state = None

    def who_win(self, state:ChessState) -> ChessType:
        """ 判断输赢
        """
        if state.chess_state[2] == 0 or state.chess_state[3] == 0:
            return ChessType.BLACK
        if state.chess_state[0]  == 0 or state.chess_state[1] == 0:
            return ChessType.RED

        return ChessType.GOON

    def calc_chess_counts(self, state:ChessState):
        """ 统计各类棋子数目以及可移动数
        """
        state.clear_chess_counts()
        for row in range(0, self.chess_size):
            for col in range(0, self.chess_size):
                if state.at(row, col) == ChessType.RED:
                    state.chess_counts[0] += 1
                elif state.at(row, col) == ChessType.BLACK:
                    state.chess_counts[2] += 1
                

    # @pyqtSlot()
    # def select_first_radio(self, game_name, game_addr, state):
    #     """ 选择是否先手
    #     """
    #     if state == Qt.Checked:
    #         self._is_rival_first_go = False
    #     else:
    #         self._is_rival_first_go = True
    #     self.start_game()
    #     print("state: ", state)

    def _check_coord(self, coord) -> bool:
        """ 检查坐标是否正确
        """
        if coord >= 0 and coord < self.chess_size:
            return True
        return False
    
    def change_state(self, state:ChessState):
        """ 棋子移动
        """
        self.curr_state = state.copy()
        self.game_running_queue.append((self._player, self.curr_state))
        self.state_change_signal.emit(self._player, self.curr_state)

        win_chess_color = self.who_win(self.curr_state)
        if win_chess_color != ChessType.GOON:
            self.gamerunning = False
            self.game_end_signal.emit(win_chess_color)

    @pyqtSlot()
    def regret_chess_slot(self):
        """ 悔棋槽函数
        """
        if len(self.game_running_queue) == 1:
            QMessageBox.warning(None, '警告', "已无法悔棋", QMessageBox.Yes | QMessageBox.No)
            return
        # print("333333333: ", len(self.checker_runing))
        # print(self.curr_state.chess_state)
        self.game_running_queue.pop()
        self._player, self.curr_state = self.game_running_queue[-1]
        # print("444444444: ", len(self.checker_runing))
        # print(self.curr_state.chess_state)
        self.state_change_signal.emit(self._player, self.curr_state)

        win_chess_color = self.who_win(self.curr_state)
        if win_chess_color != ChessType.GOON:
            self.gamerunning = False
            self.game_end_signal.emit(win_chess_color)

    def mouse_clicked_slot(self, row:int, col:int):
        """ 鼠标点击事件
        """
        print("recv: row:{}, col:{}".format(row, col))

        if self.select_chess.x == -1 and self.select_chess.y == -1 and self.select_chess.type == ChessType.EMPTY:
            self._to_select_chess(row, col)
        else :
            self._to_move_chess(row, col)
            # if self._player == -1 and self.select_chess.type == ChessType.BLACK:
            #     self._to_move_chess(row, col)
            # else:
            #     self._to_select_chess(row, col)
    
    def _to_select_chess(self, row : int, col : int):
        """ 选择棋子
        """
        if row >= 0 and row < 6 and col >= 0 and col < 6        \
            and self.curr_state.at(row, col) != ChessType.EMPTY :
            self.select_chess.x = row
            self.select_chess.y = col
            self.select_chess.type = self.curr_state.at(row, col)
            print("select")

    def _to_move_chess(self, row : int, col : int):
        """ 移动棋子
        """
        if self.select_chess.type == self.curr_state.at(row, col):
            self._to_select_chess(row, col)
            return
        # print("00")
        if self.curr_state.at(row, col) == ChessType.EMPTY:
            tmp_state = self.curr_state.copy()
            
            tmp_state.chess_state[self.select_chess.x][self.select_chess.y] = ChessType.EMPTY
            tmp_state.chess_state[row][col] = self.select_chess.type
            print("move")
            self._player = -self._player
            self.change_state(tmp_state)
            self.select_chess = ChessPoint(-1, -1, ChessType.EMPTY)




