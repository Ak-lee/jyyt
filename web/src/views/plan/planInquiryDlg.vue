<template>
  <el-dialog :title="title" v-model="visible" width="95%" :before-close="close" style="max-height: 70%">

    <div class="planinfor">
      <span style="font-size: 14px; margin-right: 5px; width: 5%">计划信息</span>
      <el-table
          :data="tableData1"
          border
          style="width: 80%;margin: auto;text-align: center;"
      >
        <el-table-column prop="lineName" label="所属线路"/>
        <el-table-column prop="id" label="任务单号"/>
        <el-table-column prop="name" label="任务名称" width="180px"/>
        <el-table-column prop="planType" label="任务类型"/>
        <el-table-column prop="makeTime" label="计划制定时间"/>
        <el-table-column prop="startTime" label="计划开始时间"/>
        <el-table-column prop="endTime" label="计划结束时间"/>
      </el-table>
    </div>

    <el-divider></el-divider>
    <div class="plancontent">
      <span style="font-size: 14px; margin-right: 5px">计划内容</span>
      <el-table
          :data="tableData2"
          border
          @cell-click="cellClick"
          height="300"
          max-height="300"
          style="width: 100%;margin: auto;text-align: center;font-size: smaller"
      >
        <el-table-column label="日期" prop="planDates" fixed align="center" width="100"/>
        <el-table-column label="星期" prop="weekDays" fixed align="center" width="60"/>
        <el-table-column
            v-for="(item, index) in trains"
            :label="item"
            :key="index"
            :prop="item"
            align="center">
        </el-table-column>
      </el-table>
    </div>

    <div slot="footer"
         class="dialog-footer" style="text-align: center">
      <el-button @click="close">关 闭</el-button>
    </div>
  </el-dialog>
</template>

<script setup>
import {getById} from '@/service/plan/planmanage'
import {selectTrain} from "@/service/selector";
import {table, tableAll} from "@/service/plan/plancontent";
import moment from "moment";

let title = $ref('单个检修任务内容查询');
let originData = $ref([]); //根据线路查询的原始数据
let plantype = $ref('')
let visible = $ref(false);
let showStations = $ref(false);
let tableData1 = $ref([]);
let sdate = $ref(''); //计划开始日期
let edate = $ref(''); //计划结束日期
let days = $ref(null); //计划总天数
let tableHead = $ref([]);
let trains = $ref([]);
let weekdaysoption = $ref(["日", "一", "二", "三", "四", "五", "六"]);

const popoverRef = $ref('');
let planstatue = $ref([]); //记录当前单元格内容是年计划内容 or 月计划内容 or 周计划内容

//根据前端表格重新组织数据结构
let obj = $computed(() => {
  return dataHandle()
})
//渲染初始表格
let tableData2 = $computed(() => {
  let arr = []
  for (let i = 0; i < days; i++) {
    let str = moment(sdate).add(i, 'days').format('YYYY-MM-DD')  // 开始时间+偏置日期，得到目标时间
    let item = {}
    item.planDates = str; //日期渲染
    item.weekDays = weekdaysoption[moment(str).day()] //星期渲染
    arr.push(item)
    for (let j in trains) {
      planstatue.push({
        j: false,
      })
    }
  }

  for (let t = 0; t < days; t++) {
    let row = obj[arr[t].planDates];
    for (let j = 0; j < trains.length; j++) {
      if (row !== undefined) {
        if (row[trains[j]] !== undefined) {
          let tasktypes = [];
          for (let pt in row[trains[j]]) {
            if (pt === '年计划') {
              if (row[trains[j]][pt][0].taskType === "均衡修") {
                tasktypes.push(row[trains[j]][pt][0].taskContent)
              } else {
                tasktypes.push(row[trains[j]][pt][0].taskType)
              }
            } else if (pt === '月计划' && plantype !== '年计划') {
              tasktypes.push(row[trains[j]][pt][0].taskType)
            } else if (pt === '周计划' && plantype === '周计划') {
              tasktypes.push(row[trains[j]][pt][0].taskType)
            }
            if (pt === plantype) {
              planstatue[t][trains[j]] = true //判断任务内容是否是本次打开的任务类型
            }
          }
          arr[t][trains[j]] = tasktypes.join('+')
        } else {
          arr[t][trains[j]] = null
        }
      } else {
        arr[t][trains[j]] = null
      }
    }
  }
  return arr;
})


//点击单元格
const cellClick = function (row, column) {
  if (row[column.property]) {
    return true;
  }
  return false
}

const init = async function (id) {
  tableHead = [];
  let body = await getById(id);
  tableData1[0] = body.data
  plantype = tableData1[0].planType
  let contentAll = await tableAll(tableData1[0].lineId);
  originData = contentAll.data
  //渲染表格内容
  sdate = moment(tableData1[0].startTime).format('YYYY-MM-DD')
  edate = moment(tableData1[0].endTime).format('YYYY-MM-DD')
  days = moment(edate).diff(moment(sdate), 'days')
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

  visible = true
};

const close = function () {
  trains = []
  tableData1 = []
  tableData2 = []
  visible = false;
};

//组织数据
const dataHandle = function () {
  let objdata = [];
  let addData = [];
  originData.forEach(function (i) {
    let date = i.planDate
    let dur = i.duration;
    for (let j = 1; j < dur; j++) {
      let temp = JSON.parse(JSON.stringify(i));
      let str = moment(date).add(j, 'days').format('YYYY-MM-DD')  // 开始时间+偏置日期，得到目标时间
      temp.planDate = str
      addData.push(temp)
    }
  })
  addData.forEach(function (j) {
    originData.push(j)
  });
  originData.forEach(function (h) {
    objdata[h.planDate] = [];
  })
  originData.forEach(function (h) {
    objdata[h.planDate][h.trainId] = [];
  })
  originData.forEach(function (h) {
    objdata[h.planDate][h.trainId][h.planType] = [];
  })
  originData.forEach(function (h) {
    let plantypes = {}; //每个计划包含计划内容、计划持续时间等内容
    plantypes.taskType = h.taskType;
    plantypes.taskContent = h.taskContent;
    plantypes.dispatchStatus = h.dispatchStatus;
    objdata[h.planDate][h.trainId][h.planType].push(plantypes);
  })

  return objdata
}

defineExpose({
  init,
});
</script>

<style scoped>
.planinfor {
  display: flex;
  justify-content: space-around;
}

.popover1 {
  margin: auto;
  text-align: -webkit-center;
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
</style>
