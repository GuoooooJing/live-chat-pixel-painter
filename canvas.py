from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QBrush, QColor, QPen, QPainter, QPaintEvent
from PyQt5.QtWidgets import QWidget
from args import DIMENSION, GRID_SIZE

class CanvasWidget(QWidget):
    def __init__(self, centralWidget):
        super(CanvasWidget, self).__init__(centralWidget)
        init_x = 35
        init_length = init_x + (DIMENSION+1)*GRID_SIZE
        self.setGeometry(QRect(init_x, init_x, init_length, init_length))
        self.pen_grid = QPen(QColor(20, 20, 20))
        self.pen_grid.setWidth(1)
        self.gray = QBrush(QColor(217, 217, 217))
        self.paint_grid = [[None]*DIMENSION for i in range(DIMENSION)]


    def paintEvent(self, a0: QPaintEvent) -> None:
        qp = QPainter(self)

        self.draw_canvas(qp)
        return super().paintEvent(a0)


    def draw_canvas(self, qp):
        qp.setPen(QColor("Black"))

        # Zero Block
        # qp.drawText(QRect(0, 0, GRID_SIZE, GRID_SIZE), Qt.AlignCenter, '0')
        for i in range(1, DIMENSION+1):
            qp.drawText(QRect(i*GRID_SIZE, 0, GRID_SIZE, GRID_SIZE), Qt.AlignCenter, str(i))
            qp.drawText(QRect(0, i*GRID_SIZE, GRID_SIZE, GRID_SIZE), Qt.AlignCenter, str(i))

        qp.setPen(QColor(0,0,0,0))
        qp.setBrush(self.gray)
        for i in range(1, DIMENSION+1):
            start = 1
            if i%2==0:
                start = 2
            for j in range(start, DIMENSION+1, 2):
                qp.drawRect(QRect(i*GRID_SIZE, j*GRID_SIZE, GRID_SIZE, GRID_SIZE))

        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if self.paint_grid[i][j]:
                    r,g,b = self.paint_grid[i][j]
                    qp.setBrush(QBrush(QColor(r, g, b)))
                    qp.drawRect(QRect((i+1)*GRID_SIZE, (j+1)*GRID_SIZE, GRID_SIZE, GRID_SIZE))

        qp.setPen(self.pen_grid)
        for i in (1, DIMENSION+1):
            qp.drawLine(GRID_SIZE, GRID_SIZE*i, GRID_SIZE*(DIMENSION+1), GRID_SIZE*i)
        
        for i in (1, DIMENSION+1):
            qp.drawLine(GRID_SIZE*i, GRID_SIZE, GRID_SIZE*i, GRID_SIZE*(DIMENSION+1))

    def delete_block(self, i, j):
        self.paint_grid[i][j] = None
        self.update()

    def paint_block(self, i, j, color):
        self.paint_grid[i][j] = color
        self.update()

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = QtWidgets.QMainWindow()
#     window.setGeometry(50,50,500,500)
#     window.setWindowTitle("Window")
#     widget = CanvasWidget()
#     window.setCentralWidget(widget)
#     widget.paint_block(0,0,(50,50,50))
#     widget.paint_block(1,1,(50,50,50))
#     widget.paint_block(15,15,(50,50,50))
#     widget.delete_block(1,1,)
#     window.show()
#     sys.exit(app.exec_())