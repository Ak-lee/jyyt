<template>
  <el-dialog :title="title" v-model="visible" width="95%" :before-close="close"
             style="height: 720px;">
    <div class="planinfor">
      <span style="font-size: 14px; margin-right: 5px; width: 5%">计划信息</span>
      <el-table
          :data="tableData1"
          border
          style="width: 55%;margin: auto;text-align: center;margin-top: 2px;font-size: smaller"
      >
        <el-table-column prop="lineName" label="所属线路" align="center"/>
        <el-table-column prop="id" label="任务单号" align="center"/>
        <el-table-column prop="name" label="任务名称" align="center"/>
        <el-table-column prop="planType" label="任务类型" align="center"/>
        <el-table-column prop="makeTime" label="计划制定时间" align="center"/>
        <el-table-column prop="startTime" label="计划开始时间" align="center"/>
        <el-table-column prop="endTime" label="计划结束时间" align="center"/>
      </el-table>
      <div class="tipsbox" style="font-size: 12px; margin-left: 5px; width: 40%">
        <pre v-if="plantype === '年计划'" style="color: firebrick">
          {{ tips.年计划 }}
        </pre>
        <pre v-else-if="plantype === '月计划'" style="color: firebrick">
          {{ tips.月计划 }}
        </pre>
        <pre v-else-if="plantype === '周计划'" style="color: firebrick">
          {{ tips.周计划 }}
        </pre>
      </div>
    </div>

    <el-divider></el-divider>
    <div class="plancontent">
      <div style="margin-bottom: 4px;">
        <span style="font-size: 14px; margin-right: 5px">计划内容</span>
        <el-button @click="outplanAddoutplanAdd" type="primary" v-show="plantype=== '年计划'" size="small">插入计划外检修任务
        </el-button>
        <el-button @click="exportExcel" size="small">导出计划内容为 Excel</el-button>
      </div>

      <div style="height: 400px; border: 1px solid #dcdfe6;">
        <el-auto-resizer>
          <template #default="{width, height}">
            <el-table-v2
                :columns="tableV2Columns"
                :data="tableV2Data2"
                :width="width"
                :height="height"
                :cell-props="cellProps"
                :class="kls"
            />
          </template>
        </el-auto-resizer>
      </div>
    </div>

    <div slot="footer"
         class="dialog-footer"
         style="display: flex;justify-content: center; margin-top: 10px;">
      <el-button type="primary"
                 size="small"
                 @click="confirm">确 定
      </el-button>
      <el-button size="small" @click="close">取 消</el-button>
    </div>

    <el-dialog append-to-body ref="taskdateChangeDlg" v-model="taskdatechangeformvisible"
               :before-close="taskdateChangeDlgClose"
               width="400"
    >
      <div>任务提前或延后至</div>
      <el-date-picker v-model="taskdateChangeTo"
                      type="date"
                      :disabled-date="disabledDate"
                      style="width: 300px; margin: 6px 0;"
                      value-format="YYYY-MM-DD">
      </el-date-picker>

      <div slot="footer"
           class="dialog-footer">
        <el-button @click="taskdateChangeDlgClose">取 消</el-button>
        <el-button type="primary"
                   :disabled="!taskdateChangeCheckStatus"
                   @click="taskdateChangeConfirm">确 定
        </el-button>
        <el-button type="primary" @click="taskDateChangeCheck">校 验</el-button>
      </div>
    </el-dialog>

    <!--调用弹窗-->
    <el-dialog width="500" append-to-body :title="title" v-model="outplanAddDlgVisible"
               :before-close="outplanAddDlgClose">

      <el-form ref="outplanAddDlgForm" label-width="150" :model="outplanAddData" :rules="outplanAddRules"
      >
        <span>季节检必须按要求全部插入，架修、大修请按需插入</span>
        <el-form-item label="季节检截止时间点：" v-show="seasonCheckTimePoint">
          <span>{{ seasonCheckTimePoint }}</span>
        </el-form-item>
        <el-row>
          <el-col :span="24">
            <el-form-item label="检修任务类型" prop="taskType">
              <el-select
                  filterable
                  clearable
                  v-model="outplanAddData.taskType"
                  placeholder="请选择检修任务类型"
                  style="width: 200px;">
                <el-option
                    :key="item" v-for="item in tasks"
                    :label="item"
                    :value="item"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="列车号" prop="trainId">
              <el-select
                  filterable
                  clearable
                  placeholder="选择列车"
                  v-model="outplanAddData.trainId"
                  style="width: 200px;">
                <el-option
                    :key="item" v-for="item in trains"
                    :label="item"
                    :value="item"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="任务开始时间" prop="planDate">
              <el-date-picker style="width: 200px;" :disabled-date="disabledDate" v-model="outplanAddData.planDate"/>
            </el-form-item>
            <el-form-item label="任务持续时间" prop="duration">
              <el-input style="width: 200px;" class="duration" type="number" v-model="outplanAddData.duration"/>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <div slot="footer"
           class="dialog-footer">
        <el-button @click="outplanAddDlgClose">取 消</el-button>
        <el-button type="primary" @click="outplanAddDlgConfirm(outplanAddDlgForm)">确 定
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="confirmDlgTitle" append-to-body v-model="confirmDlgVisible" height="400">
      <span>季节检必须按要求全部插入，架修、大修请按需插入</span>
      <el-container height="400px">
        <el-table border :data="confirmDlgTable">
          <el-table-column prop="trainId" label="列车号"></el-table-column>
          <el-table-column prop="unwheelRepair" label="架修"></el-table-column>
          <el-table-column prop="majorRepair" label="大修"></el-table-column>
          <el-table-column prop="seasonCheck" label="季节检"></el-table-column>
        </el-table>
      </el-container>
      <el-button type="primary" @click="submit">提交</el-button>
    </el-dialog>
  </el-dialog>
</template>

<script setup>
import {getById} from '@/service/plan/planmanage'
import {selectTrain} from "@/service/selector";
import {getLastTask, getNextTask, tableAll, update as updateTask, addOrUpdate} from "@/service/plan/plancontent";
import moment from "moment";
import {ElButton, ElMessage} from "element-plus";
import XLSX from "xlsx"

// ==================================================================== task date change dialog
import {tableAllByLineId} from "@/service/constraint"
import {getItemByTrainIdAndDate as getForecastByTrainAndDate} from '@/service/mileageForecast'
import {getItemByTrainIdAndDate as getHistoryByTrainAndDate} from "@/service/mileageHistory";
// =========================================================== outplanAdd 计划外检修任务插入
import {tableAll as tableAllTaskTypes} from "@/service/type";
import popover2 from "@/views/plan/popover2";

// const emit = defineEmits(['afterSubmit']);

let title = $computed(() => {
  return '计划制定管理 > ' + plantype + '编制结果编辑查询'
})
let originData = $ref([]); //根据线路查询的原始数据
// let plantypes = $ref({}); //每个计划包含计划内容、计划持续时间等内容
let plantype = $ref('')
let scheduleId = $ref('')
// let formdata = $ref('');
let visible = $ref(false);
let tableData1 = $ref([]);
let sdate = $ref(''); //计划开始日期
let edate = $ref(''); //计划结束日期
let days = $ref(null); //计划总天数
let trains = $ref([]);
let lineId = $ref('');  // 线路ID
let taskdateChangeDlg = $ref(null);
let taskChangeDlg = $ref(null);
let weekdaysoption = $ref(["日", "一", "二", "三", "四", "五", "六"]);

//备注提示
let tips = $ref({
  '年计划': "\n" +
      "1.年计划内容主要针对均衡修，按照时间周期进行计划的制定；" +
      "\n" +
      "2.季节检采用人工方式插入年计划（在表格单元格处右键单击可插入）；" +
      "\n" +
      "3.架大修到线路基础信息管理模块中进行可用车辆编辑进行状态变更；" +
      "\n" +
      "4.请按照相应条件插入季节检的任务；" +
      "\n" +
      "5.在该年计划中可能会存在架大修达到检修周期的情况，请注意任务的插入。",
  '月计划': "\n" +
      "1.月计划内容在年计划的基础上主要针对登顶检，按照时间周期进行计划的制定；\n" +
      "\n" +
      "2.可对月计划所针对的登顶检进行任务的提前或延后，但不能变动年计划制定的内容。",
  '周计划': "\n" +
      "1.周计划内容在月计划的基础上主要针对里程检，按照时间周期和里程周期进行计划的制定；\n" +
      "\n" +
      "2.可对周计划所针对的里程检进行任务的提前或延后，但不能变动月计划制定的内容。"
})
//单元格处理
// let proptemp = $ref(''); //记录表格prop
const popoverRef = $ref('');

//根据前端表格重新组织数据结构， 返回按照天拆分后的数据
let obj = $computed(() => {
  let objdata = {};

  // 跨越多天的任务拆分，
  originData.forEach(function (i) {
    if (planOrder(i.planType) < planOrder(plantype)) {
      return;
    }
    let dur = i.duration;
    for (let j = 0; j < dur; j++) {
      let temp = JSON.parse(JSON.stringify(i));
      let str = moment(temp.planDate).add(j, 'days').format('YYYY/MM/DD')  // 开始时间+偏置日期，得到目标时间
      temp.planDate = str
      temp.duration = 1

      if (!objdata[temp.planDate]) {
        objdata[temp.planDate] = {};
        objdata[temp.planDate].balancedRepairNumOneDay = 0;
        objdata[temp.planDate].mileageCheckNumOneDay = 0;
        objdata[temp.planDate].taskNumOneDay = 0;
      }
      if (!objdata[temp.planDate][temp.trainId]) {
        objdata[temp.planDate][temp.trainId] = {};
      }

      objdata[temp.planDate][temp.trainId][temp.planType] = temp;

      if (temp.planType === "月计划" || temp.planType === "周计划") {
        objdata[temp.planDate].mileageCheckNumOneDay += 1;
      }

      if (temp.planType === "年计划") {
        objdata[temp.planDate].balancedRepairNumOneDay += 1;
      }

      objdata[temp.planDate].taskNumOneDay += 1;
    }
  })

  return objdata
})

//渲染初始表格 表格版本1
let tableData2 = $computed(() => {
  let arr = []
  for (let i = 0; i < days; i++) {
    let str = moment(sdate).add(i, 'days').format('YYYY/MM/DD')  // 开始时间+偏置日期，得到目标时间
    let row = {}
    row.planDates = str; //日期渲染
    row.weekDays = weekdaysoption[moment(str).day()] //星期渲染
    arr.push(row)

    let item = obj[row.planDates];

    for (let j = 0; j < trains.length; j++) {
      if (item !== undefined && item[trains[j]] !== undefined) {
        let tasktypes = [];
        let cell = row[trains[j]] = {}
        for (let pt of Object.keys(item[trains[j]])) { // 遍历年计划、月计划、周计划
          if (item[trains[j]][pt].taskType === "均衡修") {
            tasktypes.push(item[trains[j]][pt].taskContent)
          } else {
            tasktypes.push(item[trains[j]][pt].taskType)
          }

          if (item[trains[j]][pt].planType == plantype) {
            cell.id = item[trains[j]][pt].id
          }
        }
        cell.content = tasktypes.join('+')
      } else {
        row[trains[j]] = {}
        row[trains[j]].content = null;
        row[trains[j]].id = null;
      }
    }
  }
  return arr;
})

//渲染初始表格 表格版本2
let tableV2Data2 = $computed(() => {
  let arr = []
  tableData2.forEach(i => {
    let obj = {};
    obj['date'] = i.planDates;
    obj['weekDays'] = i.weekDays;
    trains.forEach(j => {
      obj[j] = i[j];
    })
    arr.push(obj)
  })
  return arr;
})

// 用于excel 下载的对象
let tableData2Excel = $computed(() => {
  let arr = [];
  arr.push(Object.keys(tableData2[0]));
  tableData2.forEach(i => {
        let arr2 = [];
        for (let key of Object.keys(i)) {
          if (i[key].content === undefined) {
            arr2.push(i[key])
          } else {
            arr2.push(i[key].content);
          }
        }
        arr.push(arr2);
      }
  )
  return arr;
})

const exportExcel = () => {
  exportFile(tableData2Excel, lineId + "-" + plantype + "-" + sdate + "-" + edate);
}

// 数组转 Excel
const exportFile = (data, fileName) => {
  /* 把转换 JS数据数组的数组为工作表 */
  const ws = XLSX.utils.aoa_to_sheet(data);
  /* 生成的工作部病添加工作表 */
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Sheet1')
  /* 保存到文件 */
  XLSX.writeFile(wb, fileName + '.xlsx');
}

let tableV2Columns = $computed(() => {
  let arr = [
    {
      key: "date",
      dataKey: "date",
      title: "日期",
      width: 120,
    },
    {
      key: "weekDays",
      dataKey: "weekDays",
      title: "星期",
      width: 70,
      align: 'center',
    }
  ];

  trains.forEach(t => {
    let obj = {};
    obj.key = t;
    obj.dataKey = t;
    obj.title = t;
    obj.width = 80;
    obj.maxWidth = 500;
    obj.flexGrow = 1;
    obj.align = "center";

    obj.cellRenderer = ({cellData}) => (
        <>
          <popover2
              plantype={plantype}
              item={cellData}
              onEditTime={editTime}
          />
        </>
    )

    arr.push(obj);
  })
  return arr;
})

let kls = $ref('');
const cellProps = ({columnIndex}) => {
  const key = `hovering-col-${columnIndex}`
  return {
    ['data-key']: key,
    onMouseenter: () => {
      kls = key
    },
    onMouseleave: () => {
      kls = ''
    },
  }
}

let taskdatechangeformvisible = $ref(false);
let taskdatechangeItem = $ref({});
let taskdateChangeCheckStatus = $ref(false);
let taskdateChangeTo = $ref('');

//编辑时间：检修任务提前或延后
const editTime = async function (id) {
  taskdatechangeformvisible = true;
  taskdateChangeCheckStatus = false;
  originData = originData.filter(i => {
    if (i.id === id) {
      taskdatechangeItem = i    // 备份
      taskdateChangeTo = i.planDate
      return false
    } else {
      return true
    }
  })
}
let maxBalancedRepairs = $ref(0)
let maxMileageChecks = $ref(0);

const taskDateChangeCheck = async function () {
  lineId = tableData1[0].lineId;
  let constraint = await tableAllByLineId(lineId);
  let result = constraint.data;
  maxBalancedRepairs = result[0].maxBalancedRepairs;
  maxMileageChecks = result[0].maxMileageChecks;

  let newItem = JSON.parse(JSON.stringify(taskdatechangeItem));
  newItem.planDate = taskdateChangeTo;
  if (newItem.planDate !== taskdatechangeItem.planDate) {
    newItem.changeStatus = true;
  }

  originData = originData.filter(item => {
    return item.id !== taskdatechangeItem.id;
  })

  let result2 = checkDateConflict(newItem.trainId, newItem.planDate, newItem.duration)
  if (result2) {
    ElMessage.error("校验失败,目标位置已经存在检修任务")
    return;
  }
  originData.push(newItem);

  let flag = true;
  for (let key of Object.keys(obj)) { // 遍历每一天，检查单日检修任务数量约束条件
    if (obj[key].mileageCheckNumOneDay > maxMileageChecks) {
      flag = false;
    }
    if (obj[key].balancedRepairNumOneDay > maxBalancedRepairs) {
      flag = false;
    }
    if (!flag) {
      ElMessage.error("校验失败,不满足单日检修数量约束条件")
    }
  }

  // 下面的4个属性都是，尝试获得，若不能获得，则放弃该约束条件。
  let prevItem; // 可以得到上一次该任务的执行时间，用于判断时间周期, 不能查找计划周期，要查看实际执行时间
  let nextItem; // 可以得到下一次该任务的计划时间，用于判断时间周期
  let prevTaskMileage // 获取上一次该任务的里程值
  let nextTaskMileage   // 获取下一次该任务的预测里程值， 从预测的表中获取。

  let result3 = await getLastTask(newItem.id);
  prevItem = result3.data;
  result3 = await getNextTask(newItem.id);
  nextItem = result3.data;


  let tasktypeItem = tasktypeAll.filter(i => {
    return i.taskTypeName === newItem.taskType
  }).at(0);

  let mileagePeriod = tasktypeItem.mileagePeriod;
  let timePeriod = tasktypeItem.timePeriod;

  // 前后的里程周期、和时间周期，在标准周期的 0.9 ~ 1.1 范围内变动，即上下 0.1
  let mileage = await getHistoryByTrainAndDate(newItem.trainId, newItem.planDate);
  if (prevItem && mileagePeriod) {
    // 和上一个检修任务的里程周期判断
    // 这里待修改，需要读取的是实际存储的历史数据
    result3 = await getHistoryByTrainAndDate(prevItem.trainId, prevItem.planDate)
    if (result3.data) {
      prevTaskMileage = result3.data.mileage;
      if (mileage - prevTaskMileage < 0.9 * mileagePeriod ||
          mileage - prevTaskMileage > 1.1 * mileagePeriod) {
        ElMessage.error("校验失败,与前一次检修任务里程周期不符合要求，本任务预测里程：" + mileage + "；前一次检修任务里程：" + prevTaskMileage)
        flag = false;
      }
    }
  }

  if (nextItem && mileagePeriod) {
    // 和下一次检修任务的里程周期判断
    result3 = await getForecastByTrainAndDate(nextItem.trainId, nextItem.planDate)
    if (result3.data) {
      nextTaskMileage = result3.data.mileage;
      if (mileage - nextTaskMileage < 0.9 * mileagePeriod ||
          mileage - nextTaskMileage > 1.1 * mileagePeriod) {
        ElMessage.error("校验失败,与后一次检修任务里程周期不符合要求, 本任务预测里程：" + mileage + "；前一次检修任务里程：" + nextTaskMileage)
        flag = false;
      }
    }
  }

  if (prevItem && timePeriod) {
    // 和上一次检修任务判断时间周期
    let duration = moment(newItem.planDate).diff(moment(prevItem.planDate), "days");
    if (duration < 0.9 * timePeriod ||
        duration > 1.1 * timePeriod) {
      flag = false;
      ElMessage.error("校验失败,与前一次检修任务时间周期不符合要求，" + "时间周期：" + timePeriod + "; 距离上次检修" + duration + "天， 时间间隔请控制在（0.9~1.1）*时间周期")
    }
  }
  if (nextItem && timePeriod) {
    // 和下一次检修任务判断时间周期
    let duration = moment(nextItem.planDate).diff(moment(newItem.planDate), "days")
    if (duration < 0.9 * timePeriod ||
        duration > 1.1 * timePeriod) {
      ElMessage.error("校验失败,与后一次检修任务时间周期不符合要求， " + "时间周期：" + timePeriod + "; 距离下次检修" + duration + "天， 时间间隔请控制在（0.9~1.1）*时间周期")
      flag = false;
    }
  }
  if (flag) {
    taskdateChangeCheckStatus = true;
    ElMessage.success("校验成功")
    return;
  }
}

const taskdateChangeConfirm = function () {
  if (!taskdateChangeCheckStatus) {
    ElMessage.error("请先校验")
  }
  taskdatechangeformvisible = false;
}

const taskdateChangeDlgClose = function () {
  originData = originData.filter(item => {
    return item.id !== taskdatechangeItem.id;
  })
  originData.push(taskdatechangeItem);
  taskdatechangeItem = {}

  taskdatechangeformvisible = false;
}


// ===============================================
// 季节检，获取所有合规的时间组合
const seasonCheckPointCombination = async function () {
  arr = {};
  seasonCheckTimePoint = tasktypeAll.find(i => {
    return i.taskTypeName.indexOf("季节") !== -1
        && i.beAbsoluteTime === true
  }).timePeriod;

  let dates = seasonCheckTimePoint.split(",")
  let sYearStr = moment(sdate).format('YYYY')
  let eYearStr = moment(edate).format('YYYY')

  trains.forEach(k => {
    arr[k] = [];
    dates.forEach(i => {
      let date;
      date = new Date(sYearStr + "/" + i);
      if (date.getTime() >= new Date(sdate).getTime() && date.getTime() <= new Date(edate).getTime()) {
        let obj = {}
        obj.date = date;
        obj.use = false;
        arr[k].push(obj)
      }
      date = new Date(eYearStr + "/" + i);
      if (date.getTime() >= new Date(sdate).getTime() && date.getTime() <= new Date(edate).getTime()) {
        let obj = {}
        obj.date = date;
        obj.use = false;
        arr[k].push(obj)
      }
    })

    arr[k].sort((a, b) => {
      return a.date - b.date;
    });

    if (arr[k].length > dates.length) {
      arr[k] = arr[k].slice(0, dates.length);
    }
  })
}

// 季节检，占用某一个合规的时间点
const seasonCheckOccupy = function (trainId, planDate) {
  let find = false;
  for (let i = 0; i < arr[trainId].length; i++) {
    let item = arr[trainId][i]
    if (i == 0 && planDate < item.date && !item.use) {
      arr[trainId][i].use = true
      find = true;
      break;
    } else if (i !== 0) {
      let prevItem = arr[trainId][i - 1];
      if (planDate < item.date && planDate > prevItem.date && !item.use) {
        find = true;
        break;
      }
    }
  }
  return find;
}


const init = async function (id) {
  let body = await getById(id);
  tableData1[0] = body.data
  plantype = tableData1[0].planType
  scheduleId = tableData1[0].id
  lineId = tableData1[0].lineId;

  body = await tableAllTaskTypes()
  tasktypeAll = body.data

  //动态增加表头，不同的线路有不同的列车
  //加载线路列车列表
  let result = await selectTrain(tableData1[0].lineId);
  let traintemp = [];
  result.forEach(i => traintemp.push(i.id))
  // 对动态增加的表头进行排序 1-10
  trains = traintemp.sort((a, b) => {
    const r = b - a
    return r
  })

  let contentAll = await tableAll(tableData1[0].lineId);
  originData = contentAll.data
  originData.forEach(i => {
    if (i.taskType === '季节检') {
      seasonCheckOccupy(i.trainId, i.planDate);
    }
  })
  //渲染表格内容
  sdate = moment(tableData1[0].startTime).format('YYYY/MM/DD')
  edate = moment(tableData1[0].endTime).format('YYYY/MM/DD')
  days = moment(edate).diff(moment(sdate), 'days') + 1;

  await seasonCheckPointCombination();
  visible = true
};

// confirmDialog -----------------------------
let confirmDlgVisible = $ref(false);

let confirmDlgTitle = $ref('需要手动插入检修任务明细：')

let confirmDlgTable = $computed(function () {
  let table = [];

  trains.forEach(i => {
    let row = {};
    row.trainId = i;
    row.unwheelRepair = []  // 架修
    row.majorRepair = [];  // 大修
    row.seasonCheck = [];   // 季节检
    table.push(row);
  })

  originData.forEach(i => {
    let row = table.find(j => j.trainId == i.trainId);
    let str = moment(i.planDate).format("YYYY-MM-DD");
    str += "(" + i.duration + "天)"
    if (i.taskType === "季节检") {
      row.seasonCheck.push(str);
    } else if (i.taskType === "架修") {
      row.unwheelRepair.push(str);
    } else if (i.taskType === "大修") {
      row.majorRepair.push(str);
    }
  })
  return table;
})

const confirm = async function () {
  if (plantype === '年计划') {
    confirmDlgVisible = true;
  } else {
    let data = originData.filter(i => i.changeStatus == true);
    let result = await updateTask(data)
    if (result.code == 0) {
      ElMessage.success("更新成功")
      close();
    } else {
      ElMessage.error("更新失败")
    }
  }
}

const submit = async function () {
  let seasons = seasonCheckTimePoint.split(",")
  seasons = seasons.filter(i => i && i.trim());
  let flag = true
  trains.forEach(t => {
    let item = confirmDlgTable.find(i => i.trainId == t)
    if (item.seasonCheck.length < seasons.length) {
      flag = false;
    }
  })
  if (!flag) {
    ElMessage.error("季节检任务，数量不足")
  } else {
    let data = originData.filter(i => i.changeStatus == true);
    data.forEach(i => {
      if (i.id === "季节检" || i.id === "大修" || i.id === "架修") {
        i.id = '';
      }
    })
    let result = await addOrUpdate(data)
    if (result.code == 0) {
      ElMessage("更新成功")
      close();
    } else {
      ElMessage("更新失败")
    }
  }
}

const close = function () {
  trains = []
  tableData1 = []
  tableData2 = []
  visible = false;
  outplanAddDlgVisible = false;
  confirmDlgVisible = false;
  taskdatechangeformvisible = false;
};

const planOrder = function (planType) {
  let result = 0;
  if (planType === '日计划') {
    result = 1;
  } else if (planType === '周计划') {
    result = 2;
  } else if (planType === '月计划') {
    result = 3;
  } else if (planType == '年计划') {
    result = 4;
  }
  return result;
}

var arr = $ref({});   // 用于存储季节检，多个时间点的占用情况。
var tasktypeAll = $ref({});

let outplanAddDlgForm = $ref()
let outplanAddDlgVisible = $ref(false)
let tasks = $ref(['季节检', '架修', '大修'])

// 为了方便新插入的计划外数据也能移动，故需要有 id。
// id 为空只对应 不属于该计划的检修任务。如月计划外中，年计划的内容的id就为空
let outplanAddData = $ref({
  id: '',
  taskType: '',
  trainId: '',
  planDate: '',
  duration: ''
})
let seasonCheckTimePoint = $ref('')

let outplanAddoutplanAdd = async function () {
  outplanAddDlgVisible = true;
  outplanAddData = {
    id: '',
    taskType: '',
    trainId: '',
    planDate: '',
    duration: '',
  }
}
let outplanAddDlgClose = function () {
  outplanAddDlgVisible = false;
}

let outplanAddDlgConfirm = async function (formRef) {
  if (!formRef) return;
  let valid = await formRef.validate((valid, fields) => {
    if (valid) {
      return true
    } else {
      return false
    }
  })
  if (valid) {
    let flag = true;
    if (checkDateConflict(outplanAddData.trainId, outplanAddData.planDate, outplanAddData.duration)) {
      ElMessage.error("时间冲突！");
      flag = false;
    }
    let dateStr = moment(outplanAddData.planDate).add(outplanAddData.duration - 1, 'days').format('YYYY/MM/DD');
    if (new Date(dateStr).getTime() > new Date(edate).getTime()) {
      ElMessage.error("持续时间超出计划范围！");
      flag = false;
    }

    if (outplanAddData.taskType === "季节检") {
      let find = seasonCheckOccupy(outplanAddData.trainId, outplanAddData.planDate)
      if (!find) {
        ElMessage.error("季节检，时间不符合要求")
        flag = false;
      }
    }

    if (flag) {
      outplanAddData.changeStatus = true;
      outplanAddData.planType = plantype;
      outplanAddData.scheduleId = scheduleId;
      outplanAddData.id = outplanAddData.taskType;
      originData.push(outplanAddData)

      let lineId = tableData1[0].lineId;
      let constraint = await tableAllByLineId(lineId);
      let result = constraint.data;
      maxBalancedRepairs = result[0].maxBalancedRepairs;
      maxMileageChecks = result[0].maxMileageChecks;

      let flag2 = true;
      for (let key of Object.keys(obj)) { // 遍历每一天，检查单日检修任务数量约束条件
        if (obj[key].mileageCheckNumOneDay > maxMileageChecks) {
          flag2 = false;
        }
        if (obj[key].balancedRepairNumOneDay > maxBalancedRepairs) {
          flag2 = false;
        }
        if (!flag2) {
          ElMessage.error("校验失败,不满足单日检修数量约束条件")
        }
      }
      if (flag2) {
        outplanAddDlgVisible = false;
      } else {
        originData = originData.filter(i => i.id !== outplanAddData.id)
      }
    }
  }
}

const checkDateConflict = function (trainId, startDate, duration) {
  // 返回true，代表存在冲突
  let flag = false
  for (let i = 0; i < duration; i++) {
    let date = moment(startDate).add(i, "days").format("YYYY/MM/DD")
    if (obj[date] && obj[date][trainId] && obj[date][trainId][plantype]) {
      flag = true;
      break;
    }
  }
  return flag;
}

const disabledDate = function (date) {
  return date.getTime() < new Date(sdate).getTime() || date.getTime() > new Date(edate).getTime()
}

const outplanAddRules = $ref({
  trainId: [{
    required: true,
    message: "请选择列车号",
    trigger: 'blur'
  }],
  planDate: [{
    required: true,
    message: "请选择日期",
    trigger: 'blur'
  }],
  taskType: [{
    required: true,
    message: "请选择任务类型",
    trigger: 'blur'
  }],
  duration: [{
    required: true,
    message: "请输入任务持续时间",
    trigger: 'blur'
  }]
})


defineExpose({
  init,
});
</script>

<style scoped>
.planinfor {
  display: flex;
  justify-content: space-around;
}

.button1 {
  width: 180px;
}

.tipsbox {
  border: 1px solid gainsboro;
  border-radius: 2px;
}

.plancontent {
  position: relative;
}

/deep/ .hovering-col-2 [data-key='hovering-col-2'],
/deep/ .hovering-col-3 [data-key='hovering-col-3'],
/deep/ .hovering-col-4 [data-key='hovering-col-4'],
/deep/ .hovering-col-5 [data-key='hovering-col-5'],
/deep/ .hovering-col-6 [data-key='hovering-col-6'],
/deep/ .hovering-col-7 [data-key='hovering-col-7'],
/deep/ .hovering-col-8 [data-key='hovering-col-8'],
/deep/ .hovering-col-9 [data-key='hovering-col-9'],
/deep/ .hovering-col-10 [data-key='hovering-col-10'],
/deep/ .hovering-col-11 [data-key='hovering-col-11'],
/deep/ .hovering-col-12 [data-key='hovering-col-12'],
/deep/ .hovering-col-13 [data-key='hovering-col-13'],
/deep/ .hovering-col-14 [data-key='hovering-col-14'],
/deep/ .hovering-col-15 [data-key='hovering-col-15'],
/deep/ .hovering-col-16 [data-key='hovering-col-16'],
/deep/ .hovering-col-17 [data-key='hovering-col-17'],
/deep/ .hovering-col-18 [data-key='hovering-col-18'],
/deep/ .hovering-col-19 [data-key='hovering-col-19'],
/deep/ .hovering-col-20 [data-key='hovering-col-20'],
/deep/ .hovering-col-21 [data-key='hovering-col-21'],
/deep/ .hovering-col-22 [data-key='hovering-col-22'],
/deep/ .hovering-col-23 [data-key='hovering-col-23'],
/deep/ .hovering-col-24 [data-key='hovering-col-24'],
/deep/ .hovering-col-25 [data-key='hovering-col-25'],
/deep/ .hovering-col-26 [data-key='hovering-col-26'],
/deep/ .hovering-col-27 [data-key='hovering-col-27'],
/deep/ .hovering-col-28 [data-key='hovering-col-28'],
/deep/ .hovering-col-29 [data-key='hovering-col-29'],
/deep/ .hovering-col-30 [data-key='hovering-col-30'] {
  background: rgb(245, 247, 250) !important;
}

[data-key='hovering-col-0'] {
  font-weight: bold;
  user-select: none;
  pointer-events: none;
}

/*/deep/ .el-form-item .el-input__inner {*/
/*  width: 220px;*/
/*}*/

/*/deep/ .el-form-item .duration {*/
/*  width: 220px;*/
/*}*/
</style>
