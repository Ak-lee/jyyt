import copy
import datetime
import requests
import json
import numpy as np
from chinese_calendar import is_workday

def generate_day(LineId, TodayDate1):
    p1 = "http://sunjc.top:8880/"
    # LineId = 17
    p0 = "train/table/"
    p0 = p0 + str(LineId)
    url = p1 + p0
    r = requests.get(url=url)
    a = json.loads(r.text)

    p2 = "schedule/infoone/"
    DailyId = "D1720220151"
    p2 = p2 + DailyId
    url = p1 + p2 + DailyId
    r = requests.get(url=url)
    a1 = json.loads(r.text)

    TodayDate = datetime.datetime.strptime(TodayDate1, "%Y-%m-%d")
    YearOfToday = TodayDate.year
    MonthOfToday = TodayDate.month
    DayOfToday = TodayDate.day
    StrDate = str(YearOfToday) + "-" + str(MonthOfToday) + "-" + str(DayOfToday)

    p12 = "line/byLineId?lineId="
    url1 = p1 + p12 + str(LineId)
    r = requests.get(url=url1)
    a0 = json.loads(r.text)
    NumberOfTrain = a0['data'].get("trainNum")

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
    TypeOfRepair.append("季节检")
    LengthCycle.append(0)
    TimeCycle.append(0)
    DictLength = {TypeOfRepair[i]: LengthCycle[i] for i in range(len(TypeOfRepair))}  # 检修任务对应的里程周期
    DictTime = {TypeOfRepair[i]: TimeCycle[i] for i in range(len(TypeOfRepair))}  # 检修任务对应的时间周期

    p9 = "schedule_content_history/lastDayRepair?lineId=17"  # 该日期是最近检修任务的开始时间，而算法需要的是结束时间
    url = p1 + p9
    r = requests.get(url=url)
    a = json.loads(r.text)
    History_Data = []
    RepairTask1 = []
    delta = datetime.timedelta(days=1)
    for i in range(len(a['data'].keys())):
        List1 = []
        Type1 = list(a['data'].keys())[i]
        EndDate = 0  # 避免重复搜索
        List13 = []
        for c in range(1, NumberOfTrain + 1):
            List12 = []
            if c < 10:
                ID1 = "CD" + str(LineId) + "00" + str(c)
            else:
                ID1 = "CD" + str(LineId) + "0" + str(c)
            for j in range(EndDate, len(a['data'][Type1])):
                if a['data'][Type1][j]['trainId'] == ID1:
                    List12.append(j)
                else:
                    break
            start1 = datetime.datetime.strptime(a['data'].get(Type1)[List12[len(List12) - 1]]['performDate'],
                                                '%Y-%m-%d')
            DeltaDays = a['data'].get(Type1)[List12[len(List12) - 1]]['duration']
            List13.append(a['data'].get(Type1)[List12[len(List12) - 1]]['taskContent'])
            if DeltaDays > 1:
                for j in range(DeltaDays - 1):
                    start1 += delta
            List1.append(str(start1.year) + "-" + str(start1.month) + "-" + str(start1.day))
            EndDate = List12[len(List12) - 1] + 1
        History_Data.append(List1)
        RepairTask1.append(List13)
    History_Data.append([])  # 季节专检没有数据
    RepairTask1 = RepairTask1[2]

    p10 = "yardTasktype/byYard?yardId=CDCS"
    url = p1 + p10
    r = requests.get(url=url)
    a = json.loads(r.text)
    RepairModel = []
    for i in range(len(TypeOfRepair)):
        for j in range(len(a['data'])):
            if a['data'][j]["taskTypeName"] == TypeOfRepair[i]:
                List1 = []
                if len(a['data'][j]['list']) == 1:
                    List1.append(a['data'][j]['list'][0]["requireDay"])
                    List1.append(a['data'][j]['list'][0]["requireHour"])
                    List1.append(a['data'][j]['list'][0]["requireHeadcount"])
                    RepairModel.append(List1)
                else:
                    RepairModel.append(List1)
                break
    Dict1 = {TypeOfRepair[i]: RepairModel[i] for i in range(len(TypeOfRepair))}

    p11 = "yardTasktype/byYardIdAndTasktypeId?yardId=CDCS&taskTypeId=3"
    url = p1 + p11
    r = requests.get(url=url)
    a = json.loads(r.text)
    RepairModel1 = []
    List2 = []  # 记录每种检修修程的ID
    for i in range(len(a['data']['list'])):
        List2.append(a['data']['list'][i]['id'])
        List1 = []
        List1.append(a['data']['list'][i]["requireDay"])
        List1.append(a['data']['list'][i]["requireHour"])
        List1.append(a['data']['list'][i]["requireHeadcount"])
        RepairModel1.append(List1)

    p12 = "applyMonth/table?tasktypeId=3&yardId=CDCS"
    url = p1 + p12
    r = requests.get(url=url)
    a = json.loads(r.text)
    MonthList = []
    for j in range(len(List2)):
        List1 = []
        for i in range(len(a['data'])):
            if a['data'][i]['tasktypeModeId'] == List2[j]:
                List1.append(str(a['data'][i]['applyMonth']))
        MonthList.append(List1)
    for i in range(len(MonthList)):
        for j in range(len(MonthList[i])):
            month1 = MonthList[i][j]
            num1 = 0
            p01 = []
            p02 = []
            for j1 in range(i + 1, len(MonthList)):
                for k in range(len(MonthList[j1])):
                    if month1 == MonthList[j1][k]:
                        num1 += 1
                        p01.append(j1)
                        p02.append(k)
            if num1 == 1:
                MonthList[i][j] = MonthList[i][j] + "A"
                MonthList[p01[0]][p02[0]] = MonthList[p01[0]][p02[0]] + "B"

    TaskOfWeekend = []
    PositionOfWeekend = []
    TaskOfWorkday = []
    PositionOfWorkday = []
    p13 = "transplan/getTransPlan?lineId=17&applicableTime=workday&curPage=1&size=15"
    url = p1 + p13
    r = requests.get(url=url)
    a = json.loads(r.text)
    for i in range(len(a['data']['records'])):
        TaskOfWorkday.append(str(a['data']['records'][i]["undercarId"]))
        PositionOfWorkday.append(a['data']['records'][i]["instorageSite"])

    p14 = "transplan/getTransPlan?lineId=17&applicableTime=weekday&curPage=1&size=15"
    url = p1 + p14
    r = requests.get(url=url)
    a = json.loads(r.text)
    for i in range(len(a['data']['records'])):
        TaskOfWeekend.append(str(a['data']['records'][i]["undercarId"]))
        PositionOfWeekend.append(a['data']['records'][i]["instorageSite"])

    p15 = "yard/list?lineId=1"
    url = p1 + p15
    r = requests.get(url=url)
    a = json.loads(r.text)
    RepairCheKu = []
    IDRepairCheKu = []  # 车库的ID
    TypeOfBanZu1 = []
    for i in range(len(a['data'])):
        IDRepairCheKu.append(a['data'][i]["id"])
        List1 = []
        RepairCheKu.append(a['data'][i]["name"])
        p16 = "yardteam/table?yardId=" + a['data'][i]['id']
        url = p1 + p16
        r = requests.get(url=url)
        a1 = json.loads(r.text)
        for i in range(len(a1['data'])):
            List1.append(a1['data'][i]["teamType"])
        TypeOfBanZu1.append(List1)
    DictCheKuAndBanZu = {RepairCheKu[i]: TypeOfBanZu1[i] for i in range(len(RepairCheKu))}

    CanRepairTask = []
    for i in range(len(RepairCheKu)):
        p20 = "yardTasktype/byYard?yardId=" + IDRepairCheKu[i]
        url = p1 + p20
        r = requests.get(url=url)
        a = json.loads(r.text)
        List1 = []
        for i in range(len(a['data'])):
            List1.append(a['data'][i]["taskTypeName"])
        CanRepairTask.append(List1)
    DictOfPositionAndRepair = {RepairCheKu[i]: CanRepairTask[i] for i in range(len(RepairCheKu))}

    IndexList = ["配属班组", "适用检修作业", "工作时间", "白班开始时间", "白班结束时间", "夜班开始时间", "夜班结束时间"]

    NumberOfLine = []  # 股道数量
    for p0 in IDRepairCheKu:
        way1 = "yard/info/" + p0
        url = p1 + way1
        r = requests.get(url=url)
        a = json.loads(r.text)
        List1 = []
        List1.append(a['data']['serviceShopTrackwayNum'])
        List1.append(a['data']['operationShopTrackwayNum'])
        NumberOfLine.append(List1)
    TypeOfBanZu1 = []
    NumberOfBanZu1 = []
    TeamId = []
    for p0 in IDRepairCheKu:
        way1 = "yardteam/table?yardId=" + p0
        url = p1 + way1
        r = requests.get(url=url)
        a = json.loads(r.text)
        List1 = []
        List3 = []
        List4 = []
        for j in range(len(a['data'])):
            List1.append(a['data'][j]['teamType'])
            List3.append(a['data'][j]['num'])
            List4.append(a['data'][j]['teamId'])
        TypeOfBanZu1.append(List1)
        NumberOfBanZu1.append(List3)
        TeamId.append(List4)

    TypeOfBanZu = []
    RepairOfBanZu = []
    NumberOfBanZu = []
    url = p1 + "team/tableall"
    r = requests.get(url=url)
    a = json.loads(r.text)
    for i in range(len(a['data'])):
        NumberOfBanZu.append(a['data'][i]['staffNum'])
        TypeOfBanZu.append(a['data'][i]['teamType'])
        List1 = []
        task1 = a['data'][i]['skills']
        task2 = task1.split("+")
        for t in task2:
            List1.append(t)
        RepairOfBanZu.append(List1)

    RepairList = []
    TrainList = []
    url = p1 + "schedule_content/getListByLineIdAndDate?lineId=17&date=2021-09-22"
    r = requests.get(url=url)
    a = json.loads(r.text)
    for train in range(20):
        if train < 9:
            train1 = "CD" + str(LineId) + "00" + str(train + 1)
        else:
            train1 = "CD" + str(LineId) + "0" + str(train + 1)
        List1 = []
        for i in range(len(a['data'])):
            if a['data'][i]["trainId"] == train1:
                TrainList.append(train + 1)
                if a['data'][i]["taskContent"] is not None:
                    List1.append(a['data'][i]["taskContent"])
                else:
                    List1.append(a['data'][i]["taskType"])
        TotalTask = 0
        if len(List1) == 1:
            TotalTask = List1[0]
        elif len(List1) > 1:
            TotalTask = List1[0]
            for i in range(1, len(List1)):
                TotalTask = TotalTask + "+" + List1[i]
        if TotalTask != 0:
            RepairList.append(TotalTask)
    TrainList = list(set(TrainList))

    ContentOfCheKu = []
    TaskList = []
    BanZhiList = []

    for i in IDRepairCheKu:
        url = p1 + "yardTasktype/byYard?yardId=" + i
        r = requests.get(url=url)
        a = json.loads(r.text)
        List1 = []
        for i1 in range(len(a['data'])):
            List1.append(a['data'][i1]['taskTypeName'])
        TaskList.append(List1)
        url1 = p1 + "shifts/table?yardId=" + i
        r1 = requests.get(url=url1)
        a1 = json.loads(r1.text)
        List2 = []
        for j in range(len(a1['data'])):
            if a1['data'][j].get("type") == "白班":
                List2.append(a1['data'][j]['beginTime'])
                List2.append(a1['data'][j]['endTime'])
                break
        for j in range(len(a1['data'])):
            if a1['data'][j].get("type") == "夜班":
                List2.append(a1['data'][j]['beginTime'])
                List2.append(a1['data'][j]['endTime'])
                break
        BanZhiList.append(List2)

    p18 = "yardTasktype/byYard?yardId=CDCS"  # 车场信息
    url = p1 + p18
    r = requests.get(url=url)
    a = json.loads(r.text)
    List14 = []  # 检修任务类型
    List15 = []  # 对应检修任务ID
    for i in range(len(a['data'])):
        List14.append(a['data'][i]["taskTypeName"])
        List15.append(a['data'][i]["taskTypeId"])
    IdOfRepair = {List14[i]: List15[i] for i in range(len(List14))}
    for i in range(len(RepairCheKu)):
        if len(TypeOfBanZu1[i]) != 0:
            List1 = []
            if len(NumberOfBanZu1[i]) == 1:
                List1.append(str(NumberOfBanZu1[i][0]))
            elif len(NumberOfBanZu1[i]) > 1:
                str1 = str(NumberOfBanZu1[i][0])
                for j in range(1, len(NumberOfBanZu1[i])):
                    str1 = str1 + "+" + str(NumberOfBanZu1[i][j])
                List1.append(str1)
            if len(TaskList[i]) == 1:
                List1.append(TaskList[i][0])
            else:
                str2 = TaskList[i][0]
                for t1 in range(1, len(TaskList[i])):
                    str2 = str2 + "+" + TaskList[i][t1]
                List1.append(str2)

            CanRepairList = TaskList[i]
            str3 = []
            for r1 in CanRepairList:
                Id1 = IdOfRepair[r1]  # 获取检修任务的ID
                url1 = p1 + "shifts/tableByYardIdAndTasktypeId?yardId=" + IDRepairCheKu[i] + "&taskTypeId=" + str(Id1)
                r1 = requests.get(url=url1)
                a1 = json.loads(r1.text)
                str3.append(a1['data']["type"])
            str4 = str3[0]
            for k1 in range(1, len(str3)):
                str4 = str4 + "+" + str3[k1]
            List1.append(str4)
            if len(BanZhiList[i]) == 0:
                List1.append([])
            else:
                for k in range(4):
                    List1.append(BanZhiList[i][k])
            ContentOfCheKu.append(List1)
        else:
            ContentOfCheKu.append([])

    # 上一日的日计划内容
    TaskListOfTrain = []
    PositionOfWork = []
    PositionOfReturn = []
    Date1 = copy.deepcopy(TodayDate)
    Date1 = Date1 - delta
    p03 = "dayPlanHistory?lineId=" + str(LineId) + "&date=" + str(Date1.year) + "-" + str(Date1.month) + "-" + str(
        Date1.day)
    # p03 = "dayPlanHistory?lineId=17&date=2022-03-05"
    url1 = p1 + p03
    r1 = requests.get(url=url1)
    a1 = json.loads(r1.text)
    for i in range(NumberOfTrain):
        if a1['data'][i]["lastUndercarId"] is not None:
            TaskListOfTrain.append(a1['data'][i]["lastUndercarId"])
        else:
            TaskListOfTrain.append("")
        if a1['data'][i]["workYard"] is not None:
            PositionOfWork.append(a1['data'][i]["workYard"])
        else:
            PositionOfWork.append("")
        if a1['data'][i]["backYard"] is not None:
            PositionOfReturn.append(a1['data'][i]["backYard"])
        else:
            PositionOfReturn.append("")

    RepairPosition1 = []  # 车场中每种检修任务可用的检修地点
    for i in range(len(IDRepairCheKu)):
        List02 = []
        for j in CanRepairTask[i]:
            id1 = IdOfRepair[j]
            p23 = "yardShopTasktypes?yardId=" + IDRepairCheKu[i] + "&tasktypeId=" + str(id1)
            url = p1 + p23
            r = requests.get(url=url)
            a = json.loads(r.text)
            if a['data'] is not None:
                Position1 = a['data']["shopNameString"]  # eg:"检修库,运用库"
                if "," in Position1:
                    str01 = Position1.split(",")
                    P1 = str01[0]
                    for k in range(1, len(str01)):
                        P1 = P1 + "+" + str01[k]
                    List02.append(P1)
                else:
                    List02.append(Position1)
        RepairPosition1.append(List02)

    TotalRepairList = []
    for i in range(7):
        List02 = []
        for j in range(NumberOfTrain):
            List02.append("")
        TotalRepairList.append(List02)
    Date1 = copy.deepcopy(TodayDate)
    for i in range(7):
        Date1 -= delta
    Date2 = TodayDate - delta

    date1 = str(Date1.year) + "-" + str(Date1.month) + "-" + str(Date1.day)
    date2 = str(Date2.year) + "-" + str(Date2.month) + "-" + str(Date2.day)
    p06 = "schedule_content_history/tableWithCond?lineId=" + str(LineId) + "&planTypes=年计划&planTypes=月计划&planTypes=周计划&sdate=" + date1 + "&edate=" + date2
    url1 = p1 + p06
    r1 = requests.get(url=url1)
    a = json.loads(r1.text)
    for i in range(NumberOfTrain):
        NowDate = copy.deepcopy(Date1)
        if i < 9:
            Train1 = "CD" + str(LineId) + "00" + str(i + 1)
        else:
            Train1 = "CD" + str(LineId) + "0" + str(i + 1)
        for j in range(len(a['list'])):
            if a['list'][j]["trainId"] == Train1:
                Date3 = a['list'][j]["performDate"]
                Date4 = 0
                Index1 = 0  # 记录该检修任务的开始时间的索引
                for k1 in range(7):
                    if k1 == 0:
                        Date4 = NowDate
                    else:
                        Date4 = Date4 + delta
                    if Date4 == datetime.datetime.strptime(Date3, '%Y-%m-%d'):
                        Index1 = k1
                        break
                Duration = a['list'][j]["duration"]
                Content1 = 0
                if a['list'][j]["taskContent"] is None:
                    Content1 = a['list'][j]["taskType"]
                else:
                    Content1 = a['list'][j]["taskContent"]
                Index2 = copy.deepcopy(Index1) + 1
                for k2 in range(Duration - 1):
                    Index2 += 1
                if Index2 > 7:  # 检修任务的内容会超过7天的范畴
                    for k3 in range(Index1, 7):
                        if TotalRepairList[k3][i] == "":
                            TotalRepairList[k3][i] = str(Content1)
                        else:  # 当天当辆车安排有检修任务了
                            TotalRepairList[k3][i] = TotalRepairList[k3][i] + "+" + str(Content1)
                else:
                    for k3 in range(Index1, Index2):
                        if TotalRepairList[k3][i] == "":
                            TotalRepairList[k3][i] = str(Content1)
                        else:  # 当天当辆车安排有检修任务了
                            TotalRepairList[k3][i] = TotalRepairList[k3][i] + "+" + str(Content1)

    LengthOfLastWeek = [[], [], [], [], [], [], []]
    # 首先获得开始时间和结束时间
    Start1 = TodayDate
    End1 = TodayDate - delta
    for i in range(7):
        Start1 = Start1 - delta
    for i in range(7):
        List01 = []
        for j in range(NumberOfTrain):
            if i < 9:
                ID = "CD" + "1700" + str(i + 1)
            else:
                ID = "CD" + "170" + str(i + 1)
            NowDate = str(Start1.year) + "-" + str(Start1.month) + "-" + str(Start1.day)
            p24 = "mileage_history/getByTrainIdAndDate?trainId=" + ID + "&date=" + NowDate
            url = p1 + p24
            r = requests.get(url=url)
            a = json.loads(r.text)
            Length1 = a['data'].get("mileage")
            List01.append(Length1)
        LengthOfLastWeek[i] = List01
        Start1 += delta

    Time1 = datetime.date(TodayDate.year, TodayDate.month, TodayDate.day)
    number1 = Time1.weekday()
    TypeOfDay = 0
    if number1 == 6 or number1 == 7:  # 周末
        TypeOfDay = "weekend"
    else:
        TypeOfDay = "workday"
    p05 = "hotBackupTrain/getItem?lineId=" + str(LineId) + "&applicableTime=" + TypeOfDay
    url1 = p1 + p05
    r1 = requests.get(url=url1)
    a2 = json.loads(r1.text)
    Number1 = a2['data']["hotBackupTrainNum"]  # 热备任务数量

    p21 = "transplan/getTransPlan2?lineId=" + str(LineId) + "&applicableTime=" + TypeOfDay
    url1 = p1 + p21
    r1 = requests.get(url=url1)
    a1 = json.loads(r1.text)
    Number2 = 0  # 当计划日平峰任务数量
    for i in range(len(a1['data'])):
        InTime1 = a1['data'][i]["inyardTime"]
        OutTime1 = a1['data'][i]["outyardTime"]
        InTime = datetime.datetime.strptime(InTime1, '%H:%M:%S')
        OutTime = datetime.datetime.strptime(OutTime1, '%H:%M:%S')
        # 判断这个任务是否满足平峰任务的要求
        Date1 = datetime.datetime.strptime("18:00:00", '%H:%M:%S')
        Date2 = datetime.datetime.strptime("12:00:00", '%H:%M:%S')
        if (Date2 - OutTime).seconds > 0 and (InTime - Date1).seconds > 0:
            Number2 += 1

    class DailyPlanning:
        def DailyPlan(self):
            DictOfRepairType = []  # 多修程的检修任务类型
            for i in range(len(TypeOfRepair)):
                if len(Dict1[TypeOfRepair[i]]) == 0:  # 多修程的检修任务
                    DictOfRepairType.append(TypeOfRepair[i])
            if bool(True) == is_workday(datetime.date(YearOfToday, MonthOfToday, DayOfToday)):  # 工作日
                TaskList = copy.deepcopy(TaskOfWorkday)
                PositionOfRuKu = copy.deepcopy(PositionOfWorkday)
            else:
                TaskList = copy.deepcopy(TaskOfWeekend)
                PositionOfRuKu = copy.deepcopy(PositionOfWeekend)
            PositionOfLastDay = []  # 该计划日所有有检修任务的列车在上一日的停车地点
            for t1 in TrainList:
                if PositionOfWork[t1 - 1] == "" and PositionOfReturn[t1 - 1] == "":
                    str1 = TaskListOfTrain[t1 - 1]
                    if "/" in str1:
                        List3 = str1.split("/")
                        Str1 = List3[len(List3) - 1]
                        Str3 = Str1.split("次")[0]
                    else:
                        Str3 = str1.split("次")[0]
                    p1 = np.where(np.array(TaskList) == Str3)
                    PositionOfLastDay.append(PositionOfRuKu[p1[0][0]])
                elif PositionOfWork[t1 - 1] != "" and PositionOfReturn[t1 - 1] == "":
                    PositionOfLastDay.append(PositionOfWork[t1 - 1])
                elif PositionOfWork[t1 - 1] == "" and PositionOfReturn[t1 - 1] != "":
                    PositionOfLastDay.append(PositionOfReturn[t1 - 1])

            PositionOfToday = []
            CheOfToday = []
            for i in RepairCheKu:
                PositionOfToday.append([])
                CheOfToday.append([])
            Dict2 = {RepairCheKu[i]: PositionOfToday[i] for i in range(len(RepairCheKu))}
            Dict3 = {RepairCheKu[i]: CheOfToday[i] for i in range(len(RepairCheKu))}
            for che1 in range(len(TrainList)):
                RepairTask = RepairList[che1]
                RepairPosition = PositionOfLastDay[che1]
                # 判断前一计划日列车所停车场是否能够进行为其在该计划日所安排的检修任务
                if "+" in RepairTask:  # 多个检修任务组合
                    List4 = RepairTask.split("+")
                    Number1 = 0
                    for task1 in List4:
                        if task1 in DictOfPositionAndRepair[RepairPosition]:
                            Number1 += 1
                    if Number1 == len(List4):  # 该车场可以进行所有的检修任务
                        Dict2[RepairPosition].append(RepairTask)
                        Dict3[RepairPosition].append(TrainList[che1])
                    else:
                        AnotherPosition = 0
                        if len(RepairCheKu) > 1:
                            for p2 in RepairCheKu:
                                if p2 != RepairPosition:
                                    AnotherPosition = p2
                        Dict2[AnotherPosition].append(RepairTask)
                        Dict3[AnotherPosition].append(TrainList[che1])
                else:
                    if "Y" in RepairTask:
                        if "均衡修" in DictOfPositionAndRepair[RepairPosition]:
                            Dict2[RepairPosition].append(RepairTask)
                            Dict3[RepairPosition].append(TrainList[che1])
                    else:
                        if RepairTask in DictOfPositionAndRepair[RepairPosition]:
                            Dict2[RepairPosition].append(RepairTask)
                            Dict3[RepairPosition].append(TrainList[che1])
                        else:
                            AnotherPosition = 0
                            if len(RepairCheKu) > 1:
                                for p2 in RepairCheKu:
                                    if p2 != RepairPosition:
                                        AnotherPosition = p2
                            Dict2[AnotherPosition].append(RepairTask)
                            Dict3[AnotherPosition].append(TrainList[che1])
            TimeStartList = []  # 记录检修任务安排的时间点(同一车场的不同的检修任务）
            TimeEndList = []
            PositionList = []  # 记录检修任务安排的车场
            WorkerList = []  # 检修任务的班组安排记录结果
            TotalCheList00 = []
            TotalCheList01 = []
            TotalTaskList10 = []
            for p1 in RepairCheKu:
                BanZuList = DictCheKuAndBanZu[p1]  # 检修班组类型
                NumberOfBanZu = []  # 检修班组的数量
                TotalCheList010 = []
                TotalTaskList11 = []
                p2 = np.where(np.array(RepairCheKu) == p1)
                str2 = ContentOfCheKu[p2[0][0]][0]
                if "+" in str2:
                    str3 = str2.split("+")
                    for k1 in str3:
                        NumberOfBanZu.append(int(k1))
                else:
                    NumberOfBanZu.append(int(str2))
                NumberOfLine1 = copy.deepcopy(NumberOfLine[p2[0][0]])  # 车场检修股道资源 eg:[7, 17]
                NumberOfLine2 = copy.deepcopy(NumberOfLine1)
                Dict5 = {BanZuList[i]: NumberOfBanZu[i] for i in range(len(BanZuList))}
                Dict51 = copy.deepcopy(Dict5)
                Dict6 = {BanZuList[i]: RepairOfBanZu[i] for i in range(len(BanZuList))}
                TimeStartList1 = []  # 记录检修任务安排的时间点（分属于不同的列车的同一种检修任务）
                TimeEndList1 = []
                PositionList1 = []  # 记录检修任务安排的车场
                WorkerList1 = []  # 检修任务的班组安排记录结果

                TotalEndTimeList = []
                TotalPositionList = []
                TotalWorkerList = []
                TotalTaskList = []
                TotalTrainList = []
                RepairListOfPosition = Dict2[p1]  # 该车场所有的检修作业
                TrainListOfPosition = Dict3[p1]
                RepairListOfPosition1 = copy.deepcopy(RepairListOfPosition)
                TrainListOfPosition1 = copy.deepcopy(TrainListOfPosition)
                RepairListOfRepairType = []  # 不同级别的检修任务组合
                CheListOfRepairType = []
                for i in range(len(TypeOfRepair)):
                    RepairListOfRepairType.append([])
                    CheListOfRepairType.append([])
                for t1 in range(len(TypeOfRepair)):
                    ChoiceTask = TypeOfRepair[len(TypeOfRepair) - t1 - 1]
                    for t2 in range(len(RepairListOfPosition1)):
                        if ChoiceTask == "均衡修":
                            if "Y" in RepairListOfPosition1[t2]:
                                RepairListOfRepairType[t1].append(RepairListOfPosition1[t2])
                                CheListOfRepairType[t1].append(TrainListOfPosition1[t2])
                        else:
                            if ChoiceTask in RepairListOfPosition1[t2]:
                                RepairListOfRepairType[t1].append(RepairListOfPosition1[t2])
                                CheListOfRepairType[t1].append(TrainListOfPosition1[t2])
                    if len(RepairListOfRepairType[t1]) != 0:
                        for t3 in range(len(RepairListOfRepairType[t1])):
                            RepairListOfPosition1.remove(RepairListOfRepairType[t1][t3])
                            TrainListOfPosition1.remove(CheListOfRepairType[t1][t3])
                p2 = np.where(np.array(RepairCheKu) == p1)
                StartDayTime = ContentOfCheKu[p2[0][0]][3]
                EndDayTime = ContentOfCheKu[p2[0][0]][4]
                StartNightTime = ContentOfCheKu[p2[0][0]][5]
                EndNightTime = ContentOfCheKu[p2[0][0]][6]
                str4 = ContentOfCheKu[p2[0][0]][1]
                str5 = ContentOfCheKu[p2[0][0]][2]
                RepairType = str4.split("+")
                RepairTime = str5.split("+")
                StartDayTime1 = StrDate + " " + str(StartDayTime)
                StartNightTime1 = StrDate + " " + str(StartNightTime)
                Dict4 = {RepairType[i]: RepairTime[i] for i in range(len(RepairType))}
                for n1 in range(len(RepairListOfRepairType)):
                    NowRepairType = TypeOfRepair[len(TypeOfRepair) - n1 - 1]
                    if len(RepairListOfRepairType[n1]) != 0:
                        ListOfType1 = RepairListOfRepairType[n1]
                        ListOfType1 = RepairListOfRepairType[n1]
                        CheOfType1 = CheListOfRepairType[n1]
                        ChoiceTask1 = TypeOfRepair[len(TypeOfRepair) - n1 - 1]

                        List11 = []  # 记录累计时间
                        List12 = []  # 记录累计里程

                        for che2 in CheOfType1:
                            List10 = []
                            p3 = np.where(np.array(TypeOfRepair) == ChoiceTask1)
                            List11.append((datetime.datetime.strptime(
                                str(YearOfToday) + "-" + str(MonthOfToday) + "-" + str(DayOfToday),
                                '%Y-%m-%d') - datetime.datetime.strptime(History_Data[p3[0][0]][che2 - 1],
                                                                         '%Y-%m-%d')).days - 1)
                        # 然后根据累计时间数据进行检修任务的排序
                        QueueTaskList = []  # 排序后的运输任务集合
                        QueueTrainList = []  # 排序后的列车集合

                        List13 = copy.deepcopy(List11)
                        List14 = list(set(List13))
                        for t5 in List14:
                            p3 = np.where(np.array(List13) == t5)
                            if len(p3[0]) == 1:
                                QueueTaskList.append(ListOfType1[p3[0][0]])
                                QueueTrainList.append(CheOfType1[p3[0][0]])
                            else:  # 列车的累计时间相同，则需要根据服役年限的大小来确定检修任务进行的先后时间，即服役年限更大的列车更先进行检修任务
                                che1List = []
                                Task1List = []
                                YearOfTrain = []  # 先获取这些列车的服役年限的数据
                                for i in range(len(p3[0])):
                                    che1List.append(CheOfType1[p3[0][i]])
                                    Task1List.append(ListOfType1[p3[0][i]])
                                for che1 in che1List:
                                    str6 = RepairTask1[che1 - 1]  # 2Y4B/2Y3
                                    YearOfTrain.append(int(str6.split("Y")[0]))
                                YearOfTrain1 = copy.deepcopy(YearOfTrain)
                                List15 = list(set(YearOfTrain1))
                                for y in List15:
                                    p2 = np.where(np.array(YearOfTrain) == y)
                                    if len(p2[0]) == 1:
                                        QueueTaskList.append(Task1List[p2[0][0]])
                                        QueueTrainList.append(che1List[p2[0][0]])
                                    else:
                                        for i1 in range(len(p2[0])):
                                            QueueTaskList.append(Task1List[p2[0][i1]])
                                            QueueTrainList.append(che1List[p2[0][i1]])
                        List17 = []
                        List18 = []
                        for i4 in range(len(QueueTrainList)):
                            List17.append(QueueTrainList[len(QueueTrainList) - i4 - 1])
                            List18.append(QueueTaskList[len(QueueTaskList) - i4 - 1])
                        TotalCheList010.append(List17)
                        TotalTaskList11.append(List18)
                        BanZuOfRepairType = []  # 能执行该种检修任务的班组类型
                        for t2 in range(len(BanZuList)):
                            BanZu = BanZuList[len(BanZuList) - t2 - 1]
                            if NowRepairType in Dict6[BanZu]:
                                BanZuOfRepairType.append(BanZu)
                        if len(Dict1[NowRepairType]) == 0:  # 多修程检修任务
                            if len(BanZuOfRepairType) == 1:  # 执行该种检修任务的班组类型只有一种
                                NumberOfBanZu = Dict5[BanZuOfRepairType[0]]  # 检修班组的数量
                                if len(QueueTaskList) <= NumberOfBanZu:  # 检修班组的数量可以安排完所有的检修任务
                                    TimeStartList111 = []
                                    TimeEndList111 = []
                                    PositionList111 = []
                                    WorkerList111 = []
                                    if Dict4[NowRepairType] == "双班" or Dict4[NowRepairType] == "白班":  # 可以将检修任务安排在白班
                                        for i2 in range(len(QueueTaskList)):
                                            TimeStartList11 = []
                                            TimeEndList11 = []
                                            PositionList11 = []
                                            WorkerList11 = []
                                            ChoiceTask2 = QueueTaskList[
                                                len(QueueTaskList) - i2 - 1]  # 可能是单个检修任务或多个检修任务的组合
                                            ChoiceChe2 = QueueTrainList[len(QueueTrainList) - i2 - 1]
                                            TotalCheList00.append(ChoiceChe2)
                                            List21 = []
                                            if "+" in ChoiceTask2:
                                                ChoiceTask1 = ChoiceTask2.split("+")
                                                for task2 in ChoiceTask1:
                                                    List21.append(task2)
                                            else:
                                                List21.append(ChoiceTask2)
                                            TimeList1 = []  # 检修任务所需的时间和人员
                                            WorkerNumberList = []
                                            for task2 in List21:  # ["3Y4B", "登顶检"]
                                                TimeCostOfRepair = 0  # 该检修任务所需的检修耗时
                                                NumberOfWorker = 0  # 该检修任务所需的检修人员数量
                                                if "Y" in task2:
                                                    task3 = task2.split("Y")[1]  # eg: 4B
                                                    for k1 in range(len(MonthList)):
                                                        ModelList1 = MonthList[k1]
                                                        if task3 in ModelList1:
                                                            TimeCostOfRepair = RepairModel1[k1][1]
                                                            NumberOfWorker = RepairModel1[k1][2]
                                                            break
                                                    TimeList1.append(TimeCostOfRepair)
                                                    WorkerNumberList.append(NumberOfWorker)
                                                else:
                                                    p5 = np.where(np.array(TypeOfRepair) == task2)
                                                    TimeCostOfRepair = RepairModel[p5[0][0]][1]
                                                    NumberOfWorker = RepairModel[p5[0][0]][2]
                                                    TimeList1.append(TimeCostOfRepair)
                                                    WorkerNumberList.append(NumberOfWorker)
                                            for n in range(len(List21)):
                                                if n == 0:
                                                    TimeStartList11.append(
                                                        datetime.datetime.strptime(StartDayTime1, '%Y-%m-%d %H:%M:%S'))
                                                    EndDate = datetime.datetime.strptime(StartDayTime1,
                                                                                         '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
                                                        hours=TimeList1[n])
                                                    TimeEndList11.append(EndDate)
                                                    TotalEndTimeList.append(EndDate)
                                                    StrBanZu = BanZuOfRepairType[0] + str(i2 + 1)
                                                    WorkerList11.append(StrBanZu)
                                                    Dict5[BanZuOfRepairType[0]] = Dict5[BanZuOfRepairType[0]] - 1
                                                    p6 = np.where(np.array(RepairCheKu) == p1)
                                                    List22 = CanRepairTask[p6[0][0]]
                                                    p7 = np.where(np.array(List22) == "均衡修")
                                                    str4 = RepairPosition1[p6[0][0]][p7[0][0]]
                                                    if "+" in str4 or str4 == "检修库":
                                                        NumberOfLine1[0] = NumberOfLine1[0] - 1
                                                        if "Y" in List21[n]:
                                                            NumberOfLine2[0] = NumberOfLine2[0] - 1
                                                    else:
                                                        NumberOfLine1[1] = NumberOfLine1[1] - 1
                                                        if "Y" in List21[n]:
                                                            NumberOfLine2[1] = NumberOfLine2[1] - 1
                                                    TotalWorkerList.append(StrBanZu)
                                                    if "+" not in str4:
                                                        PositionList11.append(str4)
                                                        TotalPositionList.append(str4)
                                                else:
                                                    DeltaTime = TimeList1[n]
                                                    if (datetime.datetime.strptime(StrDate + " " + str(EndDayTime),
                                                                                   '%Y-%m-%d %H:%M:%S') - TimeEndList11[
                                                            n - 1]).seconds / 3600 < DeltaTime:  # 后续检修任务只能安排在夜班
                                                        TimeStartList11.append(datetime.datetime.strptime(
                                                            StrDate + " " + str(StartNightTime), '%Y-%m-%d %H:%M:%S'))
                                                        TimeEndList11.append(
                                                            TimeStartList11[n] + datetime.timedelta(hours=TimeList1[n]))
                                                        TotalEndTimeList.append(
                                                            TimeStartList11[n] + datetime.timedelta(hours=TimeList1[n]))
                                                    else:
                                                        TimeStartList11.append(TimeEndList11[n - 1])
                                                        TimeEndList11.append(
                                                            TimeStartList11[n] + datetime.timedelta(hours=TimeList1[n]))
                                                        TotalEndTimeList.append(
                                                            TimeStartList11[n] + datetime.timedelta(hours=TimeList1[n]))
                                                    if List21[n] in Dict6[BanZuOfRepairType[0]]:
                                                        WorkerList11.append(WorkerList11[0])
                                                        TotalWorkerList.append(WorkerList11[0])
                                                        PositionList11.append(PositionList11[0])
                                                        TotalPositionList.append(PositionList11[0])
                                            if len(PositionList11) == 1:
                                                T1 = str(TimeStartList11[0])
                                                T2 = str(TimeEndList11[0])
                                                P2 = str(PositionList11[0])
                                                W1 = str(WorkerList11[0])
                                            else:
                                                T1 = str(TimeStartList11[0])
                                                T2 = str(TimeEndList11[0])
                                                P2 = PositionList11[0]
                                                W1 = WorkerList11[0]
                                                for p1 in range(1, len(PositionList11)):
                                                    T1 = T1 + "+" + str(TimeStartList11[p1])
                                                    T2 = T2 + "+" + str(TimeEndList11[p1])
                                            TimeStartList111.append(T1)
                                            TimeEndList111.append(T2)
                                            PositionList111.append(P2)
                                            WorkerList111.append(W1)
                                        TimeStartList1.append(TimeStartList111)
                                        TimeEndList1.append(TimeEndList111)
                                        PositionList1.append(PositionList111)
                                        WorkerList1.append(WorkerList111)
                        else:  # 单修程检修任务
                            TimeStartList111 = []
                            TimeEndList111 = []
                            PositionList111 = []
                            WorkerList111 = []
                            if len(BanZuOfRepairType) == 1:  # 有一种检修班组可以执行该类型的检修任务
                                if Dict5[BanZuOfRepairType[0]] != 0:  # 均衡修任务安排完后，还有剩余的均衡修班组
                                    NumberOfBanZu1 = Dict5[BanZuOfRepairType[0]]  # 剩余的均衡修班组数量
                                    for n1 in range(len(QueueTaskList)):
                                        TimeStartList11 = []
                                        TimeEndList11 = []
                                        PositionList11 = []
                                        WorkerList11 = []
                                        TaskChoice = QueueTaskList[len(QueueTaskList) - n1 - 1]
                                        ChoiceChe2 = QueueTrainList[len(QueueTrainList) - n1 - 1]
                                        TotalCheList00.append(ChoiceChe2)
                                        List21 = []
                                        if "+" in TaskChoice:
                                            ChoiceTask1 = TaskChoice.split("+")
                                            for task2 in ChoiceTask1:
                                                List21.append(task2)
                                        else:
                                            List21.append(TaskChoice)
                                        TimeList1 = []  # 检修任务所需的时间
                                        for task2 in List21:
                                            TimeCostOfRepair = 0  # 该检修任务所需的检修耗时
                                            if "Y" in task2:
                                                task3 = task2.split("Y")[1]  # eg: 4B
                                                for k1 in range(len(MonthList)):
                                                    ModelList1 = MonthList[k1]  # eg:["1", "4A", "7", "10"]
                                                    if task3 in ModelList1:
                                                        TimeCostOfRepair = RepairModel1[k1][1]
                                                        break
                                                TimeList1.append(TimeCostOfRepair)
                                            else:
                                                p4 = np.where(np.array(TypeOfRepair) == task2)
                                                TimeCostOfRepair = RepairModel[p4[0][0]][1]
                                                TimeList1.append(TimeCostOfRepair)
                                        p2 = 0
                                        for n in range(len(List21)):
                                            if n == 0:
                                                if Dict51[BanZuOfRepairType[0]] == NumberOfBanZu1:  # 前一级检修任务没有内容
                                                    if Dict5[BanZuOfRepairType[0]] > 0:
                                                        if NumberOfLine1[0] != 0:  # 还有检修库股道
                                                            Start_Time1 = datetime.datetime.strptime(StartDayTime1,
                                                                                                     '%Y-%m-%d %H:%M:%S')
                                                            StrBanZu = BanZuOfRepairType[0] + str(n1 + 1)
                                                            Dict5[BanZuOfRepairType[0]] = Dict5[
                                                                                              BanZuOfRepairType[0]] - 1
                                                            StrPosition = "检修库"
                                                            NumberOfLine1[0] = NumberOfLine1[0] - 1
                                                            Model1 = Dict1[List21[n]]
                                                            if Model1[0] > 1:  # 多日检修任务
                                                                NumberOfLine2[0] = NumberOfLine2[0] - 1
                                                        else:
                                                            Start_Time1 = datetime.datetime.strptime(StartDayTime1,
                                                                                                     '%Y-%m-%d %H:%M:%S')
                                                            StrBanZu = BanZuOfRepairType[0] + str(n1 + 1)
                                                            Dict5[BanZuOfRepairType[0]] = Dict5[
                                                                                              BanZuOfRepairType[0]] - 1
                                                            StrPosition = "运用库"
                                                            NumberOfLine1[1] = NumberOfLine1[1] - 1
                                                            Model1 = Dict1[List21[n]]
                                                            if Model1[0] > 1:
                                                                NumberOfLine2[1] = NumberOfLine2[1] - 1
                                                    else:  # 班组已经全部安排完
                                                        if NumberOfLine1[0] != 0:  # 还有检修库股道
                                                            MinTime = TotalEndTimeList[0]  # 已经安排的检修任务中最早结束的检修任务的结束时间
                                                            p2 = 0
                                                            for p1 in range(1, len(TotalEndTimeList)):
                                                                if (TotalEndTimeList[p1] - MinTime).days < 0:
                                                                    MinTime = TotalEndTimeList[p1]
                                                                    p2 = p1
                                                            Start_Time1 = MinTime
                                                            StrBanZu = TotalWorkerList[p2]
                                                            StrPosition = "检修库"
                                                            NumberOfLine1[0] = NumberOfLine1[0] - 1
                                                            Model1 = Dict1[List21[n]]
                                                            if Model1[0] > 1:
                                                                NumberOfLine2[0] = NumberOfLine2[0] - 1
                                                        else:
                                                            MinTime = TotalEndTimeList[0]  # 已经安排的检修任务中最早结束的检修任务的结束时间
                                                            p2 = 0
                                                            for p1 in range(1, len(TotalEndTimeList)):
                                                                if (TotalEndTimeList[p1] - MinTime).days < 0:
                                                                    MinTime = TotalEndTimeList[p1]
                                                                    p2 = p1
                                                            Start_Time1 = MinTime
                                                            StrBanZu = TotalWorkerList[p2]
                                                            StrPosition = "运用库"
                                                            NumberOfLine1[1] = NumberOfLine1[1] - 1
                                                            Model1 = Dict1[List21[n]]
                                                            if Model1[0] > 1:
                                                                NumberOfLine2[1] = NumberOfLine2[1] - 1
                                                else:
                                                    if Dict5[BanZuOfRepairType[0]] > 0:  # 前一级检修任务后还有剩余的均衡修班组
                                                        if NumberOfLine1[0] != 0:  # 还有检修库股道
                                                            Start_Time1 = datetime.datetime.strptime(StartDayTime1,
                                                                                                     '%Y-%m-%d %H:%M:%S')
                                                            StrBanZu = BanZuOfRepairType[0] + str(
                                                                Dict51[BanZuOfRepairType[0]] - NumberOfBanZu1 + n1 + 1)
                                                            Dict5[BanZuOfRepairType[0]] = Dict5[
                                                                                              BanZuOfRepairType[0]] - 1
                                                            StrPosition = "检修库"
                                                            NumberOfLine1[0] = NumberOfLine1[0] - 1
                                                            Model1 = Dict1[List21[n]]
                                                            if Model1[0] > 1:
                                                                NumberOfLine2[0] = NumberOfLine2[0] - 1
                                                        else:
                                                            Start_Time1 = datetime.datetime.strptime(StartDayTime1,
                                                                                                     '%Y-%m-%d %H:%M:%S')
                                                            StrBanZu = BanZuOfRepairType[0] + str(
                                                                Dict51[BanZuOfRepairType[0]] - NumberOfBanZu1 + n1 + 1)
                                                            Dict5[BanZuOfRepairType[0]] = Dict5[
                                                                                              BanZuOfRepairType[0]] - 1
                                                            StrPosition = "运用库"
                                                            NumberOfLine1[1] = NumberOfLine1[1] - 1
                                                            Model1 = Dict1[List21[n]]
                                                            if Model1[1] > 1:
                                                                NumberOfLine2[1] = NumberOfLine2[1] - 1
                                                    else:
                                                        if NumberOfLine1[0] != 0:  # 还有检修库股道
                                                            MinTime = TotalEndTimeList[0]  # 已经安排的检修任务中最早结束的检修任务的结束时间
                                                            p2 = 0
                                                            for p1 in range(1, len(TotalEndTimeList)):
                                                                if (TotalEndTimeList[p1] - MinTime).days < 0:
                                                                    MinTime = TotalEndTimeList[p1]
                                                                    p2 = p1
                                                            Start_Time1 = MinTime
                                                            StrBanZu = TotalWorkerList[p2]
                                                            StrPosition = "检修库"
                                                            NumberOfLine1[0] = NumberOfLine1[0] - 1
                                                            Model1 = Dict1[List21[n]]
                                                            if Model1[0] > 1:
                                                                NumberOfLine2[0] = NumberOfLine2[0] - 1
                                                        else:
                                                            MinTime = TotalEndTimeList[0]  # 已经安排的检修任务中最早结束的检修任务的结束时间
                                                            p2 = 0
                                                            for p1 in range(1, len(TotalEndTimeList)):
                                                                if (TotalEndTimeList[p1] - MinTime).days < 0:
                                                                    MinTime = TotalEndTimeList[p1]
                                                                    p2 = p1
                                                            Start_Time1 = MinTime
                                                            StrBanZu = TotalWorkerList[p2]
                                                            StrPosition = "运用库"
                                                            NumberOfLine1[1] = NumberOfLine1[1] - 1
                                                            Model1 = Dict1[List21[n]]
                                                            if Model1[0] > 1:
                                                                NumberOfLine2[1] = NumberOfLine2[1] - 1
                                                TimeStartList11.append(Start_Time1)
                                                EndDate = Start_Time1 + datetime.timedelta(hours=TimeList1[n])
                                                TimeEndList11.append(EndDate)
                                                TotalEndTimeList.append(EndDate)
                                                WorkerList11.append(StrBanZu)
                                                TotalWorkerList.append(StrBanZu)
                                                PositionList11.append(StrPosition)
                                                TotalPositionList.append(StrPosition)
                                            else:
                                                TimeStartList11.append(TimeEndList11[n - 1])
                                                EndDate = TimeEndList11[n - 1] + datetime.timedelta(hours=TimeList1[n])
                                                TimeEndList11.append(EndDate)
                                                TotalEndTimeList.append(EndDate)
                                                WorkerList11.append(WorkerList11[n - 1])
                                                TotalWorkerList.append(WorkerList11[n - 1])
                                                PositionList11.append(PositionList11[n - 1])
                                                TotalPositionList.append(PositionList11[n - 1])
                                        if n1 >= NumberOfBanZu1:
                                            TotalEndTimeList[p2] = TimeEndList11[len(TimeEndList11) - 1]
                                            TotalWorkerList[p2] = WorkerList11[len(WorkerList11) - 1]
                                        if len(PositionList11) == 1:
                                            T1 = str(TimeStartList11[0])
                                            T2 = str(TimeEndList11[0])
                                            P2 = str(PositionList11[0])
                                            W1 = str(WorkerList11[0])
                                        else:
                                            T1 = str(TimeStartList11[0])
                                            T2 = str(TimeEndList11[0])
                                            P2 = PositionList11[0]
                                            W1 = WorkerList11[0]
                                            for p1 in range(1, len(PositionList11)):
                                                T1 = T1 + "+" + str(TimeStartList11[p1])
                                                T2 = T2 + "+" + str(TimeEndList11[p1])
                                        TimeStartList111.append(T1)
                                        TimeEndList111.append(T2)
                                        PositionList111.append(P2)
                                        WorkerList111.append(W1)
                                    TimeStartList1.append(TimeStartList111)
                                    TimeEndList1.append(TimeEndList111)
                                    PositionList1.append(PositionList111)
                                    WorkerList1.append(WorkerList111)
                                else:  # 均衡修任务安排完成后没有剩余的均衡修班组，只能有空闲的均衡修班组才能继续工作
                                    for n1 in range(len(QueueTaskList)):
                                        TimeStartList11 = []
                                        TimeEndList11 = []
                                        PositionList11 = []
                                        WorkerList11 = []
                                        TaskChoice = QueueTaskList[len(QueueTaskList) - n1 - 1]
                                        ChoiceChe2 = QueueTrainList[len(QueueTrainList) - n1 - 1]
                                        TotalCheList00.append(ChoiceChe2)
                                        List21 = []
                                        if "+" in TaskChoice:
                                            ChoiceTask1 = TaskChoice.split("+")
                                            for task2 in ChoiceTask1:
                                                List21.append(task2)
                                        else:
                                            List21.append(TaskChoice)
                                        TimeList1 = []  # 检修任务所需的时间
                                        for task2 in List21:  # ["登顶检", “里程检"]
                                            TimeCostOfRepair = 0  # 该检修任务所需的检修耗时
                                            if "Y" in task2:
                                                task3 = task2.split("Y")[1]  # eg: 4B
                                                for k1 in range(len(MonthList)):
                                                    ModelList1 = MonthList[k1]  # eg:["1", "4A", "7", "10"]
                                                    if task3 in ModelList1:
                                                        TimeCostOfRepair = RepairModel1[k1][1]
                                                        break
                                                TimeList1.append(TimeCostOfRepair)
                                            else:
                                                p4 = np.where(np.array(TypeOfRepair) == task2)
                                                TimeCostOfRepair = RepairModel[p4[0][0]][1]
                                                TimeList1.append(TimeCostOfRepair)
                                        MinTime = TotalEndTimeList[0]  # 已经安排的检修任务中最早结束的检修任务的结束时间
                                        p2 = 0
                                        for p1 in range(1, len(TotalEndTimeList)):
                                            if (TotalEndTimeList[p1] - MinTime).days < 0:
                                                MinTime = TotalEndTimeList[p1]
                                                p2 = p1
                                        for n in range(len(List21)):
                                            if n == 0:
                                                if NumberOfLine1[0] != 0:  # 还有检修库股道
                                                    StrPosition = "检修库"
                                                    NumberOfLine1[0] = NumberOfLine1[0] - 1
                                                    Model1 = Dict1[List21[n]]
                                                    if Model1[0] > 1:
                                                        NumberOfLine2[0] = NumberOfLine2[0] - 1
                                                else:
                                                    StrPosition = "运用库"
                                                    NumberOfLine1[1] = NumberOfLine1[1] - 1
                                                    Model1 = Dict1[List21[n]]
                                                    if Model1[0] > 1:
                                                        NumberOfLine2[1] = NumberOfLine2[1] - 1
                                                TimeStartList11.append(MinTime)
                                                EndDate = MinTime + datetime.timedelta(hours=TimeList1[n])
                                                TimeEndList11.append(EndDate)
                                                TotalEndTimeList.append(EndDate)
                                                WorkerList11.append(TotalWorkerList[p2])
                                                TotalWorkerList.append(TotalWorkerList[p2])
                                                PositionList11.append(StrPosition)
                                                TotalPositionList.append(StrPosition)
                                            else:
                                                TimeStartList11.append(TimeEndList11[n - 1])
                                                EndDate = TimeEndList11[n - 1] + datetime.timedelta(hours=TimeList1[n])
                                                TimeEndList11.append(EndDate)
                                                TotalEndTimeList.append(EndDate)
                                                WorkerList11.append(WorkerList11[n - 1])
                                                TotalWorkerList.append(WorkerList11[n - 1])
                                                PositionList11.append(PositionList11[n - 1])
                                                TotalPositionList.append(PositionList11[n - 1])
                                        TotalEndTimeList[p2] = TimeEndList11[len(TimeEndList11) - 1]
                                        TotalWorkerList[p2] = WorkerList11[len(WorkerList11) - 1]
                                        if len(PositionList11) == 1:
                                            T1 = str(TimeStartList11[0])
                                            T2 = str(TimeEndList11[0])
                                            P2 = str(PositionList11[0])
                                            W1 = str(WorkerList11[0])
                                        else:
                                            T1 = str(TimeStartList11[0])
                                            T2 = str(TimeEndList11[0])
                                            P2 = PositionList11[0]
                                            W1 = WorkerList11[0]
                                            for p1 in range(1, len(PositionList11)):
                                                T1 = T1 + "+" + str(TimeStartList11[p1])
                                                T2 = T2 + "+" + str(TimeEndList11[p1])
                                        TimeStartList111.append(T1)
                                        TimeEndList111.append(T2)
                                        PositionList111.append(P2)
                                        WorkerList111.append(W1)
                                    TimeStartList1.append(TimeStartList111)
                                    TimeEndList1.append(TimeEndList111)
                                    PositionList1.append(PositionList111)
                                    WorkerList1.append(WorkerList111)
                            else:  # 该种检修任务可有多种班组来执行
                                if Dict5[BanZuOfRepairType[1]] != 0:  # 前一级检修任务安排完后，还有剩余的均衡修班组
                                    Number10 = Dict5[BanZuOfRepairType[0]]  # 里程检班组数量
                                    Number11 = Dict5[BanZuOfRepairType[1]]  # 均衡修班组数量
                                    for n1 in range(len(QueueTaskList)):
                                        TimeStartList11 = []
                                        TimeEndList11 = []
                                        PositionList11 = []
                                        WorkerList11 = []
                                        TaskChoice = QueueTaskList[len(QueueTaskList) - n1 - 1]
                                        ChoiceChe2 = QueueTrainList[len(QueueTrainList) - n1 - 1]
                                        TotalCheList00.append(ChoiceChe2)
                                        List21 = []
                                        if "+" in TaskChoice:
                                            ChoiceTask1 = TaskChoice.split("+")
                                            # for task2 in ChoiceTask1:
                                            #     List21.append(task2)
                                            Position1 = []
                                            for t6 in ChoiceTask1:
                                                p1 = np.where(np.array(TypeOfRepair) == t6)
                                                Position1.append(p1[0][0])
                                            if Position1[0] > Position1[1]:
                                                List21.append(ChoiceTask1[0])
                                                List21.append(ChoiceTask1[1])
                                            else:
                                                List21.append(ChoiceTask1[1])
                                                List21.append(ChoiceTask1[0])
                                        else:
                                            List21.append(TaskChoice)
                                        TimeList1 = []  # 检修任务所需的时间
                                        for task2 in List21:  # ["登顶检", “里程检"]
                                            TimeCostOfRepair = 0  # 该检修任务所需的检修耗时
                                            if "Y" in task2:
                                                task3 = task2.split("Y")[1]  # eg: 4B
                                                for k1 in range(len(MonthList)):
                                                    ModelList1 = MonthList[k1]  # eg:["1", "4A", "7", "10"]
                                                    if task3 in ModelList1:
                                                        TimeCostOfRepair = RepairModel1[k1][1]
                                                        break
                                                TimeList1.append(TimeCostOfRepair)
                                            else:
                                                p4 = np.where(np.array(TypeOfRepair) == task2)
                                                TimeCostOfRepair = RepairModel[p4[0][0]][1]
                                                TimeList1.append(TimeCostOfRepair)
                                        p2 = 0
                                        for n in range(len(List21)):
                                            if n == 0:
                                                if Dict5[BanZuOfRepairType[0]] != 0:  # 先安排给里程检班组
                                                    if NumberOfLine1[0] != 0:  # 还有检修库股道
                                                        StrPosition = "检修库"
                                                        NumberOfLine1[0] = NumberOfLine1[0] - 1
                                                        Model1 = Dict1[List21[n]]
                                                        if Model1[0] > 1:
                                                            NumberOfLine2[0] = NumberOfLine2[0] - 1
                                                        if Dict4[NowRepairType] == "夜班":
                                                            Start_Time2 = datetime.datetime.strptime(StartNightTime1,
                                                                                                     '%Y-%m-%d %H:%M:%S')
                                                        else:
                                                            Start_Time2 = datetime.datetime.strptime(StartDayTime1,
                                                                                                     '%Y-%m-%d %H:%M:%S')
                                                        if Dict51[BanZuOfRepairType[0]] == Number10:
                                                            StrBanZu = BanZuOfRepairType[0] + str(n1 + 1)
                                                        else:
                                                            StrBanZu = BanZuOfRepairType[0] + str(
                                                                Dict51[BanZuOfRepairType[0]] - Number10 + n1 + 1)
                                                        Dict5[BanZuOfRepairType[0]] = Dict5[BanZuOfRepairType[0]] - 1
                                                    else:  # 没有检修库股道了
                                                        StrPosition = "运用库"
                                                        NumberOfLine1[1] = NumberOfLine1[1] - 1
                                                        Model1 = Dict1[List21[n]]
                                                        if Model1[0] > 1:
                                                            NumberOfLine2[1] = NumberOfLine2[1] - 1
                                                        if Dict4[NowRepairType] == "夜班":
                                                            Start_Time2 = datetime.datetime.strptime(StartNightTime1,
                                                                                                     '%Y-%m-%d %H:%M:%S')
                                                        else:
                                                            Start_Time2 = datetime.datetime.strptime(StartDayTime1,
                                                                                                     '%Y-%m-%d %H:%M:%S')
                                                        if Dict51[BanZuOfRepairType[0]] == Number10:
                                                            StrBanZu = BanZuOfRepairType[0] + str(n1 + 1)
                                                        else:
                                                            StrBanZu = BanZuOfRepairType[0] + str(
                                                                Dict51[BanZuOfRepairType[0]] - Number10 + n1 + 1)
                                                        Dict5[BanZuOfRepairType[0]] = Dict5[BanZuOfRepairType[0]] - 1
                                                else:  # 里程检班组数量为0
                                                    if Dict5[BanZuOfRepairType[1]] != 0:
                                                        if NumberOfLine1[0] != 0:  # 还有检修库股道
                                                            StrPosition = "检修库"
                                                            NumberOfLine1[0] = NumberOfLine1[0] - 1
                                                            Model1 = Dict1[List21[n]]
                                                            if Model1[0] > 1:
                                                                NumberOfLine2[0] = NumberOfLine2[0] - 1
                                                            if Dict51[
                                                                BanZuOfRepairType[1]] == Number11:  # 之前的检修任务没有安排均衡修班组
                                                                Number110 = 1
                                                                StrBanZu = BanZuOfRepairType[1] + str(Number110)
                                                                Number110 += 1
                                                            else:
                                                                Number110 = Dict51[BanZuOfRepairType[1]] - Number11 + 1
                                                                StrBanZu = BanZuOfRepairType[1] + str(Number110)
                                                                Number110 += 1
                                                            if Dict4[NowRepairType] == "夜班":
                                                                Start_Time2 = datetime.datetime.strptime(
                                                                    StartNightTime1, '%Y-%m-%d %H:%M:%S')
                                                            else:
                                                                Start_Time2 = datetime.datetime.strptime(StartDayTime1,
                                                                                                         '%Y-%m-%d %H:%M:%S')
                                                        else:
                                                            StrPosition = "运用库"
                                                            NumberOfLine1[1] = NumberOfLine1[1] - 1
                                                            Model1 = Dict1[List21[n]]
                                                            if Model1[0] > 1:
                                                                NumberOfLine2[1] = NumberOfLine2[1] - 1
                                                            if Dict51[
                                                                BanZuOfRepairType[1]] == Number11:  # 之前的检修任务没有安排均衡修班组
                                                                Number110 = 1
                                                                StrBanZu = BanZuOfRepairType[1] + str(Number110)
                                                                Number110 += 1
                                                            else:
                                                                Number110 = Dict51[BanZuOfRepairType[1]] - Number11 + 1
                                                                StrBanZu = BanZuOfRepairType[1] + str(Number110)
                                                                Number110 += 1
                                                            if Dict4[NowRepairType] == "夜班":
                                                                Start_Time2 = datetime.datetime.strptime(
                                                                    StartNightTime1, '%Y-%m-%d %H:%M:%S')
                                                            else:
                                                                Start_Time2 = datetime.datetime.strptime(StartDayTime1,
                                                                                                         '%Y-%m-%d %H:%M:%S')
                                                    else:  # 均衡修和里程检班组的数量均为0，需要等前续检修任务结束后再安排，这时候需要判断前一个任务最早结束时间和晚班开始时间的前后
                                                        if NumberOfLine1[0] != 0:  # 还有检修库股道
                                                            StrPosition = "检修库"
                                                            NumberOfLine1[0] = NumberOfLine1[0] - 1
                                                            Model1 = Dict1[List21[n]]
                                                            if Model1[0] > 1:
                                                                NumberOfLine2[0] = NumberOfLine2[0] - 1
                                                            MinTime = TotalEndTimeList[0]  # 已经安排的检修任务中最早结束的检修任务的结束时间
                                                            p2 = 0
                                                            for p1 in range(1, len(TotalEndTimeList)):
                                                                if (TotalEndTimeList[p1] - MinTime).days < 0:
                                                                    MinTime = TotalEndTimeList[p1]
                                                                    p2 = p1
                                                            if Dict4[
                                                                NowRepairType] == "夜班":  # 需要判断前一个任务最早结束时间和晚班开始时间的前后
                                                                time1 = datetime.datetime.strptime(StartNightTime1,
                                                                                                   '%Y-%m-%d %H:%M:%S')
                                                                if (time1 - MinTime).days < 0:  # 夜班开始时间更早
                                                                    Start_Time2 = MinTime
                                                                else:
                                                                    Start_Time2 = time1
                                                            else:
                                                                Start_Time2 = MinTime
                                                            StrBanZu = TotalWorkerList[p2]
                                                        else:
                                                            StrPosition = "运用库"
                                                            NumberOfLine1[1] = NumberOfLine1[1] - 1
                                                            Model1 = Dict1[List21[n]]
                                                            if Model1[0] > 1:
                                                                NumberOfLine2[1] = NumberOfLine2[1] - 1
                                                            MinTime = TotalEndTimeList[0]  # 已经安排的检修任务中最早结束的检修任务的结束时间
                                                            p2 = 0
                                                            for p1 in range(1, len(TotalEndTimeList)):
                                                                if (TotalEndTimeList[p1] - MinTime).days < 0:
                                                                    MinTime = TotalEndTimeList[p1]
                                                                    p2 = p1
                                                            if Dict4[
                                                                NowRepairType] == "夜班":  # 需要判断前一个任务最早结束时间和晚班开始时间的前后
                                                                time1 = datetime.datetime.strptime(StartNightTime1,
                                                                                                   '%Y-%m-%d %H:%M:%S')
                                                                if (time1 - MinTime).days < 0:  # 夜班开始时间更早
                                                                    Start_Time2 = MinTime
                                                                else:
                                                                    Start_Time2 = time1
                                                            else:
                                                                Start_Time2 = MinTime
                                                            StrBanZu = TotalWorkerList[p2]
                                                TimeStartList11.append(Start_Time2)
                                                EndDate = Start_Time2 + datetime.timedelta(hours=TimeList1[n])
                                                TimeEndList11.append(EndDate)
                                                TotalEndTimeList.append(EndDate)
                                                WorkerList11.append(StrBanZu)
                                                TotalWorkerList.append(StrBanZu)
                                                PositionList11.append(StrPosition)
                                                TotalPositionList.append(StrPosition)
                                            else:
                                                TimeStartList11.append(TimeEndList11[n - 1])
                                                EndDate = TimeEndList11[n - 1] + datetime.timedelta(hours=TimeList1[n])
                                                TimeEndList11.append(EndDate)
                                                TotalEndTimeList.append(EndDate)
                                                WorkerList11.append(WorkerList11[n - 1])
                                                TotalWorkerList.append(WorkerList11[n - 1])
                                                PositionList11.append(PositionList11[n - 1])
                                                TotalPositionList.append(PositionList11[n - 1])
                                        if n1 >= Number10 + Number11:
                                            TotalEndTimeList[p2] = TimeEndList11[len(TimeEndList11) - 1]
                                            TotalWorkerList[p2] = WorkerList11[len(WorkerList11) - 1]
                                        if len(PositionList11) == 1:
                                            T1 = str(TimeStartList11[0])
                                            T2 = str(TimeEndList11[0])
                                            P2 = str(PositionList11[0])
                                            W1 = str(WorkerList11[0])
                                        else:
                                            T1 = str(TimeStartList11[0])
                                            T2 = str(TimeEndList11[0])
                                            P2 = PositionList11[0]
                                            W1 = WorkerList11[0]
                                            for p1 in range(1, len(PositionList11)):
                                                T1 = T1 + "+" + str(TimeStartList11[p1])
                                                T2 = T2 + "+" + str(TimeEndList11[p1])
                                        TimeStartList111.append(T1)
                                        TimeEndList111.append(T2)
                                        PositionList111.append(P2)
                                        WorkerList111.append(W1)
                                    TimeStartList1.append(TimeStartList111)
                                    TimeEndList1.append(TimeEndList111)
                                    PositionList1.append(PositionList111)
                                    WorkerList1.append(WorkerList111)
                                else:  # 没有均衡修班组
                                    Number10 = Dict5[BanZuOfRepairType[0]]  # 里程检班组数量
                                    for n1 in range(len(QueueTaskList)):
                                        TimeStartList11 = []
                                        TimeEndList11 = []
                                        PositionList11 = []
                                        WorkerList11 = []
                                        TaskChoice = QueueTaskList[len(QueueTaskList) - n1 - 1]
                                        ChoiceChe2 = QueueTrainList[len(QueueTrainList) - n1 - 1]
                                        TotalCheList00.append(ChoiceChe2)
                                        List21 = []
                                        if "+" in TaskChoice:
                                            ChoiceTask1 = TaskChoice.split("+")
                                            for task2 in ChoiceTask1:
                                                List21.append(task2)
                                        else:
                                            List21.append(TaskChoice)
                                        TimeList1 = []  # 检修任务所需的时间
                                        for task2 in List21:  # ["登顶检", “里程检"]
                                            TimeCostOfRepair = 0  # 该检修任务所需的检修耗时
                                            if "Y" in task2:
                                                task3 = task2.split("Y")[1]  # eg: 4B
                                                for k1 in range(len(MonthList)):
                                                    ModelList1 = MonthList[k1]  # eg:["1", "4A", "7", "10"]
                                                    if task3 in ModelList1:
                                                        TimeCostOfRepair = RepairModel1[k1][1]
                                                        break
                                                TimeList1.append(TimeCostOfRepair)
                                            else:
                                                p4 = np.where(np.array(TypeOfRepair) == task2)
                                                TimeCostOfRepair = RepairModel[p4[0][0]][1]
                                                TimeList1.append(TimeCostOfRepair)
                                        p2 = 0
                                        for n in range(len(List21)):
                                            if n == 0:
                                                if Dict5[BanZuOfRepairType[0]] != 0:
                                                    if NumberOfLine1[0] != 0:  # 还有检修库股道
                                                        StrPosition = "检修库"
                                                        NumberOfLine1[0] = NumberOfLine1[0] - 1
                                                        Model1 = Dict1[List21[n]]
                                                        if Model1[0] > 1:
                                                            NumberOfLine2[0] = NumberOfLine2[0] - 1
                                                    else:
                                                        StrPosition = "运用库"
                                                        NumberOfLine1[1] = NumberOfLine1[1] - 1
                                                        Model1 = Dict1[List21[n]]
                                                        if Model1[0] > 1:
                                                            NumberOfLine2[1] = NumberOfLine2[1] - 1
                                                    if Dict51[BanZuOfRepairType[0]] == Number10:
                                                        StrBanZu = BanZuOfRepairType[0] + str(n1 + 1)
                                                    else:
                                                        StrBanZu = BanZuOfRepairType[0] + str(
                                                            Dict51[BanZuOfRepairType[0]] - Number10 + n1 + 1)
                                                    Dict5[BanZuOfRepairType[0]] = Dict5[BanZuOfRepairType[0]] - 1
                                                    if Dict4[NowRepairType] == "夜班":
                                                        Start_Time2 = datetime.datetime.strptime(StartNightTime1,
                                                                                                 '%Y-%m-%d %H:%M:%S')
                                                    else:
                                                        Start_Time2 = datetime.datetime.strptime(StartDayTime1,
                                                                                                 '%Y-%m-%d %H:%M:%S')
                                                else:
                                                    if NumberOfLine1[0] != 0:  # 还有检修库股道
                                                        StrPosition = "检修库"
                                                        NumberOfLine1[0] = NumberOfLine1[0] - 1
                                                        Model1 = Dict1[List21[n]]
                                                        if Model1[0] > 1:
                                                            NumberOfLine2[0] = NumberOfLine2[0] - 1
                                                    else:
                                                        StrPosition = "运用库"
                                                        NumberOfLine1[1] = NumberOfLine1[1] - 1
                                                        Model1 = Dict1[List21[n]]
                                                        if Model1[0] > 1:
                                                            NumberOfLine2[1] = NumberOfLine2[1] - 1
                                                    MinTime = TotalEndTimeList[0]  # 已经安排的检修任务中最早结束的检修任务的结束时间
                                                    p2 = 0
                                                    for p1 in range(1, len(TotalEndTimeList)):
                                                        if (TotalEndTimeList[p1] - MinTime).days < 0:
                                                            MinTime = TotalEndTimeList[p1]
                                                            p2 = p1
                                                    StrBanZu = TotalWorkerList[p2]
                                                    if Dict4[NowRepairType] == "夜班":  # 需要判断前一个任务最早结束时间和晚班开始时间的前后
                                                        time1 = datetime.datetime.strptime(StartNightTime1,
                                                                                           '%Y-%m-%d %H:%M:%S')
                                                        if (time1 - MinTime).days < 0:  # 夜班开始时间更早
                                                            Start_Time2 = MinTime
                                                        else:
                                                            Start_Time2 = time1
                                                    else:
                                                        Start_Time2 = MinTime
                                                TimeStartList11.append(Start_Time2)
                                                EndDate = Start_Time2 + datetime.timedelta(hours=TimeList1[n])
                                                TimeEndList11.append(EndDate)
                                                TotalEndTimeList.append(EndDate)
                                                WorkerList11.append(StrBanZu)
                                                TotalWorkerList.append(StrBanZu)
                                                PositionList11.append(StrPosition)
                                                TotalPositionList.append(StrPosition)
                                            else:
                                                TimeStartList11.append(TimeEndList11[n - 1])
                                                EndDate = datetime.datetime.strptime(TimeEndList11[n - 1],
                                                                                     '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
                                                    hours=TimeList1[n])
                                                TimeEndList11.append(EndDate)
                                                TotalEndTimeList.append(EndDate)
                                                WorkerList11.append(WorkerList11[n - 1])
                                                TotalWorkerList.append(WorkerList11[n - 1])
                                                PositionList11.append(PositionList11[n - 1])
                                                TotalPositionList.append(PositionList11[n - 1])
                                        if n1 >= Number10:
                                            TotalEndTimeList[p2] = TimeEndList11[len(TimeEndList11) - 1]
                                            TotalWorkerList[p2] = WorkerList11[len(WorkerList11) - 1]
                                        if len(PositionList11) == 1:
                                            T1 = str(TimeStartList11[0])
                                            T2 = str(TimeEndList11[0])
                                            P2 = str(PositionList11[0])
                                            W1 = str(WorkerList11[0])
                                        else:
                                            T1 = str(TimeStartList11[0])
                                            T2 = str(TimeEndList11[0])
                                            P2 = PositionList11[0]
                                            W1 = WorkerList11[0]
                                            for p1 in range(1, len(PositionList11)):
                                                T1 = T1 + "+" + str(TimeStartList11[p1])
                                                T2 = T2 + "+" + str(TimeEndList11[p1])
                                        TimeStartList111.append(T1)
                                        TimeEndList111.append(T2)
                                        PositionList111.append(P2)
                                        WorkerList111.append(W1)
                                    TimeStartList1.append(TimeStartList111)
                                    TimeEndList1.append(TimeEndList111)
                                    PositionList1.append(PositionList111)
                                    WorkerList1.append(WorkerList111)
                    else:
                        TimeStartList1.append([])
                        TimeEndList1.append([])
                        PositionList1.append([])
                        WorkerList1.append([])
                        TotalCheList010.append([])
                        TotalTaskList11.append([])
                TotalTaskList10.append(TotalTaskList11)
                TotalCheList01.append(TotalCheList010)
                TimeStartList.append(TimeStartList1)
                TimeEndList.append(TimeEndList1)
                PositionList.append(PositionList1)
                WorkerList.append(WorkerList1)
            TotalCheChangList = []
            TotalStartTimeList = []
            TotalEndTimeList = []
            TotalRepairPositionList = []
            TotalRepairBanZuList = []
            TotalRepairTaskList = []
            TotalTrainOfRepairList = TotalCheList00
            for i in range(len(TimeStartList)):  # 等同于车场数量
                for j in range(len(TimeStartList[i])):  # 同一个车场的不同类型的检修任务
                    if len(TimeStartList[i][j]) != 0:
                        for t1 in range(len(TimeStartList[i][j])):
                            TotalCheChangList.append(RepairCheKu[i])
                            TotalStartTimeList.append(TimeStartList[i][j][t1])
                            TotalEndTimeList.append(TimeEndList[i][j][t1])
                            TotalRepairPositionList.append(PositionList[i][j][t1])
                            TotalRepairBanZuList.append(WorkerList[i][j][t1])
                            TotalRepairTaskList.append(TotalTaskList10[i][j][t1])
            QueueCheChangList = []
            QueueStartTimeList = []  # 按照列车编号大小排序后的信息
            QueueEndTimeList = []
            QueueRepairPositionList = []
            QueueRepairBanZuList = []
            QueueRepairTaskList = []
            TotalTrainOfRepairList1 = copy.deepcopy(TotalTrainOfRepairList)
            TotalTrainOfRepairList.sort()
            QueueTrainOfRepairList = copy.deepcopy(TotalTrainOfRepairList)
            for che in range(len(TotalTrainOfRepairList)):
                p1 = np.where(np.array(TotalTrainOfRepairList1) == TotalTrainOfRepairList[che])
                QueueStartTimeList.append(TotalStartTimeList[p1[0][0]])
                QueueEndTimeList.append(TotalEndTimeList[p1[0][0]])
                QueueRepairPositionList.append(TotalRepairPositionList[p1[0][0]])
                QueueRepairBanZuList.append(TotalRepairBanZuList[p1[0][0]])
                QueueRepairTaskList.append(TotalRepairTaskList[p1[0][0]])
                QueueCheChangList.append(TotalCheChangList[p1[0][0]])
            ListOfAll = []
            for che1 in range(len(QueueTrainOfRepairList)):
                Train1 = QueueTrainOfRepairList[che1]
                if Train1 >= 10:
                    strTrain = str(170) + str(Train1)
                else:
                    strTrain = str(1700) + str(Train1)
                List22 = []
                if "+" in QueueRepairTaskList[che1]:  # 该列车在该计划日有多个检修任务，需要分为多行
                    strTask = []

                    ChoiceTask1 = QueueRepairTaskList[che1].split("+")
                    Position1 = []
                    for t6 in ChoiceTask1:
                        p1 = np.where(np.array(TypeOfRepair) == t6)
                        Position1.append(p1[0][0])
                    if Position1[0] > Position1[1]:
                        strTask.append(ChoiceTask1[0])
                        strTask.append(ChoiceTask1[1])
                    else:
                        strTask.append(ChoiceTask1[1])
                        strTask.append(ChoiceTask1[0])

                    strStartTime = str(QueueStartTimeList[che1]).split("+")
                    strEndTime = str(QueueEndTimeList[che1]).split("+")
                else:
                    strTask = []
                    strTask.append(QueueRepairTaskList[che1])
                    strStartTime = []
                    strStartTime.append(str(QueueStartTimeList[che1]))
                    strEndTime = []
                    strEndTime.append(str(QueueEndTimeList[che1]))
                for t2 in range(len(strTask)):
                    List23 = []
                    List23.append(strTrain)
                    List23.append(str(strStartTime[t2].split(" ")[1]) + "-" + str(strEndTime[t2].split(" ")[1]))
                    List23.append(strTask[t2])
                    List23.append(QueueCheChangList[che1])
                    List23.append(QueueRepairPositionList[che1])
                    List23.append(QueueRepairBanZuList[che1])
                    List22.append(List23)
                if len(List22) > 1:
                    for i1 in range(len(List22)):
                        ListOfAll.append(List22[i1])
                else:
                    ListOfAll.append(List22[0])
            return ListOfAll

        def Transport(self):
            # 先计算各列车距离最近一次检修任务的相对里程值
            List3 = []  # 记录相对里程值
            List31 = []  # 记录所有列车最近一次检修任务进行的计划日
            for t in range(NumberOfTrain):
                for d in range(len(LengthOfLastWeek)):
                    if TotalRepairList[len(LengthOfLastWeek) - d - 1][t] != "":
                        List3.append(LengthOfLastWeek[len(LengthOfLastWeek) - 1][t] -
                                     LengthOfLastWeek[len(LengthOfLastWeek) - d - 1][t])
                        List31.append(len(LengthOfLastWeek) - d)
                        break
            List4 = copy.deepcopy(List3)
            List4 = list(set(List4))
            List4.sort()
            QueueList = []  # 列车排序集合
            for d1 in List4:
                p1 = np.where(np.array(List3) == d1)
                if len(p1[0]) == 1:
                    QueueList.append(p1[0][0] + 1)
                else:
                    List5 = []  # 相对里程值相同的列车集合，则按照绝对里程值的大小进行排序
                    for j in range(len(p1[0])):
                        List5.append(p1[0][j] + 1)
                    LengthOfList = []  # List5中列车对应累计里程值
                    for t1 in List5:
                        LengthOfList.append(List31[t1 - 1])
                    LengthOfList1 = copy.deepcopy(LengthOfList)
                    LengthOfList1 = list(set(LengthOfList1))
                    LengthOfList1.sort()
                    for l in range(len(LengthOfList1)):
                        p2 = np.where(np.array(LengthOfList1) == LengthOfList1[len(LengthOfList1) - l - 1])
                        if len(p2[0]) == 1:  # 考虑是否有累计里程值相同的列车
                            QueueList.append(List5[p2[0][0]])
                        else:
                            for k1 in range(len(p1[0])):
                                QueueList.append(List5[p2[0][k1]])
            ListOfTask1 = []  # 平峰任务推荐列车
            ListOfTask2 = []  # 热备任务推荐列车
            Number01 = 0
            for t1 in QueueList:
                Number01 += 1
                ListOfTask2.append(t1)
                if Number01 == Number1:
                    break
            Number02 = 0
            for t1 in QueueList:
                if t1 not in ListOfTask2:
                    Number02 += 1
                    ListOfTask1.append(t1)
                if Number02 == Number2:
                    break
            ListOfTask3 = []  # 不能执行早晚高峰的列车集合
            for j1 in range(1, NumberOfTrain + 1):
                if j1 in TrainList:
                    p1 = np.where(np.array(TrainList) == j1)
                    if "Y" in RepairList[p1[0][0]]:
                        ListOfTask3.append(j1)
            return ListOfTask1, ListOfTask2, ListOfTask3

        def post1(self, r2, r3):
            scheduleId = "D1720210001"
            list1 = []
            Dict01 = {"scheduleId": scheduleId, "trainId": "CD", "startTime": "09:00:00", "endTime": "09:00:00",
                      "taskContent": "2Y4B", "taskSegment": "永义车辆段", "taskSite": "检修库", "taskTeam": "均衡修班组1"}
            for i in range(len(r2)):  # 日计划内容
                Dict01["trainId"] = r2[i][0]
                str1 = r2[i][1].split("-")
                Dict01["startTime"] = str1[0]
                Dict01["endTime"] = str1[1]
                Dict01["taskContent"] = r2[i][2]
                Dict01["taskSegment"] = r2[i][3]
                Dict01["taskSite"] = r2[i][4]
                Dict01["taskTeam"] = r2[i][5]
                Dict02 = copy.deepcopy(Dict01)
                list1.append(Dict02)
            p1 = "http://sunjc.top:8880/"
            p3 = "schedule_day/clear?scheduleId=" + scheduleId  # 删除数据库中已经有的该任务ID的数据
            url1 = p1 + p3
            response = requests.get(url1)
            print(response)  # response=<200>说明访问成功
            print(response.text)
            p2 = "schedule_day/list"
            url = p1 + p2
            response = requests.post(url, json=list1)
            print(response)  # response=<200>说明访问成功
            print(response.text)  # response.text和浏览器返回数据相同说明post数据成功

            # 列车推荐数据传入
            list2 = []
            Dict03 = {"pingfengTask": "", "hotbackupTask": "", "cannotforpeakTask": "", "dayscheduleId": "",
                      "lineId": ""}
            str2 = ""
            for c in r3[0]:
                if c < 9:
                    Train1 = "CD" + str(1700) + str(c)
                else:
                    Train1 = "CD" + str(170) + str(c)
                str2 += Train1
            Dict03["pingfengTask"] = str2
            str3 = ""
            for c in r3[1]:
                if c < 9:
                    Train2 = "CD" + str(1700) + str(c)
                else:
                    Train2 = "CD" + str(170) + str(c)
                str3 += Train2
            Dict03["hotbackupTask"] = str3
            str4 = ""
            for c in r3[2]:
                if c < 9:
                    Train3 = "CD" + str(1700) + str(c)
                else:
                    Train3 = "CD" + str(170) + str(c)
                str4 += Train3
            Dict03["canforpeakTask"] = str4
            Dict03["dayscheduleId"] = scheduleId
            Dict03["lineId"] = str(17)
            list2.append(Dict03)
            p5 = "operationPlan/clear?dayScheduleId=" + scheduleId
            url1 = p1 + p5
            response = requests.get(url1)
            print(response)  # response=<200>说明访问成功
            print(response.text)
            p6 = "operationPlan"
            url = p1 + p6
            response = requests.post(url, json=list2)
            print(response)  # response=<200>说明访问成功
            print(response.text)  # response.text和浏览器返回数据相同说明post数据成功

            # IDRepairCheKu = ["CDCS", "CDWTM"]
            RemainTrack = copy.deepcopy(NumberOfLine)
            for k1 in range(len(list1)):
                dict1 = list1[k1]
                position1 = dict1["taskSegment"]
                repairTask = dict1["taskContent"]  # 单个任务或多个任务的集合
                if "Y" in repairTask:
                    T1 = "均衡修"
                else:
                    T1 = dict1["taskContent"]
                p1 = np.where(np.array(RepairCheKu) == position1)
                if len(Dict1[T1]) != 0:  # 单修程检修任务
                    model1 = Dict1[T1]
                    if model1[0] > 1:  # 该检修任务持续多天
                        if dict1["taskSite"] == "检修库":
                            RemainTrack[p1[0][0]][0] -= 1
                        else:
                            RemainTrack[p1[0][0]][1] -= 1
                else:
                    for list2 in range(len(MonthList)):
                        if repairTask.split("Y")[1] in MonthList[list2]:
                            model2 = RepairModel1[list2]
                            if model2[0] > 1:
                                if dict1["taskSite"] == "检修库":
                                    RemainTrack[p1[0][0]][0] -= 1
                                else:
                                    RemainTrack[p1[0][0]][1] -= 1
                            break
            for d1 in range(len(IDRepairCheKu)):
                line1 = RemainTrack[d1]  # 这个计划日后该车场剩余的股道数量
                p7 = "yard/updateUsingYardTackwayNum?yardId=" + IDRepairCheKu[d1] + "&servShopTrackwayUsing=" + str(
                    NumberOfLine[d1][0] - line1[0]) + "&operShopTrackwayUsing=" + str(NumberOfLine[d1][1] - line1[1])
                url = p1 + p7
                response = requests.get(url)
                print(response)  # response=<200>说明访问成功
                print(response.text)  # response.text和浏览器返回数据相同说明post数据成功


    r1 = DailyPlanning()
    r2 = r1.DailyPlan()  # 返回日计划内容
    r3 = r1.Transport()  # 返回当日的几种任务的列车推荐
    r1.post1(r2, r3)

if __name__ == '__main__':
    generate_day(17, "2021-7-29")