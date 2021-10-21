# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import traceback
# date= "2010-01-01"
# datetime.datetime.strptime(date, )
# datestr='2017/5/2 9:53:57'

# def date2num(datestr):
#     try:
#         num = int(str(datestr)[0:4] + str(datestr)[5:7] + str(datestr)[8:10])
#         return num
#     except:
#         traceback.print_exc()
#         return 0

# def num2date(num):
#     try:
#         datestr = str(num)[0:4] + '-' + str(num)[4:6] + '-' + str(num)[6:8]
#         return datestr
#     except:
#         traceback.print_exc()
#         return ''

def date2num(date):
    try:
        year = int(str(date)[0:4])
        if year < 2000 or year >= 2100:
            print("日期超出范围")
            return
        year -= 2000
        month = int(str(date)[5:7])
        day = int(str(date)[8:10])
        div = year//4
        mod = year%4
        if mod == 0:
            count = div*(365 * 4 + 1)
        else:
            count = div*(365 * 4 + 1) + mod*365 +1
        if year % 4 == 0:
            monList = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            for i in range(month - 1):
                count += monList[i]
        else:
            monList = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            for i in range(month - 1):
                count += monList[i]
        count += day
        return count
    except:
        traceback.print_exc()
        return 0


def date_calculate(date, delta):
    try:
        year = int(str(date)[0:4])
        if year < 2000 or year >= 2100:
            print("日期超出范围")
            return
        year -= 2000
        month = int(str(date)[5:7])
        day = int(str(date)[8:10])
        div = year//4
        mod = year%4
        if mod == 0:
            count = div*(365 * 4 + 1)
        else:
            count = div*(365 * 4 + 1) + mod*365 +1
        if year % 4 == 0:
            monList = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            for i in range(month - 1):
                count += monList[i]
        else:
            monList = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            for i in range(month - 1):
                count += monList[i]
        count += day
        count += delta
        if count <= 0:
            print("超出日期范围")
            return '2000-01-01'
        # print(count)
        fYear_div = count // (365 * 4 + 1)
        fYear_mod = count % (365 * 4 + 1)
        if fYear_mod == 0:
            Y = -1
            days = 0
        elif fYear_mod > 0 and fYear_mod <= 366:
            Y = 0
            days = fYear_mod
        elif fYear_mod > 366 and fYear_mod <= 731:
            Y = 1
            days = fYear_mod - 366
        elif fYear_mod > 731 and fYear_mod <= 1096:
            Y = 2
            days = fYear_mod - 731
        else:
            Y = 3
            days = fYear_mod - 1096
        if days == 0:
            m = '12'
            d = 31
        elif Y == 0:
            if days <= 31:
                m = '01'
                d = days
            elif days <= 60:
                m = '02'
                d = days - 31
            elif days <= 91:
                m = '03'
                d = days - 60
            elif days <= 121:
                m = '04'
                d = days - 91
            elif days <= 152:
                m = '05'
                d = days - 121
            elif days <= 182:
                m = '06'
                d = days - 152
            elif days <= 213:
                m = '07'
                d = days - 182
            elif days <= 244:
                m = '08'
                d = days - 213
            elif days <= 274:
                m = '09'
                d = days - 244
            elif days <= 305:
                m = '10'
                d = days - 274
            elif days <= 335:
                m = '11'
                d = days - 305
            else:
                m = '12'
                d = days - 335
        else:
            if days <= 31:
                m = '01'
                d = days
            elif days <= 59:
                m = '02'
                d = days - 31
            elif days <= 90:
                m = '03'
                d = days - 59
            elif days <= 120:
                m = '04'
                d = days - 90
            elif days <= 151:
                m = '05'
                d = days - 120
            elif days <= 181:
                m = '06'
                d = days - 151
            elif days <= 212:
                m = '07'
                d = days - 181
            elif days <= 243:
                m = '08'
                d = days - 212
            elif days <= 273:
                m = '09'
                d = days - 243
            elif days <= 304:
                m = '10'
                d = days - 273
            elif days <= 334:
                m = '11'
                d = days - 304
            else:
                m = '12'
                d = days - 334

        if (fYear_div * 4 + Y) >= 0 and (fYear_div * 4 + Y) < 10:
            Y_str = '0' + str(fYear_div * 4 + Y)
        else:
            Y_str = str(fYear_div * 4 + Y)
        if d > 0 and d < 10:
            d_str = '0' + str(d)
        else:
            d_str = str(d)
        datestr = '20' + Y_str + '-' + m + '-' + d_str
        return datestr
    except:
        traceback.print_exc()
        return '2000-01-01'

def date_delta(enddate, startdate):
    try:
        year = int(str(enddate)[0:4])
        if year < 2000 or year >= 2100:
            print("结束日期超出范围")
            return
        year -= 2000
        month = int(str(enddate)[5:7])
        day = int(str(enddate)[8:10])
        div = year//4
        mod = year%4
        if mod == 0:
            endcount = div*(365 * 4 + 1)
        else:
            endcount = div*(365 * 4 + 1) + mod*365 +1
        if year % 4 == 0:
            monList = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            for i in range(month - 1):
                endcount += monList[i]
        else:
            monList = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            for i in range(month - 1):
                endcount += monList[i]
        endcount += day

        year = int(str(startdate)[0:4])
        if year < 2000 or year >= 2100:
            print("起始日期超出范围")
            return
        year -= 2000
        month = int(str(startdate)[5:7])
        day = int(str(startdate)[8:10])
        div = year // 4
        mod = year % 4
        if mod == 0:
            startcount = div * (365 * 4 + 1)
        else:
            startcount = div * (365 * 4 + 1) + mod * 365 + 1
        if year % 4 == 0:
            monList = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            for i in range(month - 1):
                startcount += monList[i]
        else:
            monList = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            for i in range(month - 1):
                startcount += monList[i]
        startcount += day
        
        delta = endcount - startcount
        return delta
    except:
        traceback.print_exc()
        return 
    

def type_change_alert(data):
    try:
        for i in range(len(data)):
            data[i] = list(data[i])
            if data[i][0] >= 9 and data[i][0] <= 18:
                data[i][0] = data[i][0] - 8
            elif data[i][0] >= 23 and data[i][0] <= 32:
                data[i][0] = data[i][0] - 12
            try:
                data[i][2] = float(data[i][2])
            except:
                pass
    except:
        data = []
        traceback.print_exc()
    return data

def type_change_source(data):
    '''
    对数据类型进行预处理
    :param data:
    :return:
    '''
    try:
        result = []
        for i in range(len(data)):
            data[i] = list(data[i])
            try:
                data[i][4] = float(data[i][4])
                # if data[i][1] >= 9 and data[i][1] <= 18:
                #     data[i][1] = data[i][1] - 8
                # elif data[i][1] >= 23 and data[i][1] <= 32:
                #     data[i][1] = data[i][1] - 12
                datestr = data[i][6].strftime('%Y-%m-%d %H:%M:%S')
                data[i][6] = int(datestr[:4] + datestr[5:7] + datestr[8:10])

                data[i][7] = int(data[i][7])

                if data[i][8] == '基本误差P+,H,(1.0Ib,1.0)' or 'P+,H,(1.0Ib,1.0)':
                    data[i][8] = 1
                result.append(data[i])
            except:
                print("存在无效值")
    except Exception as e:
        result = []
        print(e)
    return result

def type_change_insert(data):
    try:
        data = list(data)
        for i in range(len(data)):
            data[i] = list(data[i])
            if str(data[i][0]) == 'nan':
                data[i][0] = str(data[i][0])
        return data
    except Exception as e:
        print(e)
        return []

def type_change_result(data):
    '''
    对数据类型进行预处理
    :param data:
    :return:
    '''
    try:
        for i in range(len(data)):
            data[i] = list(data[i])
            data[i][3] = int(data[i][3])
            data[i][1] = float(data[i][1])
            if data[i][1] != 0:
                data[i][1] = "%.4f" % data[i][1]
            if data[i][2] == 1:
                data[i][2]='负向超差'
            elif data[i][2] == 2:
                data[i][2]='负向高风险'
            elif data[i][2] == 3:
                data[i][2] = '负向偏移'
            elif data[i][2] == 4:
                data[i][2]='正常'
            elif data[i][2] == 5:
                data[i][2]='正向偏移'
            elif data[i][2] == 6:
                data[i][2]='正向高风险'
            elif data[i][2] == 7:
                data[i][2]='正向超差'
            elif data[i][2] == 8:
                data[i][2]='虚拟参考'
            else:
                data[i][2]='未参与评估'
    except Exception as e:
        data = []
        print(e)
    return data

def type_change_hist(data):
    '''
    对数据类型进行预处理
    :param data:
    :return:
    '''
    try:
        for i in range(len(data)):
            data[i] = list(data[i])
            data[i][0] = int(data[i][0])
            if data[i][0] >= 9 and data[i][0] <= 18:
                data[i][0] = data[i][0] - 8
            elif data[i][0] >= 23 and data[i][0] <= 32:
                data[i][0] = data[i][0] - 12
            try:
                data[i][1] = float(data[i][1])
            except:
                data[i][1] = float('nan')
    except Exception as e:
        data = []
        print(e)
    return data

def dateRange1(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.strptime, datetime.strftime
    days = (strptime(end, format) - strptime(start, format) + timedelta(days=1)).days
    return [strptime(start, format) + timedelta(i) for i in range(0, days, step)]

def dateRange(start, end, step=1):
    days = date_delta(end, start)+1
    return [date_calculate(start, i) for i in range(0, days, step)]

# datestr='2017/5/2 00:00:00'
# datechange(datestr)
# dt = '2016-05-05'
# timeArray = time.strptime(dt, "%Y-%m-%d")
# timestamp = time.mktime(timeArray)
# print timestamp
# print type(timestamp)
#
# dt_new = float(time.strftime("%Y%m%d",timeArray))
# print dt_new
# print type(dt_new)
#
# #转换成localtime
# time_local = time.localtime(timestamp)
# #转换成新的时间格式(2016-05-05 20:28:54)
# dt = time.strftime("%Y-%m-%d",time_local)
# print dt
# print type(dt)