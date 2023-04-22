<template>
  <el-dialog append-to-body :title="title" v-model="visible" width="30%" :before-close="close">

    <el-form ref="form"
             v-model="formdata"
    >
      <el-form-item label="任务提前或延后至" prop="changeTime">
        <el-date-picker v-model="formdata.changeTime"
                        type="date"
                        format="YYYY-MM-DD"
                        :disabled-date="disableConfig"
                        :placeholder="formdata.changeTime"
                        style="width: 60%"
                        value-format="YYYY-MM-DD">
        </el-date-picker>
      </el-form-item>
    </el-form>

    <div slot="footer"
         class="dialog-footer">
      <el-button @click="close">取 消</el-button>
      <el-button type="primary"
                 @click="submit">确 定
      </el-button>
    </div>
  </el-dialog>
</template>

<script setup>

import moment from "moment";

let title = $ref('检修任务提前或延后');
let formdata = $ref([]);
let visible = $ref(false);
let sdate = $ref('');
let edate = $ref('');
const emit = defineEmits(['afterSubmit']);
let id = ''
//设置时间约束:在计划范围内选择
const disableConfig = function (time){
  let isbetween = moment(time).isBetween(sdate,edate,null,'[]');
  return !isbetween
}

const init = function (id2, sDate,eDate) {
  sdate = sDate;
  edate = eDate;
  id = id2;

  formdata.changeTime = moment().format('YYYY-MM-DD')
  visible = true;
};

const close = function () {
  formdata=[]
  visible = false;
};

const submit = function () {
  emit("afterSubmit",formdata)
  visible = false
};



defineExpose({
  init,
});


</script>

<style scoped>
.dialog-footer{
  display: flex;
  justify-content: center;
}
</style>
