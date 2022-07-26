
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QMainWindow, QLabel, QToolBar, QMessageBox, QToolButton
from PyQt5.QtWidgets import QSizePolicy,  QTextBrowser
from PyQt5.QtCore import Qt,QSize, QTimer, QTime, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap

from chess_board import ChessBoard, INTERVAL
from chess_controller import ChessController
from chess_state import ChessState, ChessType

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

        # 定时器初始化
        self._init_timer()

        # 游戏是否开始
        self._is_game_begin = False
        # player 为 1 代表红色方（自己），-1 代表黑色（对手）
        self._player = 1
        # 设置窗口
        self.setting = GameSetting()
        self.game = ChessController()

        

        # 信号连接
        ## 菜单栏 
        self.game_new_act.triggered.connect(self.start_new_game_slot)
        self.game_quit_act.triggered.connect(self.game_over_slot)
        self.game_setting_act.triggered.connect(self.game_setting)
        self.game_rule_act.triggered.connect(self.game_rule)

        ## 设置界面
        self.setting.setting_change_signal.connect(partial(self.select_first_radio))

        ## 游戏控制和棋盘显示信号
        self.game.state_change_signal.connect(partial(self.game_board_widget.set_state_slot))
        self.game.state_change_signal.connect(partial(self.updata_chess_num))
        self.game.state_change_signal.connect(partial(self.updata_player))

        ## 中央显示组件信号
        self.pushButton_restart.clicked.connect(self.start_new_game_slot)
        self.pushButton_regret.clicked.connect(self.game.regret_chess_slot)

        ## 鼠标点击事件信号连接
        self.game_board_widget.mouse_clicked_signal.connect(self.game.mouse_clicked_slot)


        # self.start_new_game_slot()
        
        
    def init_ui(self):
        """ 初始化界面
        """
        self.setWindowTitle("苏拉卡尔塔（Surakarta）")  # 窗口名称
        self.setWindowIcon(QIcon("res/icons/icon.png"))  # 窗口图标

        # 工具栏设置
        tool_new_game = QToolButton(self)
        tool_new_game.setIcon(QIcon("res/icons/icon.png"))
        tool_new_game.setToolTip("新游戏")
        tool_new_game.clicked.connect(self.start_new_game_slot)
        tool_setting = QToolButton(self)
        tool_setting.setIcon(QIcon("res/icons/setting.png"))
        tool_setting.setToolTip("设置")
        tool_setting.clicked.connect(self.game_setting)
        tool_rule = QToolButton(self)
        tool_rule.setIcon(QIcon("res/icons/rule.png"))
        tool_rule.setToolTip("规则")
        tool_rule.clicked.connect(self.game_rule)
        tool_test = QToolButton(self)
        tool_test.setIcon(QIcon("res/icons/test.png"))
        tool_test.setToolTip("测试")
        tool_test.clicked.connect(self.chess_state_test)
        tool_test2 = QToolButton(self)
        tool_test2.setIcon(QIcon("res/icons/test.png"))
        tool_test2.setToolTip("测试2")
        tool_test2.clicked.connect(self.chess_state_test2)

        self.toolBar.addWidget(tool_new_game)
        self.toolBar.addWidget(tool_setting)
        self.toolBar.addWidget(tool_rule)
        self.toolBar.addWidget(tool_test)
        self.toolBar.addWidget(tool_test2)

        # 界面组件
        self.red_time_label.setText("00:00")
        self.red_time_label.setStyleSheet("color: red")

        self.black_time_label.setText("00:00")
        self.black_time_label.setStyleSheet("color: black")

        # 状态栏
        self.black_icon = QLabel()
        self.black_icon.setPixmap(QPixmap("res/icons/blacklabel.png"))
        self.statusbar.addWidget(self.black_icon)

        self.black_label = QLabel()
        self.statusbar.addWidget(self.black_label)

        self.red_icon = QLabel()
        self.red_icon.setPixmap(QPixmap("res/icons/redlabel.png"))
        self.statusbar.addWidget(self.red_icon)

        self.red_label = QLabel()
        self.statusbar.addWidget(self.red_label)

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

    
    @pyqtSlot()
    def start_new_game_slot(self):
        """ 开始新的游戏
        """
        self.my_chess_color = ChessType.RED
        rival_chess_color = None
        if self.my_chess_color == ChessType.RED:
            rival_chess_color = ChessType.BLACK
        else:
            rival_chess_color = ChessType.RED
        print("player1: ", self._player)
        self.game.start_game(self._player, rival_chess_color)
    
    @pyqtSlot()
    def game_over_slot(self):
        """ 程序结束
        """
        self.game.game_over()
        self.close()

    @pyqtSlot()
    def game_win_slot(self, win_color:ChessType):
        """ 游戏结束
        """
        string = None
        if win_color == self.my_chess_color:
            string = "我方胜利！ \n再来一局？"
        else:
            string = "对方胜利！ \n再来一局？"
        ret = QMessageBox.question(self, '结果', string, QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.start_new_game_slot()
        else:
            self.game_over_slot()


    @pyqtSlot()
    def time_changed_slot(self):
        """ 显示时间槽函数
        """
        self.time_label.setText(QTime.currentTime().toString("HH:mm:ss"))

    
    @pyqtSlot()
    def updata_chess_num(self, player:int, state:ChessState):
        """ 更新棋子计数器
        """
        self.game.calc_chess_counts(state)
        if len(state.chess_counts) != 0:
            self.red_label.setText("<b><font color=red>{}</font></b>".format(state.counts()[0]))
            self.black_label.setText("<b><font color=black>{}</font></b>".format(state.counts()[2]))

    @pyqtSlot()
    def updata_player(self, player:int, state:ChessState):
        """ 更新玩家状态
        """
        self.red_time_label.setText("00:00")
        self.black_time_label.setText("00:00")
        self._red_time = 0
        self._black_time = 0
        self._player = player
        # self._timer
        # self._timer.setInterval(1000)
        self._timer.start()
        

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


    def _init_timer(self):
        """ 初始化定时器，用于移动棋子计时
        """
        self._red_time = 0
        self._black_time = 0
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._timer_operate_slot)
        # self._timer.start()

    @pyqtSlot()
    def _timer_operate_slot(self):
        """ 移动棋子计时槽函数，
            若 self._player == 1 对移动红色棋子计时；
            若 self._player == -1 对移动黑色棋子计时
        """
        print("plsyer2:", self._player)
        if self._player == 1:
            self._red_time += 1
        elif self._player == -1:
            self._black_time += 1
        time = self._red_time if self._player == 1 else self._black_time
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
        if self._player == 1:
            self.red_time_label.setText(str_m + ":" + str_s)
        else:
            self.black_time_label.setText(str_m + ":" + str_s)

    @pyqtSlot()
    def select_first_radio(self, game_name, game_addr, state):
        """ 选择是否先手
        """
        # 我方先走
        if state == Qt.Checked:
            self._player = 1
        else:
            self._player = -1
        print("state: ", state)
        self.start_new_game_slot()


    
    

    @pyqtSlot()
    def chess_state_test(self):
        """ 游戏规则槽函数
        """
        test_state = self.game.curr_state.copy()
        test_state.chess_state[3][1] = ChessType.BLACK
        test_state.chess_state[4][0] = ChessType.EMPTY
        self.game.change_state(test_state)
        # pass
    @pyqtSlot()
    def chess_state_test2(self):
        """ 游戏规则槽函数
        """
        test_state = self.game.first_state.copy()
        self.game.change_state(test_state)    

        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # app.setStyleSheet(get_app_qss_str("res/style/style.qss"))
    # app.setFont(get_app_font("res/style/FZLTZHUNHJW.TTF"))
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

