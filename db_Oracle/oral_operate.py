# -*- coding: utf-8 -*-

import cx_Oracle
# import pyodbc
import traceback

# class sqlserver(object):
#
#     def __init__(self, serverName='', databaseName='', userName='', password=''):
#         self.serverName = serverName
#         self.databaseName = databaseName
#         self.userName = userName
#         self.password = password
#
#     def checkconnect(self):
#         try:
#             cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
#                          SERVER=self.serverName,
#                          DATABASE=self.databaseName,
#                          UID=self.userName,
#                          PWD=self.password)
#             cur = cnxn.cursor()
#             cur.close()
#             cnxn.close()
#             return True
#         except Exception as e:
#             print(e)
#             return False
#
#     def gethistdata(self):
#         try:
#             cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
#                          SERVER=self.serverName,
#                          DATABASE=self.databaseName,
#                          UID=self.userName,
#                          PWD=self.password)
#             cur = cnxn.cursor()
#             sql = "select STATIONID,AVERGERROR from [dbo].[201705] " \
#                   "where ITEMNAME = 'P+,H,(1.0Ib,1.0)' and " \
#                   "TRIAL_DATE like '2017/5%'"
#             cur.execute(sql)
#             rows = cur.fetchall()
#             # print(rows)
#             cur.close()
#             cnxn.close()
#             return rows
#         except Exception as e:
#             print(e)
#             return []

class oracledb(object):
    def __init__(self, host='', user='',password=''):
        self.host = host
        self.user = user
        self.password = password

    def checkconnect(self):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            cur.close()
            cnxn.close()
            return True
        except:
            traceback.print_exc()
            return False

    def get_tablename(self):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select TABLE_NAME from USER_TABLES"
            cur.execute(sql)
            rows = cur.fetchall()
            tablelist = []
            for i in range(len(rows)):
                tablelist.extend(rows[i])
            cur.close()
            cnxn.close()
            return tablelist
        except:
            traceback.print_exc()
            return []

    def getOneResultData(self, date, flag):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select * " \
                  "from RESULT_DATA " \
                  "where LINE_ID = '%s' " \
                  "and EXEC_DATE = to_date('%s','yyyy-mm-dd')"% (flag, date)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getManyResultData(self, startdate, enddate, flag):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select EXEC_DATE," \
                  "ERROR1,ERROR2,ERROR3,ERROR4,ERROR5, " \
                  "ERROR6,ERROR7,ERROR8,ERROR9,ERROR10, " \
                  "ERROR11,ERROR12,ERROR13,ERROR14,ERROR15, " \
                  "ERROR16,ERROR17,ERROR18,ERROR19,ERROR20, " \
                  "FLAG1,FLAG2,FLAG3,FLAG4,FLAG5, " \
                  "FLAG6,FLAG7,FLAG8,FLAG9,FLAG10, " \
                  "FLAG11,FLAG12,FLAG13,FLAG14,FLAG15, " \
                  "FLAG16,FLAG17,FLAG18,FLAG19,FLAG20 " \
                  "from RESULT_DATA " \
                  "where LINE_ID = '{0}' " \
                  "and EXEC_DATE between to_date('{1}','yyyy-mm-dd')" \
                  "and to_date('{2}','yyyy-mm-dd')" \
                  "order by EXEC_DATE".format(flag, startdate, enddate)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getseldata(self, date):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.GUID_ID,T.STATIONID,T.TRIALTYPE," \
                  "T.METERID,T.AVERGERROR,T.TRIALRESULT," \
                  "T.TRIALEND_DATE,T.BAR_CODE,T.ITEMNAME " \
                  "from (select GUID_ID,STATIONID,TRIALTYPE," \
                  "METERID,AVERGERROR,TRIALRESULT," \
                  "TRIALEND_DATE,BAR_CODE,ITEMNAME " \
                  "from TRIAL_DATA " \
                  "union all " \
                  "select GUID_ID,STATIONID,TRIALTYPE," \
                  "METERID,AVERGERROR,TRIALRESULT," \
                  "TRIALEND_DATE,BAR_CODE,ITEMNAME " \
                  "from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME = '基本误差P+,H,(1.0Ib,1.0)' " \
                  "and T.TRIALEND_DATE " \
                  "between to_date('%s 00:00:00','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('%s 23:59:59','yyyy-mm-dd hh24:mi:ss')"% (date, date)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def insert_resultdata(self, data):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            try:

                sql = "INSERT INTO RESULT_DATA VALUES (" \
                      "to_date(:1,'yyyy-mm-dd'),:2,:3,:4,:5,:6,:7," \
                      ":8,:9,:10,:11,:12,:13,:14," \
                      ":15,:16,:17,:18,:19,:20,:21," \
                      ":22,:23,:24,:25,:26,:27,:28," \
                      ":29,:30,:31,:32,:33,:34,:35," \
                      ":36,:37,:38,:39,:40,:41,:42," \
                      ":43,:44,:45,:46,:47,:48,:49," \
                      ":50,:51,:52,:53,:54,:55,:56," \
                      ":57,:58,:59,:60,:61,:62,:63)"
                cur.executemany(sql, data)
                cnxn.commit()
                flag = True
            except:
                flag = False
                traceback.print_exc()
                cnxn.rollback()
            cur.close()
            cnxn.close()
            return flag
        except:
            traceback.print_exc()
            return False

    def gethistdata(self, start_date, end_date):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.AVERGERROR " \
                  "from (select STATIONID,AVERGERROR,ITEMNAME,TRIALEND_DATE from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,AVERGERROR,ITEMNAME,TRIALEND_DATE from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME = '基本误差P+,H,(1.0Ib,1.0)' " \
                  "and T.TRIALEND_DATE " \
                  "between to_date('%s','yyyy-mm-dd hh24:mi:ss') and " \
                  "to_date('%s','yyyy-mm-dd hh24:mi:ss')"% (start_date, end_date)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

class oracledb_old(oracledb):


    def getseldata(self, date):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.GUID_ID,T.STATIONID,T.TRIALTYPE," \
                  "T.METERID,T.AVERGERROR,T.TRIALRESULT," \
                  "T.TRIAL_DATE,T.BAR_CODE,T.ITEMNAME " \
                  "from (select GUID_ID,STATIONID,TRIALTYPE," \
                  "METERID,AVERGERROR,TRIALRESULT," \
                  "TRIAL_DATE,BAR_CODE,ITEMNAME " \
                  "from TRIAL_DATA " \
                  "union all " \
                  "select GUID_ID,STATIONID,TRIALTYPE," \
                  "METERID,AVERGERROR,TRIALRESULT," \
                  "TRIAL_DATE,BAR_CODE,ITEMNAME " \
                  "from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME = '基本误差P+,H,(1.0Ib,1.0)' " \
                  "and T.TRIAL_DATE " \
                  "between to_date('%s 00:00:00','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('%s 23:59:59','yyyy-mm-dd hh24:mi:ss')"% (date, date)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def gethistdata(self, start_date, end_date):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.AVERGERROR " \
                  "from (select STATIONID,AVERGERROR,ITEMNAME,TRIAL_DATE from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,AVERGERROR,ITEMNAME,TRIAL_DATE from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME = '基本误差P+,H,(1.0Ib,1.0)' " \
                  "and T.TRIAL_DATE " \
                  "between to_date('%s','yyyy-mm-dd hh24:mi:ss') and " \
                  "to_date('%s','yyyy-mm-dd hh24:mi:ss')" % (start_date, end_date)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []