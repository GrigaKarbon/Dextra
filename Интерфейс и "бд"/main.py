import sys
import sqlite3
import math
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QImage, QMovie, QIcon

from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QPushButton, QDialog, QWidget


class Dextra(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('metromenu.ui', self)
        self.image = QImage("Metrokolca_2025_MCD_bm.jpg")
        self.N = 294
        file2 = open("station_dict.txt", "r", encoding='utf-8').read()
        self.dict = eval(file2)
        file3 = open("color_dict.txt", "r", encoding='utf-8').read()
        self.color_dict = eval(file3)
        for i in range(self.N):
            self.comboBox.addItem(self.dict[i])
            self.comboBox_2.addItem(self.dict[i])
            self.comboBox_3.addItem(self.dict[i])
        self.label_6.resize(1147, 1641)
        self.label_6.setPixmap(QPixmap.fromImage(self.image).scaled(self.label_6.size()))
        self.scrollArea.ensureVisible(1400, 1700)
        self.comboBox.setEditable(True)
        self.comboBox.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.comboBox.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.comboBox_2.setEditable(True)
        self.comboBox_2.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.comboBox_2.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.comboBox_3.setEditable(True)
        self.comboBox_3.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.comboBox_3.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.pushButton.clicked.connect(self.return_station)
        self.scrollArea.setWidgetResizable(False)
        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.addButton(self.radioButton)
        self.buttonGroup.addButton(self.radioButton_2)
        self.radioButton.setChecked(True)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.widd = self.label_6.size().width()
        self.heigg = self.label_6.size().height()
        self.recent = set()
        self.menu.triggered.connect(self.info_cl)
        con = sqlite3.connect("usersbd.sqlite")
        cur = con.cursor()
        self.toolButton_4.clicked.connect(self.increas)
        self.increas_rate = 0
        pixmap69 = QPixmap("imgonline-com-ua-Resize-88jlnW2BxY5.jpg")
        self.label_9.setPixmap(pixmap69)
        self.toolButton.setIcon(QIcon('674941_home-icon-png-transparent.jpg'))
        self.toolButton_2.setIcon(QIcon('imgonline-com-ua-Resize-S6HtE2n4lMauW53.jpg'))
        self.toolButton_3.setIcon(QIcon('144-1442771_exit-comments-icon.png'))
        self.toolButton_5.setIcon(QIcon('png-transparent-bookmark-computer-icons-font-awesome-cross-angle-rectangle-black.png'))
        self.toolButton_6.setIcon(QIcon('png-transparent-bookmark-computer-icons-font-awesome-cross-angle-rectangle-black.png'))
        self.toolButton.hide()
        self.toolButton_2.hide()
        self.toolButton_3.hide()
        self.pushButton_4.hide()
        self.pushButton_3.hide()
        self.comboBox_3.hide()
        self.toolButton_5.hide()
        self.toolButton_6.hide()
        self.label_11.hide()
        self.scrollArea_4.hide()
        self.toolButton_3.clicked.connect(self.quit)
        self.pushButton_2.clicked.connect(self.login)
        self.pushButton_3.clicked.connect(self.settings)
        self.toolButton_2.clicked.connect(self.settings)
        self.toolButton.clicked.connect(self.set_homestat)
        self.comboBox_3.currentTextChanged.connect(self.new_homestat)
        self.comboBox_2.currentTextChanged.connect(self.check_feat)
        self.comboBox.currentTextChanged.connect(self.check_feat)
        self.current_user = ""
        self.pushButton_4.clicked.connect(self.quit)
        self.toolButton_5.clicked.connect(self.add_feat)
        self.toolButton_6.clicked.connect(self.add_feat)
        self.turn = 0
        self.x1 = 0
        self.x2 = 0
          # число вершин в графе
        file1 = open("metro_graph.txt", "r").readlines()
        self.D = []
        for line in file1:
            self.D.append(line.split())
        for i in range(len(file1)):
            file1[i] = file1[i].split()
        for i in range(len(file1)):
            for j in range(len(file1[i])):
                file1[i][j] = int(file1[i][j])
        for i in range(len(file1)):
            file1[i][i] = 0

    def zoom_in(self):
        self.label_6.resize(self.widd * 1.1, self.heigg * 1.1)
        self.heigg *= 1.1
        self.widd *= 1.1
        print(self.label_6.size())
        self.label_6.setPixmap(QPixmap.fromImage(self.image).scaled(self.label_6.size()))

    def zoom_out(self):
        self.label_6.resize(self.widd * 0.9, self.heigg * 0.9)
        self.heigg *= 0.9
        self.widd *= 0.9
        print(self.label_6.size())
        self.label_6.setPixmap(QPixmap.fromImage(self.image).scaled(self.label_6.size()))


    def arg_min(self, T, S):
        amin = -1
        m = math.inf  # максимальное значение
        for i in range(len(T)):
            t = T[i][0]
            if t < m and i not in S:
                m = t
                amin = i
        return amin

    def find_path(self, v, x2):
        self.N = len(self.D)
        self.T = []
        for i in range(self.N):
            self.T.append([1000, [1000]])
        self.T[v] = [0, [v]]  # нулевой вес для стартовой вершины
        self.S = {str(v)}
        self.M = [0] * self.N
        while v != -1:  # цикл, пока не просмотрим все вершины
            for j, dw in enumerate(self.D[v]):  # перебираем все связанные вершины с вершиной v
                if str(j) not in self.S:  # если вершина еще не просмотрена
                    w = int(self.T[v][0]) + int(dw)
                    if w < self.T[j][0]:
                        x = self.T[v][1].copy()
                        x.append(j)
                        self.T[j] = [w, x]
                        self.M[j] = v
            v = self.arg_min(self.T, self.S)  # выбираем следующий узел с наименьшим весом
            if v >= 0:  # выбрана очередная вершина
                self.S.add(v)
        path = []
        for i in self.T[x2][1]:
            path.append(self.dict[i])
        lead_color = ""
        strath = ""
        for station in range(len(path)):
            if lead_color == "" or self.color_dict[path[station]] != lead_color or station == len(path) - 1:
                strath += f"{path[station]} \n"
                lead_color = self.color_dict[path[station]]
            elif station + 1 != len(path) and self.color_dict[path[station + 1]] != lead_color:
                strath += f"{path[station]} \n"
                strath += "*переход*\n"
                lead_color = self.color_dict[path[station]]
            else:
                strath += f"    {path[station]} \n"
        if self.T[x2][0] > 60 and self.T[x2][0] % 60 != 0:
            self.label_2.setText(f'{str(self.T[x2][0])} минут/{self.T[x2][0] // 60} ч {self.T[x2][0] % 60} минут, \n {strath}')
        elif self.T[x2][0] == 60 or self.T[x2][0] % 60 == 0:
            self.label_2.setText(f'{str(self.T[x2][0])} минут/{self.T[x2][0] / 60} ч, \n {strath}')
        else:
            self.label_2.setText(f'{str(self.T[x2][0])} минут, \n {strath}')
        print(self.dict[self.x1])
        if self.x1 not in self.recent:
            self.buttonn = QPushButton(f"{self.dict[self.x1]}", self)
            self.buttonn.clicked.connect(self.return_button)
            self.recent.add(self.x1)
            self.verticalLayout.addWidget(self.buttonn)
        if self.x2 not in self.recent:
            self.buttonn2 = QPushButton(f"{self.dict[self.x2]}", self)
            self.buttonn2.clicked.connect(self.return_button)
            self.recent.add(self.x2)
            self.verticalLayout.addWidget(self.buttonn2)
        self.label_2.setWordWrap(True)


    def return_station(self):
        self.x1 = self.comboBox.currentIndex()
        self.x2 = self.comboBox_2.currentIndex()
        if self.x1 != '' and self.x2 != '':
            self.find_path(self.x1, self.x2)

    def return_button(self):
        sender = self.sender()
        text = sender.text()
        if self.radioButton.isChecked():
            self.comboBox.setCurrentText(text)
            self.comboBox.setCurrentIndex(self.comboBox.findText(text))
            self.x1 = self.comboBox.currentIndex()
            self.turn = 1
            self.radioButton_2.setChecked(True)
        else:
            self.comboBox_2.setCurrentText(text)
            self.comboBox_2.setCurrentIndex(self.comboBox_2.findText(text))
            self.x2 = self.comboBox_2.currentIndex()
            self.turn = 0
            self.radioButton.setChecked(True)

    def info_cl(self, action):
        if action == self.action:
            self.c = Infor()
            self.c.show()

    def increas(self):
        if self.increas_rate == 0:
            self.frame_2.setMinimumWidth(250)
            self.increas_rate = 1
        else:
            self.frame_2.setMinimumWidth(50)
            self.increas_rate = 0

    def login(self):
        self.bb = Loginer()
        self.bb.show()

    def loggedin(self, username, password):
        self.toolButton_5.show()
        self.toolButton_6.show()
        self.toolButton.show()
        self.toolButton_2.show()
        self.toolButton_3.show()
        self.pushButton_4.show()
        self.pushButton_3.show()
        self.comboBox_3.show()
        self.pushButton_2.hide()
        self.label_11.show()
        self.scrollArea_4.show()
        self.current_password = password
        self.current_user = username
        self.clearLayout(self.verticalLayout_2)
        con = sqlite3.connect("usersbd.sqlite")
        cur = con.cursor()
        c = cur.execute("""SELECT * FROM stations WHERE user=?""", (self.current_user, )).fetchall()
        for stat in c:
            new_button = QPushButton(f"{stat[0]}")
            new_button.clicked.connect(self.return_button)
            self.verticalLayout_2.addWidget(new_button)

        if len(username) > 20:
            self.label_10.setText(f"{username[:20]}...")
        else:
            self.label_10.setText(f"{username}")

        c = cur.execute("""SELECT EXISTS (SELECT 1 
                                                     FROM homestation 
                                                     WHERE user=?
                                                     LIMIT 1)""", (username, )).fetchone()[0]
        if c:
            homestat = cur.execute("""SELECT * FROM homestation WHERE user=?""", (username, )).fetchall()[0][0]
            self.comboBox.setCurrentText(f'{homestat}')
            self.comboBox.setCurrentIndex(self.comboBox.findText(homestat))
            self.comboBox_3.setCurrentText(f'{homestat}')
            self.comboBox_3.setCurrentIndex(self.comboBox.findText(homestat))

    def new_homestat(self):
        con = sqlite3.connect("usersbd.sqlite")
        cur = con.cursor()
        new_stat = self.comboBox_3.currentText()
        cur.execute("""UPDATE homestation
                        SET station=?
                        WHERE user=?""", (new_stat, self.current_user))
        con.commit()

    def check_feat(self):
        con = sqlite3.connect("usersbd.sqlite")
        cur = con.cursor()
        stat = self.sender().currentText()
        c = cur.execute("""SELECT EXISTS (SELECT 1 
                                                             FROM stations
                                                             WHERE user=? and station=?
                                                             LIMIT 1)""", (self.current_user, stat)).fetchone()[0]
        if c:
            if self.sender() == self.comboBox:
                self.toolButton_5.setChecked(True)
            else:
                self.toolButton_6.setChecked(True)
        else:
            if self.sender() == self.comboBox:
                self.toolButton_5.setChecked(False)
            else:
                self.toolButton_6.setChecked(False)

    def add_feat(self):
        con = sqlite3.connect("usersbd.sqlite")
        cur = con.cursor()
        if self.sender() == self.toolButton_5:
            stat = self.comboBox.currentText()
        else:
            stat = self.comboBox_2.currentText()
        c = cur.execute("""SELECT EXISTS (SELECT 1 
                                                        FROM stations
                                                        WHERE user=? and station=?
                                                        LIMIT 1)""", (self.current_user, stat)).fetchone()[0]
        if not c:
            cur.execute("""INSERT INTO stations VALUES(?, ?)""", (stat, self.current_user))
            con.commit()
            new_button = QPushButton(f"{stat}")
            new_button.clicked.connect(self.return_button)
            self.verticalLayout_2.addWidget(new_button)
        elif not self.sender().isChecked():
            for but in range(len(self.verticalLayout_2)):
                if self.verticalLayout_2.itemAt(but).widget().text() == stat:
                    delstat = self.verticalLayout_2.itemAt(but).widget()
                    self.verticalLayout_2.removeItem(self.verticalLayout_2.itemAt(but))
                    delstat.deleteLater()
                    delstat = None
            cur.execute("""DELETE FROM stations WHERE station=? and user=?""", (stat, self.current_user))
            con.commit()

    def settings(self):
        self.gggg = Settings(self.current_user, self.current_password)
        self.gggg.show()

    def del_acc(self, us, ps):
        con = sqlite3.connect("usersbd.sqlite")
        cur = con.cursor()
        self.user = us
        self.passw = ps
        cur.execute("""DELETE FROM users WHERE username=? and usernamepass=?""", (self.user, self.passw))
        cur.execute("""DELETE FROM homestation WHERE user=?""", (self.user, ))
        con.commit()
        self.quit(ex)

    def set_homestat(self):
        new_home = self.comboBox_3.currentText()
        self.comboBox.setCurrentText(f"{new_home}")
        self.comboBox.setCurrentIndex(self.comboBox.findText(new_home))

    def quit(self):
        self.current_user = ""
        self.toolButton.hide()
        self.toolButton_2.hide()
        self.toolButton_3.hide()
        self.pushButton_4.hide()
        self.pushButton_3.hide()
        self.comboBox_3.hide()
        self.toolButton_5.hide()
        self.toolButton_6.hide()
        self.pushButton_2.show()
        self.label_11.hide()
        self.scrollArea_4.hide()
        self.clearLayout(self.verticalLayout_2)
        self.comboBox.setCurrentText("")

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())



class Infor(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('metromenu2.ui', self)
        self.setWindowTitle("Справка")
        self.mov1 = QMovie("vone.gif")
        self.mov2 = QMovie("vtwo.gif")
        self.mov3 = QMovie("Видео 14-11-2023 122717.gif")

        pixmap3 = QPixmap('one.jpg')
        self.label_3.setPixmap(pixmap3)

        pixmap5 = QPixmap('EysGBuQq.jpg')
        self.label_5.setPixmap(pixmap5)

        pixmap7 = QPixmap('xftDbRPt.jpg')
        self.label_7.setPixmap(pixmap7)

        pixmap9 = QPixmap('two.jpg')
        self.label_9.setPixmap(pixmap9)

        pixmap17 = QPixmap("newone.jpg")
        self.label_17.setPixmap(pixmap17)

        pixmap19 = QPixmap("newtwo.jpg")
        self.label_19.setPixmap(pixmap19)

        self.label_15.setMovie(self.mov1)
        self.mov1.start()
        self.label_13.setMovie(self.mov2)
        self.mov2.start()
        self.label_21.setMovie(self.mov3)
        self.mov3.start()


class Loginer(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('loginscr.ui', self)
        self.setWindowTitle("Login")
        self.setFixedSize(400, 300)
        self.pushButton_2.clicked.connect(self.check_db)
        self.pushButton.clicked.connect(self.start_register)

    def check_db(self):
        con = sqlite3.connect("usersbd.sqlite")
        cur = con.cursor()
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if username != '' and password != '':
            c = cur.execute("""SELECT EXISTS (SELECT 1 
                                             FROM users 
                                             WHERE username=? and usernamepass=?
                                             LIMIT 1)""", (username, password, )).fetchone()[0]
            if c:
                Dextra.loggedin(ex, username, password)
                self.close()
            else:
                self.label_5.setText("Пользователь не найден(")
        else:
            self.label_5.setText("Имя или пароль не могут быть пустыми!")

    def start_register(self):
        self.gg = Register()
        self.gg.show()
        self.close()


class Register(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('regscr.ui', self)
        self.setWindowTitle("Регистрация")
        self.setFixedSize(400, 268)
        self.pushButton.clicked.connect(self.add_bd)

    def add_bd(self):
        con = sqlite3.connect("usersbd.sqlite")
        cur = con.cursor()
        usernamee = self.lineEdit.text()
        paas = self.lineEdit_2.text()
        if usernamee != '' and paas != '':
            c = cur.execute("""SELECT EXISTS (SELECT 1 
                                                     FROM users 
                                                     WHERE username=?
                                                     LIMIT 1)""", (usernamee, )).fetchone()[0]
            if not c:
                cur.execute("INSERT INTO users VALUES (?, ?)", [usernamee, paas])
                cur.execute("INSERT INTO homestation VALUES (?, ?)", ["", usernamee])
                con.commit()
                self.close()
            else:
                self.label_5.setText("Такой логин уже занят(")
        else:
            self.label_5.setText('Имя или пароль не могут быть пустыми!!')


class Settings(QWidget):
    def __init__(self, username, password):
        super().__init__()
        uic.loadUi('settings.ui', self)
        self.setWindowTitle("Настройки")
        self.setFixedSize(620, 449)
        self.username = username
        self.password = password
        self.pushButton.clicked.connect(self.log_change)
        self.pushButton_2.clicked.connect(self.pass_change)
        self.pushButton_3.clicked.connect(self.ac_del)

    def log_change(self):
        con = sqlite3.connect("usersbd.sqlite")
        cur = con.cursor()
        new_log = self.lineEdit.text()
        c = cur.execute("""SELECT EXISTS (SELECT 1 
                                                             FROM users 
                                                             WHERE username=?
                                                             LIMIT 1)""", (new_log,)).fetchone()[0]
        if not c:
            cur.execute("""UPDATE users SET username=? WHERE username=?""", (new_log, self.username))
            cur.execute("""UPDATE stations SET user=? WHERE user=?""", (new_log, self.username))
            cur.execute("""UPDATE homestation SET user=? WHERE user=?""", (new_log, self.username))
            ex.label_10.setText(new_log)
            self.label_3.setText("Успешно!")
            con.commit()
        else:
            self.label_3.setText("Такой логин уже занят(")

    def pass_change(self):
        con = sqlite3.connect("usersbd.sqlite")
        cur = con.cursor()
        new_pass = self.lineEdit_2.text()
        cur.execute("""UPDATE users SET usernamepass=? WHERE username=?""", (new_pass, self.username))
        self.label_5.setText("Успешно!")
        con.commit()

    def ac_del(self):
        self.ggg = Confirm(self.username, self.password)
        self.ggg.show()
        self.close()


class Confirm(QDialog):
    def __init__(self, us, ps):
        super().__init__()
        self.setFixedSize(340, 160)
        self.setWindowTitle("Подтверждение")
        self.username = us
        self.password = ps
        uic.loadUi('conf_dial.ui', self)
        self.pushButton_2.clicked.connect(self.ac_bb)
        self.pushButton.clicked.connect(self.ne_bb)

    def ac_bb(self):
        Dextra.del_acc(Dextra, self.username, self.password)
        self.close()

    def ne_bb(self):
        self.close()

def excepthook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ex = Dextra()
    ex.show()
    sys.exit(app.exec_())