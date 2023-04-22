import copy
import datetime
import requests
import json
import numpy as np
import re
import random
import math

def generate_week(LineId, Start_Time1, End_Time1):
    p1 = "http://sunjc.top:8880/"
    # LineId = 17  # 线路ID
    p0 = "train/table/"
    p0 = p0 + str(LineId)
    url = p1 + p0
    r = requests.get(url=url)
    a = json.loads(r.text)

    p12 = "line/byLineId?lineId="
    url1 = p1 + p12 + str(LineId)
    r = requests.get(url=url1)
    a0 = json.loads(r.text)
    NumberOfTrain = a0['data'].get("trainNum")

    p2 = "schedule_content_history/lastMonthRepair?lineId=17"
    url = p1 + p2
    r = requests.get(url=url)
    a1 = json.loads(r.text)
    History_Data0 = []
    for i in range(NumberOfTrain):
        if i < 9:
            Train1 = "CD" + str(LineId) + "00" + str(i + 1)
        else:
            Train1 = "CD" + str(LineId) + "0" + str(i + 1)
        for j in range(len(a1['list'])):
            if a1['list'][j]["trainId"] == Train1:
                History_Data0.append(a1['list'][j]["performDate"])
                break

    List0 = ["年计划", "月计划", "周计划"]  # 计划任务类型

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
    TypeOfRepair2 = []
    LengthCycle2 = []
    TimeCycle2 = []
    for i in range(len(TypeOfRepair)):
        TypeOfRepair2.append(TypeOfRepair[len(TypeOfRepair) - i - 1])
        LengthCycle2.append(LengthCycle[len(LengthCycle) - i - 1])
        TimeCycle2.append(TimeCycle[len(TimeCycle) - i - 1])
    TypeOfRepair = copy.deepcopy((TypeOfRepair2))
    LengthCycle = copy.deepcopy((LengthCycle2))
    TimeCycle = copy.deepcopy((TimeCycle2))
    DictLengthCycle = {TypeOfRepair[i]: LengthCycle[i] for i in range(len(TypeOfRepair))}  # 检修任务对应的里程周期
    DictTimeCycle = {TypeOfRepair[i]: TimeCycle[i] for i in range(len(TypeOfRepair))}  # 检修任务对应的时间周期
    Dict1 = {List0[i]: TypeOfRepair[i] for i in range(len(List0))}  # 检修计划与检修任务的对应关系
    Dict3 = {TypeOfRepair[i]: MultiModel[i] for i in range(len(TypeOfRepair))}  # 检修任务和是否为多修程信息匹配关系

    p3 = "schedule/tableWeekPlanNoPage"  # 周计划信息
    url = p1 + p3
    r = requests.get(url=url)
    a = json.loads(r.text)

    delta = datetime.timedelta(days=1)
    Start_Time = datetime.datetime.strptime(Start_Time1, "%Y-%m-%d")
    End_Time = datetime.datetime.strptime(End_Time1, "%Y-%m-%d") + delta
    Days = (End_Time - Start_Time).days

    p11 = "onedayMax/tableAllByLineId?lineId="
    p11 = p11 + str(LineId)
    url = p1 + p11
    r = requests.get(url=url)
    a1 = json.loads(r.text)
    NumberOfTask = a1['data'][0]['maxMileageChecks']  # 里程检任务数量约束

    p82 = "yardTasktype/byYard?yardId=CDCS"  # 车场信息
    url = p1 + p82
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

    p15 = "schedule_content/getListByScheduleIdAndRange?scheduleId="  # 获取月计划对应的登顶检的任务
    MonthId = "M1720210001"
    p14 = p15 + MonthId + "&start=" + str(Start_Time) + "&end=" + str(End_Time)
    url = p1 + p14
    r = requests.get(url=url)
    a3 = json.loads(r.text)
    p16 = "schedule_content/getListByScheduleIdAndRange?scheduleId="  # 获取年计划对应计划内容
    YearId = "Y1720210001"
    p17 = p16 + YearId + "&start=" + str(Start_Time) + "&end=" + str(End_Time)
    url = p1 + p17
    r = requests.get(url=url)
    a4 = json.loads(r.text)
    # 在这里是分别获取对应时间段的月计划和年计划内容，然后拼接在一起
    MonthTaskList = []  # 这里面的日期是字符型，需要转化格式
    Day1 = copy.deepcopy(Start_Time)
    while Day1 < End_Time:
        List1 = []
        List1.append(str(Day1.year) + "-" + str(Day1.month) + "-" + str(Day1.day))
        for j in range(NumberOfTrain + 1):
            List1.append("")
        MonthTaskList.append(List1)
        Day1 += delta
    Day1 = copy.deepcopy(Start_Time)
    P1 = 0
    while Day1 < End_Time:
        for i in range(len(a4['list'])):
            str1 = a4['list'][i]["planDate"]
            Date1 = datetime.datetime.strptime(str1, '%Y-%m-%d')
            if Date1.year == Day1.year and Date1.month == Day1.month and Date1.day == Day1.day:
                train1 = a4['list'][i]['trainId']
                train2 = int(train1.split("CD")[1]) % 100
                duration = a4['list'][i]["duration"]
                taskContent = a4['list'][i]["taskContent"]
                P2 = copy.deepcopy(P1)
                for j in range(duration):
                    if P2 < Days:
                        MonthTaskList[P2][train2] = taskContent
                        P2 += 1
        Day1 += delta
        P1 += 1

    Day1 = copy.deepcopy(Start_Time)
    P1 = 0
    while Day1 < End_Time:
        for i in range(len(a3['list'])):
            if len(a3['list'][i]['id']) < 10:
                str1 = a3['list'][i]["planDate"]
                Date1 = datetime.datetime.strptime(str1, '%Y-%m-%d')
                if Date1.year == Day1.year and Date1.month == Day1.month and Date1.day == Day1.day:
                    train1 = a3['list'][i]['trainId']
                    train2 = int(train1.split("CD")[1]) % 100
                    duration = a3['list'][i]["duration"]
                    taskContent = a3['list'][i]["taskType"]
                    MonthTaskList[P1][train2] = taskContent
        Day1 += delta
        P1 += 1
    for i in range(7):
        print(MonthTaskList[i])

    InitialLength0 = []  # 接口没问题，数据不足
    p13 = "schedule_content_history/allTypeLeast?lineId=" + str(LineId) + "&deadline=" + "2021-09-28"  # 这个时间是计划开始时间
    url = p1 + p13
    r = requests.get(url=url)
    a = json.loads(r.text)
    DateList1 = []
    for i in range(NumberOfTrain):
        List1 = []
        List1.append(a["data"].get("year")[i]["performDate"])  # 最近一次均衡修
        List1.append(a["data"].get("week")[i]["performDate"])  # 最近一次登顶检
        Date1 = datetime.datetime.strptime(List1[0], '%Y-%m-%d')
        Date2 = datetime.datetime.strptime(List1[1], '%Y-%m-%d')
        Delta1 = (Date1 - Date2).days
        if Delta1 > 0:
            DateList1.append(List1[0])
        elif Delta1 < 0:
            DateList1.append(List1[1])
        else:
            DateList1.append(List1[0])
    for i in range(NumberOfTrain):
        if i < 9:
            ID = "CD" + "1700" + str(i + 1)
        else:
            ID = "CD" + "170" + str(i + 1)
        LastDate = DateList1[i]
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
        InitialLength0.append(Length2 - Length1)

    PreDictLengthList = []
    sDate = str(Start_Time.year) + "-" + str(Start_Time.month) + "-" + str(Start_Time.day)
    eDate = str(End_Time.year) + "-" + str(End_Time.month) + "-" + str(End_Time.day)
    List3 = []
    for i in range(NumberOfTrain):
        if i < 9:
            ID = "CD" + "1700" + str(i + 1)
        else:
            ID = "CD" + "170" + str(i + 1)
        p18 = "mileageForecast/getByTrainIdAndRange?trainId=" + ID + "&sdate=" + sDate + "&edate=" + eDate
        # 因为预测数据返回的是绝对里程值，而需要的是单个计划日的相对里程值，所以需要知道计划开始前一天的绝对里程数据
        url = p1 + p18
        r = requests.get(url=url)
        a = json.loads(r.text)
        List1 = []
        for j in range(len(a['data'])):
            List1.append(a['data'][j]["mileage"])
        List3.append(List1)
    LengthOfLastDay = []  # 记录所有列车上一个计划日的绝对里程数据
    delta = datetime.timedelta(days=1)
    LastDay = Start_Time - delta
    LastDate = str(LastDay.year) + "-" + str(LastDay.month) + "-" + str(LastDay.day)
    for i in range(NumberOfTrain):
        if i < 9:
            ID = "CD" + "1700" + str(i + 1)
        else:
            ID = "CD" + "170" + str(i + 1)
        p14 = "mileage_history/getByTrainIdAndDate?trainId=" + ID + "&date=" + LastDate
        url = p1 + p14
        r = requests.get(url=url)
        a1 = json.loads(r.text)
        Length2 = a1['data'].get("mileage")
        LengthOfLastDay.append(Length2)
    List15 = []
    for i in range(7):
        List4 = []
        for j in range(NumberOfTrain):
            List4.append(List3[j][i])
        List15.append(List4)
    # 取相对里程值
    List5 = []
    for i in range(7):
        for j in range(NumberOfTrain):
            if i == 0:  # 首个计划日的相对里程数据 = 首个计划日的绝对里程数据 - 首个计划日前的绝对里程数据
                List5.append(List15[i][j] - LengthOfLastDay[j])
            else:  # 后面计划日的相对里程数据 = 该计划日的绝对里程数据 - 前一日的绝对里程数据
                List15.append(List15[i][j] - List5[i][j - 1])
        PreDictLengthList.append(List5)

    class WeekPlanning1:
        def __init__(self, numberOfTrain, repairType, dictTimeCycle):
            self.NumberOfTrain = numberOfTrain
            self.TypeOfRepair = repairType
            self.DictTimeCycle = dictTimeCycle

        def WeekPlan(self):
            History_Data = copy.deepcopy(History_Data0)
            InitialLength = copy.deepcopy(InitialLength0)
            Day = copy.deepcopy(Start_Time)
            delta = datetime.timedelta(days=1)
            P2 = 0
            TotalTrainList = []  # 记录每个计划日有检修任务的列车集合
            DeltaDaysList = []  # 每个计划日的每辆列车的累计里程值
            while Day <= End_Time:
                TaskOfTrain = []  # 当个计划日有登顶检任务的列车集合
                P2 += 1
                DeltaDays = []  # 计划日所有列车的累计时间
                DeltaLength = []  # 计划日所有列车的累计里程
                for t in range(NumberOfTrain):
                    DeltaDays.append(0)
                    DeltaLength.append(0)
                AdvanceTrainList = []  # 记录当个计划日有均衡修任务的列车集合
                AdvanceTrainList1 = []  # 记录当个计划日有登顶检任务的列车集合
                # 先确定当个计划日是否有均衡修任务
                for row1 in range(len(MonthTaskList)):
                    Date1 = datetime.datetime.strptime(MonthTaskList[row1][0], '%Y-%m-%d')
                    if Date1.year == Day.year and Date1.month == Day.month and Date1.day == Day.day:
                        for col1 in range(1, len(MonthTaskList[row1])):
                            if "Y" in MonthTaskList[row1][col1] or Dict1["年计划"] in MonthTaskList[row1][col1]:
                                AdvanceTrainList.append(col1)
                                if DictLengthCycle[Dict1["周计划"]] != 0:
                                    History_Data[col1 - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(Day.day)
                                    InitialLength[col1 - 1] = 0
                                else:
                                    History_Data[col1 - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(Day.day)
                            else:
                                if DictLengthCycle[Dict1["周计划"]] != 0:
                                    DeltaDays[col1 - 1] = (datetime.datetime.strptime(
                                        str(Day.year) + "-" + str(Day.month) + "-" + str(Day.day),
                                        '%Y-%m-%d') - datetime.datetime.strptime(History_Data[col1 - 1],
                                                                                 '%Y-%m-%d')).days - 1
                                    DeltaLength = copy.deepcopy(InitialLength)
                                else:
                                    DeltaDays[col1 - 1] = (datetime.datetime.strptime(
                                        str(Day.year) + "-" + str(Day.month) + "-" + str(Day.day),
                                        '%Y-%m-%d') - datetime.datetime.strptime(History_Data[col1 - 1],
                                                                                 '%Y-%m-%d')).days - 1
                            if Dict1["月计划"] in MonthTaskList[row1][col1]:
                                AdvanceTrainList1.append(col1)
                        break
                DeltaDaysList.append(DeltaDays)
                DeltaDays1 = []
                for d1 in DeltaDays:
                    if d1 not in DeltaDays1:
                        DeltaDays1.append(d1)
                DeltaDays1.sort()
                QueueTrainList = []
                for d2 in DeltaDays1:
                    p1 = np.where(np.array(DeltaDays) == d2)
                    List1 = random.sample(range(1, len(p1[0]) + 1), len(p1[0]))
                    for d3 in List1:
                        QueueTrainList.append(p1[0][d3 - 1] + 1)
                Number1 = len(AdvanceTrainList1)  # 记录当个计划日安排有登顶检和里程检的检修任务数量
                for t1 in range(len(QueueTrainList)):
                    ChoiceTrain = QueueTrainList[len(QueueTrainList) - 1 - t1]
                    if ChoiceTrain not in AdvanceTrainList:
                        if DictLengthCycle[Dict1["周计划"]] != 0 and DictTimeCycle[Dict1["周计划"]] != 0:
                            if math.floor(DictTimeCycle[Dict1["周计划"]] * 0.9) <= DeltaDays[ChoiceTrain - 1] < \
                                    DictTimeCycle[Dict1["周计划"]] or math.floor(DictLengthCycle[Dict1["周计划"]] * 0.9) <= \
                                    DeltaLength[ChoiceTrain - 1] < DictLengthCycle[Dict1["周计划"]]:
                                r1 = random.random()
                                if r1 <= 0.3:
                                    TaskOfTrain.append(ChoiceTrain)
                                    Number1 += 1
                                    History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(
                                        Day.day)
                                    InitialLength[ChoiceTrain - 1] = 0
                                else:
                                    for row2 in range(len(PreDictLengthList)):
                                        NowDate = PreDictLengthList[row2][0]
                                        if NowDate.year == Day.year and NowDate.month == Day.month and NowDate.day == Day.day:
                                            InitialLength[ChoiceTrain - 1] += PreDictLengthList[row2][ChoiceTrain]
                                            break
                            elif DictTimeCycle[Dict1["周计划"]] <= DeltaDays[ChoiceTrain - 1] < math.ceil(
                                    DictTimeCycle[Dict1["周计划"]] * 1.1) or DictLengthCycle[Dict1["周计划"]] <= DeltaLength[
                                ChoiceTrain - 1] < math.ceil(DictLengthCycle[Dict1["周计划"]] * 1.1):
                                r1 = random.random()
                                if r1 <= 0.6:
                                    TaskOfTrain.append(ChoiceTrain)
                                    Number1 += 1
                                    History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(
                                        Day.day)
                                    InitialLength[ChoiceTrain - 1] = 0
                                else:
                                    for row2 in range(len(PreDictLengthList)):
                                        NowDate = PreDictLengthList[row2][0]
                                        if NowDate.year == Day.year and NowDate.month == Day.month and NowDate.day == Day.day:
                                            InitialLength[ChoiceTrain - 1] += PreDictLengthList[row2][ChoiceTrain]
                                            break
                            elif DeltaDays[ChoiceTrain - 1] == math.ceil(DictTimeCycle[Dict1["周计划"]] * 1.1) or \
                                    DeltaLength[ChoiceTrain - 1] == math.ceil(DictLengthCycle[Dict1["周计划"]] * 1.1):
                                TaskOfTrain.append(ChoiceTrain)
                                Number1 += 1
                                History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(
                                    Day.day)
                                InitialLength[ChoiceTrain - 1] = 0
                        elif DictLengthCycle[Dict1["周计划"]] == 0 and DictTimeCycle[Dict1["周计划"]] != 0:
                            if math.floor(DictTimeCycle[Dict1["周计划"]] * 0.9) <= DeltaDays[ChoiceTrain - 1] < \
                                    DictTimeCycle[Dict1["周计划"]]:
                                r1 = random.random()
                                if r1 <= 0.3:
                                    TaskOfTrain.append(ChoiceTrain)
                                    Number1 += 1
                                    History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(
                                        Day.day)
                            elif DictTimeCycle[Dict1["周计划"]] <= DeltaDays[ChoiceTrain - 1] < math.ceil(
                                    DictTimeCycle[Dict1["周计划"]] * 1.1):
                                r1 = random.random()
                                if r1 <= 0.6:
                                    TaskOfTrain.append(ChoiceTrain)
                                    Number1 += 1
                                    History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(
                                        Day.day)
                            elif DeltaDays[ChoiceTrain - 1] == math.ceil(DictTimeCycle[Dict1["周计划"]] * 1.1):
                                TaskOfTrain.append(ChoiceTrain)
                                Number1 += 1
                                History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(
                                    Day.day)
                    else:  # 当个计划日有均衡修的列车默认执行了一次登顶检
                        if DictLengthCycle[Dict1["月计划"]] != 0 and DictTimeCycle[Dict1["月计划"]] != 0:
                            History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(Day.day)
                            InitialLength[ChoiceTrain - 1] = 0
                        else:
                            History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(Day.day)
                    if Number1 >= NumberOfTask:
                        break
                TotalTrainList.append(TaskOfTrain)
                Day += delta
            return TotalTrainList, DeltaDaysList

        def Fitness(self, TotalTrainList, DeltaDaysList):  # 根据里程损失值来判定适应度值
            fitness1 = 0
            for i in range(len(TotalTrainList)):
                for t1 in TotalTrainList[i]:
                    fitness1 += math.ceil(DictTimeCycle[Dict1["周计划"]] * 1.1) - DeltaDaysList[i][t1 - 1]
            return fitness1

        def best(self):
            Maxgen = 100
            r21 = self.WeekPlan()
            r31 = self.Fitness(r21[0], r21[1])
            BestFitness = copy.deepcopy(r31)
            BestTrainList = copy.deepcopy(r21[0])
            for i in range(Maxgen):
                r2 = self.WeekPlan()
                r3 = self.Fitness(r2[0], r2[1])
                if r3 < BestFitness:
                    BestFitness = r3
                    BestTrainList = r2[0]
            # 先计算检修任务均衡性指标
            NumberList1 = []  # 记录每个计划日的检修任务数量
            for i in range(6):
                Number1 = 0  # 记录当个计划日的检修任务数量
                for j in range(1, NumberOfTrain + 1):
                    if MonthTaskList[i][j] != "":
                        Number1 += 1
                Number1 += len(BestTrainList[i])
                NumberList1.append(Number1)
            Sum1 = 0
            for k in NumberList1:
                Sum1 += k
            Average1 = int(Sum1 / len(NumberList1))
            FangCha = 0
            for j in NumberList1:
                FangCha += (j - Average1) * (j - Average1)

            TotalTaskList = []
            for d in range(Days):
                List2 = []
                for t in range(1, NumberOfTrain + 1):
                    if MonthTaskList[d][t] != "" and t in BestTrainList[d]:  # 当列车当个计划日有登顶检和均衡修任务
                        List2.append(MonthTaskList[d][t] + " + " + "里程检")
                    elif MonthTaskList[d][t] == "" and t in BestTrainList[d]:  # 当列车当个计划日有登顶检任务
                        List2.append("里程检")
                    elif MonthTaskList[d][t] != "" and t not in BestTrainList[d]:  # 当列车当个计划日有均衡修任务
                        List2.append(MonthTaskList[d][t])
                    else:
                        List2.append("")
                TotalTaskList.append(List2)

            scheduleId = "W1720210001"
            list1 = []
            Delta = datetime.timedelta(days=1)
            Day1 = copy.deepcopy(Start_Time)
            Dict01 = {"scheduleId": scheduleId, "trainId": "CD", "planDate": 2021, "duration": 2, "taskType": "登顶检",
                      "taskContent": "None"}  # 年计划对应的计划内容
            for k in range(len(TotalTaskList)):
                List1 = TotalTaskList[k]
                for j in range(NumberOfTrain):
                    if "Y" in List1[j]:  # 属于年计划对应的检修任务
                        if j < 9:
                            Train1 = "CD" + "1700" + str(j + 1)
                        else:
                            Train1 = "CD" + "170" + str(j + 1)
                        str1 = List1[j].split("Y")[1]
                        duration1 = Dict2[str1][1]  # 该检修任务持续的时间
                        # 判断该检修任务开始的计划日是否处于该计划周期内，若位于，则说明该检修任务属于该个周计划
                        if k == 0:  # 计划周期的首个计划日
                            if TotalTaskList[k + duration1 - 1][j] == List1[j]:
                                Dict01["trainId"] = Train1
                                Dict01["planDate"] = str(Day1)
                                Dict01["duration"] = duration1
                                Dict01["taskType"] = Dict1["年计划"]
                                Dict01["taskContent"] = List1[j]
                                Dict02 = copy.deepcopy(Dict01)
                                Dict02["applyMonth"] = int(re.findall("\d+", List1[j])[1])
                                list1.append(Dict02)
                        else:  # 如果不是计划周期的首个计划日，则判断某辆车出现检修任务的前一个计划日是否有相同类型的检修任务来判断其是否属于该计划周期的内容
                            if "Y" not in TotalTaskList[k - 1][j]:
                                Dict01["trainId"] = Train1
                                Dict01["planDate"] = str(Day1)
                                Dict01["duration"] = duration1
                                Dict01["taskType"] = Dict1["年计划"]
                                Dict01["taskContent"] = List1[j]
                                Dict02 = copy.deepcopy(Dict01)
                                Dict02["applyMonth"] = int(re.findall("\d+", List1[j])[1])
                                list1.append(Dict02)
                Day1 += Delta

            list2 = []  # 月计划对应的计划内容
            Day1 = copy.deepcopy(Start_Time)
            for k in range(len(TotalTaskList)):
                List1 = TotalTaskList[k]
                for j in range(NumberOfTrain):
                    if Dict1["月计划"] in List1[j]:
                        if j < 9:
                            Train1 = "CD" + "1700" + str(j + 1)
                        else:
                            Train1 = "CD" + "170" + str(j + 1)
                        if Dict3[Dict1["月计划"]][1] == 1:  # 单日检修任务
                            Dict01["trainId"] = Train1
                            Dict01["planDate"] = str(Day1)
                            Dict01["duration"] = 1
                            Dict01["taskType"] = Dict1["月计划"]
                            Dict01["taskContent"] = "None"
                            Dict02 = copy.deepcopy(Dict01)
                            Dict02["applyMonth"] = "None"
                            list2.append(Dict02)
                Day1 += Delta

            list3 = []  # 周计划对应的计划内容
            Day1 = copy.deepcopy(Start_Time)
            for k in range(len(TotalTaskList)):
                List1 = TotalTaskList[k]
                for j in range(NumberOfTrain):
                    if Dict1["周计划"] in List1[j]:
                        if j < 9:
                            Train1 = "CD" + "1700" + str(j + 1)
                        else:
                            Train1 = "CD" + "170" + str(j + 1)
                        if Dict3[Dict1["周计划"]][1] == 1:  # 单日检修任务
                            Dict01["trainId"] = Train1
                            Dict01["planDate"] = str(Day1)
                            Dict01["duration"] = 1
                            Dict01["taskType"] = Dict1["周计划"]
                            Dict01["taskContent"] = "None"
                            Dict02 = copy.deepcopy(Dict01)
                            Dict02["applyMonth"] = "None"
                            list3.append(Dict02)
                Day1 += Delta

            p1 = "http://sunjc.top:8880/"
            p3 = "schedule_content/clear?scheduleId=" + scheduleId  # 删除数据库中已经有的该任务ID的数据
            url1 = p1 + p3
            response = requests.get(url1)
            print(response)  # response=<200>说明访问成功
            print(response.text)

            p2 = "schedule_content/list"
            url = p1 + p2
            # post_data = json.dumps(list1)
            response = requests.post(url, json=list1)
            response1 = requests.post(url, json=list2)
            response2 = requests.post(url, json=list3)
            print(response)  # response=<200>说明访问成功
            print(response.text)  # response.text和浏览器返回数据相同说明post数据成功
            print(response1)  # response=<200>说明访问成功
            print(response1.text)
            print(response2)  # response=<200>说明访问成功
            print(response2.text)

    result = WeekPlanning1(NumberOfTrain, TypeOfRepair, DictTimeCycle)
    result.best()

if __name__ == '__main__':
    generate_week(17, "2021-9-19", "2021-9-25")