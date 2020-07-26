from PyQt5.QtCore import QObject, QCoreApplication, Qt, pyqtSignal, QRect
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QToolTip, QMessageBox, \
    QDesktopWidget, QHBoxLayout, QLCDNumber, QSlider, QFrame, QColorDialog
import sys

from PyQt5.uic.properties import QtCore, QtGui
class Communicator(QObject):
    closeApp = pyqtSignal()

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()


    def init_UI(self):
        col = QColor(0, 0, 0)
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)
        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.frm.setGeometry(130, 22, 100, 100)
        qr = QRect()


        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Color dialog')

        self.show()

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def showDialog(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())


def main():
    app = QApplication(sys.argv)
    window = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


