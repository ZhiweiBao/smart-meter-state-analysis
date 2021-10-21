# -*- coding: utf-8 -*-

"""
Module implementing database_setting.
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog

from ui.Ui_database_setting import Ui_database_setting
import os
import configparser
from db_Oracle import oral_operate


class database_setting(QDialog, Ui_database_setting):
    """
    Class documentation goes here.
    """
    signal_connect = pyqtSignal(list)
    signal_connect_2 = pyqtSignal(list)
    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(database_setting, self).__init__(parent)
        self.setupUi(self)
        currentPath = os.getcwd()
        ini_path = currentPath + "\database_config.ini"
        ini_exist = os.path.exists(ini_path)
        if ini_exist == 1:
            # ---已存在配置文件，
            try:
                # ---读取当前exist的数值
                config = configparser.ConfigParser()
                config.read_file(open(r"%s" % ini_path))
                serverName = config.get("数据库信息1", "服务器名称")
                userName = config.get("数据库信息1", "用户名")
                self.lineEdit_serverName.setText(serverName)
                self.lineEdit_userName.setText(userName)

                serverName2 = config.get("数据库信息2", "服务器名称")
                userName2 = config.get("数据库信息2", "用户名")
                self.lineEdit_serverName_2.setText(serverName2)
                self.lineEdit_userName_2.setText(userName2)
            except Exception as e:
                print(e)

    @pyqtSlot()
    def on_pushButton_connect_clicked(self):
        #-----get db releated info from ui----
        serverName = self.lineEdit_serverName.text()
        userName   = self.lineEdit_userName.text()
        password   = self.lineEdit_password.text()
        serverName2 = self.lineEdit_serverName_2.text()
        userName2 = self.lineEdit_userName_2.text()
        #-----check data ------
        if len(serverName) !=0 and len(userName) !=0 and len(password) !=0:
            pass
        else:
            QtWidgets.QMessageBox.warning(self, "警告:", "请录入完整的数据库信息！")
            return
        #---read db config data---
        currentPath = os.getcwd()
        ini_path = currentPath + "\database_config.ini"
        ini_exist = os.path.exists(ini_path)
        # ---if database_config is not exist created it-------
        config = configparser.ConfigParser()
        if ini_exist == 0:
            try:
                # -----创建配置文件config.ini---------
                config.add_section("数据库信息1")
                config.set("数据库信息1", "服务器名称", serverName)
                config.set("数据库信息1", "用户名", userName)

                config.add_section("数据库信息2")
                config.set("数据库信息2", "服务器名称", serverName2)
                config.set("数据库信息2", "用户名", userName2)
                config.write(open(r"%s" % ini_path, "w"))
            except Exception as e:
                print(e)
        else:
            # -----改写exiest的数值
            config.read(r"%s" % ini_path)
            config.set("数据库信息1", "服务器名称", serverName)
            config.set("数据库信息1", "用户名", userName)
            config.write(open(r"%s" % ini_path, "r+"))

        #------connect sqlserver database----
        db_op = oral_operate.oracledb(serverName, userName, password)
        flag = db_op.checkconnect()
        if flag:
            QtWidgets.QMessageBox.information(self, "消息:", "数据库1连接成功！")
        else:
            QtWidgets.QMessageBox.warning(self, "警告:", "数据库1连接失败！")
            return
        self.signal_connect.emit([serverName, userName, password])

    @pyqtSlot()
    def on_pushButton_connect_2_clicked(self):
        #-----get db releated info from ui----
        serverName = self.lineEdit_serverName_2.text()
        userName   = self.lineEdit_userName_2.text()
        password   = self.lineEdit_password_2.text()
        serverName2 = self.lineEdit_serverName.text()
        userName2 = self.lineEdit_userName.text()
        #-----check data ------
        if len(serverName) !=0 and len(userName) !=0 and len(password) !=0:
            pass
        else:
            QtWidgets.QMessageBox.warning(self, "警告:", "请录入完整的数据库信息！")
            return
        #---read db config data---
        currentPath = os.getcwd()
        ini_path = currentPath + "\database_config.ini"
        ini_exist = os.path.exists(ini_path)
        # ---if database_config is not exist created it-------
        config = configparser.ConfigParser()
        if ini_exist == 0:
            try:
                # -----创建配置文件config.ini---------
                config.add_section("数据库信息1")
                config.set("数据库信息1", "服务器名称", serverName2)
                config.set("数据库信息1", "用户名", userName2)

                config.add_section("数据库信息2")
                config.set("数据库信息2", "服务器名称", serverName)
                config.set("数据库信息2", "用户名", userName)
                config.write(open(r"%s" % ini_path, "w"))
            except Exception as e:
                print(e)
        else:
            # -----改写exiest的数值
            config.read(r"%s" % ini_path)
            config.set("数据库信息2", "服务器名称", serverName)
            config.set("数据库信息2", "用户名", userName)
            config.write(open(r"%s" % ini_path, "r+"))

        #------connect sqlserver database----
        db_op = oral_operate.oracledb_old(serverName, userName, password)
        flag = db_op.checkconnect()
        if flag:
            QtWidgets.QMessageBox.information(self, "消息:", "数据库2连接成功！")
        else:
            QtWidgets.QMessageBox.warning(self, "警告:", "数据库2连接失败！")
            return
        self.signal_connect_2.emit([serverName, userName, password])

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    database_setting = QtWidgets.QDialog()
    ui = Ui_database_setting()
    ui.setupUi(database_setting)
    database_setting.show()
    sys.exit(app.exec_())