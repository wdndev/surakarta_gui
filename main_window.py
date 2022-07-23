
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QMainWindow, QLabel, QToolBar, QMessageBox, QToolButton
from PyQt5.QtWidgets import QSizePolicy,  QTextBrowser
from PyQt5.QtCore import Qt,QSize, QTimer, QTime, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic

from chess_board import ChessBoard, INTERVAL

from functools import partial

from pyui import GameRule, GameSetting

from ui.main_window_ui import Ui_MainWindow
class MainWindow(Ui_MainWindow, QMainWindow):
    """ 主窗口
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setupUi(self)
        self.init_ui()

        # 游戏是否开始
        self._is_game_begin = False
        # player 为 -1 代表红色方，1 代表黑色
        self._player = -1
        # 设置窗口
        self.setting = GameSetting()

        

        # 信号连接
        ## 菜单栏 游戏按钮

        ## 菜单栏 设置按钮
        self.game_setting_act.triggered.connect(self.game_setting)

        ## 菜单栏 帮助按钮
        self.game_rule_act.triggered.connect(self.game_rule)

        ## 设置界面
        self.setting.setting_change_signal.connect(partial(self.game_board_widget.select_first_radio))
        
    @pyqtSlot()
    def test_slot(self, a:int):
        print("aaaaaaaaaaa: ", a)

    def init_ui(self):
        """ 初始化界面
        """
        self.setWindowTitle("苏拉卡尔塔（Surakarta）")  # 窗口名称
        self.setWindowIcon(QIcon("res/icons/icon.png"))  # 窗口图标

        # 工具栏设置
        tool_new_game = QToolButton(self)
        tool_new_game.setIcon(QIcon("res/icons/icon.png"))
        tool_new_game.setToolTip("新游戏")
        tool_setting = QToolButton(self)
        tool_setting.setIcon(QIcon("res/icons/setting.png"))
        tool_setting.setToolTip("设置")
        tool_setting.clicked.connect(self.game_setting)

        self.toolBar.addWidget(tool_new_game)
        self.toolBar.addWidget(tool_setting)

        # 状态栏
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        self.statusbar.addWidget(self.spacer, 1)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.statusbar.addWidget(self.time_label)
        self.time_label.setStyleSheet("color: black;")

        self.timer = QTimer()
        self.timer.timeout.connect(self.time_changed_slot)
        self.timer.start(1000)
        self.red_time_label.setText("00:00")
        self.red_time_label.setStyleSheet("color: red")

        self.black_time_label.setText("00:00")
        self.black_time_label.setStyleSheet("color: black")
        

    # def init_ui(self):
    #     # 窗口初始化
    #     self.setWindowTitle("苏拉卡尔塔（Surakarta）")  # 窗口名称
    #     self.setWindowIcon(QIcon("res/icons/icon.png"))  # 窗口图标
    #     # 窗口大小: 430*400
    #     self.resize(470, 550)                            # 窗口大小: 430*400,  窗口可以随着内容自动变化长度
    #     self.setMinimumSize(QSize(0, 0))                 # 窗口最小的大小
    #     self.setMaximumSize(QSize(16777215, 16777215))   # 窗口最大的大小

    #     # 菜单栏设置
    #     self.menuBar = self.menuBar()
    #     game_menu = self.menuBar.addMenu("游戏")
    #     game_menu.addAction(QIcon("res/icons/icon1.png"), "新游戏")
    #     game_menu.addAction(QIcon("res/icons/reset.png"), "重新开始")
    #     game_menu.addAction(QIcon("res/icons/close.png"), "退出")

    #     setting_menu = self.menuBar.addMenu("设置")

    #     help_menu = self.menuBar.addMenu("帮助")
    #     help_menu.addAction(QIcon(""), "游戏规则", self.game_rule)
    #     help_menu.addAction(QIcon(""), "关于")
    #     self.menuBar.addMenu(help_menu)
        
    #     # 工具栏设置
    #     lift_tool_bar = QToolBar(self)
    #     pointer_reset = QToolButton(self)
    #     pointer_reset.setIcon(QIcon("res/icons/icon.png"))
    #     pointer_reset.setToolTip("新游戏")
    #     pointer_reset2 = QToolButton(self)
    #     pointer_reset2.setIcon(QIcon("res/icons/setting.png"))
    #     pointer_reset2.setToolTip("设置")

    #     lift_tool_bar.addWidget(pointer_reset)
    #     lift_tool_bar.addWidget(pointer_reset2)
    #     lift_tool_bar.setAllowedAreas(Qt.ToolBarArea.LeftToolBarArea)
    #     self.addToolBar(lift_tool_bar)

    #     # 中央组件设置
    #     self.window = ChessBoard()
    #     self.setCentralWidget(self.window)

    #     # 状态栏
    #     self.statusBar = self.statusBar()

    #     # self.white_icon = QLabel()
    #     # self.white_icon.setPixmap(QPixmap("res/icons/whitelabel.png"))
    #     # self.statusBar.addWidget(self.white_icon)

    #     # self.white_label = QLabel()
    #     # self.statusBar.addWidget(self.white_label)

    #     # self.black_icon = QLabel()
    #     # self.black_icon.setPixmap(QPixmap("res/icons/blacklabel.png"))
    #     # self.statusBar.addWidget(self.black_icon)

    #     # self.black_label = QLabel()
    #     # self.statusBar.addWidget(self.black_label)

    #     self.spacer = QWidget()
    #     self.spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
    #     self.statusBar.addWidget(self.spacer, 1)

    #     self.time_label = QLabel()
    #     self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    #     self.statusBar.addWidget(self.time_label)
    #     self.time_label.setStyleSheet("color: black;")

    #     self.timer = QTimer()
    #     self.timer.timeout.connect(self.time_changed_slot)
    #     self.timer.start(1000)

    @pyqtSlot()
    def time_changed_slot(self):
        """ 显示时间槽函数
        """
        self.time_label.setText(QTime.currentTime().toString("HH:mm:ss"))

    @pyqtSlot()
    def game_rule(self):
        """ 游戏规则槽函数
        """
        self.rule_ui = GameRule()
        rule_str = open("res/surakarta__rule.html" ,'r', encoding='utf-8').read()
        self.rule_ui.textBrowser.setText(rule_str)
        self.rule_ui.pushButton.clicked.connect(lambda:self.rule_ui.close())

        self.rule_ui.show()

    @pyqtSlot()
    def game_setting(self):
        """ 游设置槽函数
        """
        self.setting.show()
    
    def _did_click_btn(self, tag):
        """ 棋子按钮按下回调函数
        """
        if self._is_game_begin is False:
            return
        # 判断是否轮到当前玩家下棋
        if self._player == -1 and tag > 12 :
            return
        elif self._player == 1 and tag < 13:
            return


            

    @staticmethod
    def _get_chess_frame(x, y):
        interval = INTERVAL
        begin_x = interval * 2
        begin_y = interval * 2
        return begin_x + x * interval, begin_y + y * interval, x, y
        
        
        




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # app.setStyleSheet(get_app_qss_str("res/style/style.qss"))
    # app.setFont(get_app_font("res/style/FZLTZHUNHJW.TTF"))
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

