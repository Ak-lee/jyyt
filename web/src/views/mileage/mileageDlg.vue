<template>
  <el-dialog
      :title="title"
      v-model="visible"
      width="25%"
      :before-close="close"
      style="border: 1px solid red;"
  >

    <el-form ref="form"
             v-model="formdata"
    >

      <el-form-item label="列车号"
                    :label-width="120">
        <el-input v-model="formdata.trainId"
                  autocomplete="off"
                  v-bind:disabled="!isInsert"
        ></el-input>
      </el-form-item>
      <el-form-item label="日期"
                    :label-width="120">
        <el-date-picker
            v-model="formdata.date"
            type="date"
            placeholder="请选择日期"
            v-bind:disabled="!isInsert"
        />
      </el-form-item>
      <el-form-item label="里程"
                    :label-width="120">
        <el-input v-model="formdata.mileage"
                  autocomplete="off"></el-input>
      </el-form-item>

      <el-form-item
          label="校验结果"
      >
        <span>{{ reviewMsg }}</span>
      </el-form-item>
    </el-form>
    <div slot="footer"
         v-show="!showStations"
         class="dialog-footer">
      <el-button @click="visible = false">取 消</el-button>
      <el-button type="warning" @click="reviewItem">校 验</el-button>
      <el-button type="primary" @click="submit" v-if="isInsert" v-bind:disabled="!status">提 交</el-button>
      <el-button type="primary" @click="updateItem" v-if="!isInsert" v-bind:disabled="!status">更 新</el-button>
    </div>
  </el-dialog>

</template>

<script setup>
import {ref, reactive} from "vue";
import {add, getById, update} from '@/service/line'
import {post} from "@/utils/request";

const emit = defineEmits(['afterSubmit']);

let formdata = $ref({});
let visible = $ref(false)
let reviewMsg = $ref("");
let status = $ref(false);
let isInsert = $ref(true)

let selectCondtion = {};

const init = async function (rowId, trainId, date, mileage, isInsert2) {
  formdata.id = rowId;
  formdata.trainId = trainId;
  formdata.date = date;
  formdata.mileage = mileage;
  selectCondtion.trainId = trainId;
  selectCondtion.date = date;
  // 前端读取 excel 返回的日期是一个 long 数
  // 后端数据库返回的日期是一个字符串。
  if (isInsert2 && isNaN(Number(date))) {
    formdata.date = "";
  }
  status = false;
  reviewMsg = "";
  visible = true
  isInsert = isInsert2;
};

const close = function () {
  formdata = {};
  visible = false;
};

const reviewItem = async function () {
  reviewMsg = '';
  var flag = true
  if (formdata.date === '') {
    reviewMsg += "日期必填；"
    flag = false;
  }
  if (formdata.trainId === "") {
    reviewMsg += "列车号不能为空";
    flag = false;
  }
  if (formdata.mileage === "") {
    reviewMsg += "里程数据不能为空"
    flag = false;
  }
  if (isNaN(Number(formdata.mileage))) {
    reviewMsg += "里程数据解析失败；"
    flag = false;
  }
  if (flag && isInsert) {
    await reviewOnline();
  }
  if (flag && !isInsert) {
    reviewMsg = "检查通过"
    status = true;
  }
}

const reviewOnline = async function () {
  let res = await post("/api/excel/reviewItem", formdata)
  if (res.type === "新增") {
    reviewMsg = "检查通过"
    status = true;
  } else {
    reviewMsg += res.type;
  }
}

const submit = async function () {
  await post("/api/excel/saveItem", formdata,)
  emit("afterSubmit", formdata)
  visible = false;
};

const updateItem = async function () {
  let obj = {};
  obj.mileageHistory = formdata;
  obj.trainId = selectCondtion.trainId;
  obj.date = selectCondtion.date;
  await post("/api/excel/updateItem", obj)
  emit("afterSubmit", formdata)
  visible = false;
}

defineExpose({
  init,
});
</script>

<style scoped>

</style>
