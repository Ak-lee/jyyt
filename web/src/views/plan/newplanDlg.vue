<template>
  <el-dialog :title="title" v-model="visible" width="50%" :before-close="close">
    <el-form ref="formRef"
             :model="formdata"
             v-model="formdata"
             v-show="!showStations"
             :rules="rules"
             label-width="30%"
    >
      <el-row>
        <div style="color: red; font-size:16px;margin-bottom: 10px;">新建计划前请确保上一级计划已创建并下发（年计划除外）</div>
        <el-col :span="24">
          <el-form-item label="所属线路" prop="lineId">
            <el-select v-model="formdata.lineId"
                       filterable
                       clearable
                       :placeholder="formdata.lineId"
                       style="width: 60%">
              <el-option
                  :key="index" v-for="(item, index) in linesWithStatus"
                  :disabled="item.disabled"
                  :label="item.lineName"
                  :value="item.lineId"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row style="display:flex;justify-content: center">
        <el-col :span="9">
          <span>格式：{{ planoptions[plantype] }}+线路号+年份+4位编号</span>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-form-item label="任务编号" prop="id">
            <el-input v-model="formdata.id" style="width: 60%"
                      :placeholder="'编号形式如：'+planoptions[plantype]+'1720220001'"/>
          </el-form-item>
        </el-col>

      </el-row>

      <el-row>
        <el-col :span="24">
          <el-form-item label="任务名称" prop="name">
            <el-input v-model="formdata.name" style="width: 60%"/>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="24">
          <el-form-item label="计划制定时间" prop="makeTime">
            <el-date-picker v-model="formdata.makeTime"
                            type="date"
                            format="YYYY-MM-DD"
                            :placeholder="formdata.makeTime"
                            style="width: 60%"
                            value-format="YYYY-MM-DD"
                            disabled>
            </el-date-picker>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="24">
          <el-form-item label="计划开始时间"
                        prop="startTime">
            <el-date-picker v-model="formdata.startTime"
                            type="date"
                            format="YYYY-MM-DD"
                            :placeholder="formdata.startTime"
                            :disabled-date="disableConfigstart"
                            style="width: 60%"
                            value-format="YYYY-MM-DD">
            </el-date-picker>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="24">
          <el-form-item label="计划结束时间"
                        prop="endTime">
            <el-date-picker v-model="formdata.endTime"
                            type="date"
                            format="YYYY-MM-DD"
                            :placeholder="formdata.endTime"
                            :disabled-date="disableConfigend"
                            style="width: 60%"
                            value-format="YYYY-MM-DD">
            </el-date-picker>
          </el-form-item>
        </el-col>
      </el-row>

    </el-form>

    <div
        v-show="!showStations"
        class="dialog-footer"
        style="display: flex;justify-content: center">
      <el-button type="primary"
                 @click="submit(formRef)">确 定
      </el-button>
      <el-button @click="visible = false">取 消</el-button>
    </div>
  </el-dialog>
</template>

<script setup>
import {add, tableDataAllNoPage} from '@/service/plan/planmanage'
import {selectLine} from "@/service/selector"
import {ref} from "vue";
import {ElMessage} from "element-plus";
import moment from "moment";

const emit = defineEmits(['afterSubmit']);

let title = $computed(() => {
  return '新增' + plantype
})
let plantype = $ref('')
let formdata = $ref('');
let visible = $ref(false);
let showStations = $ref(false);
let lines = $ref([]);
let tableAlready = $ref([]);
let prevLevelPlan = $ref([]);
let planoptions = $ref({'年计划': 'Y', '月计划': 'M', '周计划': 'W', '日计划': 'D'})
let dateoptions = $ref({'年计划': 'years', '月计划': 'months', '周计划': 'weeks', '日计划': 'days'})
//校验规则
let rules = $ref({
  lineId: [{required: true, message: '请选择所属线路', trigger: 'change'}],
  id: [{required: true, message: '请输入任务编号', trigger: 'blur'}],
  name: [{required: true, message: '请输入任务名称', trigger: 'blur'}],
  makeTime: [{required: true, message: '请选择制定时间', trigger: 'change'}],
  startTime: [{required: true, message: '请选择制定时间', trigger: 'change'}],
  endTime: [{required: true, message: '请选择制定时间', trigger: 'change'}],
})
const formRef = ref('');

//设置开始时间约束
const disableConfigstart = function (time) {
  return time.getTime() <= Date.now()
}

//设置结束时间约束
const disableConfigend = function (time) {
  return time.getTime() < Date.now() + (3600 * 1000 * 24)
}

//获取当前日期函数
const getNowFormatDate = function () {
  let date = new Date(),
      seperator1 = '-', //格式分隔符
      year = date.getFullYear(), //获取完整的年份(4位)
      month = date.getMonth() + 1, //获取当前月份(0-11,0代表1月)
      strDate = date.getDate() // 获取当前日(1-31)
  if (month >= 1 && month <= 9) month = '0' + month // 如果月份是个位数，在前面补0
  if (strDate >= 0 && strDate <= 9) strDate = '0' + strDate // 如果日是个位数，在前面补0
  let currentdate = year + seperator1 + month + seperator1 + strDate
  return currentdate
}

const linesWithStatus = $computed(() => {
  let arr = [];

  arr = [...lines];

  tableAlready.forEach(j => {
    arr.forEach(k => {
      if (k.lineId === j.lineId) {
        k.disabled = true;
      }
    })
  })

  arr.forEach(m => {
    // 如果没有 disabled, 检查上一级计划
    if (!m.disabled) {
      if (prevLevelPlan.length) {
        let flag = false;
        prevLevelPlan.forEach(n => {
          if (m.lineId === n.lineId) {
            flag = true;
          }
        })
        if (!flag) {
          // 若不存在上一级目录
          m.disabled = true;
        }
      }
    }
  })
  return arr;
})

const init = async function (planType) {
  plantype = planType
  formdata = {};
  //加载线路列表
  let resline;
  resline = await selectLine();
  resline.forEach(i => lines.push(
      {
        "lineName": i.name,
        "lineId": i.id
      }
  ));
  let data = await tableDataAllNoPage(planType);

  tableAlready = data.list;

  let prevLevelPlanType = "";
  switch (planType) {
    case "月计划":
      prevLevelPlanType = "年计划";
      break;
    case "周计划":
      prevLevelPlanType = "月计划";
      break;
    case "日计划":
      prevLevelPlanType = "周计划";
      break;
  }
  if (prevLevelPlanType) {
    data = await tableDataAllNoPage(prevLevelPlanType)
    prevLevelPlan = data.list;
  }

  formdata.makeTime = getNowFormatDate();
  formdata.startTime = moment(formdata.makeTime).add(1, dateoptions.日计划).format('YYYY-MM-DD')
  formdata.endTime = moment(formdata.endTime).add(1, dateoptions[plantype]).format('YYYY-MM-DD')
  visible = true;
};

const close = function () {
  visible = false;
  plantype = '';
  formdata = '';
  lines = [];
};

const submit = async function (formEl) {
  let flag = 0;
  await formEl.validate((valid) => {
    if (!valid) {
      flag = 1;
      ElMessage("数据校验失败！请调整数据后重试")
    }
  })

  formdata.planType = plantype
  formdata.year = formdata.startTime.substring(0, 4)
  //如果校验成功，提交
  if (flag === 0) {
    let result = await add(formdata);
    if (result.code == 0) {
      emit("afterSubmit")
      visible = false;
      ElMessage.success("计划新增成功");
    } else {
      ElMessage.error(result.msg);
    }
  }
};


defineExpose({
  init,
});
</script>

<style scoped>

</style>
