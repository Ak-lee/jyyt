<template>
  <el-dialog class="container" :title="title" v-model="visible" :before-close="close" width="60%">
    <div>
      <el-table
          max-height="400"
          :data="formdata" border>
        <el-table-column align="center" type="index" label="序号"/>
        <el-table-column prop="date" align="center" label="日期"/>
        <el-table-column prop="weektime" align="center" label="星期"/>
        <el-table-column align="center" label="属性">
          <template #default="{row}">
            <el-select @change="(e) => handleChange(e, row)" v-model="row.attribute">
              <el-option label="工作" value="工作"/>
              <el-option label="休息" value="休息"/>
            </el-select>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </el-dialog>

</template>

<script setup>
import {tableWithCond, update} from "@/service/workcalendar.js";
import {ElMessage} from "element-plus";
import moment from "moment";

const emit = defineEmits(['afterSubmit'])

let formdata = $ref('');
let visible = $ref(false);
let calendarId = $ref('');
let year = $ref('');
let month = $ref('');

let title = $computed(() => {
  return year + "年 " + month + " 月， 生产日历详情";
})

let handleChange = async function (e, row) {
  row.attribute = e;

  let result = await update(row);
  if (result.code == 0) {
    ElMessage.success("更新成功");
  } else {
    ElMessage.error("更新失败");
  }
}

const init = async function (calendarId_, year_, month_) {
  let result = await tableWithCond(calendarId_, year_, month_);
  calendarId = calendarId_;
  year = year_;
  month = month_;
  formdata = result.list;

  let weekdaysoption = ["日", "一", "二", "三", "四", "五", "六"];
  formdata.forEach(i => {
    i.date = moment(i.date).format("YYYY-MM-DD")
    i.weektime = weekdaysoption[moment(i.date).day()] //星期渲染
  })
  visible = true;
};

const close = function () {
  visible = false;
  formdata = '';
  calendarId = '';
  year = '';
  month = '';
  emit("afterSubmit")
}

defineExpose({
  init,
});
</script>

<style scoped>

</style>