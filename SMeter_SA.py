# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
# while True:
#     user_password = input('Please input your password:')
#     if user_password == '123':
#         print('Thanks for login!')
#         print('开始运行')
#         break
#     else:
#         print('Your password is wrong!')
#         print('Please input again!')

from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtCore import Qt, pyqtSlot, QTimer, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor
from ui.Ui_SMeter_SA import Ui_MainWindow
from database_setting import database_setting
from db_Oracle import oral_operate
import threads
import os
import configparser
from datetime import datetime
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import dates as mdates
from mpl_toolkits.axes_grid1 import Grid
# import Process
# mlab_process = Process.initialize()
from typechange import typechange
import traceback
# import sys, threading
#
# sys.setrecursionlimit(100000)

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(Qt.Window)
        self.showMaximized()
        self.setWindowFlags(Qt.WindowStaysOnBottomHint)
        self.database_set = database_setting()
        self.database_info = []
        self.database_info_local = []
        self.database_info_old = []


        currentPath = os.getcwd()
        ini_path = currentPath + "\date_config.ini"
        ini_exist = os.path.exists(ini_path)

        if ini_exist == 1:
            # ---已存在配置文件，
            try:
                # ---读取当前exist的数值
                config = configparser.ConfigParser()
                config.read_file(open(r"%s" % ini_path))
                tableDate = config.get("数据表", "日期")
                self.DateEdit_table.setDate(QtCore.QDate(int(tableDate[0:4]),int(tableDate[5:7]),int(tableDate[8:10])))

                plotStartDate = config.get("误差变化折线图1", "起始日期")
                plotEndDate = config.get("误差变化折线图1", "结束日期")
                self.DateEdit_start_plot.setDate(QtCore.QDate(int(plotStartDate[0:4]),int(plotStartDate[5:7]),int(plotStartDate[8:10])))
                self.DateEdit_end_plot.setDate(QtCore.QDate(int(plotEndDate[0:4]), int(plotEndDate[5:7]), int(plotEndDate[8:10])))

                plotStartDate2 = config.get("误差变化折线图2", "起始日期")
                plotEndDate2 = config.get("误差变化折线图2", "结束日期")
                self.DateEdit_start_plot_2.setDate(
                    QtCore.QDate(int(plotStartDate2[0:4]), int(plotStartDate2[5:7]), int(plotStartDate2[8:10])))
                self.DateEdit_end_plot_2.setDate(
                    QtCore.QDate(int(plotEndDate2[0:4]), int(plotEndDate2[5:7]), int(plotEndDate2[8:10])))

                histStartDateTime = config.get("误差分布直方图1", "起始时间")
                histEndDateTime = config.get("误差分布直方图1", "结束时间")
                self.DateTimeEdit_start_hist.setDateTime(QtCore.QDateTime(QtCore.QDate(int(histStartDateTime[0:4]),
                                                                                         int(histStartDateTime[5:7]),
                                                                                         int(histStartDateTime[8:10])),
                                                                            QtCore.QTime(int(histStartDateTime[11:13]),
                                                                                         int(histStartDateTime[14:16]),
                                                                                         int(histStartDateTime[17:]))
                                                                            ))
                self.DateTimeEdit_end_hist.setDateTime(QtCore.QDateTime(QtCore.QDate(int(histEndDateTime[0:4]),
                                                                                      int(histEndDateTime[5:7]),
                                                                                      int(histEndDateTime[8:10])),
                                                                         QtCore.QTime(int(histEndDateTime[11:13]),
                                                                                      int(histEndDateTime[14:16]),
                                                                                      int(histEndDateTime[17:]))
                                                                         ))

                histStartDateTime2 = config.get("误差分布直方图2", "起始时间")
                histEndDateTime2 = config.get("误差分布直方图2", "结束时间")
                self.DateTimeEdit_start_hist_2.setDateTime(QtCore.QDateTime(QtCore.QDate(int(histStartDateTime2[0:4]),
                                                                                       int(histStartDateTime2[5:7]),
                                                                                       int(histStartDateTime2[8:10])),
                                                                          QtCore.QTime(int(histStartDateTime2[11:13]),
                                                                                       int(histStartDateTime2[14:16]),
                                                                                       int(histStartDateTime2[17:]))
                                                                          ))
                self.DateTimeEdit_end_hist_2.setDateTime(QtCore.QDateTime(QtCore.QDate(int(histEndDateTime2[0:4]),
                                                                                     int(histEndDateTime2[5:7]),
                                                                                     int(histEndDateTime2[8:10])),
                                                                        QtCore.QTime(int(histEndDateTime2[11:13]),
                                                                                     int(histEndDateTime2[14:16]),
                                                                                     int(histEndDateTime2[17:]))
                                                                        ))

            except Exception as e:
                print(e)

        layout_plot = QtWidgets.QVBoxLayout(self.widget_plot)
        self.fig_plot = Figure()
        self.dynamic_canvas_plot = FigureCanvas(self.fig_plot)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_plot.addWidget(NavigationToolbar(self.dynamic_canvas_plot, self))
        layout_plot.addWidget(self.dynamic_canvas_plot)

        layout_plot2 = QtWidgets.QVBoxLayout(self.widget_plot_2)
        self.fig_plot2 = Figure()
        self.dynamic_canvas_plot2 = FigureCanvas(self.fig_plot2)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_plot2.addWidget(NavigationToolbar(self.dynamic_canvas_plot2, self))
        layout_plot2.addWidget(self.dynamic_canvas_plot2)


        layout_hist = QtWidgets.QVBoxLayout(self.widget_hist)
        self.fig_hist = Figure()
        self.dynamic_canvas_hist = FigureCanvas(self.fig_hist)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_hist.addWidget(NavigationToolbar(self.dynamic_canvas_hist, self))
        layout_hist.addWidget(self.dynamic_canvas_hist)

        layout_hist2 = QtWidgets.QVBoxLayout(self.widget_hist_2)
        self.fig_hist2 = Figure()
        self.dynamic_canvas_hist2 = FigureCanvas(self.fig_hist2)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout_hist2.addWidget(NavigationToolbar(self.dynamic_canvas_hist2, self))
        layout_hist2.addWidget(self.dynamic_canvas_hist2)

    @pyqtSlot()
    def on_pushButton_database_setting_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            self.database_set.setWindowFlags(Qt.Dialog)
        except Exception as e:
            print(e)
        self.database_set.show()

        self.database_set.signal_connect.connect(self.get_database_setting)
        self.database_set.signal_connect_2.connect(self.get_database_setting2)

    def get_database_setting(self, database_setting):
        self.database_info = database_setting
        self.database_info_local = database_setting

    def get_database_setting2(self, database_setting):
        self.database_info_old = database_setting


    @pyqtSlot()
    def on_pushButton_table_clicked(self):
        try:
            self.pushButton_table.setDisabled(True)
            if self.database_info == []:
                QtWidgets.QMessageBox.warning(self, "Warning:", "数据库1未进行配置！")
                self.pushButton_table.setEnabled(True)
                return
            if self.database_info_old == []:
                QtWidgets.QMessageBox.warning(self, "Warning:", "数据库2未进行配置！")
                self.pushButton_table.setEnabled(True)
                return
            dtText = self.DateEdit_table.text()
            dtn = datetime.now()
            dtTextNum = int(str(dtText)[0:4]+str(dtText)[5:7]+str(dtText)[8:10])
            dtnNum = int(str(dtn)[0:4]+str(dtn)[5:7]+str(dtn)[8:10])
            if dtTextNum >= dtnNum:
                QtWidgets.QMessageBox.warning(self, "Warning:", "无法查看当天及未来的日期！")
                self.pushButton_table.setEnabled(True)
                return
            currentPath = os.getcwd()
            ini_path = currentPath + "\date_config.ini"
            ini_exist = os.path.exists(ini_path)
            # ---if database_config is not exist created it-------
            config = configparser.ConfigParser()
            if ini_exist == 0:
                try:
                    # -----创建配置文件config.ini---------
                    # TODO
                    config.add_section("数据表")
                    config.set("数据表", "日期", self.DateEdit_table.text())
                    config.add_section("误差变化折线图1")
                    config.set("误差变化折线图1", "起始日期", self.DateEdit_start_plot.text())
                    config.set("误差变化折线图1", "结束日期", self.DateEdit_end_plot.text())
                    config.add_section("误差分布直方图1")
                    config.set("误差分布直方图1", "起始时间", self.DateTimeEdit_start_hist.text())
                    config.set("误差分布直方图1", "结束时间", self.DateTimeEdit_end_hist.text())

                    config.add_section("误差变化折线图2")
                    config.set("误差变化折线图2", "起始日期", self.DateEdit_start_plot_2.text())
                    config.set("误差变化折线图2", "结束日期", self.DateEdit_end_plot_2.text())
                    config.add_section("误差分布直方图2")
                    config.set("误差分布直方图2", "起始时间", self.DateTimeEdit_start_hist_2.text())
                    config.set("误差分布直方图2", "结束时间", self.DateTimeEdit_end_hist_2.text())
                    config.write(open(r"%s" % ini_path, "w"))
                except:
                    traceback.print_exc()
            else:
                # -----改写exiest的数值
                config.read(r"%s" % ini_path)
                config.set("数据表", "日期", self.DateEdit_table.text())
                config.write(open(r"%s" % ini_path, "r+"))


            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1], self.database_info_old[2])
            db_op_local = oral_operate.oracledb(self.database_info_local[0], self.database_info_local[1],
                                                self.database_info_local[2])
            flag = db_op.checkconnect()
            flag_old = db_op_old.checkconnect()
            flag_local = db_op_local.checkconnect()
            if flag and flag_local and flag_old:
                try:
                    self.tableThread = threads.table_data()
                    self.tableThread.setValue(self.database_info, self.database_info_old, self.database_info_local,
                                              self.DateEdit_table.text())
                    self.tableThread.signal_data.connect(self.table_view)
                    self.tableThread.start()

                except:
                    traceback.print_exc()
                    self.pushButton_table.setDisabled(False)
            else:
                QtWidgets.QMessageBox.warning(self, "Warning:", "数据库连接失败！")
                self.pushButton_table.setEnabled(True)
                return
        except:
            traceback.print_exc()
            self.pushButton_table.setEnabled(True)

    def table_view(self, days, data, data2, notenough, notengough2):
        try:
            if data == [] and data2 == []:
                QtWidgets.QMessageBox.warning(self, "Warning:", "近%s天内无数据！" % days)
                self.pushButton_table.setDisabled(False)
                return
            elif notenough == 1 and notengough2 == 1:
                QtWidgets.QMessageBox.warning(self, "Warning:", "当天内无数据！")
                self.pushButton_table.setDisabled(False)
                return
            else:
                self.label_Date_table.setText("当前日期：%s" % self.DateEdit_table.text())
            headers = ['流水线1检定单元', '误差评估值', '状态评估', '数据量', '流水线2检定单元', '误差评估值', '状态评估', '数据量']
            self.tableWidget_db_data.setColumnCount(len(headers))  # 设置表格的列数
            self.tableWidget_db_data.setRowCount(20)  # 设置表格的行数
            # ---------set headers--------
            for i in range(len(headers)):
                self.tableWidget_db_data.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(
                    "%s" % headers[i]))
            # ---------set datas----------
            zerodata = [[0, 'nan', '无', 0],
                        [0, 'nan', '无', 0],
                        [0, 'nan', '无', 0],
                        [0, 'nan', '无', 0],
                        [0, 'nan', '无', 0],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0 ],
                        [0, 'nan', '无', 0 ]
                        ]
            if notenough == 1:
                data = zerodata
            if notengough2 == 1:
                data2 = zerodata
            for i in range(len(data)):
                for j in range(len(data[0])):
                    item0 = QtWidgets.QTableWidgetItem("%s" % data[i][j])
                    # item0 = QtGui.QTableWidgetItem("%s" % data[i][j].decode('gbk'))
                    item0.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # -------禁止修改已写入的数据！！！-------
                    item0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_db_data.setItem(i, j, item0)
                if data[i][2] == '负向超差' or data[i][2] == '正向超差':
                    self.tableWidget_db_data.item(i, 2).setBackground(QtGui.QBrush(QColor(255, 0, 0)))
                    self.tableWidget_db_data.item(i, 2).setForeground(QtGui.QBrush(QColor(240, 240, 240)))
                if data[i][2] == '负向高风险' or data[i][2] == '正向高风险':
                    self.tableWidget_db_data.item(i, 2).setBackground(QtGui.QBrush(QColor(255, 127, 0)))
                if data[i][2] == '负向偏移' or data[i][2] == '正向偏移':
                    self.tableWidget_db_data.item(i, 2).setBackground(QtGui.QBrush(QColor(255, 255, 0)))
                if data[i][2] == '虚拟参考':
                    self.tableWidget_db_data.item(i, 2).setBackground(QtGui.QBrush(QColor(191, 191, 191)))
                if data[i][2] == '未参与评估':
                    self.tableWidget_db_data.item(i, 2).setBackground(QtGui.QBrush(QColor(127, 127, 127)))
                if data[i][3] < 500:
                    self.tableWidget_db_data.item(i, 3).setBackground(QtGui.QBrush(QColor(255, 255, 0)))
            for i in range(len(data2)):
                for j in range(len(data2[0])):
                    item0 = QtWidgets.QTableWidgetItem("%s" % data2[i][j])
                    # item0 = QtGui.QTableWidgetItem("%s" % data[i][j].decode('gbk'))
                    item0.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # -------禁止修改已写入的数据！！！-------
                    item0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_db_data.setItem(i, j+4, item0)
                if data2[i][2] == '负向超差' or data2[i][2] == '正向超差':
                    self.tableWidget_db_data.item(i, 6).setBackground(QtGui.QBrush(QColor(255, 0, 0)))
                    self.tableWidget_db_data.item(i, 6).setForeground(QtGui.QBrush(QColor(240, 240, 240)))
                if data2[i][2] == '负向高风险' or data2[i][2] == '正向高风险':
                    self.tableWidget_db_data.item(i, 6).setBackground(QtGui.QBrush(QColor(255, 127, 0)))
                if data2[i][2] == '负向偏移' or data2[i][2] == '正向偏移':
                    self.tableWidget_db_data.item(i, 6).setBackground(QtGui.QBrush(QColor(255, 255, 0)))
                if data2[i][2] == '虚拟参考':
                    self.tableWidget_db_data.item(i, 6).setBackground(QtGui.QBrush(QColor(191, 191, 191)))
                if data2[i][2] == '未参与评估':
                    self.tableWidget_db_data.item(i, 6).setBackground(QtGui.QBrush(QColor(127, 127, 127)))
                if data2[i][3] < 500:
                    self.tableWidget_db_data.item(i, 7).setBackground(QtGui.QBrush(QColor(255, 255, 0)))
            self.tableWidget_db_data.resizeColumnsToContents()
        except:
            traceback.print_exc()
        self.pushButton_table.setDisabled(False)

    @pyqtSlot()
    def on_pushButton_plot_clicked(self):
        try:
            self.pushButton_plot.setDisabled(True)
            if self.database_info == [] or self.database_info_local == []:
                QtWidgets.QMessageBox.warning(self, "Warning:", "请先完成数据库连接！")
                self.pushButton_plot.setEnabled(True)
                return
            dtStartText = self.DateEdit_start_plot.text()
            dtEndText = self.DateEdit_end_plot.text()
            dtn = datetime.now()
            dtStartTextNum = int(str(dtStartText)[0:4] + str(dtStartText)[5:7] + str(dtStartText)[8:10])
            dtEndTextNum = int(str(dtEndText)[0:4] + str(dtEndText)[5:7] + str(dtEndText)[8:10])
            dtnNum = int(str(dtn)[0:4] + str(dtn)[5:7] + str(dtn)[8:10])
            if dtStartTextNum >= dtEndTextNum:
                QtWidgets.QMessageBox.warning(self, "Warning:", "起止时间有误！")
                self.pushButton_plot.setEnabled(True)
                return
            if dtEndTextNum >= dtnNum:
                QtWidgets.QMessageBox.warning(self, "Warning:", "无法查看当天及未来的日期！")
                self.pushButton_plot.setEnabled(True)
                return
            currentPath = os.getcwd()
            ini_path = currentPath + "\date_config.ini"
            ini_exist = os.path.exists(ini_path)
            # ---if database_config is not exist created it-------
            config = configparser.ConfigParser()
            if ini_exist == 0:
                try:
                    # -----创建配置文件config.ini---------
                    # TODO
                    config.add_section("数据表")
                    config.set("数据表", "日期", self.DateEdit_table.text())
                    config.add_section("误差变化折线图1")
                    config.set("误差变化折线图1", "起始日期", self.DateEdit_start_plot.text())
                    config.set("误差变化折线图1", "结束日期", self.DateEdit_end_plot.text())
                    config.add_section("误差分布直方图1")
                    config.set("误差分布直方图1", "起始时间", self.DateTimeEdit_start_hist.text())
                    config.set("误差分布直方图1", "结束时间", self.DateTimeEdit_end_hist.text())

                    config.add_section("误差变化折线图2")
                    config.set("误差变化折线图2", "起始日期", self.DateEdit_start_plot_2.text())
                    config.set("误差变化折线图2", "结束日期", self.DateEdit_end_plot_2.text())
                    config.add_section("误差分布直方图2")
                    config.set("误差分布直方图2", "起始时间", self.DateTimeEdit_start_hist_2.text())
                    config.set("误差分布直方图2", "结束时间", self.DateTimeEdit_end_hist_2.text())
                    config.write(open(r"%s" % ini_path, "w"))
                except:
                    traceback.print_exc()
            else:
                # -----改写exiest的数值
                config.read(r"%s" % ini_path)
                config.set("误差变化折线图1", "起始日期", self.DateEdit_start_plot.text())
                config.set("误差变化折线图1", "结束日期", self.DateEdit_end_plot.text())
                config.write(open(r"%s" % ini_path, "r+"))
            startdate = typechange.date2num(self.DateEdit_start_plot.text())
            enddate = typechange.date2num(self.DateEdit_end_plot.text())
            if (enddate - startdate) <= 5:
                QtWidgets.QMessageBox.warning(self, "Warning:", "时间间隔过短！")
                self.pushButton_plot.setEnabled(True)
                return
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_local = oral_operate.oracledb(self.database_info_local[0], self.database_info_local[1],
                                                self.database_info_local[2])
            flag = db_op.checkconnect()
            flag_local = db_op_local.checkconnect()
            if flag and flag_local:
                self.plotThread = threads.plot_data()
                self.plotThread.setValue(self.database_info, self.database_info_local,
                                          self.DateEdit_start_plot.text(),
                                          self.DateEdit_end_plot.text(),
                                         1)
                self.plotThread.signal_plotdata.connect(self.plot)
                self.plotThread.start()

                # datalist = dataProcess.findManyData(startdate, enddate, self.database_info, self.database_info_local)
                # self.plot(datalist)
            else:
                QtWidgets.QMessageBox.warning(self, "Warning:", "数据库连接失败！")
                self.pushButton_plot.setEnabled(True)
                return
        except:
            traceback.print_exc()
            self.pushButton_plot.setEnabled(True)

    def plot(self, datalist):
        try:
            self.fig_plot.clf()
            if self.ComboBox_SID_plot.currentText() == '总视图':
                self.grid_plot = Grid(self.fig_plot, rect=111, nrows_ncols=(4, 5), axes_pad=0.5, label_mode='L')
                self.fig_plot.tight_layout()
                i = 0
                for ax in self.grid_plot:
                    self.example_plot(ax, datalist[0], datalist[i+1], datalist[i+21], i+1)
                    i += 1
                    QtWidgets.QApplication.processEvents()
            elif self.ComboBox_SID_plot.currentText() == '1':
                i = 1
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '2':
                i = 2
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '3':
                i = 3
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '4':
                i = 4
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '5':
                i = 5
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '6':
                i = 6
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '7':
                i = 7
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '8':
                i = 8
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '9':
                i = 9
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '10':
                i = 10
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '11':
                i = 11
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '12':
                i = 12
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '13':
                i = 13
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '14':
                i = 14
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '15':
                i = 15
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '16':
                i = 16
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '17':
                i = 17
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '18':
                i = 18
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '19':
                i = 19
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot.currentText() == '20':
                i = 20
                ax = self.fig_plot.add_subplot(111)
                self.fig_plot.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            else:
                return
            # self.fig_plot.tight_layout()
            self.pushButton_plot.setEnabled(True)
        except:
            traceback.print_exc()
            self.pushButton_plot.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_plot_2_clicked(self):
        try:
            self.pushButton_plot_2.setDisabled(True)
            if self.database_info_old == [] or self.database_info_local == []:
                QtWidgets.QMessageBox.warning(self, "Warning:", "请先完成数据库连接！")
                self.pushButton_plot_2.setEnabled(True)
                return
            dtStartText = self.DateEdit_start_plot_2.text()
            dtEndText = self.DateEdit_end_plot_2.text()
            dtn = datetime.now()
            dtStartTextNum = int(str(dtStartText)[0:4] + str(dtStartText)[5:7] + str(dtStartText)[8:10])
            dtEndTextNum = int(str(dtEndText)[0:4] + str(dtEndText)[5:7] + str(dtEndText)[8:10])
            dtnNum = int(str(dtn)[0:4] + str(dtn)[5:7] + str(dtn)[8:10])
            if dtStartTextNum >= dtEndTextNum:
                QtWidgets.QMessageBox.warning(self, "Warning:", "起止时间有误！")
                self.pushButton_plot_2.setEnabled(True)
                return
            if dtEndTextNum >= dtnNum:
                QtWidgets.QMessageBox.warning(self, "Warning:", "无法查看当天及未来的日期！")
                self.pushButton_plot_2.setEnabled(True)
                return
            currentPath = os.getcwd()
            ini_path = currentPath + "\date_config.ini"
            ini_exist = os.path.exists(ini_path)
            # ---if database_config is not exist created it-------
            config = configparser.ConfigParser()
            if ini_exist == 0:
                try:
                    # -----创建配置文件config.ini---------
                    # TODO
                    config.add_section("数据表")
                    config.set("数据表", "日期", self.DateEdit_table.text())
                    config.add_section("误差变化折线图1")
                    config.set("误差变化折线图1", "起始日期", self.DateEdit_start_plot.text())
                    config.set("误差变化折线图1", "结束日期", self.DateEdit_end_plot.text())
                    config.add_section("误差分布直方图1")
                    config.set("误差分布直方图1", "起始时间", self.DateTimeEdit_start_hist.text())
                    config.set("误差分布直方图1", "结束时间", self.DateTimeEdit_end_hist.text())

                    config.add_section("误差变化折线图2")
                    config.set("误差变化折线图2", "起始日期", self.DateEdit_start_plot_2.text())
                    config.set("误差变化折线图2", "结束日期", self.DateEdit_end_plot_2.text())
                    config.add_section("误差分布直方图2")
                    config.set("误差分布直方图2", "起始时间", self.DateTimeEdit_start_hist_2.text())
                    config.set("误差分布直方图2", "结束时间", self.DateTimeEdit_end_hist_2.text())
                    config.write(open(r"%s" % ini_path, "w"))
                except:
                    traceback.print_exc()
            else:
                # -----改写exiest的数值
                config.read(r"%s" % ini_path)
                config.set("误差变化折线图2", "起始日期", self.DateEdit_start_plot_2.text())
                config.set("误差变化折线图2", "结束日期", self.DateEdit_end_plot_2.text())
                config.write(open(r"%s" % ini_path, "r+"))
            startdate = typechange.date2num(self.DateEdit_start_plot_2.text())
            enddate = typechange.date2num(self.DateEdit_end_plot_2.text())
            if (enddate - startdate + 1) <= 5:
                QtWidgets.QMessageBox.warning(self, "Warning:", "时间间隔过短！")
                self.pushButton_plot_2.setEnabled(True)
                return
            db_op = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1], self.database_info_old[2])
            db_op_local = oral_operate.oracledb(self.database_info_local[0], self.database_info_local[1],
                                                self.database_info_local[2])
            flag = db_op.checkconnect()
            flag_local = db_op_local.checkconnect()
            if flag and flag_local:
                self.plotThread2 = threads.plot_data()
                self.plotThread2.setValue(self.database_info_old, self.database_info_local,
                                         self.DateEdit_start_plot_2.text(),
                                         self.DateEdit_end_plot_2.text(),
                                         2)
                self.plotThread2.signal_plotdata.connect(self.plot2)
                self.plotThread2.start()

                # datalist = dataProcess.findManyData(startdate, enddate, self.database_info, self.database_info_local)
                # self.plot(datalist)
            else:
                QtWidgets.QMessageBox.warning(self, "Warning:", "数据库连接失败！")
                self.pushButton_plot_2.setEnabled(True)
                return
        except:
            traceback.print_exc()
            self.pushButton_plot_2.setEnabled(True)

    def plot2(self, datalist):
        try:
            self.fig_plot2.clf()
            if self.ComboBox_SID_plot_2.currentText() == '总视图':
                self.grid_plot2 = Grid(self.fig_plot2, rect=111, nrows_ncols=(4, 5), axes_pad=0.5, label_mode='L')
                self.fig_plot2.tight_layout()
                i = 0
                for ax in self.grid_plot2:
                    self.example_plot(ax, datalist[0], datalist[i + 1], datalist[i + 21], i + 1)
                    i += 1
                    QtWidgets.QApplication.processEvents()
            elif self.ComboBox_SID_plot_2.currentText() == '1':
                i = 1
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '2':
                i = 2
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '3':
                i = 3
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '4':
                i = 4
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '5':
                i = 5
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '6':
                i = 6
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '7':
                i = 7
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '8':
                i = 8
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '9':
                i = 9
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '10':
                i = 10
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '11':
                i = 11
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '12':
                i = 12
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '13':
                i = 13
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '14':
                i = 14
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '15':
                i = 15
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '16':
                i = 16
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '17':
                i = 17
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '18':
                i = 18
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '19':
                i = 19
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            elif self.ComboBox_SID_plot_2.currentText() == '20':
                i = 20
                ax = self.fig_plot2.add_subplot(111)
                self.fig_plot2.tight_layout()
                self.example_plot(ax, datalist[0], datalist[i], datalist[i + 20], i, 6)
            else:
                return
            # self.fig_plot.tight_layout()
            self.pushButton_plot_2.setEnabled(True)
        except:
            traceback.print_exc()
            self.pushButton_plot_2.setEnabled(True)

    def example_plot(self, ax, datelist, errorlist, numlist, stationID, datedelta=3, fontsize=12):
        try:
            ax.cla()
            # t = np.linspace(0, 10, 101)
            # ax.plot(t, np.sin(t))
            xdata = []
            ydata = []
            ndata = []
            for i in range(len(datelist)):
                if str(errorlist[i]) != 'nan':
                    xdata.append(datelist[i])
                    ydata.append(errorlist[i])
                    ndata.append(numlist[i])
            for i in range(len(xdata)):
                xdata[i] = typechange.date2num(xdata[i])
            # max_indx = np.argmax(ydata)
            # min_indx = np.argmax(ydata)
            ax.grid()
            dateRange = typechange.dateRange(str(datelist[0])[:10], str(datelist[-1])[:10], int(typechange.date_delta(datelist[-1], datelist[0])/datedelta))
            date2numRange = [0 for i in range(len(dateRange))]
            for i in range(len(dateRange)):
                date2numRange[i] = typechange.date2num(dateRange[i])
            for i in range(len(dateRange)):
                dateRange[i] = str(dateRange[i])[5:10]
            ax.set_xlim(typechange.date2num(str(datelist[0])[:10]), typechange.date2num(str(datelist[-1])[:10]))
            ax.set_xticks(date2numRange)
            ax.set_xticklabels(dateRange)
            # ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            ax.set_ylim(-0.1,0.1)
            ax.set_xlabel('date', fontsize=fontsize)
            ax.set_ylabel('error', fontsize=fontsize)
            ax.set_title('%s' % stationID, fontsize=fontsize)
            if len(ydata) == 0:
                return
            max_indx = int(np.argmax(np.array(ydata)))
            min_indx = int(np.argmin(np.array(ydata)))
            ax.plot(xdata, ydata, linestyle='solid', marker='o')
            ax.plot(xdata[max_indx], ydata[max_indx], color='red', marker='o')
            ax.plot(xdata[min_indx], ydata[min_indx], color='green', marker='o')
            show_max = '%.4f' % ydata[max_indx]
            ax.annotate(show_max, xy=(xdata[max_indx], ydata[max_indx]), xytext=(xdata[max_indx], ydata[max_indx]+0.01))
            show_min = '%.4f' % ydata[min_indx]
            ax.annotate(show_min, xy=(xdata[min_indx], ydata[min_indx]), xytext=(xdata[min_indx], ydata[min_indx]-0.02))
            for i in range(len(ndata)):
                if ndata[i] < 500:
                    ax.scatter(xdata[i], ydata[i], color='', marker='o', edgecolors='gray', s=200)

            # ax.draw()
            ax.figure.canvas.draw()
        except:
            traceback.print_exc()

    @pyqtSlot()
    def on_pushButton_hist_clicked(self):
        try:
            self.pushButton_hist.setDisabled(True)
            if self.database_info == []:
                QtWidgets.QMessageBox.warning(self, "Warning:", "请先完成数据库连接！")
                self.pushButton_hist.setEnabled(True)
                return
            currentPath = os.getcwd()
            ini_path = currentPath + "\date_config.ini"
            ini_exist = os.path.exists(ini_path)
            # ---if database_config is not exist created it-------
            config = configparser.ConfigParser()
            if ini_exist == 0:
                try:
                    # -----创建配置文件config.ini---------
                    # TODO
                    config.add_section("数据表")
                    config.set("数据表", "日期", self.DateEdit_table.text())
                    config.add_section("误差变化折线图1")
                    config.set("误差变化折线图1", "起始日期", self.DateEdit_start_plot.text())
                    config.set("误差变化折线图1", "结束日期", self.DateEdit_end_plot.text())
                    config.add_section("误差分布直方图1")
                    config.set("误差分布直方图1", "起始时间", self.DateTimeEdit_start_hist.text())
                    config.set("误差分布直方图1", "结束时间", self.DateTimeEdit_end_hist.text())

                    config.add_section("误差变化折线图2")
                    config.set("误差变化折线图2", "起始日期", self.DateEdit_start_plot_2.text())
                    config.set("误差变化折线图2", "结束日期", self.DateEdit_end_plot_2.text())
                    config.add_section("误差分布直方图2")
                    config.set("误差分布直方图2", "起始时间", self.DateTimeEdit_start_hist_2.text())
                    config.set("误差分布直方图2", "结束时间", self.DateTimeEdit_end_hist_2.text())
                    config.write(open(r"%s" % ini_path, "w"))
                except:
                    traceback.print_exc()
            else:
                # -----改写exiest的数值
                config.read(r"%s" % ini_path)
                config.set("误差分布直方图1", "起始时间", self.DateTimeEdit_start_hist.text())
                config.set("误差分布直方图1", "结束时间", self.DateTimeEdit_end_hist.text())
                config.write(open(r"%s" % ini_path, "r+"))
            # self.database_info = ['115.156.152.146:1521/orcl', 'AMMETER', '123456']
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            # self.database_info = ['DESKTOP-R1MVU05', 'SMeter', 'sa', '422526']
            # db_op = oral_operate.sqlserver(self.database_info[0], self.database_info[1], self.database_info[2], self.database_info[3])
            startdate = typechange.date2num(self.DateTimeEdit_start_hist.text())
            enddate = typechange.date2num(self.DateTimeEdit_end_hist.text())
            if (enddate - startdate) <= 0:
                QtWidgets.QMessageBox.warning(self, "Warning:", "起止时间错误！")
                self.pushButton_hist.setEnabled(True)
                return
            flag = db_op.checkconnect()
            if flag:
                self.histThread = threads.hist_data()
                self.histThread.setValue(self.database_info, self.DateTimeEdit_start_hist.text(), self.DateTimeEdit_end_hist.text(), 1)
                self.histThread.signal_histdata.connect(self.plot_hist)
                self.histThread.start()
            else:
                QtWidgets.QMessageBox.warning(self, "Warning:", "数据库连接失败！")
                self.pushButton_hist.setEnabled(True)
                return
        except:
            traceback.print_exc()

    # TODO
    def plot_hist(self, error):
        try:
            self.fig_hist.clf()
            if self.ComboBox_SID_hist.currentText() == '总视图':
                self.grid_hist = Grid(self.fig_hist, rect=111, nrows_ncols=(4, 5), axes_pad=0.5, label_mode='L')
                self.fig_hist.tight_layout()
                i = 0
                for ax in self.grid_hist:
                    self.example_hist(ax, error[i], i + 1)
                    i += 1
                # time.sleep(1)
                    QtWidgets.QApplication.processEvents()
            elif self.ComboBox_SID_hist.currentText() == '1':
                i = 1
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '2':
                i = 2
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '3':
                i = 3
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '4':
                i = 4
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '5':
                i = 5
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '6':
                i = 6
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '7':
                i = 7
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '8':
                i = 8
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '9':
                i = 9
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '10':
                i = 10
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '11':
                i = 11
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '12':
                i = 12
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '13':
                i = 13
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '14':
                i = 14
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '15':
                i = 15
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '16':
                i = 16
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '17':
                i = 17
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '18':
                i = 18
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '19':
                i = 19
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist.currentText() == '20':
                i = 20
                ax = self.fig_hist.add_subplot(111)
                self.fig_hist.tight_layout()
                self.example_hist(ax, error[i-1], i)
            else:
                return
            # self.fig_hist.tight_layout()
            self.pushButton_hist.setEnabled(True)
        except:
            traceback.print_exc()
            self.pushButton_hist.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_hist_2_clicked(self):
        try:
            self.pushButton_hist_2.setDisabled(True)
            if self.database_info_old == []:
                QtWidgets.QMessageBox.warning(self, "Warning:", "请先完成数据库连接！")
                self.pushButton_hist_2.setEnabled(True)
                return
            currentPath = os.getcwd()
            ini_path = currentPath + "\date_config.ini"
            ini_exist = os.path.exists(ini_path)
            # ---if database_config is not exist created it-------
            config = configparser.ConfigParser()
            if ini_exist == 0:
                try:
                    # -----创建配置文件config.ini---------
                    # TODO
                    config.add_section("数据表")
                    config.set("数据表", "日期", self.DateEdit_table.text())
                    config.add_section("误差变化折线图1")
                    config.set("误差变化折线图1", "起始日期", self.DateEdit_start_plot.text())
                    config.set("误差变化折线图1", "结束日期", self.DateEdit_end_plot.text())
                    config.add_section("误差分布直方图1")
                    config.set("误差分布直方图1", "起始时间", self.DateTimeEdit_start_hist.text())
                    config.set("误差分布直方图1", "结束时间", self.DateTimeEdit_end_hist.text())

                    config.add_section("误差变化折线图2")
                    config.set("误差变化折线图2", "起始日期", self.DateEdit_start_plot_2.text())
                    config.set("误差变化折线图2", "结束日期", self.DateEdit_end_plot_2.text())
                    config.add_section("误差分布直方图2")
                    config.set("误差分布直方图2", "起始时间", self.DateTimeEdit_start_hist_2.text())
                    config.set("误差分布直方图2", "结束时间", self.DateTimeEdit_end_hist_2.text())
                    config.write(open(r"%s" % ini_path, "w"))
                except:
                    traceback.print_exc()
            else:
                # -----改写exiest的数值
                config.read(r"%s" % ini_path)
                config.set("误差分布直方图2", "起始时间", self.DateTimeEdit_start_hist_2.text())
                config.set("误差分布直方图2", "结束时间", self.DateTimeEdit_end_hist_2.text())
                config.write(open(r"%s" % ini_path, "r+"))
            # self.database_info = ['115.156.152.146:1521/orcl', 'AMMETER', '123456']
            db_op = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1], self.database_info_old[2])
            # self.database_info = ['DESKTOP-R1MVU05', 'SMeter', 'sa', '422526']
            # db_op = oral_operate.sqlserver(self.database_info[0], self.database_info[1], self.database_info[2], self.database_info[3])
            startdate = typechange.date2num(self.DateTimeEdit_start_hist_2.text())
            enddate = typechange.date2num((self.DateTimeEdit_end_hist_2.text()))
            if (enddate - startdate) <= 0:
                QtWidgets.QMessageBox.warning(self, "Warning:", "起止时间错误！")
                self.pushButton_hist.setEnabled(True)
                return
            flag = db_op.checkconnect()
            if flag:
                self.histThread2 = threads.hist_data()
                self.histThread2.setValue(self.database_info_old, self.DateTimeEdit_start_hist_2.text(), self.DateTimeEdit_end_hist_2.text(), 2)
                self.histThread2.signal_histdata.connect(self.plot_hist2)
                self.histThread2.start()
            else:
                QtWidgets.QMessageBox.warning(self, "Warning:", "数据库连接失败！")
                self.pushButton_hist_2.setEnabled(True)
                return
        except:
            traceback.print_exc()
            self.pushButton_hist_2.setEnabled(True)

    # TODO
    def plot_hist2(self, error):
        try:
            self.fig_hist2.clf()
            if self.ComboBox_SID_hist_2.currentText() == '总视图':
                self.grid_hist2 = Grid(self.fig_hist2, rect=111, nrows_ncols=(4, 5), axes_pad=0.5, label_mode='L')
                self.fig_hist2.tight_layout()
                i = 0
                for ax in self.grid_hist2:
                    self.example_hist(ax, error[i], i + 1)
                    i += 1
                # time.sleep(1)
                    QtWidgets.QApplication.processEvents()
            elif self.ComboBox_SID_hist_2.currentText() == '1':
                i = 1
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '2':
                i = 2
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '3':
                i = 3
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '4':
                i = 4
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '5':
                i = 5
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '6':
                i = 6
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '7':
                i = 7
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '8':
                i = 8
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '9':
                i = 9
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '10':
                i = 10
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '11':
                i = 11
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '12':
                i = 12
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '13':
                i = 13
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '14':
                i = 14
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '15':
                i = 15
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '16':
                i = 16
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '17':
                i = 17
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '18':
                i = 18
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '19':
                i = 19
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            elif self.ComboBox_SID_hist_2.currentText() == '20':
                i = 20
                ax = self.fig_hist2.add_subplot(111)
                self.fig_hist2.tight_layout()
                self.example_hist(ax, error[i-1], i)
            else:
                return
            # self.fig_hist.tight_layout()
            self.pushButton_hist_2.setEnabled(True)
        except:
            traceback.print_exc()
            self.pushButton_hist_2.setEnabled(True)


    # TODO
    def example_hist(self, ax, error, stationID, fontsize=12):
        try:
            ax.cla()
            binsequence = np.arange(-0.21, 0.23, 0.02)
            ax.grid()
            ax.plot([0, 0], [0, 25], color='gray', linewidth=1.2)
            ax.set_yticks([0,5,10,15,20,25,30,35,40,45,50])
            ax.set_yticklabels([0,10,20,30,40,50,60,70,80,90,100])
            if len(error) == 0:
                return
            ax.hist(error, bins=binsequence, density=True, stacked=True, facecolor="blue", edgecolor="black", alpha=0.7)
            ax.set_ylim(0, 25)

            ax.set_xlabel('error', fontsize=fontsize)
            ax.set_ylabel('%', fontsize=fontsize)
            ax.set_title('%s' % stationID, fontsize=fontsize)
            ax.figure.canvas.draw()
        except:
            traceback.print_exc()

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               "本程序",
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.Cancel,
                                               QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            self.database_set.close()
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.setrecursionlimit(1000000)
    sys.exit(app.exec_())

#
# def mycodestart():
#     app = QtWidgets.QApplication(sys.argv)
#     ui = MainWindow()
#     ui.show()
#     sys.exit(app.exec_())
#
# if __name__ == '__main__':
#     import sys, threading
#     sys.setrecursionlimit(100000)
#     threading.stack_size(200000000)
#     thread = threading.Thread(target=mycodestart)
#     thread.start()
