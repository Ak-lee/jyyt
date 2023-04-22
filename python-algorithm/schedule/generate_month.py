import copy
import datetime
import requests
import json
import numpy as np
import random
import math

def generate_month(LineId, Start_Time1, End_Time1):
    p1 = "http://sunjc.top:8880/"
    # LineId = 17  # 线路ID
    p0 = "train/table/"
    p0 = p0 + str(LineId)
    url = p1 + p0
    r = requests.get(url=url)
    a = json.loads(r.text)

    delta = datetime.timedelta(days=1)
    Start_Time = datetime.datetime.strptime(Start_Time1, "%Y-%m-%d")
    End_Time = datetime.datetime.strptime(End_Time1, "%Y-%m-%d")
    Days = (End_Time - Start_Time).days

    p12 = "line/byLineId?lineId="
    url1 = p1 + p12 + str(LineId)
    r = requests.get(url=url1)
    a0 = json.loads(r.text)
    NumberOfTrain = a0['data'].get("trainNum")

    p4 = "schedule_content_history/lastMonthRepair?lineId=17"
    url = p1 + p4
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
    Dict3 = {TypeOfRepair[i]: MultiModel[i] for i in range(len(TypeOfRepair))}  # 检修任务和是否为多修程信息匹配关系
    Dict1 = {List0[i]: TypeOfRepair[i] for i in range(len(List0))}  # 检修计划与检修任务的对应关系
    DictLengthCycle = {TypeOfRepair[i]: LengthCycle[i] for i in range(len(TypeOfRepair))}  # 检修任务对应的里程周期
    DictTimeCycle = {TypeOfRepair[i]: TimeCycle[i] for i in range(len(TypeOfRepair))}  # 检修任务对应的时间周期

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

    p8 = "onedayMax/tableAllByLineId?lineId="
    p8 = p8 + str(LineId)
    url = p1 + p8
    r = requests.get(url=url)
    a = json.loads(r.text)
    NumberOfTask = a['data'][0]['maxBalancedRepairs']  # 均衡修任务数量约束

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

    p9 = "schedule_content/getListByScheduleIdAndRange?scheduleId=Y1720210001&start=2021-09-19&end=2021-10-18"
    url = p1 + p9
    r = requests.get(url=url)
    a = json.loads(r.text)
    YearTaskList = []  # 这里面的日期是字符型，需要转化格式
    Day1 = copy.deepcopy(Start_Time)
    while Day1 < End_Time:
        List1 = []
        for j in range(NumberOfTrain + 1):
            List1.append("")
        YearTaskList.append(List1)
        Day1 += delta
    for i in range(len(a['list'])):
        data1 = a['list'][i]
        str1 = data1["trainId"]
        if str1[len(str1) - 2] == "0":
            train1 = int(str1[len(str1) - 1])
        else:
            train1 = int(str1[len(str1) - 2] + str1[len(str1) - 1])
        Date1 = data1["planDate"]
        DeltaDay1 = data1["duration"]
        TaskType = data1["taskContent"]
        DeltaDay2 = (datetime.datetime.strptime(Date1, '%Y-%m-%d') - datetime.datetime.strptime(
            str(Day1.year) + "-" + str(Day1.month) + "-" + str(Day1.day), '%Y-%m-%d')).days
        for j in range(DeltaDay2, DeltaDay2 + DeltaDay1):
            YearTaskList[j][train1 - 1] = TaskType
    Day2 = copy.deepcopy(Start_Time)
    P2 = 0
    while Day2 < End_Time:
        YearTaskList[P2][0] = str(Day2.year) + "-" + str(Day2.month) + "-" + str(Day2.day)
        P2 += 1
        Day2 += delta

    PreDictLengthList = []
    if DictLengthCycle[Dict1["月计划"]] == 0:
        PreDictLengthList = []

    InitialLength0 = []
    p13 = "schedule_content_history/allTypeLeast?lineId=" + str(LineId) + "&deadline=" + "2021-09-28"  # 这个时间是计划开始时间
    url = p1 + p13
    r = requests.get(url=url)
    a = json.loads(r.text)
    DateList1 = []
    for i in range(NumberOfTrain):
        List1 = []
        List1.append(a["data"].get("year")[i]["performDate"])  # 最近一次均衡修
        List1.append(a["data"].get("month")[i]["performDate"])  # 最近一次登顶检
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
        # NowDate = "2021-09-28"
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

    class MonthPlanning1:
        def __init__(self, numberOfTrain, repairType, dictTimeCycle):
            self.NumberOfTrain = numberOfTrain
            self.TypeOfRepair = repairType
            self.DictTimeCycle = dictTimeCycle

        def MonthPlan(self):
            History_Data = copy.deepcopy(History_Data0)
            InitialLength = copy.deepcopy(InitialLength0)
            Day = copy.deepcopy(Start_Time)
            delta = datetime.timedelta(days=1)
            P2 = 0
            TotalTrainList = []  # 记录每个计划日有检修任务的列车集合
            DeltaDaysList = []  # 每个计划日的每辆列车的累计里程值
            while Day < End_Time:
                TaskOfTrain = []  # 当个计划日有登顶检任务的列车集合
                P2 += 1
                DeltaDays = []  # 计划日所有列车的累计时间
                DeltaLength = []  # 计划日所有列车的累计里程
                for t in range(NumberOfTrain):
                    DeltaDays.append(0)
                    DeltaLength.append(0)
                AdvanceTrainList = []  # 记录当个计划日有均衡修任务的列车集合
                # 先确定当个计划日是否有均衡修任务
                for row1 in range(len(YearTaskList)):
                    Date1 = datetime.datetime.strptime(YearTaskList[row1][0], '%Y-%m-%d')
                    if Date1.year == Day.year and Date1.month == Day.month and Date1.day == Day.day:
                        for col1 in range(1, len(YearTaskList[row1])):
                            if "Y" in YearTaskList[row1][col1] or Dict1["年计划"] in YearTaskList[row1][col1]:
                                AdvanceTrainList.append(col1)
                                if DictLengthCycle[Dict1["月计划"]] != 0:
                                    History_Data[col1 - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(Day.day)
                                    InitialLength[col1 - 1] = 0
                                else:
                                    History_Data[col1 - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(Day.day)
                            else:
                                if DictLengthCycle[Dict1["月计划"]] != 0:
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
                        break
                # 将列车按照状态进行排序（按照累计时间）
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
                Number1 = 0  # 记录当个计划日安排有登顶检的列车数量
                for t1 in range(len(QueueTrainList)):
                    ChoiceTrain = QueueTrainList[len(QueueTrainList) - 1 - t1]
                    if ChoiceTrain not in AdvanceTrainList:
                        if DictLengthCycle[Dict1["月计划"]] != 0 and DictTimeCycle[Dict1["月计划"]] != 0:
                            if math.floor(DictTimeCycle[Dict1["月计划"]] * 0.9) <= DeltaDays[ChoiceTrain - 1] < \
                                    DictTimeCycle[Dict1["月计划"]] or math.floor(DictLengthCycle[Dict1["月计划"]] * 0.9) <= \
                                    DeltaLength[ChoiceTrain - 1] < DictLengthCycle[Dict1["月计划"]]:
                                r1 = random.random()
                                if r1 <= 0.2:
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
                                    # for row2 in range(2, BookSheet1.max_row + 1):
                                    #     a1 = str(BookSheet1.cell(row2, 1).value)
                                    #     b1 = datetime.datetime.strptime(a1, "%Y-%m-%d")
                                    #     if b1.year == Day.year and b1.month == Day.month and b1.day == Day.day:
                                    #         InitialLength[ChoiceTrain - 1] += BookSheet1.cell(row2, ChoiceTrain + 1).value
                                    #         break
                            elif DictTimeCycle[Dict1["月计划"]] <= DeltaDays[ChoiceTrain - 1] < math.ceil(
                                    DictTimeCycle[Dict1["月计划"]] * 1.1) or DictLengthCycle[Dict1["月计划"]] <= DeltaLength[
                                ChoiceTrain - 1] < math.ceil(DictLengthCycle[Dict1["月计划"]] * 1.1):
                                r1 = random.random()
                                if r1 <= 0.5:
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
                                    # for row2 in range(2, BookSheet1.max_row + 1):
                                    #     a1 = str(BookSheet1.cell(row2, 1).value)
                                    #     b1 = datetime.datetime.strptime(a1, "%Y-%m-%d")
                                    #     if b1.year == Day.year and b1.month == Day.month and b1.day == Day.day:
                                    #         InitialLength[ChoiceTrain - 1] += BookSheet1.cell(row2, ChoiceTrain + 1).value
                                    #         break
                            elif DeltaDays[ChoiceTrain - 1] == math.ceil(DictTimeCycle[Dict1["月计划"]] * 1.1) or \
                                    DeltaLength[ChoiceTrain - 1] == math.ceil(DictLengthCycle[Dict1["月计划"]] * 1.1):
                                TaskOfTrain.append(ChoiceTrain)
                                Number1 += 1
                                History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(
                                    Day.day)
                                InitialLength[ChoiceTrain - 1] = 0
                            else:
                                break
                        elif DictLengthCycle[Dict1["月计划"]] == 0 and DictTimeCycle[Dict1["月计划"]] != 0:
                            if math.floor(DictTimeCycle[Dict1["月计划"]] * 0.9) <= DeltaDays[ChoiceTrain - 1] < \
                                    DictTimeCycle[Dict1["月计划"]]:
                                r1 = random.random()
                                if r1 <= 0.2:
                                    TaskOfTrain.append(ChoiceTrain)
                                    Number1 += 1
                                    History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(
                                        Day.day)
                            elif DictTimeCycle[Dict1["月计划"]] <= DeltaDays[ChoiceTrain - 1] < math.ceil(
                                    DictTimeCycle[Dict1["月计划"]] * 1.1):
                                r1 = random.random()
                                if r1 <= 0.5:
                                    TaskOfTrain.append(ChoiceTrain)
                                    Number1 += 1
                                    History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(
                                        Day.day)
                            elif DeltaDays[ChoiceTrain - 1] == math.ceil(DictTimeCycle[Dict1["月计划"]] * 1.1):
                                TaskOfTrain.append(ChoiceTrain)
                                Number1 += 1
                                History_Data[ChoiceTrain - 1] = str(Day.year) + "-" + str(Day.month) + "-" + str(
                                    Day.day)
                            else:
                                break
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
                    fitness1 += math.ceil(DictTimeCycle[Dict1["月计划"]] * 1.1) - DeltaDaysList[i][t1 - 1]
            return fitness1

        def best(self):
            Maxgen = 100
            r21 = self.MonthPlan()
            r31 = self.Fitness(r21[0], r21[1])
            BestFitness = copy.deepcopy(r31)
            BestTrainList = copy.deepcopy(r21[0])
            for i in range(Maxgen):
                r2 = self.MonthPlan()
                r3 = self.Fitness(r2[0], r2[1])
                if r3 < BestFitness:
                    BestFitness = r3
                    BestTrainList = r2[0]
            TotalTaskList = []
            for d in range(Days):
                List2 = []
                for t in range(1, NumberOfTrain + 1):
                    if YearTaskList[d][t] != "" and t in BestTrainList[d]:  # 当列车当个计划日有登顶检和均衡修任务
                        List2.append(YearTaskList[d][t] + " + " + "登顶检")
                    elif YearTaskList[d][t] == "" and t in BestTrainList[d]:  # 当列车当个计划日有登顶检任务
                        List2.append("登顶检")
                    elif YearTaskList[d][t] != "" and t not in BestTrainList[d]:  # 当列车当个计划日有均衡修任务
                        List2.append(YearTaskList[d][t])
                    else:
                        List2.append("")
                TotalTaskList.append(List2)
            return TotalTaskList

        def Import(self, TotalTaskList):
            scheduleId = "M1720210001"
            list1 = []
            Delta = datetime.timedelta(days=1)
            Dict01 = {"scheduleId": scheduleId, "trainId": "CD", "planDate": 2021, "duration": 2, "taskType": "登顶检",
                      "taskContent": "None", "applyMonth": "None"}
            Day1 = copy.deepcopy(Start_Time)
            P1 = 0
            while Day1 < End_Time:
                P1 += 1
                for t in range(NumberOfTrain):
                    if TotalTaskList[P1 - 1][t] != "":
                        Task1 = TotalTaskList[P1 - 1][t]
                        if t < 9:
                            Train1 = "CD" + "1700" + str(t + 1)
                        else:
                            Train1 = "CD" + "170" + str(t + 1)
                        if "Y" in Task1:  # 当日当列车有检修任务
                            Dict01["trainId"] = Train1
                            Dict01["planDate"] = str(Day1.year) + "-" + str(Day1.month) + "-" + str(Day1.day)
                            str1 = Task1.split("Y")
                            DeltaDays = Dict2[str1[1]][1]  # 该种检修任务的持续时间
                            Start_Time1 = 0
                            if P1 + DeltaDays - 1 > Days:
                                Dict01["duration"] = DeltaDays
                                Dict01["taskContent"] = Task1
                                Dict01["taskType"] = Dict1["年计划"]
                                Dict11 = copy.deepcopy(Dict01)
                                Dict01["applyMonth"] = "None"
                                list1.append(Dict11)
                            else:
                                for j in range(P1 + DeltaDays - 1, 0, -1):
                                    if "Y" in TotalTaskList[j - 1][t]:
                                        Start_Time1 = j
                                        break
                                Day2 = 0  # 计划内容中该检修任务的连续时间
                                for j in range(Start_Time1, 0, -1):
                                    if "Y" in TotalTaskList[j - 1][t]:
                                        Day2 += 1
                                    else:
                                        break
                                if Day2 == DeltaDays:  # 说明该检修任务全部安排正在计划周期内
                                    # 需要判断这是该检修任务的第几个计划日的任务，只记录首个计划日的信息
                                    Start_Time2 = 0  # 记录该检修任务开始的时间
                                    if P1 < 3:
                                        for k2 in range(0, P1 + 3 - 1):
                                            if "Y" in TotalTaskList[k2][t]:
                                                Start_Time2 = k2 + 1
                                                break
                                    else:
                                        for k2 in range(P1 - 2, P1 + 2):
                                            if "Y" in TotalTaskList[k2 - 1][t]:
                                                Start_Time2 = k2
                                                break
                                    if Start_Time2 == P1:  # 这是该检修任务的首个计划日
                                        Dict01["duration"] = DeltaDays
                                        Dict01["taskContent"] = Task1
                                        Dict01["taskType"] = Dict1["年计划"]
                                        Dict11 = copy.deepcopy(Dict01)
                                        Dict01["applyMonth"] = "None"
                                        list1.append(Dict11)
                        else:
                            Dict01["trainId"] = Train1
                            Dict01["planDate"] = str(Day1.year) + "-" + str(Day1.month) + "-" + str(Day1.day)
                            Dict01["duration"] = Dict3[Dict1["月计划"]][1]
                            Dict01["taskContent"] = Dict1["月计划"]
                            Dict01["taskType"] = Dict1["月计划"]
                            Dict11 = copy.deepcopy(Dict01)
                            Dict01["applyMonth"] = "None"
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

    result = MonthPlanning1(NumberOfTrain, TypeOfRepair, DictTimeCycle)
    r1 = result.best()
    result.Import(r1)

if __name__ == '__main__':
    generate_month(17)