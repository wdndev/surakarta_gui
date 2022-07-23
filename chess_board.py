# -*- coding: utf-8 -*-
#  @file        - chess_board.py
#  @author      - dongnian.wang(dongnian.wang@outlook.com)
#  @brief       - 棋盘类
#  @version     - 0.0
#  @date        - 2022.07.20
#  @copyright   - Copyright (c) 2021 

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sip
from chess_button import ChessButton, TargetButton

from chess_state import ChessState, ChessType
from copy import deepcopy

INTERVAL = 50
LONG_RADIUS = INTERVAL * 4
SHORT_RADIUS = INTERVAL * 2
CHESS_SIZE = 35


class ChessBoard(QWidget):
    """ 棋盘类
    """

    """ 信号
    """
    mouse_clicked_signal = pyqtSignal(int, int)

    def __init__(self, *__args):
        super().__init__(*__args)

        self.chess_size = 6             # 棋盘大小
        self.curr_state = None          # 当前棋盘状态
        self.zoom = 18

        # self.first_state = ChessState(self.chess_size)
        # for i in range(0, 2):
        #     for j in range(0, self.chess_size):
        #         self.first_state.chess_state[i][j] = ChessType.BLACK
        
        # for i in range(4, 6):
        #     for j in range(0, self.chess_size):
        #         self.first_state.chess_state[i][j] = ChessType.RED
        
        # self.curr_state = self.first_state.copy()

        self.rival_chess_color = None


        # # 棋子点击时，回调函数
        # self.click_callback = None
        # # 
        # self.target_click_callback = None
        # # 移动棋子回调函数
        # self.chess_move_callback = None
        # # 游戏开始回调函数，参数为 self._is_rival_first_go
        # self.game_begin_callback = None
        # # 改变下棋模式回调函数，1：人人； 2：人机
        # self.change_mode_callback = None
        # # 生成棋谱回调函数
        # self.gen_callback = None    
        # self.targets = []
        # # 棋盘上棋子列表
        # self.chess_list = []
        # player 为 -1代表红色方正在下棋，1 代表黑色方正在下棋
        self._player = -1
        
        # # self._init_view()
        # # 定时器初始化
        # self._init_timer()
        # # 棋子按钮初始化
        # self._setup_buttons()

    def copy(self):
        """ 深拷贝
        """
        return deepcopy(self)
    
    def state(self) -> ChessState:
        """ 返回现在的状态
        """
        return self.curr_state

    def set_state_slot(self, state:ChessState):
        """ 设置棋局状态
        """
        # print(state.size())
        if state != None:
            self.curr_state = state
            # print(state.size())
            self.chess_size = state.size()
            self.repaint()
        else :
            self.clear_slot()

    def clear_slot(self):
        """ 清除点集和当前状态
        """
        self.curr_state = None
        self.update()

    
    def _init_timer(self):
        """ 初始化定时器，用于移动棋子计时
        """
        self._red_time = 0
        self._black_time = 0
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._timer_operate_slot)

    @pyqtSlot()
    def _timer_operate_slot(self):
        """ 移动棋子计时槽函数，
            若 self._player == -1 对移动红色棋子计时；
            若 self._player == 1 对移动黑色棋子计时
        """
        if self._player == -1:
            self._red_time += 1
        else:
            self._black_time += 1
        time = self._red_time if self._player == -1 else self._black_time
        m = int(time / 60)
        if m < 10:
            str_m = "0{m}".format(m=m)
        else:
            str_m = str(m)
        s = time - m * 60
        if s < 10:
            str_s = "0{s}".format(s=s)
        else:
            str_s = str(s)
        if self._player == -1:
            self.red_time_label.setText(str_m + ":" + str_s)
        else:
            self.black_time_label.setText(str_m + ":" + str_s)

    def _setup_buttons(self):
        """ 绘制棋子，棋子本质为自定义按钮
        """
        begin_x = 10+INTERVAL * 2
        begin_y = 10+INTERVAL * 2
        for i in range(0, 24):
            btn = ChessButton(self)
            if i < 6:
                btn.setup_view(False)
                btn.setGeometry(begin_x + INTERVAL * i - CHESS_SIZE / 2,
                                begin_y - CHESS_SIZE / 2,
                                CHESS_SIZE,
                                CHESS_SIZE)
            elif i < 12:
                btn.setup_view(False)
                btn.setGeometry(begin_x + INTERVAL * (i - 6) - CHESS_SIZE / 2,
                                begin_y + INTERVAL - CHESS_SIZE / 2,
                                CHESS_SIZE,
                                CHESS_SIZE)
            elif i < 18:
                btn.setup_view(True)
                btn.setGeometry(begin_x + INTERVAL * (i - 12) - CHESS_SIZE / 2,
                                begin_y + INTERVAL * 4 - CHESS_SIZE / 2,
                                CHESS_SIZE,
                                CHESS_SIZE)
            else:
                btn.setup_view(True)
                btn.setGeometry(begin_x + INTERVAL * (i - 18) - CHESS_SIZE / 2,
                                begin_y + INTERVAL * 5 - CHESS_SIZE / 2,
                                CHESS_SIZE,
                                CHESS_SIZE)
            btn.setText(str(i + 1))
            btn.tag = i + 1
            btn.clicked.connect(self._click_btn_slot)
            self.chess_list.append(btn)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton: 
            begin_x = 10 + INTERVAL * 2 - 18
            begin_y = 10 + INTERVAL * 2 - 18
            row = int( int((event.pos().y() - begin_y) * (self.chess_size) / 300))
            col = int((event.pos().x() - begin_x) * (self.chess_size) / 300)
            # print("event.pos:", event.pos())
            print("coord: row:{}, col:{}".format(row, col))
            self.mouse_clicked_signal.emit(int(row),int(col))

    def paintEvent(self, QPaintEvent):
        """ 重写绘图函数，绘制棋盘
        """
        painter = QPainter(self)

        deep_gree = QColor(0x00, 0x7c, 0x00, 255)
        blue = QColor(0x00, 0xcc, 0xff, 255)
        yellow = QColor(0xfc, 0xfe, 0x00, 255)
        black = QColor(0x00, 0x00, 0x00, 255)
        red = QColor(0xff, 0x00, 0x00, 255)
       
        # 深绿色 007C00
        pen = QPen(deep_gree, 5, Qt.SolidLine)
        painter.setPen(pen)
        ## 左上
        painter.drawArc(10, 10, LONG_RADIUS, LONG_RADIUS, 0, 270 * 16)
        ## 左下
        painter.drawArc(10, 10+INTERVAL * 5, LONG_RADIUS, LONG_RADIUS, 90 * 16, 270 * 16)
        ## 右上
        painter.drawArc(10+INTERVAL * 5, 10+0, LONG_RADIUS, LONG_RADIUS, -90 * 16, 270 * 16)
        ## 右下
        painter.drawArc(10+INTERVAL * 5, 10+INTERVAL * 5, LONG_RADIUS, LONG_RADIUS, -180 * 16, 270 * 16)
        ## 竖线
        painter.drawLine(10+INTERVAL * 4, 10+INTERVAL * 2, 10+INTERVAL * 4, 10+INTERVAL * 7)
        painter.drawLine(10+INTERVAL * 5, 10+INTERVAL * 2, 10+INTERVAL * 5, 10+INTERVAL * 7)
        ## 横线
        painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 4, 10+INTERVAL * 7, 10+INTERVAL * 4)
        painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 5, 10+INTERVAL * 7, 10+INTERVAL * 5)

        # 蓝色 #00CCFF
        pen.setColor(blue)
        painter.setPen(pen)
        ## 左上
        painter.drawArc(10+INTERVAL, 10+INTERVAL, SHORT_RADIUS, SHORT_RADIUS, 0, 270 * 16)
        ## 左下
        painter.drawArc(10+INTERVAL, 10+INTERVAL * 6, SHORT_RADIUS, SHORT_RADIUS, 90 * 16, 270 * 16)
        ## 右上
        painter.drawArc(10+INTERVAL * 6, 10+INTERVAL, SHORT_RADIUS, SHORT_RADIUS, -90 * 16, 270 * 16)
        ## 右下
        painter.drawArc(10+INTERVAL * 6, 10+INTERVAL * 6, SHORT_RADIUS, SHORT_RADIUS, -180 * 16, 270 * 16)
        ## 竖线
        painter.drawLine(10+INTERVAL * 3, 10+INTERVAL * 2, 10+INTERVAL * 3, 10+INTERVAL * 7)
        painter.drawLine(10+INTERVAL * 6, 10+INTERVAL * 2, 10+INTERVAL * 6, 10+INTERVAL * 7)
        ## 横线
        painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 3, 10+INTERVAL * 7, 10+INTERVAL * 3)
        painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 6, 10+INTERVAL * 7, 10+INTERVAL * 6)

        # 黄线 FCFE00
        pen.setColor(yellow)
        painter.setPen(pen)
        ## 竖线
        painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 2, 10+INTERVAL * 2, 10+INTERVAL * 7)
        painter.drawLine(10+INTERVAL * 7, 10+INTERVAL * 2, 10+INTERVAL * 7, 10+INTERVAL * 7)
        ## 横线
        painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 2, 10+INTERVAL * 7, 10+INTERVAL * 2)
        painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 7, 10+INTERVAL * 7, 10+INTERVAL * 7)

        # 如果棋局状态发生了改变
        begin_x = 10 + INTERVAL * 2
        begin_y = 10 + INTERVAL * 2
        if self.curr_state is not None:
            painter.setPen(QPen(QColor(0x00, 0x00, 0x00, 0), self.zoom * 0.0025))
            for row in range(0, self.chess_size):
                for col in range(0, self.chess_size):
                    # 画红棋子
                    coord_row = begin_y + INTERVAL * col
                    coord_col = begin_x + INTERVAL * row
                    painter.setBrush(QBrush(red))
                    if self.curr_state.at(row, col) == ChessType.RED:
                        painter.drawEllipse(QPoint(coord_row, coord_col), self.zoom, self.zoom)
                    
                    # 画黑棋子
                    painter.setBrush(QBrush(black))
                    if self.curr_state.at(row, col) == ChessType.BLACK:
                        painter.drawEllipse(QPoint(coord_row, coord_col), self.zoom, self.zoom)


        # # 左上
        # painter.drawArc(10, 10, LONG_RADIUS, LONG_RADIUS, 0, 270 * 16)
        # painter.drawArc(10+INTERVAL, 10+INTERVAL, SHORT_RADIUS, SHORT_RADIUS, 0, 270 * 16)

        # # 左下
        # painter.drawArc(10, 10+INTERVAL * 5, LONG_RADIUS, LONG_RADIUS, 90 * 16, 270 * 16)
        # painter.drawArc(10+INTERVAL, 10+INTERVAL * 6, SHORT_RADIUS, SHORT_RADIUS, 90 * 16, 270 * 16)

        # # 右上
        # painter.drawArc(10+INTERVAL * 5, 10+0, LONG_RADIUS, LONG_RADIUS, -90 * 16, 270 * 16)
        # painter.drawArc(10+INTERVAL * 6, 10+INTERVAL, SHORT_RADIUS, SHORT_RADIUS, -90 * 16, 270 * 16)

        # # 右下
        # painter.drawArc(10+INTERVAL * 5, 10+INTERVAL * 5, LONG_RADIUS, LONG_RADIUS, -180 * 16, 270 * 16)
        # painter.drawArc(10+INTERVAL * 6, 10+INTERVAL * 6, SHORT_RADIUS, SHORT_RADIUS, -180 * 16, 270 * 16)

        # pen.setColor(Qt.red)
        # painter.setPen(pen)
        # # 竖线
        # painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 2, 10+INTERVAL * 2, 10+INTERVAL * 7)
        # painter.drawLine(10+INTERVAL * 3, 10+INTERVAL * 2, 10+INTERVAL * 3, 10+INTERVAL * 7)
        # painter.drawLine(10+INTERVAL * 4, 10+INTERVAL * 2, 10+INTERVAL * 4, 10+INTERVAL * 7)
        # painter.drawLine(10+INTERVAL * 5, 10+INTERVAL * 2, 10+INTERVAL * 5, 10+INTERVAL * 7)
        # painter.drawLine(10+INTERVAL * 6, 10+INTERVAL * 2, 10+INTERVAL * 6, 10+INTERVAL * 7)
        # painter.drawLine(10+INTERVAL * 7, 10+INTERVAL * 2, 10+INTERVAL * 7, 10+INTERVAL * 7)

        # # 横线
        # painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 2, 10+INTERVAL * 7, 10+INTERVAL * 2)
        # painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 3, 10+INTERVAL * 7, 10+INTERVAL * 3)
        # painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 4, 10+INTERVAL * 7, 10+INTERVAL * 4)
        # painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 5, 10+INTERVAL * 7, 10+INTERVAL * 5)
        # painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 6, 10+INTERVAL * 7, 10+INTERVAL * 6)
        # painter.drawLine(10+INTERVAL * 2, 10+INTERVAL * 7, 10+INTERVAL * 7, 10+INTERVAL * 7)


