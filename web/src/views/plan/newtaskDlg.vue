<template>
  <el-dialog append-to-body :title="title" v-model="visible" width="40%" :before-close="close">
    <div style="margin-bottom: 10px;">只能将下一次要执行的任务提前</div>
    <el-form ref="form"
             v-model="formdata"
             label-width="140"
    >
      <el-row :gutter="20">
        <el-form-item label="车号">
          <el-select v-model="formdata.trainId" placeholder="下拉框中选择车号">
            <el-option :key="item.id" v-for="item in trains" :label="item.id" :value="item.id"/>
          </el-select>
        </el-form-item>
      </el-row>

      <el-row :gutter="20">
        <el-form-item label="作业内容">
          <el-select v-model="formdata.taskType" placeholder="点击选择">
            <el-option label="均衡修" value="均衡修"/>
            <el-option label="季节专检" value="季节专检"/>
            <el-option label="登顶检" value="登顶检"/>
            <el-option label="里程检" value="里程检"/>
          </el-select>
        </el-form-item>
      </el-row>

      <el-row :gutter="20">
        <el-form-item label="作业场/段">
          <el-select v-model="formdata.taskSegment">
            <el-option v-for="item in yardList" :key="item.id" :label="item.name" :value="item.name"/>
          </el-select>
        </el-form-item>
      </el-row>
      <el-row :gutter="20">
        <el-form-item label="作业地点">
          <el-select v-model="formdata.taskSite" :disabled="!taskSiteList.length">
            <el-option v-for="item in taskSiteList" :key="item" :label="item" :value="item"/>
          </el-select>
        </el-form-item>
      </el-row>

      <el-row :gutter="20">
        <el-form-item label="作业班组">
          <el-select v-model="formdata.taskTeam">
            <el-option v-for="item in yardTeamList" :key="item" :label="item" :value="item"/>
          </el-select>
        </el-form-item>
      </el-row>

      <el-row :gutter="20">
        <el-form-item label="任务持续时间（天）">
          <el-input type="number" v-model="formdata.duration" disabled/>
        </el-form-item>
      </el-row>

      <el-row :gutter="20">
        <el-form-item label="任务进行到第几天">
          <el-input type="number" v-model="formdata.offsetDay"/>
        </el-form-item>
      </el-row>

      <el-row :gutter="20">
        <el-form-item label="说明" v-show="descStr">
          <div>
            {{ descStr }}
          </div>
        </el-form-item>
      </el-row>
    </el-form>

    <div style="text-align: center;">
      <el-button @click="close">取 消</el-button>
      <el-button type="primary"
                 :disabled="disabled"
                 @click="submit">确 定
      </el-button>
    </div>
  </el-dialog>
</template>

<script setup>
import {tableNoPage} from "@/service/train";
import {watchEffect} from "vue"
import {getNextTaskItem} from "@/service/plan/plancontent"
import {getById} from "@/service/plan/planmanage";
import {ElMessage} from "element-plus";
import {getByLineId} from "@/service/yard";
import {table as yardTeamTable} from "@/service/yardteam"

let title = $ref('添加 提前执行的任务');
let formdata = $ref({});
let lineId = $ref("")
let trains = $ref([]);
let visible = $ref(false);
const emit = defineEmits(['afterSubmit']);
let tableData = $ref(null);
let descStr = $ref("")
let disabled = $ref(true);
let yardList = $ref([]);
let taskSiteList = $ref([]);  // 检修场地，最多两个，即检修库和运用库
let yardTeamList = $ref([]);

const init = async function (data, line_id) {
  lineId = line_id;
  tableData = data;
  visible = true;
  let result = await tableNoPage(lineId);
  trains = result.data;
  await renderYardList(lineId);
};

const renderYardList = async function () {
  let res = await getByLineId(lineId);
  yardList = res.data;
};

watchEffect(async function () {
  if (formdata.trainId && formdata.taskType) {
    // 怎么获取该日计划之后的内容。
    // 拿到日计划的开始时间、
    let scheduleId = tableData.at(0).scheduleId;
    let result = await getById(scheduleId);

    // 获取下一个计划，即用于提前的任务
    let item = await getNextTaskItem(result.data.startTime, formdata.taskType, formdata.trainId)
    if (item.data) {
      descStr = "将 " + item.data.planDate + " 的 " + item.data.taskType + " 提前到今日( " + result.data.startTime + " ) 执行. "
      if (item.data.taskContent) {
        descStr += " 检修模式为：" + item.data.taskContent;
        formdata.taskContent = item.data.taskContent;
        formdata.applyMonth = item.data.applyMonth;
      }
      if (formdata.duration) {
        formdata.duration = item.data.duration;
      } else {
        formdata.duration = 1;
      }
      descStr += ", 持续时间：" + item.data.duration + "天";
    } else {
      ElMessage.info("无法获取下一次待执行该种检修任务");
      formdata.duration = 1;
      descStr = ""
      disabled = true;
    }
  }
}, {deep: true});

watchEffect(async function () {
  if (formdata.taskSegment) {
    let item = yardList.find(i => {
      return i.name === formdata.taskSegment
    })
    let taskSegmentId = item.id;
    let arr = [];
    if (item.hasServiceShop) {
      arr.push("检修库");
    }
    if (item.hasOperationShop) {
      arr.push("运用库");
    }
    taskSiteList = arr;

    let res = await yardTeamTable(taskSegmentId);
    let data = res.data
    yardTeamList = [];
    data.forEach(i => {
      for (let j = 0; j < i.num; j++) {
        let k = j + 1;
        yardTeamList.push(i.teamType + k);
      }
    })
  }
}, {deep: true});

watchEffect(function () {
  if (formdata.trainId &&
      formdata.taskType &&
      formdata.taskSegment &&
      formdata.taskSite &&
      formdata.taskTeam &&
      formdata.duration &&
      formdata.offsetDay
  ) {
    disabled = false;
  }
}, {deep: true})

const close = function () {
  formdata = {}
  descStr = ""
  visible = false;
  disabled = true;
};

const submit = function () {
  emit("afterSubmit", formdata)
  visible = false
  close();
};


defineExpose({
  init,
});


</script>

<style scoped>

</style>
