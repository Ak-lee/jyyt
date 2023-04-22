<template>
  <el-dialog :title="title" v-model="visible" width="1100" :before-close="close">

    <el-row>
      <div class="plancontent">
        <span style="font-size: 14px; margin-right: 5px">初始计划内容:</span>
        <el-table
            :data="tableData1"
            border
            max-height="300px"
            style="width: 100%; margin-top: 10px; text-align: center"
        >
          <el-table-column type="index" label="序号"/>
          <el-table-column prop="trainId" label="车号"/>
          <el-table-column prop="startTime" label="作业开始时间"/>
          <el-table-column prop="endTime" label="作业结束时间"/>
          <el-table-column prop="taskType" label="检修模式"/>
          <el-table-column prop="taskContent" label="作业内容"/>
          <el-table-column prop="duration" label="任务共几天"/>
          <el-table-column prop="offsetDay" label="进行到第几天"/>
          <el-table-column prop="taskSegment" label="作业场/段"/>
          <el-table-column prop="taskSite" label="作业地点"/>
          <el-table-column prop="taskTeam" label="作业班组"/>
        </el-table>
      </div>
      <el-divider></el-divider>

      <div class="ImplementationContent">
        <span style="font-size: 14px; margin-right: 5px">当日实际执行内容:</span>
        <div style="color: red; font-size: 14px; margin: 6px 0;">
          <span>注意：出现计划提前或延后执行时，将触发计划内容重新生成，请及时关注.</span>
        </div>
        <el-button @click="confirmAll" size="small">
          <el-icon>
            <Check/>
          </el-icon>
          <span>全部确认</span>
        </el-button>

        <el-button style="margin-left: 10px" @click="addRow" size="small">
          <el-icon>
            <CirclePlus/>
          </el-icon>
          <span>提前执行任务</span>
        </el-button>
        <el-table
            :data="tableData2"
            border
            max-height="500px"
            style="width: 100%; min-width: 800px; margin-top: 4px;text-align: center"
        >
          <el-table-column align="center" type="index" label="序号"/>
          <el-table-column align="center" prop="trainId" label="车号"/>
          <el-table-column align="center" prop="taskType" label="检修模式"/>
          <el-table-column align="center" prop="taskContent" label="作业内容"/>
          <el-table-column prop="duration" label="任务共几天"/>
          <el-table-column label="进行到第几天">
            <template #default="{row}">
              <span>{{ row.offsetDay + 1 }}</span>
            </template>
          </el-table-column>
          <el-table-column align="center" prop="taskSegment" label="作业场/段"/>
          <el-table-column align="center" prop="taskSite" label="作业地点"/>
          <el-table-column align="center" prop="taskTeam" label="作业班组"/>
          <el-table-column align="center" prop="status" label="状态"/>
          <el-table-column align="center" label="操作" width="220">
            <template #default="{row}">
              <el-button @click="checkRow(row)" size="small">
                <el-icon>
                  <Check/>
                </el-icon>
                <span>准点执行</span>
              </el-button>

              <el-button size="small" @click="deleteRow(row) ">
                <el-icon>
                  <Remove/>
                </el-icon>
                <span>任务延后</span>
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-row>


    <div slot="footer"
         class="dialog-footer"
         style="display: flex;justify-content: center">
      <el-button type="primary"
                 @click="submit">提 交
      </el-button>
      <el-button @click="close">取 消</el-button>
    </div>

    <newtask-dlg ref="newtaskdlg" @afterSubmit="handleAfterSubmit"></newtask-dlg>
    <newtasksubmit-dlg ref="newtasksubmitdlg" @afterSubmit="handleAfterSubmit2"></newtasksubmit-dlg>
  </el-dialog>

</template>

<script setup>
import {getById, table} from '@/service/plan/dayplancontent'
import {Check, CirclePlus, Remove} from '@element-plus/icons-vue'
import {ref} from "vue";
import {get} from "@/utils/request";
import NewtaskDlg from "@/views/plan/newtaskDlg";
import NewtasksubmitDlg from "@/views/plan/newtasksubmitDlg";
import {ElMessage} from "element-plus";
import {getById as getScheduleById} from "@/service/plan/planmanage"

let title = $ref("计划数据反馈")
let visible = $ref(false);
let tableData1 = $ref([]);
let tableData2 = $ref([]);
let newtaskdlg = $ref(null);
let newtasksubmitdlg = $ref(null);
let scheduleid = $ref('')
let scheduleInfo = $ref({});

const init = async function (id) {
  scheduleid = id
  let data = await getScheduleById(scheduleid);
  this.scheduleInfo = data.data;
  let body = await table(id);
  tableData1 = body.data
  for (let i = 0; i < tableData1.length; i++) {
    tableData2.push({
      trainId: tableData1[i].trainId,
      taskType: tableData1[i].taskType,
      taskContent: tableData1[i].taskContent,
      scheduleId: tableData1[i].scheduleId,
      taskId: tableData1[i].taskId,
      taskSegment: tableData1[i].taskSegment,
      taskSite: tableData1[i].taskSite,
      taskTeam: tableData1[i].taskTeam,
      date: this.scheduleInfo.startTime,
      duration: tableData1[i].duration,
      offsetDay: tableData1[i].offsetDay,
      lineId: this.scheduleInfo.lineId,
      applyMonth: tableData1[i].applyMonth,
    })
  }

  visible = true
};

const deleteRow = function (row) {
  row.status = "任务延后";
}

const checkRow = function (row) {
  row.status = "准点执行"
}


const confirmAll = function () {
  tableData2.forEach(i => {
    if (!i.status) {
      // 若没有 status，
      i.status = "准点执行";
    }
  })
}

const addRow = function () {
  newtaskdlg.init(tableData2, tableData1.at(0).lineId);
}

const handleAfterSubmit = function (obj) {
  obj.status = "任务提前";
  obj.scheduleId = scheduleid
  tableData2.push(obj);
}

const submit = function () {
  let flag = false;
  for (let idx in tableData2) {
    if (!tableData2[idx].status) {
      // 若没有 status，
      flag = true;
      break;
    }
  }
  if (flag) {
    ElMessage.error("存在未确认的检修任务. 提交失败.")
  } else {
    newtasksubmitdlg.init(tableData2);
  }
}

const handleAfterSubmit2 = function () {
  tableData1 = []
  tableData2 = []
  visible = false;
}


const close = function () {
  tableData1 = []
  tableData2 = []
  visible = false;
}
defineExpose({
  init,
});
</script>

<style scoped>
.plancontent {
  margin: 0 auto;
}

.ImplementationContent {
  margin: 0 auto;
}

.dialog-footer {
  margin-top: 20px;
}
</style>
