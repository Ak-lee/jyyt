<template>
  <el-dialog :title="title" v-model="visible" width="500" :before-close="close">
    <el-form ref="formRef"
             :model="formdata"
             label-width="200"
             :rules="rules"
    >
      <el-row :gutter="20">
        <el-form-item label="检修任务名称" prop="taskTypeName">
          <el-input v-model="formdata.taskTypeName"
                    autocomplete="off"
                    :disabled="!isNew && edit"></el-input>
        </el-form-item>
      </el-row>
      <el-row :gutter="20">
        <el-form-item label="里程周期" prop="mileagePeriod">
          <el-input v-model="formdata.mileagePeriod"/>
        </el-form-item>
      </el-row>

      <el-row :gutter="20">
        <el-form-item label="是否为多修程" prop="beMultiMode">
          <el-radio-group v-model="formdata.beMultiMode">
            <el-radio :label="true">是</el-radio>
            <el-radio :label="false">否</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-row>

      <el-row>
        <el-form-item label="时间周期是否使用时间点表示" prop="beAbsoluteTime">
          <el-tooltip
              effect="dark"
              content="通常季节专检使用若干个时间节点表达时间周期，时间点使用英文逗号分隔，如4-30,10-30"
          >
            <el-radio-group v-model="formdata.beAbsoluteTime">
              <el-radio :label="true">是</el-radio>
              <el-radio :label="false">否</el-radio>
            </el-radio-group>
          </el-tooltip>
        </el-form-item>
      </el-row>

      <el-row :gutter="20">
        <el-form-item label="时间周期" prop="timePeriod">
          <el-input v-model="formdata.timePeriod"/>
        </el-form-item>
      </el-row>

      <el-row :gutter="20">
        <el-form-item v-show="formdata.beMultiMode" label="多修程-子修程数量" prop="timePeriod">
          <el-input v-model="formdata.multiModeNum"/>
        </el-form-item>
      </el-row>
    </el-form>


    <div slot="footer"
         class="dialog-footer"
         style="display: flex;justify-content: center">
      <el-button type="primary"
                 @click="submit">确 定
      </el-button>
      <el-button @click="visible = false">取 消</el-button>
    </div>
  </el-dialog>

</template>

<script setup>
import {getById, add, update} from '@/service/type'
import {ref, reactive, watch} from "vue";
import {ElMessage} from "element-plus";

const emit = defineEmits(['afterSubmit']);

let title = $computed(() => {
  return isNew ? '新建检修类型' : '检修类型编辑'
})

let isNew = $ref(false);
let typeId = $ref('');
let formdata = reactive({
  id: 0,
  taskTypeName: '',
  mileagePeriod: 0,
  beMultiMode: false,
  beAbsoluteTime: false,
  timePeriod: '',
  multiModeNum: 1
});
let visible = $ref(false);
const formRef = $ref();

watch(
    () => formdata.beMultiMode,
    (val, preVal) => {
      //val为修改后的值,preVal为修改前的值
      if (preVal && !val) {
        // 从多修程变成了单修程
        formdata.multiModeNum = 1;
      }
    }
)

const validateTimePeriod = (rule, value, callback) => {
  if (formdata.beAbsoluteTime) {
    let dates = value.split(",")
    let re = /^(0[1-9]|1[0-2]|[0-9])-(0[1-9]|1[0-9]|2[0-9]|3[0-1]|[0-9])$/;
    let flag = true;

    dates.forEach((date) => {
      let arr = re.exec(date)
      if (arr) {
        let month = Number(arr[1])
        let day = Number(arr[2])

        switch (month) {
          case 2:   // 2月29日需要在闰年才合法，这里统一判断为不合法，不考虑年的信息
            if (day > 28) {
              flag = false;
            }
            break;
          case 4:
            if (day > 30) flag = false;
            break;
          case 6:
            if (day > 30) flag = false;
            break;
          case 9:
            if (day > 30) flag = false;
            break;
        }
      } else {
        flag = false;
      }
    })
    if (flag) {
      callback(); // 通过校验
    } else {
      callback(new Error("使用时间点模式时，请使用形如 4-30,10-30 的格式输入数据"))
    }
  } else {
    if (isNaN(Number(value))) {
      callback(new Error("不使用时间点模式下，时间周期请输入数字"))
    } else {
      callback()
    }
  }
}

const rules = reactive({
  timePeriod: [{validator: validateTimePeriod, trigger: 'blur'}]
})

const init = async function (id, isNew2) {
  isNew = isNew2;
  typeId = id;
  formdata.id = '';
  formdata.taskTypeName = '';
  formdata.mileagePeriod = 0;
  formdata.beMultiMode = false;
  formdata.beAbsoluteTime = false;
  formdata.timePeriod = '';
  formdata.multiModeNum = 1;

  if (!isNew) {
    let body = await getById(typeId);
    let data = body.data
    formdata.id = data.id;
    formdata.taskTypeName = data.taskTypeName;
    formdata.mileagePeriod = data.mileagePeriod;
    formdata.beMultiMode = data.beMultiMode;
    formdata.beAbsoluteTime = data.beAbsoluteTime;
    formdata.timePeriod = data.timePeriod;
    formdata.multiModeNum = data.multiModeNum;
  }
  visible = true;
};

const close = function () {
  visible = false;
};

const submit = async function () {
  let flag = true
  await formRef.validate((valid) => {
    if (!valid) {
      ElMessage.error("数据校验失败");
      flag = false
      return false;
    }
  })
  if (!flag) {
    return;
  }
  if (isNew) {
    let r = await add(formdata);
    if (r.code == 0) {
      emit("afterSubmit");
      visible = false;
    } else {
      ElMessage.error(r.msg);
    }
  } else {
    let r = await update(formdata);
    if (r.code == 0) {
      ElMessage.success("修改成功");
      emit("afterSubmit");
      visible = false;
    } else {
      ElMessage.error(r.msg);
    }
  }
  emit("afterSubmit");
  visible = false;
};

const reset = function () {
  formRef.resetFields();
}

defineExpose({
  init,
});
</script>

<style scoped>

</style>
