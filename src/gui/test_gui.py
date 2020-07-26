import sys
from random import randint

from PyQt5.QtCore import pyqtSignal, QBasicTimer, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QMainWindow, QFrame, QApplication, QDesktopWidget


class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.status_bar = self.statusBar()
        self.t_board = Board(self)
        self.initUI()

    def initUI(self):
        self.setCentralWidget(self.t_board)

        self.t_board.msg2_status_bar[str].connect(self.status_bar.showMessage)

        self.t_board.start()

        self.resize(180, 380)
        self.center()
        self.setWindowTitle('Tetris')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


class Board(QFrame):
    msg2_status_bar = pyqtSignal(str)

    BoardWidth = 10
    BoardHeight = 22
    Speed = 300

    def __init__(self, parent):
        super().__init__(parent)

        self.isPaused = False
        self.isStarted = False
        self.board = []
        self.numLinesRemoved = 0
        self.curY = 0
        self.curX = 0
        self.isWaitingAfterLine = False
        self.timer = QBasicTimer()
        self.init_board()

    def init_board(self):

        self.setFocusPolicy(Qt.StrongFocus)
        self.clear_board()

    def shape_at(self, x, y):
        return self.board[(y * Board.BoardWidth) + x]

    def set_shape_at(self, x, y, shape):
        self.board[(y * Board.BoardWidth) + x] = shape

    def square_width(self):
        return self.contentsRect().width() // Board.BoardWidth

    def square_height(self):
        return self.contentsRect().height() // Board.BoardHeight

    def start(self):

        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clear_board()

        self.msg2_status_bar.emit(str(self.numLinesRemoved))

        self.new_piece()
        self.timer.start(Board.Speed, self)

    def pause(self):

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2_status_bar.emit("paused")

        else:
            self.timer.start(Board.Speed, self)
            self.msg2_status_bar.emit(str(self.numLinesRemoved))

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()

        board_top = rect.bottom() - Board.BoardHeight * self.square_height()

        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shape_at(j, Board.BoardHeight - i - 1)

                if shape != Tetrominoe.NoShape:
                    self.draw_square(painter,
                                     rect.left() + j * self.square_width(),
                                     board_top + i * self.square_height(), shape)

        if self.cur_piece.shape() != Tetrominoe.NoShape:

            for i in range(4):
                x = self.curX + self.cur_piece.x(i)
                y = self.curY - self.cur_piece.y(i)
                self.draw_square(painter, rect.left() + x * self.square_width(),
                                 board_top + (Board.BoardHeight - y - 1) * self.square_height(),
                                 self.cur_piece.shape())

    def keyPressEvent(self, event):

        if not self.isStarted or self.cur_piece.shape() == Tetrominoe.NoShape:
            super(Board, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return

        elif key == Qt.Key_Left:
            self.try_move(self.cur_piece, self.curX - 1, self.curY)

        elif key == Qt.Key_Right:
            self.try_move(self.cur_piece, self.curX + 1, self.curY)

        elif key == Qt.Key_Down:
            self.try_move(self.cur_piece.rotate_right(), self.curX, self.curY)

        elif key == Qt.Key_Up:
            self.try_move(self.cur_piece.rotate_left(), self.curX, self.curY)

        elif key == Qt.Key_Space:
            self.drop_down()

        elif key == Qt.Key_D:
            self.one_line_down()

        else:
            super(Board, self).keyPressEvent(event)

    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():

            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.new_piece()
            else:
                self.one_line_down()

        else:
            super(Board, self).timerEvent(event)

    def clear_board(self):

        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Tetrominoe.NoShape)

    def drop_down(self):

        new_y = self.curY

        while new_y > 0:

            if not self.try_move(self.cur_piece, self.curX, new_y - 1):
                break

            new_y -= 1

        self.piece_dropped()

    def one_line_down(self):

        if not self.try_move(self.cur_piece, self.curX, self.curY - 1):
            self.piece_dropped()

    def piece_dropped(self):

        for i in range(4):
            x = self.curX + self.cur_piece.x(i)
            y = self.curY - self.cur_piece.y(i)
            self.set_shape_at(x, y, self.cur_piece.shape())

        self.remove_full_lines()

        if not self.isWaitingAfterLine:
            self.new_piece()

    def remove_full_lines(self):

        num_full_lines = 0
        rows_to_remove = []

        for i in range(Board.BoardHeight):

            n = 0
            for j in range(Board.BoardWidth):
                if not self.shape_at(j, i) == Tetrominoe.NoShape:
                    n = n + 1

            if n == 10:
                rows_to_remove.append(i)

        rows_to_remove.reverse()

        for m in rows_to_remove:

            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                    self.set_shape_at(l, k, self.shape_at(l, k + 1))

        num_full_lines = num_full_lines + len(rows_to_remove)

        if num_full_lines > 0:
            self.numLinesRemoved = self.numLinesRemoved + num_full_lines
            self.msg2_status_bar.emit(str(self.numLinesRemoved))

            self.isWaitingAfterLine = True
            self.cur_piece.setShape(Tetrominoe.NoShape)
            self.update()

    def new_piece(self):

        self.cur_piece = Shape()
        self.cur_piece.se_random_shape()
        self.curX = Board.BoardWidth // 2 + 1
        self.curY = Board.BoardHeight - 1 + self.cur_piece.min_y()

        if not self.try_move(self.cur_piece, self.curX, self.curY):
            self.cur_piece.setShape(Tetrominoe.NoShape)
            self.timer.stop()
            self.isStarted = False
            self.msg2_status_bar.emit("Game over")

    def try_move(self, newPiece, newX, newY):

        for i in range(4):

            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)

            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                return False

            if self.shape_at(x, y) != Tetrominoe.NoShape:
                return False

        self.cur_piece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()

        return True

    def draw_square(self, painter, x, y, shape):

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.square_height() - 1, x, y)
        painter.drawLine(x, y, x + self.square_width() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.square_height() - 1,
                         x + self.square_width() - 1, y + self.square_height() - 1)
        painter.drawLine(x + self.square_width() - 1,
                         y + self.square_height() - 1, x + self.square_width() - 1, y + 1)


class Tetrominoe(object):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class Shape(object):
    coordsTable = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),
        ((0, -1), (0, 0), (1, 0), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((-1, 0), (0, 0), (1, 0), (0, 1)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((-1, -1), (0, -1), (0, 0), (0, 1)),
        ((1, -1), (0, -1), (0, 0), (0, 1))
    )

    def __init__(self):

        self.coords = [[0, 0] for i in range(4)]
        self.pieceShape = Tetrominoe.NoShape

        self.setShape(Tetrominoe.NoShape)

    def shape(self):
        return self.pieceShape

    def setShape(self, shape):

        table = Shape.coordsTable[shape]

        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def se_random_shape(self):
        self.setShape(randint(1, 7))

    def x(self, index):
        return self.coords[index][0]

    def y(self, index):
        return self.coords[index][1]

    def set_x(self, index, x):
        self.coords[index][0] = x

    def set_y(self, index, y):
        self.coords[index][1] = y

    def min_x(self):

        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

    def max_x(self):

        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    def min_y(self):

        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    def max_y(self):

        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

    def rotate_left(self):

        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.set_x(i, self.y(i))
            result.set_y(i, -self.x(i))

        return result

    def rotate_right(self):

        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.set_x(i, -self.y(i))
            result.set_y(i, self.x(i))

        return result


def main():
    app = QApplication([])
    tetris = Tetris()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
