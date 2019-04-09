#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import cv2
from test import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import os

model = torch.load('model.pkl',map_location='cpu')
class_names = get_all_classes()

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)

        # self.face_recong = face.Recognition()
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()
        self.__flag_work = 0
        self.x = 0
        self.count = 0
        self.clip = []
    def set_ui(self):

        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()

        self.button_open_camera = QtWidgets.QPushButton(u'open camera')

        self.button_close = QtWidgets.QPushButton(u'exit')




        # Button 的颜色修改
        button_color = [self.button_open_camera, self.button_close]
        for i in range(2):
            button_color[i].setStyleSheet("QPushButton{color:black}"
                                          "QPushButton:hover{color:red}"
                                          "QPushButton{background-color:rgb(78,255,255)}"
                                          "QPushButton{border:2px}"
                                          "QPushButton{border-radius:10px}"
                                          "QPushButton{padding:2px 4px}")

        self.button_open_camera.setMinimumHeight(50)
        self.button_close.setMinimumHeight(50)

        # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
        self.move(500, 500)

        self.result_label = QtWidgets.QLabel()
        self.result_label.setFixedSize(300,100)
        self.result_label.setAutoFillBackground(False)
        self.result_label.setFont(QtGui.QFont("Roman times",20,QtGui.QFont.Bold))
        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(100, 100)

        self.label_show_camera.setFixedSize(641, 481)
        self.label_show_camera.setAutoFillBackground(False)

        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_close)
        self.__layout_fun_button.addWidget(self.label_move)

        self.__layout_main.addLayout(self.__layout_fun_button)
        self.__layout_main.addWidget(self.label_show_camera)

        self.__layout_main.addWidget(self.result_label)

        self.setLayout(self.__layout_main)
        self.label_move.raise_()
        self.setWindowTitle(u'action recognition')

        '''
        # 设置背景图片
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('background.jpg')))
        self.setPalette(palette1)
        '''

    def slot_init(self):
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_close.clicked.connect(self.close)

    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"check the computer connect the camera",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            # if msg==QtGui.QMessageBox.Cancel:
            #                     pass
            else:
                self.timer_camera.start(30)

                self.button_open_camera.setText(u'close camera')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'open camera')

    def show_camera(self):



        # face = self.face_detect.align(self.image)
        # if face:
        #     pass

        flag, self.image = self.cap.read()

        # resize to the test size
        tmp_ = center_crop(cv2.resize(self.image, (171, 128)))

        # seems normalize color
        tmp = tmp_ - np.array([[[90.0, 98.0, 102.0]]])

        self.clip.append(tmp)

        if len(self.clip) == 16:
            # 16 * 112 * 112 * 3
            inputs = np.array(self.clip).astype(np.float32)

            # 1 * 16 * 112 * 112 * 3
            inputs = np.expand_dims(inputs, axis=0)

            # 1 * 3 * 16 * 112 * 112
            inputs = np.transpose(inputs, (0, 4, 1, 2, 3))

            inputs = torch.from_numpy(inputs)

            inputs = torch.autograd.Variable(inputs).to(device)

            # put into model
            outputs = model.forward(inputs)

            # get the probs
            probs = torch.nn.Softmax(dim=1)(outputs)

            # get the label index
            label = torch.max(probs, 1)[1].detach().cpu().numpy()[0]

            # cv2.putText(self.image, class_names[label].split(' ')[-1].strip(), (20, 20),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.6,
            #             (0, 0, 255), 1)
            # cv2.putText(self.image, "prob: %.4f" % probs[0][label], (20, 40),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.6,
            #             (0, 0, 255), 1)
            self.result_label.setText('Action: {} \n Prob: {:.4f}'.format(class_names[label].split(' ')[-1].strip(),probs[0][label]))
            self.clip.pop(0)



        show = cv2.resize(self.image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        # print(show.shape[1], show.shape[0])
        # show.shape[1] = 640, show.shape[0] = 480
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        # self.x += 1
        # self.label_move.move(self.x,100)

        # if self.x ==320:
        #     self.label_show_camera.raise_()

        # def show_camera(self):
        #     clip = []
        #
        #     flag, self.image = self.cap.read()
        #     # face = self.face_detect.align(self.image)
        #     # if face:
        #     #     pass
        #     while flag:
        #
        #     show = cv2.resize(self.image, (640, 480))
        #     show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        #     # print(show.shape[1], show.shape[0])
        #     # show.shape[1] = 640, show.shape[0] = 480
        #     showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        #     self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        #     # self.x += 1
        #     # self.label_move.move(self.x,100)
        #
        #     # if self.x ==320:
        #     #     self.label_show_camera.raise_()



    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cacel = QtWidgets.QPushButton()

        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"close", u"close or not！")

        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cacel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'Yes')
        cacel.setText(u'No')
        # msg.setDetailedText('sdfsdff')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            #             self.socket_client.send_command(self.socket_client.current_user_command)
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()

    sys.exit(App.exec_())