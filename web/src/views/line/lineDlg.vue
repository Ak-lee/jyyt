<template>
  <el-dialog :title="title" v-model="visible" width="40%" :before-close="close">

    <el-form ref="form"
             v-model="formdata"
             v-show="!showStations"
    >
      <el-form-item label="线路号" :label-width="140">
        <el-input
            v-model="formdata.id"
            :disabled="!isNew"
        ></el-input>
      </el-form-item>
      <el-form-item label="线路名称"
                    :label-width="140">
        <el-input v-model="formdata.name"
                  autocomplete="off"
                  :disabled="!edit"></el-input>
      </el-form-item>
      <el-form-item label="线路长度（千米）"
                    :label-width="140">
        <el-input v-model="formdata.lineLength"
                  :disabled="!edit"
                  placeholder="单位（千米）"
                  autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="单程运行时间(分钟)"
                    :label-width="140">
        <el-input v-model="formdata.journeyTime"
                  :disabled="!edit"
                  placeholder="单位（分钟）"
                  autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="备注信息" :label-width="140">
        <el-input v-model="formdata.remark" type="textarea" :disabled="!edit"/>
      </el-form-item>
    </el-form>
    <div slot="footer"
         v-show="!showStations"
         class="dialog-footer">
      <el-button @click="visible = false">取 消</el-button>
      <el-button type="primary"
                 @click="submit">确 定
      </el-button>
    </div>
    <el-table v-show="showStations"
              :data="staTable"
    >
      <el-table-column prop="id" label="车站编号" width="180"/>
      <el-table-column prop="name" label="车站名称" width="180"/>
      <el-table-column prop="nearYard" label="附近车场" width="180"/>
      <el-table-column prop="belongto" label="所在区" width="180"/>
    </el-table>

    <div slot="footer"
         v-show="showStations"
         class="dialog-footer">
      <el-button type="primary"
                 @click="toLine">确 定
      </el-button>
      <el-button @click="toLine">取 消</el-button>
    </div>
  </el-dialog>

</template>

<script setup>
import {ref, reactive} from "vue";
import {add, getById, update} from '@/service/line'
import {table} from '@/service/station'
import {ElMessage} from "element-plus";

const emit = defineEmits(['afterSubmit']);

let isNew = $computed(() => {
  return lineId === ''
})
let title = $computed(() => {
  return isNew ? '新建' : '修改'
})
let lineId = $ref('');
let formdata = $ref('');

let visible = $ref(false);
let edit = $ref(false);
let showStations = $ref(false);
let staTable = $ref([]);
let form = $ref(null);


const toLine = function () {
  showStations = false;
};
const init = async function (id, editable) {
  lineId = id;
  edit = editable
  if (isNew) {
    formdata = {}
  } else {
    let body = await getById(lineId);
    formdata = body.data
  }
  visible = true;
};

const close = function () {
  form.resetFields();
  visible = false;
};

const submit = async function () {
  if (isNew) {
    let r = await add(formdata);
    if (r.code == 0) {
      emit("afterSubmit");
      visible = false;
    } else {
      ElMessage(r.msg);
    }

  } else {
    await update(formdata);
    emit("afterSubmit");
    visible = false;
  }

};

defineExpose({
  init,
});
</script>

<style scoped>

</style>
