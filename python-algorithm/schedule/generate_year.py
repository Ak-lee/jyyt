import copy
import datetime
import requests
import json
import numpy as np
import re
import random
import math

def generate_year(LineId, Start_Time1, End_Time1):
    p1 = "http://sunjc.top:8880/"
    p0 = "train/table/"
    p0 = p0 + str(LineId)
    url = p1 + p0
    r = requests.get(url=url)
    a = json.loads(r.text)
    p2 = "schedule/tableYearPlanNoPage"  # 年计划信息

    BookSheet2 = []
    Start_Time = datetime.datetime.strptime(Start_Time1, "%Y-%m-%d")
    End_Time = datetime.datetime.strptime(End_Time1, "%Y-%m-%d")

    p12 = "line/byLineId?lineId="
    url1 = p1 + p12 + str(LineId)
    r = requests.get(url=url1)
    a0 = json.loads(r.text)
    NumberOfTrain = a0['data'].get("trainNum")

    # p5 = "workcalendar/tableNoPage?sdate=2022-01-10&edate=2022-12-31"  # 单线的生产日历
    p5 = "workcalendar/tableNoPage?sdate=" + str(Start_Time.year) + "-" + str(Start_Time.month) + "-" + str(
        Start_Time.day) + "&edate=" + str(End_Time.year) + "-" + str(End_Time.month) + "-" + str(End_Time.day)
    url = p1 + p5
    r = requests.get(url=url)
    a1 = json.loads(r.text)
    CalendarList = []
    for i in range(len(a1['list'])):
        calendarOfDay = []
        str1 = a1['list'][i]['date']
        str2 = str1.split("T")
        str11 = datetime.datetime.strptime(str2[0], '%Y-%m-%d')
        Time1 = datetime.date(str11.year, str11.month, str11.day)
        calendarOfDay.append(Time1)
        number1 = Time1.weekday()
        if number1 == 1:
            calendarOfDay.append("周一")
        elif number1 == 2:
            calendarOfDay.append("周二")
        elif number1 == 3:
            calendarOfDay.append("周三")
        elif number1 == 4:
            calendarOfDay.append("周四")
        elif number1 == 5:
            calendarOfDay.append("周五")
        elif number1 == 6:
            calendarOfDay.append("周六")
        else:
            calendarOfDay.append("周日")
        calendarOfDay.append(a1['list'][i]['attribute'])
        CalendarList.append(calendarOfDay)

    p6 = "schedule_content_history/lastRepairType?lineId=17"  # 各列车最近的一次检修任务信息
    url = p1 + p6
    r = requests.get(url=url)
    a2 = json.loads(r.text)
    History_Data = []
    History_Repair = []
    delta = datetime.timedelta(days=1)
    EndDate = 0  # 避免重复搜索
    for i in range(1, NumberOfTrain + 1):
        if i < 10:
            ID1 = "CD" + str(LineId) + "00" + str(i)
        else:
            ID1 = "CD" + str(LineId) + "0" + str(i)
        DateList1 = []
        for k in range(EndDate, len(a2['data'])):
            m = a2['data'][k]['trainId']
            if a2['data'][k]['trainId'] == ID1:
                DateList1.append(k)
            else:
                break
        str1 = datetime.datetime.strptime(a2['data'][DateList1[len(DateList1) - 1]]["performDate"], '%Y-%m-%d')
        DeltaDays = a2['data'][DateList1[len(DateList1) - 1]]['duration']
        if DeltaDays > 1:
            for j in range(DeltaDays - 1):
                str1 += delta
        History_Data.append(str(str1.year) + "-" + str(str1.month) + "-" + str(str1.day))
        History_Repair.append(a2['data'][DateList1[len(DateList1) - 1]]['taskContent'])
        EndDate = DateList1[len(DateList1) - 1] + 1

    List0 = ["周计划", "月计划", "年计划"]  # 计划任务类型

    p7 = "tasktype/tableAll"  # 检修任务类型信息
    url = p1 + p7
    r = requests.get(url=url)
    a = json.loads(r.text)
    TypeOfRepair1 = []
    LengthList1 = []
    TimeList1 = []
    MultiModel1 = []  # 是否为多修程
    for i in range(len(a['data'])):
        TypeOfRepair1.append(a['data'][i]['taskTypeName'])
        LengthList1.append(a['data'][i]['mileagePeriod'])
        TimeList1.append(a['data'][i]['timePeriod'])
        MultiModel1.append(a['data'][i]['beMultiMode'])
    TypeOfRepair = []  # 检修任务类型
    LengthCycle = []
    TimeCycle = []
    MultiModel = []
    List1 = []
    for i in TimeList1:
        if "-" not in i:
            List1.append(int(i))
    List1.sort()
    for i in List1:
        s1 = np.where(np.array(TimeList1) == str(i))
        TypeOfRepair.append(TypeOfRepair1[s1[0][0]])
        LengthCycle.append(int(LengthList1[s1[0][0]]))
        TimeCycle.append(int(TimeList1[s1[0][0]]))
        MultiModel.append(MultiModel1[s1[0][0]])
    DictLengthCycle = {TypeOfRepair[i]: LengthCycle[i] for i in range(len(TypeOfRepair))}  # 检修任务对应的里程周期
    DictTimeCycle = {TypeOfRepair[i]: TimeCycle[i] for i in range(len(TypeOfRepair))}  # 检修任务对应的时间周期
    Dict1 = {List0[i]: TypeOfRepair[i] for i in range(len(List0))}  # 检修计划与检修任务的对应关系
    Dict3 = {TypeOfRepair[i]: MultiModel[i] for i in range(len(TypeOfRepair))}  # 检修任务和是否为多修程信息匹配关系

    p8 = "onedayMax/tableAllByLineId?lineId="
    p8 = p8 + str(LineId)
    url = p1 + p8
    r = requests.get(url=url)
    a = json.loads(r.text)
    NumberOfTask = a['data'][0]['maxBalancedRepairs']  # 均衡修任务数量约束

    p8 = "yardTasktype/byYard?yardId=CDCS"  # 车场信息
    url = p1 + p8
    r = requests.get(url=url)
    a = json.loads(r.text)
    RepairTypeOfSingle = []  # 单修程检修任务
    ModelListOfSingle = []
    for i in range(len(a['data'])):
        List2 = []
        if a['data'][i]['taskTypeName'] in TypeOfRepair:
            if len(a['data'][i]['list']) == 1:
                RepairTypeOfSingle.append(a['data'][i]['taskTypeName'])
                List2.append(a['data'][i]['list'][0]['requireHour'])
                List2.append(a['data'][i]['list'][0]['requireDay'])
                List2.append(a['data'][i]['list'][0]['requireHeadcount'])
                ModelListOfSingle.append(List2)
    Dict3 = {RepairTypeOfSingle[i]: ModelListOfSingle[i] for i in range(len(RepairTypeOfSingle))}

    p9 = "applyMonth/table?tasktypeId=3"  # 多修程信息
    CharacterList = []
    for i in range(65, 91):
        CharacterList.append(chr(i))
    url = p1 + p9
    r = requests.get(url=url)
    a = json.loads(r.text)
    MonthList1 = []
    ModelList1 = []
    for i in range(len(a['data'])):
        Model1 = []
        Model1.append(a['data'][i]["requireHour"])
        Model1.append(a['data'][i]["requireDay"])
        Model1.append(a['data'][i]["requireHeadcount"])
        month1 = a['data'][i]["applyMonth"]
        if str(month1) not in MonthList1:
            MonthList1.append(str(month1))
            ModelList1.append(Model1)
        else:  # 具有多修程的月份
            p01 = np.where(np.array(MonthList1) == str(month1))
            num1 = len(p01[0])  # 该月份已经出现的次数
            for j in range(num1):
                p2 = p01[0][j]  # 月份在List3中出现的位置
                MonthList1[p01[0][j]] = str(MonthList1[p01[0][j]]) + chr(65 + j)
            MonthList1.append(str(month1) + chr(65 + num1))
            ModelList1.append(Model1)
    Dict2 = {MonthList1[i]: ModelList1[i] for i in range(len(MonthList1))}

    p10 = "onedayMax/tableAllByLineId?lineId="
    p10 = p10 + str(LineId)
    url = p1 + p10
    r = requests.get(url=url)
    a = json.loads(r.text)
    NumberOfTask = a['data'][0]['maxBalancedRepairs']  # 均衡修任务数量约束

    if DictLengthCycle[Dict1["年计划"]] == 0:
        PreDictLengthList = []

    ModelOfLastYear1 = []
    p21 = "schedule_content_history/lastMultiModeRepair?lineId=17&deadline=2023-10-09"
    url = p1 + p21
    r = requests.get(url=url)
    a = json.loads(r.text)
    List3 = []
    for i in range(len(a['data'])):  # 具有多修程的月份数量
        List4 = []
        for j in range(len(a['data'][i])):
            List4.append(a['data'][i][j]['taskContent'].split("Y")[1])
        List3.append(List4)
    NumberOfTrain = 20
    for i in range(NumberOfTrain):
        List5 = []
        for j in range(len(List3)):
            List5.append(List3[j][i])
        ModelOfLastYear1.append(List5)

    InitialLength = []
    p13 = "schedule_content_history/lastRepairType?lineId=17"
    url = p1 + p13
    r = requests.get(url=url)
    a = json.loads(r.text)
    for i in range(NumberOfTrain):
        if i < 9:
            ID = "CD" + "1700" + str(i + 1)
        else:
            ID = "CD" + "170" + str(i + 1)
        LastDate = a['data'][i]["performDate"]  # 该列车上一次检修任务的时间
        NowDate = str(Start_Time.year) + "-" + str(Start_Time.month) + "-" + str(Start_Time.day)
        p14 = "mileage_history/getByTrainIdAndDate?trainId=" + ID + "&date=" + LastDate
        url = p1 + p14
        r = requests.get(url=url)
        a = json.loads(r.text)
        Length1 = a['data'].get("mileage")
        p15 = "mileage_history/getByTrainIdAndDate?trainId=" + ID + "&date=" + NowDate
        url = p1 + p15
        r = requests.get(url=url)
        a1 = json.loads(r.text)
        Length2 = a1['data'].get("mileage")
        InitialLength.append(Length2 - Length1)

    class QingDaoSiFang:
        def __init__(self, start_Time, end_Time):
            self.Start_Time = start_Time
            self.End_Time = end_Time

        def YearPlan(self):
            Day = self.Start_Time
            P2 = 0  # 记录计划日是整个计划周期的第几天
            Delta = datetime.timedelta(days=1)
            TotalRepairList = []  # 记录整个计划周期所有的列车的均衡修任务安排结果
            for i in range(NumberOfTrain):
                TotalRepairList.append([])
            TotalTrainList = []  # 整个计划周期内每个计划日有检修任务的列车集合
            ColOfDay = 2  # 记录在日历中属性所在列
            MaxDays = 0  # 检修任务所需要耗费的最大检修天数
            for i in range(len(ModelList1)):
                if int(ModelList1[i][1]) > MaxDays:
                    MaxDays = int(ModelList1[i][1])
            while Day < self.End_Time:
                TrainOfToday = []
                for i in range(1, NumberOfTrain + 1):
                    TrainOfToday.append(i)
                P2 += 1
                RepairListOfDay = []  # 单个计划日所有列车的检修任务安排结果,eg:[["2Y4B","2Y4B"],["2Y3"]]
                TrainListOfDay = []  # 当计划日有检修任务的列车集合
                # if BookSheet1.cell(P2 + 1, ColOfDay).value == "休息":  # 休息日不安排检修任务
                if CalendarList[P2 + 1][ColOfDay] == "休息":
                    for k in range(NumberOfTrain):
                        if len(TotalRepairList[k]) < P2:
                            TotalRepairList[k].append("No Work")
                    Day += Delta
                    TotalTrainList.append([])
                else:  # 当个计划日工作
                    DeltaDays = []  # 记录该计划日所有列车的累计时间或累计里程
                    DeltaLength = InitialLength
                    for t1 in range(NumberOfTrain):
                        delta1 = (datetime.datetime.strptime(str(Day.year) + "-" + str(Day.month) + "-" + str(Day.day),
                                                             '%Y-%m-%d') - datetime.datetime.strptime(History_Data[t1],
                                                                                                      '%Y-%m-%d')).days
                        if delta1 > 0:
                            DeltaDays.append(delta1 - 1)
                        else:
                            DeltaDays.append(0)
                    QueueTrainList = []  # 按照列车状态排序后的列表
                    # 按照列车状态进行排序
                    DeltaDays1 = copy.deepcopy(DeltaDays)
                    DeltaDays2 = []
                    for k1 in DeltaDays1:
                        if k1 not in DeltaDays2:
                            DeltaDays2.append(k1)
                    DeltaDays2.sort()
                    for delta2 in DeltaDays2:
                        p1 = np.where(np.array(DeltaDays) == delta2)
                        for i in range(len(p1[0])):
                            QueueTrainList.append(p1[0][i] + 1)
                    EarlyTrainList = []  # 当个计划日已经安排有检修任务的列车集合
                    RepairDay = 0  # 记录当个计划日已经安排的检修任务数量
                    if len(TotalRepairList) == P2 - 1:  # 当个计划日没有已经安排的检修任务
                        RepairDay = 0
                    else:
                        for t2 in range(NumberOfTrain):
                            if len(TotalRepairList[t2]) >= P2:
                                TrainOfToday.remove(t2 + 1)
                                RepairDay += 1
                                EarlyTrainList.append(t2 + 1)
                    k1 = 1
                    for t1 in range(NumberOfTrain):  # 该部分是找出该计划日必须提前的检修任务
                        ChoiceTrain = QueueTrainList[NumberOfTrain - t1 - 1]  # 先取状态不好的列车
                        # 确定该列车下一个检修任务的代号以及所需要耗费的天数
                        TaskOfTrain = []  # 该列车在该计划日的安排
                        LastRepairTask = History_Repair[ChoiceTrain - 1]  # 上一个检修任务
                        List01 = re.findall("\d+", LastRepairTask)
                        Year1 = int(List01[0])
                        Month1 = int(List01[1])
                        if Month1 == 12:
                            Year2 = Year1 + 1
                            Month2 = 1
                        else:
                            Year2 = Year1
                            Month2 = Month1 + 1
                        List11 = []  # 多修程 eg:["1"]/["4A","4B"]
                        for j in range(len(MonthList1)):
                            if int(re.findall("\d+", MonthList1[j])[0]) == Month2:
                                List11.append(MonthList1[j])
                        if len(List11) == 1:
                            SymbolOfNextTask = str(Year2) + "Y" + str(Month2)
                            NumberOfNextTask = int(Dict2[str(Month2)][1])
                        else:
                            NextModel = 0
                            for m in List11:
                                if m in ModelOfLastYear1[ChoiceTrain - 1]:
                                    p2 = np.where(np.array(List11) == m)
                                    if p2[0][0] == len(List11) - 1:
                                        NextModel = List11[0]
                                    else:
                                        NextModel = List11[p2[0][0] + 1]
                                    break
                            SymbolOfNextTask = str(Year2) + "Y" + str(NextModel)
                            NumberOfNextTask = int(Dict2[NextModel][1])

                        if DictLengthCycle[Dict1["年计划"]] == 0 and DictTimeCycle[Dict1["年计划"]] != 0:
                            if DeltaDays[ChoiceTrain - 1] <= math.ceil(DictTimeCycle[Dict1["年计划"]] * 1.1):
                                if NumberOfNextTask == 1:  # 下一个检修任务只需要耗费一天
                                    P3 = copy.deepcopy(P2)
                                    P3 += 1
                                    LengthOfHoliday = 0  # 判断是否有节假日，若是，该节假日有多少天
                                    # if BookSheet1.cell(P3 + 1, ColOfDay).value == "休息":
                                    #     for k in range(P3, BookSheet1.max_row + 1):
                                    #         if BookSheet1.cell(k + 1, ColOfDay).value == "休息":
                                    if CalendarList[P3 + 1][ColOfDay] == "休息":
                                        for k in range(P3, len(CalendarList)):
                                            if CalendarList[k + 1][ColOfDay] == "休息":
                                                LengthOfHoliday += 1
                                            else:
                                                break
                                    else:  # 下一个计划日不是节假日
                                        LengthOfHoliday = 0
                                    if LengthOfHoliday > 0:  # 下一个计划日是节假日
                                        if DeltaDays[ChoiceTrain - 1] + NumberOfNextTask + LengthOfHoliday > math.ceil(
                                                DictTimeCycle[Dict1["年计划"]] * 1.1):  # 将检修任务安排在节假日后会超过其检修周期，所以必须安排在该节假日
                                            TrainListOfDay.append(ChoiceTrain)
                                            TaskOfTrain.append(SymbolOfNextTask)
                                            RepairListOfDay.append(TaskOfTrain)
                                            TotalRepairList[ChoiceTrain - 1].append(SymbolOfNextTask)
                                            History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(
                                                Day.month) + "-" + str(Day.day)
                                            History_Repair[ChoiceTrain - 1] = SymbolOfNextTask
                                        else:
                                            continue
                                    else:  # 检修任务已经在检修周期内
                                        continue
                                else:  # 下一个检修任务需要耗费多天，以及检修任务结束后的第一天是否是节假日
                                    P3 = copy.deepcopy(P2)
                                    LengthOfHoliday = 0  # 判断检修任务结束后是否有节假日，若是，该节假日有多少天
                                    for k3 in range(NumberOfNextTask):
                                        P3 += 1
                                    # if BookSheet1.cell(P3 + 1, ColOfDay).value == "休息":  # 检修任务结束后有节假日，再获取节假日的天数
                                    if CalendarList[P3 + 1][ColOfDay] == "休息":
                                        Day9 = 0  # 记录节假日结束后的日期
                                        # for k2 in range(P3 + 1, BookSheet1.max_row + 1):
                                        #     if BookSheet1.cell(k2 + 1, ColOfDay).value == "工作":
                                        for k2 in range(P3 + 1, len(CalendarList)):
                                            if CalendarList[k2 + 1][ColOfDay] == "工作":
                                                Day9 = k2
                                                break
                                        LengthOfHoliday = Day9 - P3  # 该节假日的天数
                                        if DeltaDays[ChoiceTrain - 1] + NumberOfNextTask + LengthOfHoliday > math.ceil(
                                                DictTimeCycle[Dict1["年计划"]] * 1.1):
                                            TrainListOfDay.append(ChoiceTrain)
                                            Day1 = copy.deepcopy(Day)
                                            for d7 in range(NumberOfNextTask):
                                                TotalRepairList[ChoiceTrain - 1].append(SymbolOfNextTask)
                                            for d7 in range(NumberOfNextTask - 1):
                                                Day1 += Delta
                                            History_Data[ChoiceTrain - 1] = str(Day1.year) + "-" + str(
                                                Day1.month) + "-" + str(Day1.day)
                                            History_Repair[ChoiceTrain - 1] = SymbolOfNextTask
                                        else:  # 计划周期后仍旧没有超过检修任务的检修周期
                                            continue
                                    else:
                                        continue
                        elif DictLengthCycle[Dict1["年计划"]] != 0 and DictTimeCycle[Dict1["年计划"]] != 0:
                            if DeltaDays[ChoiceTrain - 1] <= math.ceil(DictTimeCycle[Dict1["年计划"]] * 1.1) or \
                                    InitialLength[
                                        ChoiceTrain - 1] <= math.ceil(DictLengthCycle[Dict1["年计划"]] * 1.1):
                                if NumberOfNextTask == 1:  # 下一个检修任务只需要耗费一天
                                    P3 = copy.deepcopy(P2)
                                    P3 += 1  # 当个计划日的后一日
                                    Day1 = copy.deepcopy(Day)
                                    Day2 = copy.deepcopy(Day)
                                    # Day1 += Delta
                                    LengthOfHoliday = 0  # 判断是否有节假日，若是，该节假日有多少天
                                    Length1ofHoliday = 0  # 节假日期间累计的里程值
                                    for k1 in range(1, BookSheet2.max_row + 1):
                                        a1 = str(BookSheet2.cell(k1, 1).value)
                                        b1 = datetime.datetime.strptime(a1, "%Y-%m-%d")
                                        if b1.year == Day2.year and b1.month == Day2.month and b1.day == Day2.day:
                                            Length1ofHoliday += BookSheet2.cell(k1, ChoiceTrain + 1).value  # 当个计划日的里程值
                                            break
                                    # if BookSheet1.cell(P3 + 1, ColOfDay).value == "休息":
                                    if CalendarList[P3 + 1][ColOfDay] == "休息":
                                        # for k in range(P3, BookSheet1.max_row + 1):  # 从后一日开始进行遍历
                                        for k in range(P3, len(CalendarList)):
                                            Day1 += Delta
                                            # if BookSheet1.cell(k + 1, ColOfDay).value == "休息":
                                            if CalendarList[k + 1][ColOfDay] == "休息":
                                                LengthOfHoliday += 1
                                                for k1 in range(1, BookSheet2.max_row + 1):
                                                    # a1 = str(BookSheet1.cell(k1, 1).value)
                                                    # b1 = datetime.datetime.strptime(a1, "%Y-%m-%d")
                                                    b1 = CalendarList[k1][0]
                                                    if b1.year == Day1.year and b1.month == Day1.month and b1.day == Day1.day:
                                                        Length1ofHoliday += BookSheet2.cell(k1, ChoiceTrain + 1).value
                                                        break
                                            else:
                                                break
                                    else:  # 下一个计划日不是节假日
                                        LengthOfHoliday = 0
                                        Length1ofHoliday = 0
                                    if LengthOfHoliday > 0:  # 下一个计划日是节假日
                                        if DeltaDays[ChoiceTrain - 1] + NumberOfNextTask + LengthOfHoliday > math.ceil(
                                                DictTimeCycle[Dict1["年计划"]] * 1.1) or InitialLength[
                                            ChoiceTrain - 1] + Length1ofHoliday > math.ceil(
                                            DictLengthCycle[Dict1["年计划"]] * 1.1):  # 将检修任务安排在节假日后会超过其检修周期，所以必须安排在该节假日
                                            TrainListOfDay.append(ChoiceTrain)
                                            TaskOfTrain.append(SymbolOfNextTask)
                                            RepairListOfDay.append(TaskOfTrain)
                                            TotalRepairList[ChoiceTrain - 1].append(SymbolOfNextTask)
                                            History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(
                                                Day.month) + "-" + str(Day.day)
                                            History_Repair[ChoiceTrain - 1] = SymbolOfNextTask
                                        else:
                                            continue
                                    else:  # 检修任务已经在检修周期内
                                        continue
                                else:  # 下一个检修任务需要耗费多天，以及检修任务结束后的第一天是否是节假日
                                    P3 = copy.deepcopy(P2)
                                    LengthOfHoliday = 0  # 判断检修任务结束后是否有节假日，若是，该节假日有多少天
                                    for k3 in range(NumberOfNextTask):
                                        P3 += 1
                                    Length1ofHoliday = 0  # 节假日期间累计的里程值
                                    Day1 = copy.deepcopy(Day)
                                    Day2 = copy.deepcopy(Day)
                                    for k3 in range(NumberOfNextTask):
                                        for k1 in range(1, BookSheet2.max_row + 1):
                                            a1 = str(BookSheet2.cell(k1, 1).value)
                                            b1 = datetime.datetime.strptime(a1, "%Y-%m-%d")
                                            if b1.year == Day2.year and b1.month == Day2.month and b1.day == Day2.day:
                                                Length1ofHoliday += BookSheet2.cell(k1,
                                                                                    ChoiceTrain + 1).value  # 当个计划日的里程值
                                                break
                                        Day2 += Delta
                                    # if BookSheet1.cell(P3 + 1, ColOfDay).value == "休息":  # 检修任务结束后有节假日，再获取节假日的天数
                                    if CalendarList[P3 + 1][ColOfDay] == "休息":
                                        Day9 = 0  # 记录节假日结束后的日期
                                        # for k2 in range(P3 + 1, BookSheet1.max_row + 1):
                                        #     if BookSheet1.cell(k2 + 1, ColOfDay).value == "工作":
                                        for k2 in range(P3 + 1, len(CalendarList)):
                                            if CalendarList[k2 + 1][ColOfDay] == "工作":
                                                Day9 = k2
                                                break
                                        LengthOfHoliday = Day9 - P3  # 该节假日的天数
                                        for n1 in range(LengthOfHoliday):
                                            Day2 += Delta
                                            for k1 in range(1, BookSheet2.max_row + 1):
                                                a1 = str(BookSheet2.cell(k1, 1).value)
                                                b1 = datetime.datetime.strptime(a1, "%Y-%m-%d")
                                                if b1.year == Day2.year and b1.month == Day2.month and b1.day == Day2.day:
                                                    Length1ofHoliday += BookSheet2.cell(k1,
                                                                                        ChoiceTrain + 1).value  # 当个计划日的里程值
                                                    break
                                        if DeltaDays[ChoiceTrain - 1] + NumberOfNextTask + LengthOfHoliday > math.ceil(
                                                DictTimeCycle[Dict1["年计划"]] * 1.1) or InitialLength[
                                            ChoiceTrain - 1] + Length1ofHoliday > math.ceil(
                                            DictLengthCycle[Dict1["年计划"]] * 1.1):
                                            TrainListOfDay.append(ChoiceTrain)
                                            Day1 = copy.deepcopy(Day)
                                            for d7 in range(NumberOfNextTask):
                                                TotalRepairList[ChoiceTrain - 1].append(SymbolOfNextTask)
                                            for d7 in range(NumberOfNextTask - 1):
                                                Day1 += Delta
                                            History_Data[ChoiceTrain - 1] = str(Day1.year) + "-" + str(
                                                Day1.month) + "-" + str(Day1.day)
                                            History_Repair[ChoiceTrain - 1] = SymbolOfNextTask
                                        else:  # 计划周期后仍旧没有超过检修任务的检修周期
                                            continue
                                    else:
                                        continue
                    if len(TrainListOfDay) != 0:  # 当个计划日有需要提前的检修任务
                        RepairDay += len(TrainListOfDay)
                        for t3 in TrainListOfDay:
                            TrainOfToday.remove(t3)
                    # 除已经安排完成的检修任务之外，还有当个计划日由于检修任务达到了最大检修周期而必须进行的检修任务
                    if RepairDay >= NumberOfTask:
                        for t4 in TrainOfToday:
                            if DictLengthCycle[Dict1["年计划"]] == 0 and DictTimeCycle[Dict1["年计划"]] != 0:
                                if DeltaDays[t4 - 1] == math.ceil(DictTimeCycle[Dict1["年计划"]] * 1.1):
                                    LastRepairTask = History_Repair[t4 - 1]  # 上一个检修任务
                                    List01 = re.findall("\d+", LastRepairTask)
                                    Year1 = int(List01[0])
                                    Month1 = int(List01[1])
                                    if Month1 == 12:
                                        Year2 = Year1 + 1
                                        Month2 = 1
                                    else:
                                        Year2 = Year1
                                        Month2 = Month1 + 1
                                    List11 = []  # 多修程 eg:["1"]/["4A","4B"]
                                    for j in range(len(MonthList1)):
                                        if int(re.findall("\d+", MonthList1[j])[0]) == Month2:
                                            List11.append(MonthList1[j])
                                    if len(List11) == 1:
                                        SymbolOfNextTask = str(Year2) + "Y" + str(Month2)
                                        NumberOfNextTask = int(Dict2[str(Month2)][1])
                                    else:
                                        NextModel = 0
                                        for m in List11:
                                            if m in ModelOfLastYear1[t4 - 1]:
                                                p2 = np.where(np.array(List11) == m)
                                                if p2[0][0] == len(List11) - 1:
                                                    NextModel = List11[0]
                                                else:
                                                    NextModel = List11[p2[0][0] + 1]
                                                break
                                        SymbolOfNextTask = str(Year2) + "Y" + str(NextModel)
                                        NumberOfNextTask = int(Dict2[NextModel][1])
                                    Day2 = copy.deepcopy(Day)
                                    for i2 in range(NumberOfNextTask):
                                        TotalRepairList[t4 - 1].append(SymbolOfNextTask)
                                        Day2 += Delta
                                    History_Data[t4 - 1] = str(Day2.year) + "-" + str(Day2.month) + "-" + str(Day2.day)
                                    History_Repair[t4 - 1] = SymbolOfNextTask
                            if DictLengthCycle[Dict1["年计划"]] != 0 and DictTimeCycle[Dict1["年计划"]] != 0:
                                if DeltaDays[t4 - 1] == math.ceil(DictTimeCycle[Dict1["年计划"]] * 1.1) or InitialLength[
                                    t4 - 1] == math.ceil(DictLengthCycle[Dict1["年计划"]] * 1.1):
                                    LastRepairTask = History_Repair[t4 - 1]  # 上一个检修任务
                                    List01 = re.findall("\d+", LastRepairTask)
                                    Year1 = int(List01[0])
                                    Month1 = int(List01[1])
                                    if Month1 == 12:
                                        Year2 = Year1 + 1
                                        Month2 = 1
                                    else:
                                        Year2 = Year1
                                        Month2 = Month1 + 1
                                    List11 = []  # 多修程 eg:["1"]/["4A","4B"]
                                    for j in range(len(MonthList1)):
                                        if int(re.findall("\d+", MonthList1[j])[0]) == Month2:
                                            List11.append(MonthList1[j])
                                    if len(List11) == 1:
                                        SymbolOfNextTask = str(Year2) + "Y" + str(Month2)
                                        NumberOfNextTask = int(Dict2[str(Month2)][1])
                                    else:
                                        NextModel = 0
                                        for m in List11:
                                            if m in ModelOfLastYear1[t4 - 1]:
                                                p2 = np.where(np.array(List11) == m)
                                                if p2[0][0] == len(List11) - 1:
                                                    NextModel = List11[0]
                                                else:
                                                    NextModel = List11[p2[0][0] + 1]
                                                break
                                        SymbolOfNextTask = str(Year2) + "Y" + str(NextModel)
                                        NumberOfNextTask = int(Dict2[NextModel][1])
                                    Day2 = copy.deepcopy(Day)
                                    for i2 in range(NumberOfNextTask):
                                        TotalRepairList[t4 - 1].append(SymbolOfNextTask)
                                        Day2 += Delta
                                    History_Data[t4 - 1] = str(Day2.year) + "-" + str(Day2.month) + "-" + str(Day2.day)
                                    InitialLength[t4 - 1] = 0
                                    History_Repair[t4 - 1] = SymbolOfNextTask
                    else:  # 需要安排后的列车的检修任务，但由于前有可能有提前的检修任务出现，所以可能也会出现某个计划日的检修任务超过其检修任务数量约束，也需要进行调整
                        for t1 in range(NumberOfTrain):  # 该部分是找出该计划日必须提前的检修任务
                            ChoiceTrain = QueueTrainList[NumberOfTrain - t1 - 1]
                            if ChoiceTrain in TrainOfToday:  # 从当个计划日剩余的列车中寻找满足检修任务周期的列车
                                if DictLengthCycle[Dict1["年计划"]] == 0 and DictTimeCycle[Dict1["年计划"]] != 0:
                                    if math.floor(DictTimeCycle[Dict1["年计划"]] * 0.9) <= DeltaDays[ChoiceTrain - 1] < \
                                            DictTimeCycle[Dict1["年计划"]]:  # 0.9T-T
                                        r1 = random.random()
                                        if r1 >= 0.5:
                                            LastRepairTask = History_Repair[ChoiceTrain - 1]  # 上一个检修任务
                                            List01 = re.findall("\d+", LastRepairTask)
                                            Year1 = int(List01[0])
                                            Month1 = int(List01[1])
                                            if Month1 == 12:
                                                Year2 = Year1 + 1
                                                Month2 = 1
                                            else:
                                                Year2 = Year1
                                                Month2 = Month1 + 1
                                            List11 = []  # 多修程 eg:["1"]/["4A","4B"]
                                            for j in range(len(MonthList1)):
                                                if int(re.findall("\d+", MonthList1[j])[0]) == Month2:
                                                    List11.append(MonthList1[j])
                                            if len(List11) == 1:
                                                SymbolOfNextTask = str(Year2) + "Y" + str(Month2)
                                                NumberOfNextTask = int(Dict2[str(Month2)][1])
                                            else:
                                                NextModel = 0
                                                for m in List11:
                                                    if m in ModelOfLastYear1[ChoiceTrain - 1]:
                                                        p2 = np.where(np.array(List11) == m)
                                                        if p2[0][0] == len(List11) - 1:
                                                            NextModel = List11[0]
                                                        else:
                                                            NextModel = List11[p2[0][0] + 1]
                                                        break
                                                SymbolOfNextTask = str(Year2) + "Y" + str(NextModel)
                                                NumberOfNextTask = int(Dict2[NextModel][1])
                                            # 该部分算法的目的是确保即将安排的检修任务不会位于节假日
                                            if NumberOfNextTask == 1:  # 单日检修任务
                                                Day2 = copy.deepcopy(Day)
                                                for i2 in range(NumberOfNextTask):
                                                    TotalRepairList[ChoiceTrain - 1].append(SymbolOfNextTask)
                                                for i2 in range(NumberOfNextTask - 1):
                                                    Day2 += Delta
                                                History_Data[ChoiceTrain - 1] = str(Day2.year) + "-" + str(
                                                    Day2.month) + "-" + str(Day2.day)
                                                History_Repair[ChoiceTrain - 1] = SymbolOfNextTask
                                                RepairDay += 1
                                            else:  # 多日检修任务
                                                LengthOfHoliday = 0  # 记录该节假日的天数
                                                P21 = copy.deepcopy(P2)
                                                for l in range(NumberOfNextTask - 1):
                                                    P21 += 1
                                                    # if BookSheet1.cell(P21 + 1, ColOfDay).value == "休息":
                                                    if CalendarList[P21 + 1][ColOfDay] == "休息":
                                                        LengthOfHoliday += 1
                                                if LengthOfHoliday == 0:  # 没有检修任务位于节假日，则将检修任务直接安排在该计划日
                                                    Day2 = copy.deepcopy(Day)
                                                    for i2 in range(NumberOfNextTask):
                                                        TotalRepairList[ChoiceTrain - 1].append(SymbolOfNextTask)
                                                    for i2 in range(NumberOfNextTask - 1):
                                                        Day2 += Delta
                                                    History_Data[ChoiceTrain - 1] = str(Day2.year) + "-" + str(
                                                        Day2.month) + "-" + str(Day2.day)
                                                    History_Repair[ChoiceTrain - 1] = SymbolOfNextTask
                                                    RepairDay += 1
                                    elif DictTimeCycle[Dict1["年计划"]] <= DeltaDays[ChoiceTrain - 1] <= math.ceil(
                                            DictTimeCycle[Dict1["年计划"]] * 1.1):
                                        LastRepairTask = History_Repair[ChoiceTrain - 1]  # 上一个检修任务
                                        List01 = re.findall("\d+", LastRepairTask)
                                        Year1 = int(List01[0])
                                        Month1 = int(List01[1])
                                        if Month1 == 12:
                                            Year2 = Year1 + 1
                                            Month2 = 1
                                        else:
                                            Year2 = Year1
                                            Month2 = Month1 + 1
                                        List11 = []  # 多修程 eg:["1"]/["4A","4B"]
                                        for j in range(len(MonthList1)):
                                            if int(re.findall("\d+", MonthList1[j])[0]) == Month2:
                                                List11.append(MonthList1[j])
                                        if len(List11) == 1:
                                            SymbolOfNextTask = str(Year2) + "Y" + str(Month2)
                                            NumberOfNextTask = int(Dict2[str(Month2)][1])
                                        else:
                                            NextModel = 0
                                            for m in List11:
                                                if m in ModelOfLastYear1[ChoiceTrain - 1]:
                                                    p2 = np.where(np.array(List11) == m)
                                                    if p2[0][0] == len(List11) - 1:
                                                        NextModel = List11[0]
                                                    else:
                                                        NextModel = List11[p2[0][0] + 1]
                                                    break
                                            SymbolOfNextTask = str(Year2) + "Y" + str(NextModel)
                                            NumberOfNextTask = int(Dict2[NextModel][1])
                                            # 该部分算法的目的是确保即将安排的检修任务不会位于节假日
                                        if NumberOfNextTask == 1:  # 单日检修任务
                                            Day2 = copy.deepcopy(Day)
                                            for i2 in range(NumberOfNextTask):
                                                TotalRepairList[ChoiceTrain - 1].append(SymbolOfNextTask)
                                            for i2 in range(NumberOfNextTask - 1):
                                                Day2 += Delta
                                            History_Data[ChoiceTrain - 1] = str(Day2.year) + "-" + str(
                                                Day2.month) + "-" + str(Day2.day)
                                            History_Repair[ChoiceTrain - 1] = SymbolOfNextTask
                                            RepairDay += 1
                                        else:  # 多日检修任务
                                            LengthOfHoliday = 0  # 记录该节假日的天数
                                            P21 = copy.deepcopy(P2)
                                            for l in range(NumberOfNextTask - 1):
                                                P21 += 1
                                                # if BookSheet1.cell(P21 + 1, ColOfDay).value == "休息":
                                                if CalendarList[P21 + 1][ColOfDay] == "休息":
                                                    LengthOfHoliday += 1
                                            if LengthOfHoliday == 0:  # 没有检修任务位于节假日，则将检修任务直接安排在该计划日
                                                Day2 = copy.deepcopy(Day)
                                                for i2 in range(NumberOfNextTask):
                                                    TotalRepairList[ChoiceTrain - 1].append(SymbolOfNextTask)
                                                for i2 in range(NumberOfNextTask - 1):
                                                    Day2 += Delta
                                                History_Data[ChoiceTrain - 1] = str(Day2.year) + "-" + str(
                                                    Day2.month) + "-" + str(Day2.day)
                                                History_Repair[ChoiceTrain - 1] = SymbolOfNextTask
                                                RepairDay += 1
                                    elif DeltaDays[ChoiceTrain - 1] < math.floor(DictTimeCycle[Dict1["年计划"]] * 0.9):
                                        break
                                    if RepairDay == 2:
                                        break
                                if DictLengthCycle[Dict1["年计划"]] != 0 and DictTimeCycle[Dict1["年计划"]] != 0:
                                    if math.floor(DictTimeCycle[Dict1["年计划"]] * 0.9) <= DeltaDays[ChoiceTrain - 1] < \
                                            DictTimeCycle[Dict1["年计划"]] or math.floor(
                                        DictLengthCycle[Dict1["年计划"]] * 0.9) <= InitialLength[ChoiceTrain - 1] < \
                                            DictLengthCycle[Dict1["年计划"]]:  # 0.9T-T
                                        r1 = random.random()
                                        if r1 >= 0.5:
                                            LastRepairTask = History_Repair[ChoiceTrain - 1]  # 上一个检修任务
                                            List01 = re.findall("\d+", LastRepairTask)
                                            Year1 = int(List01[0])
                                            Month1 = int(List01[1])
                                            if Month1 == 12:
                                                Year2 = Year1 + 1
                                                Month2 = 1
                                            else:
                                                Year2 = Year1
                                                Month2 = Month1 + 1
                                            List11 = []  # 多修程 eg:["1"]/["4A","4B"]
                                            for j in range(len(MonthList1)):
                                                if int(re.findall("\d+", MonthList1[j])[0]) == Month2:
                                                    List11.append(MonthList1[j])
                                            if len(List11) == 1:
                                                SymbolOfNextTask = str(Year2) + "Y" + str(Month2)
                                                NumberOfNextTask = int(Dict2[str(Month2)][1])
                                            else:
                                                NextModel = 0
                                                for m in List11:
                                                    if m in ModelOfLastYear1[ChoiceTrain - 1]:
                                                        p2 = np.where(np.array(List11) == m)
                                                        if p2[0][0] == len(List11) - 1:
                                                            NextModel = List11[0]
                                                        else:
                                                            NextModel = List11[p2[0][0] + 1]
                                                        break
                                                SymbolOfNextTask = str(Year2) + "Y" + str(NextModel)
                                                NumberOfNextTask = int(Dict2[NextModel][1])
                                            # 该部分算法的目的是确保即将安排的检修任务不会位于节假日
                                            if NumberOfNextTask == 1:  # 单日检修任务
                                                Day2 = copy.deepcopy(Day)
                                                for i2 in range(NumberOfNextTask):
                                                    TotalRepairList[ChoiceTrain - 1].append(SymbolOfNextTask)
                                                for i2 in range(NumberOfNextTask - 1):
                                                    Day2 += Delta
                                                History_Data[ChoiceTrain - 1] = str(Day2.year) + "-" + str(
                                                    Day2.month) + "-" + str(Day2.day)
                                                InitialLength[ChoiceTrain - 1] = 0
                                                History_Repair[ChoiceTrain - 1] = SymbolOfNextTask
                                                RepairDay += 1
                                            else:  # 多日检修任务
                                                LengthOfHoliday = 0  # 记录该节假日的天数
                                                P21 = copy.deepcopy(P2)
                                                for l in range(NumberOfNextTask - 1):
                                                    P21 += 1
                                                    # if BookSheet1.cell(P21 + 1, ColOfDay).value == "休息":
                                                    if CalendarList[P21 + 1][ColOfDay] == "休息":
                                                        LengthOfHoliday += 1
                                                if LengthOfHoliday == 0:  # 没有检修任务位于节假日，则将检修任务直接安排在该计划日
                                                    Day2 = copy.deepcopy(Day)
                                                    for i2 in range(NumberOfNextTask):
                                                        TotalRepairList[ChoiceTrain - 1].append(SymbolOfNextTask)
                                                    for i2 in range(NumberOfNextTask - 1):
                                                        Day2 += Delta
                                                    History_Data[ChoiceTrain - 1] = str(Day2.year) + "-" + str(
                                                        Day2.month) + "-" + str(Day2.day)
                                                    InitialLength[ChoiceTrain - 1] = 0
                                                    History_Repair[ChoiceTrain - 1] = SymbolOfNextTask
                                                    RepairDay += 1
                                        else:
                                            for row2 in range(2, BookSheet2.max_row + 1):
                                                a1 = str(BookSheet2.cell(row2, 1).value)
                                                b1 = datetime.datetime.strptime(a1, "%Y-%m-%d")
                                                if b1.year == Day.year and b1.month == Day.month and b1.day == Day.day:
                                                    InitialLength[ChoiceTrain - 1] += BookSheet2.cell(row2,
                                                                                                      ChoiceTrain + 1).value
                                                    break
                                    elif DictTimeCycle[Dict1["年计划"]] <= DeltaDays[ChoiceTrain - 1] <= math.ceil(
                                            DictTimeCycle[Dict1["年计划"]] * 1.1) or DictLengthCycle[Dict1["年计划"]] <= \
                                            InitialLength[ChoiceTrain - 1] <= math.ceil(
                                        DictLengthCycle[Dict1["年计划"]] * 1.1):
                                        LastRepairTask = History_Repair[ChoiceTrain - 1]  # 上一个检修任务
                                        List01 = re.findall("\d+", LastRepairTask)
                                        Year1 = int(List01[0])
                                        Month1 = int(List01[1])
                                        if Month1 == 12:
                                            Year2 = Year1 + 1
                                            Month2 = 1
                                        else:
                                            Year2 = Year1
                                            Month2 = Month1 + 1
                                        List11 = []  # 多修程 eg:["1"]/["4A","4B"]
                                        for j in range(len(MonthList1)):
                                            if int(re.findall("\d+", MonthList1[j])[0]) == Month2:
                                                List11.append(MonthList1[j])
                                        if len(List11) == 1:
                                            SymbolOfNextTask = str(Year2) + "Y" + str(Month2)
                                            NumberOfNextTask = int(Dict2[str(Month2)][1])
                                        else:
                                            NextModel = 0
                                            for m in List11:
                                                if m in ModelOfLastYear1[ChoiceTrain - 1]:
                                                    p2 = np.where(np.array(List11) == m)
                                                    if p2[0][0] == len(List11) - 1:
                                                        NextModel = List11[0]
                                                    else:
                                                        NextModel = List11[p2[0][0] + 1]
                                                    break
                                            SymbolOfNextTask = str(Year2) + "Y" + str(NextModel)
                                            NumberOfNextTask = int(Dict2[NextModel][1])
                                            # 该部分算法的目的是确保即将安排的检修任务不会位于节假日
                                        if NumberOfNextTask == 1:  # 单日检修任务
                                            Day2 = copy.deepcopy(Day)
                                            for i2 in range(NumberOfNextTask):
                                                TotalRepairList[ChoiceTrain - 1].append(SymbolOfNextTask)
                                            for i2 in range(NumberOfNextTask - 1):
                                                Day2 += Delta
                                            History_Data[ChoiceTrain - 1] = str(Day2.year) + "-" + str(
                                                Day2.month) + "-" + str(Day2.day)
                                            History_Repair[ChoiceTrain - 1] = SymbolOfNextTask
                                            InitialLength[ChoiceTrain - 1] = 0
                                            RepairDay += 1
                                        else:  # 多日检修任务
                                            LengthOfHoliday = 0  # 记录该节假日的天数
                                            P21 = copy.deepcopy(P2)
                                            for l in range(NumberOfNextTask - 1):
                                                P21 += 1
                                                # if BookSheet1.cell(P21 + 1, ColOfDay).value == "休息":
                                                if CalendarList[P21 + 1][ColOfDay] == "休息":
                                                    LengthOfHoliday += 1
                                            if LengthOfHoliday == 0:  # 没有检修任务位于节假日，则将检修任务直接安排在该计划日
                                                Day2 = copy.deepcopy(Day)
                                                for i2 in range(NumberOfNextTask):
                                                    TotalRepairList[ChoiceTrain - 1].append(SymbolOfNextTask)
                                                for i2 in range(NumberOfNextTask - 1):
                                                    Day2 += Delta
                                                History_Data[ChoiceTrain - 1] = str(Day2.year) + "-" + str(
                                                    Day2.month) + "-" + str(Day2.day)
                                                InitialLength[ChoiceTrain - 1] = 0
                                                History_Repair[ChoiceTrain - 1] = SymbolOfNextTask
                                                RepairDay += 1
                                    elif DeltaDays[ChoiceTrain - 1] < math.floor(DictTimeCycle[Dict1["年计划"]] * 0.9) and \
                                            InitialLength[ChoiceTrain - 1] < math.floor(
                                        DictLengthCycle[Dict1["年计划"]] * 0.9):
                                        break
                                    if RepairDay == 2:
                                        break
                    # 当这些检修任务安排完成之后，需要对计划日超过检修数量约束的列车的检修任务进行调整，范围包括该计划日之前以及之后的一段时间内
                    NumberOfTask1 = 0  # 记录当个计划日所安排的检修任务的最大的日期
                    for k in range(NumberOfTrain):
                        if len(TotalRepairList[k]) > NumberOfTask1:
                            NumberOfTask1 = len(TotalRepairList[k])
                    NumberTaskOfToday = []  # 计划日从后向前
                    DayOfList = []  # 记录所有遍历的计划日
                    for p3 in range(NumberOfTask1, P2 - MaxDays, -1):  # 不存在将检修任务提前至P2当个计划日前的计划日
                        DayOfList.append(p3)
                        if p3 < P2:  # 当个计划日之前的计划日
                            Number1 = 0
                            for k in range(NumberOfTrain):
                                if "Y" in TotalRepairList[k][p3 - 1]:
                                    Number1 += 1
                            NumberTaskOfToday.append(Number1)
                        else:  # 当个计划日及后续计划日
                            Number1 = 0
                            for k in range(NumberOfTrain):
                                if len(TotalRepairList[k]) >= p3:  # 在p3当个计划日有检修任务
                                    Number1 += 1
                            NumberTaskOfToday.append(Number1)
                    TimeList1 = []  # 记录检修任务数量超过约束的计划日
                    for p3 in range(len(NumberTaskOfToday) - 1, -1, -1):
                        if NumberTaskOfToday[p3] > NumberOfTask:
                            TimeList1.append(DayOfList[p3])
                    if len(TimeList1) > 0:  # eg:TimeList1:[62]
                        CheList = []  # 记录检修任务过多的列车以及对应的检修任务集合[[9,14,18],[11,14,18]]
                        RepairList = []  # eg:[["2Y5A","2Y4B","2Y4B"],["2Y5A","2Y4B","2Y4B"]]
                        for d2 in range(len(TimeList1)):
                            CheList1 = []
                            RepairList1 = []
                            day1 = TimeList1[d2]
                            for c1 in range(NumberOfTrain):  # 确定检修任务数量过多的单个计划日的检修任务集合以及列车集合
                                if len(TotalRepairList[c1]) >= day1:
                                    CheList1.append(c1 + 1)
                                    ChoiceTask = TotalRepairList[c1][day1 - 1]
                                    RepairList1.append(ChoiceTask)
                            CheList.append(CheList1)
                            RepairList.append(RepairList1)
                        NumberOfDayList = []  # 检修任务过多所出现的检修任务的检修模式中耗费的天数，目的是尽量能找到单日检修任务方便进行调整,eg:[[1,2,2],[1,2,2]]
                        for repairlist in RepairList:
                            NumberOfDays = []
                            for repair in repairlist:
                                if "Y" in repair:
                                    str1 = repair.split("Y")
                                    NumberOfDays.append(int(Dict2[str1[1]][1]))
                                else:
                                    NumberOfDays.append(0)
                            NumberOfDayList.append(NumberOfDays)
                        if len(NumberOfDayList) == 1:  # 只有一个计划日的检修任务数量超过了检修数量约束,eg:[[2,2,2]]/[[1,2,2]]
                            List12 = NumberOfDayList[0]  # eg:[1,2,2]/[2,2,2]/[1,1,2]/[1,1,1]
                            Number11 = 0
                            for day5 in List12:  # 单日检修任务的数量
                                if day5 == 1:
                                    Number11 += 1
                            Number25 = 0
                            for k2 in List12:
                                if k2 != 0:
                                    Number25 += 1
                            if Number25 - Number11 > NumberOfTask:  # 这种情况下需要调整多日检修任务和单日检修任务
                                if Number11 != 0:  # 有单日检修任务，先调整单日的，再调整多日的
                                    p1 = np.where(np.array(List12) == 1)
                                    for p2 in range(len(p1[0])):
                                        ChoiceTrain1 = CheList[0][p1[0][p2]]
                                        for day6 in range(TimeList1[0] - 1, 2, -1):
                                            # if BookSheet1.cell(day6 + 1, ColOfDay).value == "工作":
                                            if CalendarList[day6 + 1][ColOfDay] == "工作":
                                                Number12 = 0
                                                for t4 in range(NumberOfTrain):
                                                    if "Y" in TotalRepairList[t4][day6 - 1]:
                                                        Number12 += 1
                                                if Number12 < NumberOfTask:
                                                    if TimeList1[0] >= P2:  # 是当个计划日及后续计划日的检修任务超过约束
                                                        TotalRepairList[ChoiceTrain1 - 1].remove(
                                                            RepairList[0][p1[0][p2]])
                                                        TotalRepairList[ChoiceTrain1 - 1][day6 - 1] = RepairList[0][
                                                            p1[0][p2]]  # RepairList[0][p1[0][p2]]为任务编号
                                                    else:  # 是当个计划日前的检修任务超过检修约束
                                                        TotalRepairList[ChoiceTrain1 - 1][day6 - 1] = RepairList[0][
                                                            p1[0][p2]]
                                                        TotalRepairList[ChoiceTrain1 - 1][TimeList1[0] - 1] = "No Work"
                                                    break
                                    # 调整多日检修任务
                                    RemainTask = len(List12) - Number11
                                    NumberOfAdjust = RemainTask - NumberOfTask  # 后续需要调整的多日检修任务的数量
                                    Number13 = copy.deepcopy(NumberOfAdjust)
                                    for n2 in range(len(List12)):
                                        if List12[n2] > 1:  # 寻找多日检修任务
                                            Number13 -= 1
                                            # 寻找到多日检修任务的首个任务从哪个计划日开始，最晚是从P2当个计划日开始
                                            ChoiceTrain2 = CheList[0][n2]
                                            ChoiceTask2 = RepairList[0][n2]
                                            Date2 = List12[n2]  # 记录该列车该检修任务所持续的时间
                                            StartDate = 0
                                            for day7 in range(TimeList1[0] - MaxDays, TimeList1[0] + MaxDays, 1):
                                                if "Y" in TotalRepairList[ChoiceTrain2 - 1][day7 - 1]:
                                                    StartDate = day7
                                                    break
                                            for day8 in range(StartDate - 1, 2, -1):  # 从该检修任务开始计划日的前一日开始向前进行搜寻
                                                DateList = []  # 寻找到连续的Date2个工作日，倒序[62, 61]
                                                Day8 = copy.deepcopy(day8)
                                                for n3 in range(Date2):
                                                    DateList.append(Day8)
                                                    Day8 -= 1
                                                Number14 = 0
                                                for day9 in DateList:
                                                    # if BookSheet1.cell(day9 + 1, ColOfDay).value == "工作":
                                                    if CalendarList[day9 + 1][ColOfDay] == "工作":
                                                        Number14 += 1
                                                if Number14 == len(DateList):  # 若DateList中这些连续的计划日均处于工作日中
                                                    Number15 = 0
                                                    for k1 in range(len(DateList)):
                                                        ChoiceDate = DateList[len(DateList) - k1 - 1]
                                                        Number16 = 0  # 记录当个计划日的检修任务数量
                                                        for c5 in range(NumberOfTrain):
                                                            if "Y" in TotalRepairList[c5][ChoiceDate - 1]:
                                                                Number16 += 1
                                                        if Number16 < NumberOfTask:  # 当个计划日的检修任务数量没有达到检修数量约束
                                                            Number15 += 1
                                                    if Number15 == len(DateList):  # 连续Number14个工作日的检修任务数量没有达到检修任务数量约束
                                                        # 这样就可以把该多日任务插入到DateList所代表的连续多个计划日
                                                        for d5 in DateList:
                                                            TotalRepairList[ChoiceTrain2 - 1][d5 - 1] = ChoiceTask2
                                                        List13 = []  # 记录初始检修任务所在计划日集合
                                                        StartDate1 = copy.deepcopy(StartDate)
                                                        for k2 in range(Date2):
                                                            List13.append(StartDate1)
                                                            StartDate1 += 1
                                                        for date1 in range(len(List13)):  # eg:[61,62,63]
                                                            date2 = List13[len(List13) - date1 - 1]
                                                            if date2 >= P2:
                                                                TotalRepairList[ChoiceTrain2 - 1].pop(date2 - 1)
                                                            else:
                                                                TotalRepairList[ChoiceTrain2 - 1][date2 - 1] = "No Work"
                                                        break
                                            if Number13 == 0:
                                                break
                                else:  # 直接调整多日检修任务
                                    Number17 = len(List12) - NumberOfTask  # 需要调整的多日检修任务数量
                                    Number18 = copy.deepcopy(Number17)
                                    for n2 in range(len(List12)):
                                        Number18 -= 1
                                        ChoiceTrain2 = CheList[0][n2]
                                        ChoiceTask2 = RepairList[0][n2]
                                        Date2 = List12[n2]  # 记录该列车该检修任务所持续的时间
                                        StartDate = 0
                                        for day7 in range(TimeList1[0] - MaxDays, TimeList1[0] + MaxDays, 1):
                                            if "Y" in TotalRepairList[ChoiceTrain2 - 1][day7 - 1]:
                                                StartDate = day7
                                                break
                                        Number24 = 0
                                        for day8 in range(StartDate - 1, 2, -1):  # 从该检修任务开始计划日的前一日开始向前进行搜寻
                                            DateList = []  # 寻找到连续的Date2个工作日，倒序[62, 61]
                                            Day8 = copy.deepcopy(day8)
                                            for n3 in range(Date2):
                                                DateList.append(Day8)
                                                Day8 -= 1
                                            Number14 = 0
                                            for day9 in DateList:
                                                # if BookSheet1.cell(day9 + 1, ColOfDay).value == "工作":
                                                if CalendarList[day9 + 1][ColOfDay] == "工作":
                                                    Number14 += 1
                                            if Number14 == len(DateList):  # 若DateList中这些连续的计划日均处于工作日中
                                                Number15 = 0
                                                for k1 in range(len(DateList)):
                                                    ChoiceDate = DateList[len(DateList) - k1 - 1]
                                                    Number16 = 0  # 记录当个计划日的检修任务数量
                                                    for c5 in range(NumberOfTrain):
                                                        if "Y" in TotalRepairList[c5][ChoiceDate - 1]:
                                                            Number16 += 1
                                                    if Number16 < NumberOfTask:  # 当个计划日的检修任务数量没有达到检修数量约束
                                                        Number15 += 1
                                                if Number15 == len(DateList):  # 连续Number14个工作日的检修任务数量没有达到检修任务数量约束
                                                    # 这样就可以把该多日任务插入到DateList所代表的连续多个计划日
                                                    Number24 += 1
                                                    for d5 in DateList:
                                                        TotalRepairList[ChoiceTrain2 - 1][d5 - 1] = ChoiceTask2
                                                    List13 = []  # 记录初始检修任务所在计划日集合
                                                    StartDate1 = copy.deepcopy(StartDate)
                                                    for k2 in range(Date2):
                                                        List13.append(StartDate1)
                                                        StartDate1 += 1
                                                    for date1 in range(len(List13)):  # eg:[61,62,63]
                                                        date2 = List13[len(List13) - date1 - 1]
                                                        if date2 >= P2:
                                                            TotalRepairList[ChoiceTrain2 - 1].pop(date2 - 1)
                                                        else:
                                                            TotalRepairList[ChoiceTrain2 - 1][date2 - 1] = "No Work"
                                                    break
                                        if Number24 == 0:  # 前面的数据不能进行调整
                                            MinDeltaDays = 100
                                            ChoiceTrain3 = 0
                                            for train1 in CheList[0]:
                                                if DeltaDays[train1 - 1] < MinDeltaDays:
                                                    MinDeltaDays = DeltaDays[train1 - 1]
                                                    ChoiceTrain3 = train1
                                            p4 = np.where(np.array(CheList[0]) == ChoiceTrain3)
                                            ChoiceTask3 = RepairList[0][p4[0][0]]  # eg:2Y4B
                                            NumberOfTask1 = int(Dict2[ChoiceTask3.split("Y")[1]][1])
                                            EndOfHoliday = 0  # 节假日结束后的计划日
                                            # for d10 in range(P2 + NumberOfTask1, BookSheet1.max_row + 1):
                                            #     if BookSheet1.cell(d10 + 1, ColOfDay).value == "工作":
                                            for d10 in range(P2 + NumberOfTask1, len(CalendarList)):
                                                if CalendarList[d10 + 1][ColOfDay] == "工作":
                                                    EndOfHoliday = d10
                                                    break
                                            starttime1 = 0
                                            for d11 in range(P2 - MaxDays, P2 + MaxDays):
                                                if "Y" in TotalRepairList[ChoiceTrain3 - 1][d11 - 1]:
                                                    starttime1 = d11
                                                    break
                                            MaxNumber = copy.deepcopy(len(TotalRepairList[ChoiceTrain3 - 1]))
                                            for k4 in range(starttime1, EndOfHoliday):
                                                if k4 <= MaxNumber:
                                                    TotalRepairList[ChoiceTrain3 - 1][k4 - 1] = "No Work"
                                                else:
                                                    TotalRepairList[ChoiceTrain3 - 1].append("No Work")
                                            for k5 in range(EndOfHoliday, EndOfHoliday + NumberOfTask1):
                                                TotalRepairList[ChoiceTrain3 - 1].append(ChoiceTask3)
                                        if Number18 == 0:
                                            break
                            else:  # 这种情况下只需要调整单日检修任务  # eg:[1,1,2]/[1,1,1]/[1,2,2]
                                NumberOfAdjust = Number25 - NumberOfTask  # 需要调整的单日检修任务数量
                                NumberOfAdjust1 = copy.deepcopy(NumberOfAdjust)
                                Number26 = 0
                                for n1 in range(len(List12)):
                                    if List12[n1] == 1:
                                        NumberOfAdjust1 -= 1
                                        ChoiceTrain2 = CheList[0][n1]
                                        ChoiceTask2 = RepairList[0][n1]
                                        Number26 = 0
                                        for day6 in range(TimeList1[0] - 1, 2, -1):
                                            # if BookSheet1.cell(day6 + 1, ColOfDay).value == "工作":
                                            if CalendarList[day6 + 1][ColOfDay] == "工作":
                                                Number19 = 0
                                                for t5 in range(NumberOfTrain):
                                                    if "Y" in TotalRepairList[t5][day6 - 1]:
                                                        Number19 += 1
                                                if Number19 < NumberOfTask:
                                                    Number26 += 1
                                                    if TimeList1[0] >= P2:  # 是当个计划日及后续计划日的检修任务超过约束
                                                        TotalRepairList[ChoiceTrain2 - 1].remove(ChoiceTask2)
                                                        TotalRepairList[ChoiceTrain2 - 1][
                                                            day6 - 1] = ChoiceTask2  # RepairList[0][p1[0][p2]]为任务编号
                                                    else:  # 是当个计划日前的检修任务超过检修约束
                                                        TotalRepairList[ChoiceTrain2 - 1][day6 - 1] = ChoiceTask2
                                                        TotalRepairList[ChoiceTrain2 - 1][TimeList1[0] - 1] = "No Work"
                                                    break
                                        if NumberOfAdjust1 == 0:
                                            break
                                if Number26 == 0:  # 前面的计划日不能调整当日的单日检修任务，只能那个选择状态好的列车将其检修任务后延
                                    List14 = []
                                    List15 = []
                                    for m1 in range(len(List12)):
                                        if List12[m1] == 1:
                                            List14.append(CheList[0][m1])
                                            List15.append(RepairList[0][m1])
                                    List16 = []  # 记录需要调整的列车编号
                                    List17 = copy.deepcopy(List14)
                                    for k6 in range(NumberOfAdjust1):
                                        min0 = 100
                                        mintrain = 0
                                        for t10 in List17:
                                            if DeltaDays[t10 - 1] < min0:
                                                min0 = DeltaDays[t10 - 1]
                                                mintrain = t10
                                        List16.append(mintrain)
                                        List17.remove(mintrain)
                                    for t11 in List17:
                                        ChoiceTrain2 = t11
                                        p5 = np.where(np.array(CheList[0]) == ChoiceTrain2)
                                        ChoiceTask2 = RepairList[0][p5[0][0]]
                                        NumberOfTask1 = 1
                                        EndOfHoliday = 0  # 节假日结束后的计划日
                                        # for d10 in range(P2 + NumberOfTask1, BookSheet1.max_row + 1):
                                        #     if BookSheet1.cell(d10 + 1, ColOfDay).value == "工作":
                                        for d10 in range(P2 + NumberOfTask1, len(CalendarList)):
                                            if CalendarList[d10 + 1][ColOfDay] == "工作":
                                                EndOfHoliday = d10
                                                break
                                        starttime1 = 0
                                        for d11 in range(P2 - MaxDays, P2 + MaxDays):
                                            if "Y" in TotalRepairList[ChoiceTrain2 - 1][d11 - 1]:
                                                starttime1 = d11
                                                break
                                        MaxNumber = copy.deepcopy(len(TotalRepairList[ChoiceTrain2 - 1]))
                                        for k4 in range(starttime1, EndOfHoliday):
                                            if k4 <= MaxNumber:
                                                TotalRepairList[ChoiceTrain2 - 1][k4 - 1] = "No Work"
                                            else:
                                                TotalRepairList[ChoiceTrain2 - 1].append("No Work")
                                        for k5 in range(EndOfHoliday, EndOfHoliday + NumberOfTask1):
                                            TotalRepairList[ChoiceTrain2 - 1].append(ChoiceTask2)
                        else:  # 有多个计划日的检修任务数量超过了单个计划日的检修任务数量约束,eg:[[1,2,2],[1,2,2]]
                            # 先判断多个计划日是否是连续的
                            Number20 = 1
                            n2 = TimeList1[0]
                            for t6 in range(1, len(TimeList1)):
                                if TimeList1[t6] == n2 + 1:
                                    Number20 += 1
                                    n2 = TimeList1[t6]
                            if Number20 == len(TimeList1):  # 是连续的多个计划日
                                if len(TimeList1) == 2:  # 两个连续的计划日
                                    Number21 = 0  # 记录这多个计划日是否可以只调整单日检修任务
                                    for list1 in NumberOfDayList:  # eg:[[1,2,2],[1,2,2]]/[[2,2,2],[2,2,2]]
                                        Number22 = 0
                                        for n4 in list1:  # [1,2,2]/[2,2,2]
                                            if n4 == 1:
                                                Number22 += 1
                                        if len(list1) - Number22 <= NumberOfTask:  # 当个计划日可以只调整单日检修任务
                                            Number21 += 1
                                    if Number21 == len(NumberOfDayList):  # 连续的多个计划日均可以通过调整单计划日任务来达到目的
                                        for l1 in range(len(NumberOfDayList)):
                                            ChoiceDay = TimeList1[l1]  # 所选择的计划日
                                            TrainList = CheList[l1]  # 当个计划日有检修任务的列车集合
                                            TaskList = RepairList[l1]  # 当个计划日的检修任务集合
                                            NumberOfAdjust = len(TrainList) - NumberOfTask  # 当个计划日需要调整的检修任务数量
                                            NumberOfAdjust1 = copy.deepcopy(NumberOfAdjust)
                                            for l2 in range(len(TrainList)):
                                                if NumberOfDayList[l1][l2] == 1:
                                                    NumberOfAdjust1 -= 1
                                                    ChoiceTrain = TrainList[l2]
                                                    ChoiceTask = TaskList[l2]
                                                    for d6 in range(ChoiceDay - 1, 2, 0):
                                                        # if BookSheet1.cell(d6 + 1, ColOfDay).value == "休息" and d6 not in TimeList1:  # 就是不要将要调整的任务插入到另一个将要调整任务的计划日
                                                        if CalendarList[d6 + 1][
                                                            ColOfDay] == "休息" and d6 not in TimeList1:
                                                            NumberOfDay = 0  # 当个计划日已经安排的检修任务数量
                                                            for n5 in range(NumberOfTrain):
                                                                if "Y" in TotalRepairList[n5][d6 - 1]:
                                                                    NumberOfDay += 1
                                                            if NumberOfDay < NumberOfTask:  # 可以插入
                                                                if ChoiceDay >= P2:
                                                                    TotalRepairList[ChoiceTrain - 1].remove(ChoiceTask)
                                                                    TotalRepairList[ChoiceTrain - 1][
                                                                        d6 - 1] = ChoiceTask
                                                                else:
                                                                    TotalRepairList[ChoiceTrain - 1][
                                                                        d6 - 1] = ChoiceTask
                                                                    TotalRepairList[ChoiceTrain - 1][
                                                                        ChoiceDay - 1] = "No Work"
                                                                break
                                                    if NumberOfAdjust1 == 0:
                                                        break
                                    else:  # 部分计划日需要调整多日检修任务
                                        # 找出计划日间有检修任务的相同的列车
                                        CommonTrain = []  # 多个计划日中存在的共有的列车,eg:[14,18]，且可能会存在3日检修任务
                                        for t7 in CheList[0]:  # eg:[[9,14,18],[11,14,18]]
                                            for t8 in CheList[1]:
                                                if t7 == t8:
                                                    CommonTrain.append(t8)
                                                    break
                                        # 直接调整CommonTrain中的列车的任务
                                        number1 = len(CheList[0])
                                        number2 = len(CheList[1])
                                        for train in CommonTrain:
                                            StartDate = 0
                                            for day7 in range(P2 - MaxDays, P2 + MaxDays, 1):
                                                if "Y" in TotalRepairList[train - 1][day7 - 1]:
                                                    StartDate = day7
                                                    break
                                            if StartDate == P2:  # 若小于P2则说明该列车的该检修任务至少是3日检修任务，暂不选择进行调整
                                                Number23 = 0  # 判断在这段时间内能否找到合适的插入点
                                                for j in range(P2 - 1, 0, -1):
                                                    p1 = np.where(np.array(CheList[0]) == train)
                                                    task1 = RepairList[0][p1[0][0]]
                                                    delta3 = NumberOfDayList[0][p1[0][0]]
                                                    DateList = []  # 寻找到连续的Date2个工作日，倒序[62, 61]
                                                    Day8 = copy.deepcopy(j)
                                                    for n3 in range(delta3):
                                                        DateList.append(Day8)
                                                        Day8 -= 1
                                                    Number14 = 0
                                                    for day9 in DateList:
                                                        # if BookSheet1.cell(day9 + 1, ColOfDay).value == "工作":
                                                        if CalendarList[day9 + 1][ColOfDay] == "工作":
                                                            Number14 += 1
                                                    if Number14 == len(DateList):  # 若DateList中这些连续的计划日均处于工作日中
                                                        Number15 = 0
                                                        for k1 in range(len(DateList)):
                                                            ChoiceDate = DateList[len(DateList) - k1 - 1]
                                                            Number16 = 0  # 记录当个计划日的检修任务数量
                                                            for c5 in range(NumberOfTrain):
                                                                if "Y" in TotalRepairList[c5][ChoiceDate - 1]:
                                                                    Number16 += 1
                                                            if Number16 < NumberOfTask:  # 当个计划日的检修任务数量没有达到检修数量约束
                                                                Number15 += 1
                                                        if Number15 == len(
                                                                DateList):  # 连续Number14个工作日的检修任务数量没有达到检修任务数量约束
                                                            # 这样就可以把该多日任务插入到DateList所代表的连续多个计划日
                                                            Number23 += 1
                                                            for d5 in DateList:
                                                                TotalRepairList[train - 1][d5 - 1] = task1
                                                            List13 = []  # 记录初始检修任务所在计划日集合
                                                            StartDate1 = copy.deepcopy(StartDate)
                                                            for k2 in range(delta3):
                                                                List13.append(StartDate1)
                                                                StartDate1 += 1
                                                            for date1 in range(len(List13)):  # eg:[61,62,63]
                                                                date2 = List13[len(List13) - date1 - 1]
                                                                if date2 >= P2:
                                                                    TotalRepairList[train - 1].pop(date2 - 1)
                                                                else:
                                                                    TotalRepairList[train - 1][date2 - 1] = "No Work"
                                                            break
                                                if Number23 == 0:  # 在内部不能进行调整，只能将状态更好的列车向后排，但可能会超过最大检修周期
                                                    # 找出CommonTrain中状态更好的列车
                                                    N1 = max(NumberTaskOfToday)  # eg:4
                                                    N2 = N1 - NumberOfTask  # 需要调整的列车数量
                                                    MinDeltaDays = 100
                                                    ChoiceTrain3 = 0
                                                    CommonTrain1 = copy.deepcopy(CommonTrain)
                                                    for train1 in CommonTrain1:
                                                        if DeltaDays[train1 - 1] < MinDeltaDays:
                                                            MinDeltaDays = DeltaDays[train1 - 1]
                                                            ChoiceTrain3 = train1
                                                    p4 = np.where(np.array(CheList[0]) == ChoiceTrain3)
                                                    ChoiceTask3 = RepairList[0][p4[0][0]]  # eg:2Y4B
                                                    NumberOfTask1 = int(Dict2[ChoiceTask3.split("Y")[1]][1])
                                                    EndOfHoliday = 0  # 节假日结束后的计划日
                                                    # for d10 in range(P2 + NumberOfTask1, BookSheet1.max_row + 1):
                                                    #     if BookSheet1.cell(d10 + 1, ColOfDay).value == "工作":
                                                    for d10 in range(P2 + NumberOfTask1, len(CalendarList)):
                                                        if CalendarList[d10 + 1][ColOfDay] == "工作":
                                                            EndOfHoliday = d10
                                                            break
                                                    starttime1 = 0
                                                    for d11 in range(P2 - MaxDays, P2 + MaxDays):
                                                        if "Y" in TotalRepairList[ChoiceTrain3 - 1][d11 - 1]:
                                                            starttime1 = d11
                                                            break
                                                    MaxNumber = copy.deepcopy(len(TotalRepairList[ChoiceTrain3 - 1]))
                                                    for k4 in range(starttime1, EndOfHoliday):
                                                        if k4 <= MaxNumber:
                                                            TotalRepairList[ChoiceTrain3 - 1][k4 - 1] = "No Work"
                                                        else:
                                                            TotalRepairList[ChoiceTrain3 - 1].append("No Work")
                                                    for k5 in range(EndOfHoliday, EndOfHoliday + NumberOfTask1):
                                                        TotalRepairList[ChoiceTrain3 - 1].append(ChoiceTask3)
                                                number1 -= 1
                                                number2 -= 1
                                                if number1 <= NumberOfTask and number2 <= NumberOfTask:
                                                    break
                        # 调整该计划日的任务:
                        for c3 in range(NumberOfTrain):
                            if len(TotalRepairList[c3]) < P2:  # 当个计划日没有安排检修任务
                                TotalRepairList[c3].append("No Work")
                        # 调整History_Data和History_Repair的数据
                        for c4 in range(NumberOfTrain):
                            if len(TotalRepairList[c4]) == P2:  # P2计划日后没有安排检修任务
                                Number4 = 0
                                for d4 in range(P2, 0, -1):
                                    Number4 += 1
                                    if "Y" in TotalRepairList[c4][d4 - 1]:
                                        Task2 = TotalRepairList[c4][d4 - 1]
                                        Date1 = copy.deepcopy(Day)
                                        for n in range(Number4 - 1):
                                            Date1 -= Delta
                                        History_Data[c4] = str(Date1.year) + "-" + str(Date1.month) + "-" + str(
                                            Date1.day)
                                        History_Repair[c4] = Task2
                                        break
                            else:  # 当个计划日后仍旧有检修任务
                                length = len(TotalRepairList[c4])
                                deltalength = length - P2
                                Date2 = copy.deepcopy(Day)
                                for i in range(deltalength):
                                    Date2 += Delta
                                History_Data[c4] = str(Date2.year) + "-" + str(Date2.month) + "-" + str(Date2.day)
                                History_Repair[c4] = TotalRepairList[c4][length - 1]
                    else:  # 当个计划日的检修任务数量符合约束
                        for c5 in range(NumberOfTrain):
                            if len(TotalRepairList[c5]) < P2:  # 当个计划日没有安排检修任务
                                TotalRepairList[c5].append("No Work")
                    Day += Delta
            return TotalRepairList

        def main1(self, TotalRepairList):
            scheduleId = "Y1720210001"
            list1 = []
            Delta = datetime.timedelta(days=1)
            Dict01 = {"scheduleId": scheduleId, "trainId": "CD", "planDate": 2021, "duration": 2, "taskType": "均衡修",
                      "taskContent": "2Y4B", "applyMonth": 4}
            for t in range(NumberOfTrain):
                End_Time1 = copy.deepcopy(End_Time)
                Start_Time3 = copy.deepcopy(Start_Time)
                Day1 = copy.deepcopy(Start_Time)
                P1 = 0
                for i in range((End_Time1 - Start_Time3).days):
                    P1 += 1
                    Task1 = TotalRepairList[t][P1 - 1]
                    if "Y" in Task1:  # 当日当列车有检修任务
                        if t < 9:
                            Train1 = "CD" + "1700" + str(t + 1)
                        else:
                            Train1 = "CD" + "170" + str(t + 1)
                        Dict01["trainId"] = Train1
                        Dict01["planDate"] = str(Day1.year) + "-" + str(Day1.month) + "-" + str(Day1.day)
                        str1 = Task1.split("Y")
                        DeltaDays = Dict2[str1[1]][1]  # 该种检修任务的持续时间
                        Start_Time1 = 0
                        for j in range(P1 + DeltaDays - 1, 0, -1):
                            if "Y" in TotalRepairList[t][j - 1]:
                                Start_Time1 = j
                                break
                        Day2 = 0  # 计划内容中该检修任务的连续时间
                        for j in range(Start_Time1, 0, -1):
                            if "Y" in TotalRepairList[t][j - 1]:
                                Day2 += 1
                            else:
                                break
                        if Day2 == DeltaDays:  # 说明该检修任务全部安排正在计划周期内
                            # 需要判断这是该检修任务的第几个计划日的任务，只记录首个计划日的信息
                            Start_Time2 = 0  # 记录该检修任务开始的时间
                            if P1 < 3:
                                for k2 in range(0, P1 + 3 - 1):
                                    if "Y" in TotalRepairList[t][k2]:
                                        Start_Time2 = k2 + 1
                                        break
                            else:
                                for k2 in range(P1 - 2, P1 + 2):
                                    if "Y" in TotalRepairList[t][k2 - 1]:
                                        Start_Time2 = k2
                                        break
                            if Start_Time2 == P1:  # 这是该检修任务的首个计划日
                                Dict01["duration"] = DeltaDays
                                Dict01["taskContent"] = Task1
                                Dict01["applyMonth"] = int(re.findall("\d+", Task1)[1])
                                Dict11 = copy.deepcopy(Dict01)
                                list1.append(Dict11)
                    Day1 += Delta
            p1 = "http://sunjc.top:8880/"
            p3 = "schedule_content/clear?scheduleId=" + scheduleId  # 删除数据库中已经有的该任务ID的数据
            url1 = p1 + p3
            response = requests.get(url1)
            print(response)  # response=<200>说明访问成功
            print(response.text)

            p2 = "schedule_content/list"
            url = p1 + p2
            response = requests.post(url, json=list1)
            print(response)  # response=<200>说明访问成功
            print(response.text)  # response.text和浏览器返回数据相同说明post数据成功

    result = QingDaoSiFang(Start_Time, End_Time)
    TotalRepairList = result.YearPlan()
    result.main1(TotalRepairList)

if __name__ == '__main__':
    generate_year(17)