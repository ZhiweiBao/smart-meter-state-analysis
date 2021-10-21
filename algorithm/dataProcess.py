import traceback
from db_Oracle import oral_operate
import matlab
import time
from typechange import typechange
import Process
mlab_process = Process.initialize()


def findData(date, database_info, database_info_local, flag=1):
    # if n <= 0:
    #     return []
    try:
        zerodata = ['nan', 'nan', 'nan', 'nan', 'nan',
                    'nan', 'nan', 'nan', 'nan', 'nan',
                    'nan', 'nan', 'nan', 'nan', 'nan',
                    'nan', 'nan', 'nan', 'nan', 'nan',
                    9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                    9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if flag == 2:
            db_op = oral_operate.oracledb_old(database_info[0], database_info[1], database_info[2])
        else:
            db_op = oral_operate.oracledb(database_info[0], database_info[1], database_info[2])
        db_op_local = oral_operate.oracledb(database_info_local[0], database_info_local[1],
                                            database_info_local[2])
        result_data = db_op_local.getOneResultData(str(date)[:10], flag)
        # 判断这一天有没有结果数据*
        if result_data == []:
            # 无结果数据，进行计算
            source_data = db_op.getseldata(str(date)[:10])
            if source_data == []:
                # 当天无原始数据，将结果存为空值，标记为0，并寻找前一天的数据进行展示
                rdata = [date]
                rdata.extend(zerodata)
                rdata.append(1)
                rdata.append(flag)
                result_data.append(rdata)
                db_op_local.insert_resultdata(result_data)
                # data = self.findData(date - timedelta(days=1), n - 1)
                return [], 1
            else:
                # 当天有原始数据，取三天有效数据进行计算
                i = 1
                while i <= 7:
                    date1 = typechange.date_calculate(date, -i)
                    source_data1 = db_op.getseldata(str(date1)[:10])
                    if source_data1 == []:
                        i += 1
                    else:
                        source_data.extend(source_data1)
                        j = 1
                        while j <= 7:
                            date2 = typechange.date_calculate(date1, -j)
                            source_data2 = db_op.getseldata(str(date2)[:10])
                            if source_data2 == []:
                                j += 1
                            else:
                                source_data.extend(source_data2)
                                break
                        break
                handle_data = typechange.type_change_source(source_data)
                exec_data = mlab_process.DPFunV1(matlab.double(handle_data))
                exec_data = typechange.type_change_insert(exec_data)
                rdata = [date]
                for i in range(20):
                    rdata.append(exec_data[i][0])
                for i in range(20):
                    rdata.append(exec_data[i][1])
                for i in range(20):
                    rdata.append(exec_data[i][2])
                rdata.append(exec_data[0][3])
                rdata.append(flag)
                result_data.append(rdata)
                db_op_local.insert_resultdata(result_data)
                notenough = exec_data[0][3]
                if notenough == 1:
                    # 计算后，原始数据不足，将结果存为空值，标记为0，并寻找前一天的结果数据

                    # data = self.findData(date - timedelta(days=1), n - 1)
                    return [], notenough
                else:
                    # 计算后，原始数据足够，将数据存入，并进行显示
                    data = []
                    for i in range(20):
                        data.append([i + 1, rdata[i + 1], rdata[i + 21], rdata[i + 41]])
                    data = typechange.type_change_result(data)
                    return data, notenough
        else:
            # 有结果数据，判断标记是否为1
            notenough = result_data[0][-2]
            if notenough == 1:
                # 标记为0，寻找前一天的数据进行展示（回到*）
                # data = self.findData(date - timedelta(days=1), n - 1)
                return [], notenough
            else:
                # 标记为0，取当天结果数据进行展示
                data = []
                for i in range(20):
                    data.append([i + 1, result_data[0][i + 1], result_data[0][i + 21], result_data[0][i + 41]])
                data = typechange.type_change_result(data)
                return data, notenough
    except:
        traceback.print_exc()
        return [], 1

def findManyData(startdate, enddate, database_info, database_info_local, flag):
    try:
        db_op_local = oral_operate.oracledb(database_info_local[0], database_info_local[1],
                                            database_info_local[2])
        resultdata = db_op_local.getManyResultData(str(startdate)[:10], str(enddate)[:10], flag)
        days = typechange.date_delta(enddate, startdate) + 1
        datelist = []
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        data5 = []
        data6 = []
        data7 = []
        data8 = []
        data9 = []
        data10 = []
        data11 = []
        data12 = []
        data13 = []
        data14 = []
        data15 = []
        data16 = []
        data17 = []
        data18 = []
        data19 = []
        data20 = []
        num1 = []
        num2 = []
        num3 = []
        num4 = []
        num5 = []
        num6 = []
        num7 = []
        num8 = []
        num9 = []
        num10 = []
        num11 = []
        num12 = []
        num13 = []
        num14 = []
        num15 = []
        num16 = []
        num17 = []
        num18 = []
        num19 = []
        num20 = []
        if len(resultdata) < days:
            for i in range(days):
                findData(typechange.date_calculate(enddate, -i), database_info, database_info_local, flag)
                time.sleep(0.1)
            resultdata = db_op_local.getManyResultData(str(startdate)[:10], str(enddate)[:10], flag)
        for i in range(days):
            datelist.append(resultdata[i][0])
            data1.append(float(resultdata[i][1]))
            data2.append(float(resultdata[i][2]))
            data3.append(float(resultdata[i][3]))
            data4.append(float(resultdata[i][4]))
            data5.append(float(resultdata[i][5]))
            data6.append(float(resultdata[i][6]))
            data7.append(float(resultdata[i][7]))
            data8.append(float(resultdata[i][8]))
            data9.append(float(resultdata[i][9]))
            data10.append(float(resultdata[i][10]))
            data11.append(float(resultdata[i][11]))
            data12.append(float(resultdata[i][12]))
            data13.append(float(resultdata[i][13]))
            data14.append(float(resultdata[i][14]))
            data15.append(float(resultdata[i][15]))
            data16.append(float(resultdata[i][16]))
            data17.append(float(resultdata[i][17]))
            data18.append(float(resultdata[i][18]))
            data19.append(float(resultdata[i][19]))
            data20.append(float(resultdata[i][20]))
            num1.append(int(resultdata[i][21]))
            num2.append(int(resultdata[i][22]))
            num3.append(int(resultdata[i][23]))
            num4.append(int(resultdata[i][24]))
            num5.append(int(resultdata[i][25]))
            num6.append(int(resultdata[i][26]))
            num7.append(int(resultdata[i][27]))
            num8.append(int(resultdata[i][28]))
            num9.append(int(resultdata[i][29]))
            num10.append(int(resultdata[i][30]))
            num11.append(int(resultdata[i][31]))
            num12.append(int(resultdata[i][32]))
            num13.append(int(resultdata[i][33]))
            num14.append(int(resultdata[i][34]))
            num15.append(int(resultdata[i][35]))
            num16.append(int(resultdata[i][36]))
            num17.append(int(resultdata[i][37]))
            num18.append(int(resultdata[i][38]))
            num19.append(int(resultdata[i][39]))
            num20.append(int(resultdata[i][40]))
        datalist = [datelist, data1, data2, data3, data4, data5,
                    data6, data7, data8, data9, data10,
                    data11, data12, data13, data14, data15,
                    data16, data17, data18, data19, data20,
                    num1, num2, num3, num4, num5,
                    num6, num7, num8, num9, num10,
                    num11, num12, num13, num14, num15,
                    num16, num17, num18, num19, num20]
        return datalist
    except:
        traceback.print_exc()
        return []