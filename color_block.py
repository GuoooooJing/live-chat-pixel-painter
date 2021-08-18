from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtWidgets import QWidget
from args import COLOR_CODE, COLOR_X, DIMENSION, GRID_SIZE, COLOR_BLOCK_SIZE, WHITE_TEXT

class ColorBlock(QWidget):
    def __init__(self, centralWidget) -> None:
        super(ColorBlock, self).__init__(centralWidget)
        self.col = COLOR_X
        self.leng = len(COLOR_CODE)
        self.row = self.leng // self.col
        self.x = (DIMENSION+4)*GRID_SIZE
        self.y = (DIMENSION//2)*GRID_SIZE
        self.setGeometry(QRect(self.x, self.y, (self.col+1)*COLOR_BLOCK_SIZE, (self.row+1)*COLOR_BLOCK_SIZE))



    def drawBlock(self, qp):

        qp.setPen(QColor('Black'))
        for i in range(self.row):
            for j in range(self.col):
                pos_x = j*COLOR_BLOCK_SIZE
                pos_y = i*COLOR_BLOCK_SIZE
                r,g,b = COLOR_CODE[i*self.col+j]
                qp.setBrush(QBrush(QColor(r,g,b)))
                qp.drawRect(QRect(pos_x, pos_y, COLOR_BLOCK_SIZE, COLOR_BLOCK_SIZE))
                if i*self.col+j+1 in WHITE_TEXT:
                    qp.setPen(QColor('White'))
                    qp.drawText(QRect(pos_x, pos_y, COLOR_BLOCK_SIZE, COLOR_BLOCK_SIZE), Qt.AlignCenter, str(i*self.col+j+1))
                    # qp.drawText(pos_x+COLOR_BLOCK_SIZE//5, pos_y+COLOR_BLOCK_SIZE, str(i*self.col+j+1))
                    qp.setPen(QColor('Black'))
                else:
                    # qp.drawText(pos_x+COLOR_BLOCK_SIZE//5, pos_y+COLOR_BLOCK_SIZE, str(i*self.col+j+1))
                    qp.drawText(QRect(pos_x, pos_y, COLOR_BLOCK_SIZE, COLOR_BLOCK_SIZE), Qt.AlignCenter, str(i*self.col+j+1))
    
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        pq = QPainter(self)
        self.drawBlock(pq)
        return super().paintEvent(a0)
