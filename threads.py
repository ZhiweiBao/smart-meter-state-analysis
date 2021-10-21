from PyQt5 import QtCore
import traceback
from db_Oracle import oral_operate
from typechange import typechange
from algorithm import dataProcess
# import time
from datetime import datetime, timedelta
# import struct
# import binascii
# import re
# import matlab
# import Process
# Process = Process.initialize()


# lock = threading.Lock()

class table_data(QtCore.QThread):
    signal_data = QtCore.pyqtSignal(int, list, list, int, int)

    def __init__(self, parent=None):
        super(table_data, self).__init__(parent)


    def setValue(self, database_info, database_info_old, database_info_local, date):
        self.database_info = database_info
        self.database_info_old = database_info_old
        self.database_info_local = database_info_local
        self.date = date

    def run(self):
        try:
            days = 7
            data, notenough = dataProcess.findData(self.date, self.database_info, self.database_info_local, 1)
            data2, notenough2 = dataProcess.findData(self.date, self.database_info_old, self.database_info_local, 2)
            for i in range(1, days):
                if data == []:
                    date = typechange.date_calculate(self.date, -i)
                    data = dataProcess.findData(date, self.database_info, self.database_info_local, 1)[0]
                else:
                    break
            for i in range(1, days):
                if data2 == []:
                    date = typechange.date_calculate(self.date, -i)
                    data2 = dataProcess.findData(date, self.database_info_old, self.database_info_local, 2)[0]
                else:
                    break
            # TODO
            self.signal_data.emit(days, data, data2, notenough, notenough2)
        except:
            traceback.print_exc()

class plot_data(QtCore.QThread):
    signal_plotdata = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(plot_data, self).__init__(parent)


    def setValue(self, database_info, database_info_local, startdate, enddate, flag=1):
        self.database_info = database_info
        self.database_info_local = database_info_local
        self.startdate = startdate
        self.enddate = enddate
        self.flag = flag

    def run(self):
        try:
            datalist = dataProcess.findManyData(self.startdate, self.enddate, self.database_info, self.database_info_local, self.flag)
            self.signal_plotdata.emit(datalist)
        except:
            traceback.print_exc()


class hist_data(QtCore.QThread):
    signal_histdata = QtCore.pyqtSignal(list)

    def __int__(self, parent=None):
        super(hist_data, self).__init__(parent)

    def setValue(self, database_info, start_date, end_date, flag=1):
        self.serverName = database_info[0]
        # self.dbName =database_info[1]
        self.userName = database_info[1]
        self.password = database_info[2]
        self.start_date = start_date
        self.end_date = end_date
        self.flag = flag
        # print(database_info)

    def run(self):
        try:
            if self.flag == 2:
                db_op = oral_operate.oracledb_old(self.serverName, self.userName, self.password)
            else:
                db_op = oral_operate.oracledb(self.serverName, self.userName, self.password)
            # db_op = oral_operate.sqlserver(self.serverName, self.dbName, self.userName, self.password)

            data = typechange.type_change_hist(db_op.gethistdata(self.start_date, self.end_date))
                # data = typechange.type_change_2(db_op.gethistdata('2018-06-01 00:00:00', '2018-06-01 23:59:59'))
                # data = typechange.type_change_2(db_op.gethistdata())
            error1 = []
            error2 = []
            error3 = []
            error4 = []
            error5 = []
            error6 = []
            error7 = []
            error8 = []
            error9 = []
            error10 = []
            error11 = []
            error12 = []
            error13 = []
            error14 = []
            error15 = []
            error16 = []
            error17 = []
            error18 = []
            error19 = []
            error20 = []
            for i in range(len(data)):
                if data[i][0] == 1:
                    error1.append(data[i][1])
                elif data[i][0] == 2:
                    error2.append(data[i][1])
                elif data[i][0] == 3:
                    error3.append(data[i][1])
                elif data[i][0] == 4:
                    error4.append(data[i][1])
                elif data[i][0] == 5:
                    error5.append(data[i][1])
                elif data[i][0] == 6:
                    error6.append(data[i][1])
                elif data[i][0] == 7:
                    error7.append(data[i][1])
                elif data[i][0] == 8:
                    error8.append(data[i][1])
                elif data[i][0] == 9:
                    error9.append(data[i][1])
                elif data[i][0] == 10:
                    error10.append(data[i][1])
                elif data[i][0] == 11:
                    error11.append(data[i][1])
                elif data[i][0] == 12:
                    error12.append(data[i][1])
                elif data[i][0] == 13:
                    error13.append(data[i][1])
                elif data[i][0] == 14:
                    error14.append(data[i][1])
                elif data[i][0] == 15:
                    error15.append(data[i][1])
                elif data[i][0] == 16:
                    error16.append(data[i][1])
                elif data[i][0] == 17:
                    error17.append(data[i][1])
                elif data[i][0] == 18:
                    error18.append(data[i][1])
                elif data[i][0] == 19:
                    error19.append(data[i][1])
                elif data[i][0] == 20:
                    error20.append(data[i][1])
                else:
                    print("超出表位范围！")
            error = [error1, error2, error3, error4, error5,
                     error6, error7, error8, error9, error10,
                     error11, error12, error13, error14, error15,
                     error16, error17, error18, error19, error20]
            self.signal_histdata.emit(error)
        except Exception as e:
            print(e)



