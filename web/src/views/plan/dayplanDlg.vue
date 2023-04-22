<template>
  <el-dialog :title="title" v-model="visible" width="90%" :before-close="close">
    <span style="font-size: 14px; margin-right: 8px">计划信息:</span>
    <el-table
        :data="tableData1"
        border
        style="width: 80%;margin: auto;text-align: center"
    >
      <el-table-column prop="lineName" label="所属线路"/>
      <el-table-column prop="id" label="任务单号"/>
      <el-table-column prop="name" label="任务名称" width="180px"/>
      <el-table-column prop="planType" label="任务类型"/>
      <el-table-column prop="makeTime" label="计划制定时间"/>
      <el-table-column prop="startTime" label="计划开始时间"/>
      <el-table-column prop="endTime" label="计划结束时间"/>
    </el-table>

    <el-divider></el-divider>
    <el-row>
      <span style="font-size: 14px; margin-right: 8px">计划内容:</span>
    </el-row>

    <el-table
        :data="tableData2"
        border
        max-height="500"
        style="width: 80%;margin: auto;text-align: center"
    >
      <el-table-column type="index" label="序号" width="80px"/>
      <el-table-column prop="trainId" label="车号"/>
      <el-table-column prop="startTime" label="作业开始时间"/>
      <el-table-column prop="endTime" label="作业结束时间"/>
      <el-table-column prop="taskType" label="任务类型"/>
      <el-table-column prop="taskContent" label="作业内容"/>
      <el-table-column prop="taskSegment" label="作业场/段"/>
      <el-table-column prop="taskSite" label="作业地点"/>
      <el-table-column prop="taskTeam" label="作业班组"/>
    </el-table>

    <el-row>
      <span style="font-size: 14px; margin:10px;">运营计划列车推荐:</span>
    </el-row>
    <el-table :data="tableData3"
              border
              max-height="500"
              style="width: 80%;margin: auto;text-align: center"
    >
      <el-table-column label="运营任务类型" prop="type"/>
      <el-table-column label="列车编号（按推荐程度排序）" prop="trainsNo"/>
    </el-table>

    <div slot="footer"
         class="dialog-footer" style="text-align: center; margin-top: 10px;">
      <el-button size="small" @click="close">关 闭</el-button>
    </div>
  </el-dialog>
</template>

<script setup>
import {getById} from '@/service/plan/planmanage'
import {table} from '@/service/plan/dayplancontent'
import {get} from '@/utils/request'

let title = $ref("单个检修任务内容查询")
let visible = $ref(false);
let tableData1 = $ref([]);
let tableData2 = $ref([]);
let plantype = $ref('')

let tableData3 = $ref([])

const init = async function (id) {
  tableData1 = [];
  tableData2 = [];
  tableData3 = [];

  let body = await getById(id);
  tableData1[0] = body.data
  let body1 = await table(id);
  tableData2 = body1.data

  let params = {
    dayScheduleId: id
  }

  get("/api/operationPlan/getByDayScheduleId", params)
      .then((res) => {
        let operationPlan = res.data;

        for (let key in operationPlan) {
          let obj = {};
          if (key === "pingfengTask") {
            obj.type = "平峰任务"
            obj.trainsNo = operationPlan[key]
            tableData3.push(obj);
          } else if (key === "hotBackupTask") {
            obj.type = "热备任务"
            obj.trainsNo = operationPlan[key]
            tableData3.push(obj);
          } else if (key === "cannotForPeakTask") {
            obj.type = "不可用于早晚高峰"
            obj.trainsNo = operationPlan[key]
            tableData3.push(obj);
          }
        }
      }, () => {
        console.log("网络错误.")
      })
  visible = true
};

const close = function () {
  visible = false;
};

defineExpose({
  init,
});
</script>

<style scoped>
.plancontent {
  position: relative;
}
</style>
