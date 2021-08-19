import time
import json
from PyQt5 import QtCore
from datetime import date
from canvas import CanvasWidget
from PyQt5.QtWidgets import qApp, QMainWindow, QApplication, QPushButton, QAction
from canvas import CanvasWidget
from args import COLOR_BLOCK_SIZE, COLOR_X, DIMENSION, GRID_SIZE
import sys
from color_block import ColorBlock
from bili_listener import Listener
from bili_chat import Spider

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        length = GRID_SIZE*(DIMENSION+6)+COLOR_BLOCK_SIZE*(COLOR_X+1)
        height = GRID_SIZE*(DIMENSION+4)
        self.setGeometry(50,50,length,height)
        self.setWindowTitle("Pixel Art")
        self.canvas = CanvasWidget(self)
        self.colorBlock = ColorBlock(self)

        # push button to start
        # self.pushButton = QPushButton(self)
        # self.pushButton.resize(113, 32)
        # self.pushButton.setGeometry(QtCore.QRect(GRID_SIZE*(DIMENSION//2-1), GRID_SIZE*(DIMENSION+1), 113, 32))
        # self.pushButton.setText("Start")
        # self.pushButton.clicked.connect(self.start)

        self.statusBar()

        self.init_menubar()
        print("Initailized main window")
        self.log = []

    def init_menubar(self):

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit the program')
        exitAct.triggered.connect(qApp.quit)

        saveAct = QAction('&Save', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('Save the current paint')
        saveAct.triggered.connect(self.SaveLog)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&Setting')
        fileMenu.addAction(saveAct)
        fileMenu.addAction(exitAct)

        self.new_painting()

    def SaveLog(self):
        print("Saved")
        savelog = {}
        savelog['board'] = self.canvas.paint_grid
        savelog['userlog'] = self.log

        currentdate = date.today().strftime("%y_%m_%d")
        filename = currentdate+'.txt'
        with open(filename, 'w') as outfile:
            json.dump(savelog, outfile)

    def start(self):
        print("button clicked")
        self.new_painting()


    def new_painting(self):
        print("Start listening for the chat")
        self.worker = UpdateChatThread()
        self.worker.start()
        self.worker.command.connect(self.update_canvas)

    def update_canvas(self, res):
        for x, y, color, uid, msgtime in res:
            print("uid:{:<10}, position:({},{}), color:{}, time:{}".format(uid, x, y, color, msgtime))
            self.log.append({'x':x-1, 'y':y-1, 'color':color, 'uid':uid, 'time':msgtime})
            self.canvas.paint_block(x-1, y-1, color)
    


class UpdateChatThread(QtCore.QThread):
    command = QtCore.pyqtSignal(list)
    def __init__(self) -> None:
        super(UpdateChatThread, self).__init__()
        # self.bili_listener = Listener()
        self.chat = Spider()

    def run(self):
        while True:
            # res = self.bili_listener.get_command(input("input command with code 2 format\n"), 2)
            # self.command.emit(res)
            res = self.chat.get_msg()
            if not res:
                continue
            self.command.emit(res)
            # try:
            #     msg_bytes = self.chat.ws.recv()
            #     print(msg_bytes)
            #     msg = self.chat._handle_message(msg_bytes)
            #     print("msg return:", msg)
            #     if msg:  
            #         self.command.emit(msg)
            # except Exception as e:
            #     print("Get message failed")
            #     pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

