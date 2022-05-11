import sys
import candle_driver
from PyQt5.QtCore import QSize, Qt,QTimer,QDateTime
from PyQt5.QtCore import pyqtSlot
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
        self.tabs.addTab(self.tab1, "Move")
        self.tabs.addTab(self.tab2, "Sensors")

        # Create first tab "Move"
        self.button_move = QPushButton('Start_moving', self)
        self.button_move.clicked.connect(self.on_move_button_click)

        self.button_stop = QPushButton('Stop', self)
        self.button_stop.clicked.connect(self.on_stop_button_click)

        self.button_zero = QPushButton('Zero', self)
        self.button_zero.clicked.connect(self.on_zero_button_click)

        self.button_get_offset = QPushButton('Get_offset', self)
        self.button_get_offset.clicked.connect(self.on_button_get_offset)

        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.button_move)
        self.tab1.layout.addWidget(self.button_zero)
        self.tab1.layout.addWidget(self.button_stop)
        self.tab1.layout.addWidget(self.button_get_offset)

        self.tab1.setLayout(self.tab1.layout)
        self.tab2_label_layout = QGridLayout(self)

        self.button_read_data = QPushButton('Read_data', self)
        self.button_read_data.clicked.connect(self.on_read_button_click)

        self.labels = []
        for x in range(14):
            self.labels.append(QLabel(self))
            self.labels[x].setAlignment(Qt.AlignCenter)
            self.labels[x].adjustSize()

        for x in range(2):
            for y in range(7):
                self.tab2_label_layout.addWidget(self.labels[7*x + y], x, y)
                self.labels[7 * x + y].setText("0")
        self.tab2_label_layout.addWidget( self.button_read_data, 3, 0)

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
        if self.visual_debug_mode:
            print("test")
            for i in range(14):
                self.setLabelcolor(i,0,self.colorVar,(255 - self.colorVar))
                self.colorVar += 1
                if self.colorVar > 255:
                    self.colorVar = 0
        else:
            # start receiving data
            self.ch.start()
            # normal frame
            try:
                frame_type, can_id, can_data, extended, ts = self.ch.read(10)
                if(can_id == 0x416):
                    # declaring byte value
                    int_val = int.from_bytes(can_data[1:5], "big", signed=True)
                    self.labels[int(can_data[0])-1].setText(str(int_val))

                    if int_val < 0:
                        pass
                    elif int_val >= 0 and int_val < 5000:
                        int_val_out = int_val / 20
                        self.setLabelcolor(int(can_data[0])-1,0 , int_val_out, (255 - int_val_out))
                    elif int_val >= 5000 and int_val < 30000:
                        int_val_out = (int_val - 5000) / 99
                        self.setLabelcolor(int(can_data[0]) - 1, int_val_out, (255 - int_val_out),0)

                if(can_id == 0x426):
                    int_val = int.from_bytes(can_data[1:5], "big", signed=True)
                    self.labels[7 + (int(can_data[0]) - 1)].setText(str(int_val))

                    int_val_out = int_val / 59

                    if int_val < 0:
                        pass
                    elif int_val >= 0 and int_val < 5000:
                        int_val_out = int_val / 20
                        self.setLabelcolor(7 + int(can_data[0]) - 1, 0, int_val_out, (255 - int_val_out))
                    elif int_val >= 5000 and int_val < 30000:
                        int_val_out = (int_val - 5000) / 99
                        self.setLabelcolor(7 + int(can_data[0]) - 1, int_val_out, (255 - int_val_out), 0)

            except TimeoutError:
                #print('CAN read timeout')
                # close everything
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
            self.timer.start(10)

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
    window.show()

    app.exec()

