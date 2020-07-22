import sys

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QFont
class Test(QWidget):
    qr:QRect

    def center(self):
        qr = self.frameGeometry()


# def main():
#     app = QApplication(sys.argv)
#     w = QWidget()
#     w.sef
#     w.resize(250, 150)
#     w.move(300, 300)
#     w.setWindowTitle('Simple')
#     w.show()
#     sys.exit(app.exec_())

if __name__ == '__main__':
    s = iter('qwerty12')
    for i in s:
        pass
    print('tt',*s)

    # main()
