from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtCore import QObject, QPoint, pyqtSignal, pyqtSlot

from functools import partial


from ui.rule_show_ui import Ui_ChessRule
class GameRule(Ui_ChessRule, QWidget):
    """ 游戏规则界面
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("游戏规则")

from ui.setting_ui import Ui_Setting
class GameSetting(Ui_Setting, QMainWindow):
    """ 游戏设置类
    """

    """ 信号
    """
    setting_change_signal = pyqtSignal(str, str, int)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("游戏设置")

        # 默认值
        self.checkBox_sente.setChecked(True)

        # 信号
        self.pushButton_cancel.clicked.connect(partial(self.close))
        self.pushButton_ok.clicked.connect(partial(self.setting_slot))

    @pyqtSlot()
    def setting_slot(self):
        """ 设置槽函数， 用于发送设置界面的参数
        """
        game_name = self.lineEdit_name.text()
        game_addr = self.lineEdit_addr.text()
        check_box_state = self.checkBox_sente.checkState()
        # print("name: {}, adr:{}, state: {}".format(game_name, game_addr, check_box_state))
        # print(type(game_name))
        self.setting_change_signal.emit(game_name, game_addr, check_box_state)
        self.close()



        