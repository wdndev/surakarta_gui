# -*- coding: utf-8 -*-
#  @file        - chess_button.py
#  @author      - dongnian.wang(dongnian.wang@outlook.com)
#  @brief       - 自定义按钮
#  @version     - 0.0
#  @date        - 2022.07.20
#  @copyright   - Copyright (c) 2021 

from PyQt5.QtWidgets import QPushButton

class ChessButton(QPushButton):
    """ 棋子类，用于绘制棋子
    """
    def __init__(self, *__args):
        super().__init__(*__args)
        """ 初始化
        """
        self.tag = 0
        self.size = 30

    def setup_view(self, is_red):
        """ 棋子颜色、形状初始化
        """
        if is_red:
            color = "red"
        else:
            color = "black"
        self.setStyleSheet("background-color: {back};" 
                           "border-radius: {radius};" 
                           "color: white".format(back=color, radius=self.size / 2))

class TargetButton(QPushButton):

    def __init__(self, *__args):
        super().__init__(*__args)
        self.x = None
        self.y = None
        self.size = 15
        self.setStyleSheet("background: #FFFF00;" 
                           "border-radius: {radius};" 
                           "color: black".format(radius=self.size / 2))
        self.setGeometry(0, 0, self.size, self.size)
        self.setText("x")

    def setup_frame(self, frame):
        self.x = frame[2]
        self.y = frame[3]
        self.move(frame[1] - self.size / 2, frame[0] - self.size / 2)
