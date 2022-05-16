import sys
import candle_driver
from PyQt5.QtCore import QSize, Qt,QTimer,QDateTime
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont,QPixmap,QIcon
from PyQt5.QtWidgets import QSizePolicy

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, \
QWidget, QAction, QTabWidget, QVBoxLayout, QLabel,QGridLayout

class MyTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.visual_debug_mode = False
        self.moving_flag = False
        self.reading_flag =False
        self.colorVar = 0

        self.layout = QVBoxLayout(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.getForceData)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        # Add tabs
        self.tabs.addTab(self.tab2, "Данные")
        self.tabs.addTab(self.tab1, "Управление")

        # Create first tab "Move"
        self.button_move = QPushButton('Начать движение', self)
        self.button_move.setFont(QFont('Arial', 22))
        self.button_move.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.button_move.clicked.connect(self.on_move_button_click)

        self.button_stop = QPushButton('Остановка', self)
        self.button_stop.setFont(QFont('Arial', 22))
        self.button_stop.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.button_stop.clicked.connect(self.on_stop_button_click)

        self.button_zero = QPushButton('Нулевое положение', self)
        self.button_zero.setFont(QFont('Arial', 22))
        self.button_zero.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #self.button_zero.clicked.connect(self.on_zero_button_click)

        self.button_get_offset = QPushButton('Обнуление', self)
        self.button_get_offset.setFont(QFont('Arial', 22))
        self.button_get_offset.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #self.button_get_offset.clicked.connect(self.on_button_get_offset)

        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.button_move)
        self.tab1.layout.addWidget(self.button_zero)
        self.tab1.layout.addWidget(self.button_stop)
        self.tab1.layout.addWidget(self.button_get_offset)

        self.tab1.setLayout(self.tab1.layout)
        self.tab2_label_layout = QGridLayout(self)

        self.button_read_data = QPushButton('Считывание данных', self)
        self.button_read_data.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.button_read_data.setFont(QFont('Times', 10))
        #self.button_read_data.setIcon(QIcon('image.png'))
        self.button_read_data.clicked.connect(self.on_read_button_click)

        self.button_visual_start = QPushButton('Движение по синусу', self)
        self.button_visual_start.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.button_visual_start.setFont(QFont('Times', 10))
        self.button_visual_start.clicked.connect(self.on_move_button_click)

        self.button_visual_stop = QPushButton('Остановка', self)
        self.button_visual_stop.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.button_visual_stop.setFont(QFont('Times', 10))
        self.button_visual_stop.clicked.connect(self.on_stop_button_click)

        self.button_visual_zero = QPushButton('Нулевое положение', self)
        self.button_visual_zero.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.button_visual_zero.setFont(QFont('Times', 10))
        self.button_visual_zero.clicked.connect(self.on_zero_button_click)

        self.button_visual_get_offset = QPushButton('Обнуление', self)
        self.button_visual_get_offset.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.button_visual_get_offset.setFont(QFont('Times', 10))
        self.button_visual_get_offset.clicked.connect(self.on_button_get_offset)

        self.button_visual_up = QPushButton('Движение вверх', self)
        self.button_visual_up.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.button_visual_up.setFont(QFont('Times', 10))
        self.button_visual_up.clicked.connect(self.on_up_button_click)

        self.button_visual_down = QPushButton('Движение вниз', self)
        self.button_visual_down.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.button_visual_down.setFont(QFont('Times', 10))
        self.button_visual_down.clicked.connect(self.on_down_button_click)

        self.labels = []
        self.pictureLabels = []
        for x in range(14):
            self.labels.append(QLabel(self))
            self.labels[x].setAlignment(Qt.AlignCenter)
            self.labels[x].setFont(QFont('Arial', 22))

        for x in range(2):
            self.pictureLabels.append(QLabel(self))

        pixmap1 = QPixmap('pic_2.png')
        pixmap2 = QPixmap('pic_1.png')

        self.pictureLabels[0].setPixmap(pixmap1)
        self.pictureLabels[1].setPixmap(pixmap2)


        for x in range(2):
            for y in range(7):
                self.tab2_label_layout.addWidget(self.labels[7*x + y], x, y)
                self.labels[7 * x + y].setText("0")
                strOut = "background-color:rgb(" + str(0) + "," + str(0) + "," + str(255) + ")"
                # print(strOut)
                self.labels[7 * x + y].setStyleSheet(strOut)

        self.tab2_label_layout.addWidget(self.pictureLabels[0], 0, 7)
        self.tab2_label_layout.addWidget(self.pictureLabels[1], 1, 7)
        self.tab2_label_layout.addWidget(self.button_visual_up, 2, 0)
        self.tab2_label_layout.addWidget(self.button_visual_down, 2, 1)
        self.tab2_label_layout.addWidget(self.button_visual_start, 2, 2)
        self.tab2_label_layout.addWidget(self.button_visual_zero, 2, 3)
        self.tab2_label_layout.addWidget(self.button_visual_stop, 2, 4)
        self.tab2_label_layout.addWidget(self.button_visual_get_offset, 2, 5)
        self.tab2_label_layout.addWidget(self.button_read_data, 2, 6)

        self.tab2.setLayout(self.tab2_label_layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Can control
        if not self.visual_debug_mode:
            # lists all available candle devices
            devices = candle_driver.list_devices()

            if not len(devices):
                print('No candle devices found.')
                exit()

            print('Found {} candle devices.'.format(len(devices)))
            # use first availabel device
            self.device = devices[0]
            # open device (blocks other processes from using it)
            self.device.open()
            print('Device timestamp: %d' % self.device.timestamp())  # in usec
            # open first channel
            self.ch = self.device.channel(0)
            self.ch.set_bitrate(500000)

    def __exit__(self):
        self.device.close()

    def getForceData(self):
        print("0")
        if self.visual_debug_mode:

            for i in range(14):
                self.setLabelcolor(i,0,self.colorVar,(255 - self.colorVar))
                self.colorVar += 1
                if self.colorVar > 255:
                    self.colorVar = 0
        else:
            print("0_1")
            # start receiving data
            try:
                print("0_1_1")

                if self.ch.start():
                    print("1")
                    # normal frame

                    frame_type, can_id, can_data, extended, ts = self.ch.read(25)
                    if(can_id == 0x416):
                        print("2")
                        # declaring byte value
                        int_val = int.from_bytes(can_data[1:5], "big", signed=True)
                        int_val_out = 0
                        self.labels[int(can_data[0])-1].setText(str(int_val))
                        print("2_1")

                        if int_val < 0:
                            self.setLabelcolor(int(can_data[0]) - 1, 0, 0, 255)
                        elif int_val >= 0 and int_val < 3500:
                            int_val_out = int_val / 14
                            self.setLabelcolor(int(can_data[0])-1,0 , int_val_out, (255 - int_val_out))
                        elif int_val >= 3500 and int_val < 7000:
                            int_val_out = (int_val - 3500) / 14
                            self.setLabelcolor(int(can_data[0]) - 1, int_val_out, (255 - int_val_out),0)
                        print("2_2")

                    if(can_id == 0x426):
                        print("3")
                        int_val = int.from_bytes(can_data[1:5], "big", signed=True)
                        self.labels[7 + (int(can_data[0]) - 1)].setText(str(int_val))
                        int_val_out = 0
                        print("3_1")
                        if int_val < 0:
                            self.setLabelcolor(7 + int(can_data[0]) - 1, 0, 0, 255)
                        elif int_val >= 0 and int_val < 3500:
                            int_val_out = int_val / 14
                            self.setLabelcolor(7 + int(can_data[0]) - 1, 0, int_val_out, (255 - int_val_out))
                        elif int_val >= 3500 and int_val < 7000:
                            int_val_out = (int_val - 3500) / 14
                            self.setLabelcolor(7 + int(can_data[0]) - 1, int_val_out, (255 - int_val_out), 0)
                        print("3_2")
            except TimeoutError:
                #print('CAN read timeout')
                # close everything
                print("4")
                self.ch.stop()


    def setLabelcolor(self,label_num,R,G,B):
        strOut = "background-color:rgb(" + str(R) + "," + str(G) + "," + str(B) + ")"
        #print(strOut)
        self.labels[label_num].setStyleSheet(strOut)

    @pyqtSlot()
    def on_move_button_click(self):
        print('Send command to start move')
        if not self.visual_debug_mode:
            # start receiving data
            self.ch.start()
            # normal frame
            self.ch.write(0x207, b'abcdefgh')
            # close everything
            self.ch.stop()
            print("Message sent")


    @pyqtSlot()
    def on_zero_button_click(self):
        print('Send command to zero move')
        if not self.visual_debug_mode:
            # start receiving data
            self.ch.start()
            # normal frame
            self.ch.write(0x201, b'abcdefgh')
            # close everything
            self.ch.stop()
            print("Message sent zero")

    @pyqtSlot()
    def on_stop_button_click(self):
        print('Send command to stop move')
        if not self.visual_debug_mode:
            # start receiving data
            self.ch.start()
            # normal frame
            self.ch.write(0x200, b'abcdefgh')
            # close everything
            self.ch.stop()
            print("Message sent stop")

    @pyqtSlot()
    def on_button_get_offset(self):
        print('Send command to stop move')
        if not self.visual_debug_mode:
            # start receiving data
            self.ch.start()
            # normal frame
            self.ch.write(0x204, b'abcdefgh')
            # close everything
            self.ch.stop()
            print("Message sent stop")

    @pyqtSlot()
    def on_up_button_click(self):
        print('Send command to up move')
        if not self.visual_debug_mode:
            # start receiving data
            self.ch.start()
            # normal frame
            self.ch.write(0x203, b'\x01\xFF\x00\x0A\x00\x00\x00\x00')
            # close everything
            self.ch.stop()
            print("Message sent stop")

    @pyqtSlot()
    def on_down_button_click(self):
        print('Send command to down move')
        if not self.visual_debug_mode:
            # start receiving data
            self.ch.start()
            # normal frame
            self.ch.write(0x203, b'\x00\xFF\x00\x0A\x00\x00\x00\x00')
            # close everything
            self.ch.stop()
            print("Message sent stop")

    @pyqtSlot()
    def on_read_button_click(self):
        self.reading_flag = not self.reading_flag
        if self.reading_flag:
            print('Start reading')
            if not self.visual_debug_mode:
                # start receiving data
                self.ch.start()
                # normal frame
                self.ch.write(0x206, b'abcdefgh')
                # close everything
                self.ch.stop()
            print('Start timer')
            self.timer.start(1) #10

        else:
            print('Stop reading')
            self.timer.stop()
            if not self.visual_debug_mode:
                # start receiving data
                self.ch.start()
                # normal frame
                self.ch.write(0x200, b'abcdefgh')
                # close everything
                self.ch.stop()


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = QApplication.desktop()
    screenRect = desktop.screenGeometry()
    height = int(screenRect.height()*0.9)
    width = screenRect.width()
    window = MainWindow()
    window.resize(width, height)
    window.setWindowTitle("TBM Axis Control")
    window.show()
    app.exec()

