<template>
  <el-dialog class="container" :title="title" v-model="visible" width="40%" :before-close="close">

    <el-form ref="form"
             :model="formdata"
             :rules="rules"
    >
      <el-col :span="15">
        <el-form-item label="线路名称" :label-width="200" prop="lineId">
          <el-select v-model="formdata.lineId"
                     filterable
                     clearable
                     :disabled="!isNew && edit"
                     :placeholder="formdata.lineId">
            <el-option
                :key="index" v-for="(item, index) in lines"
                :label="item.name"
                :value="item.id"
            />
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="15">
        <el-form-item label="单计划日最大均衡修数量(个)"
                      :label-width="200" prop="maxBalancedRepairs">
          <el-input v-model="formdata.maxBalancedRepairs"
                    :disabled="!edit"
                    autocomplete="off"
          ></el-input>
        </el-form-item>
      </el-col>

      <el-col :span="15">
        <el-form-item label="单计划日最大里程检数量(个)"
                      :label-width="200" prop="maxMileageChecks">
          <el-input v-model="formdata.maxMileageChecks"
                    :disabled="!edit"
                    autocomplete="off"
          ></el-input>
        </el-form-item>
      </el-col>
    </el-form>
    <div slot="footer"
         class="dialog-footer">
      <el-button size="small" @click="visible = false">取 消</el-button>
      <el-button size="small" type="primary"
                 @click="submit">确 定
      </el-button>
    </div>
  </el-dialog>

</template>

<script setup>
import {get} from "@/utils/request";
import {add, getById, update, table} from '@/service/constraint'

const emit = defineEmits(['afterSubmit']);
let isNew = $computed(() => {
  return onedayMaxId === ''
})

//校验规则
let rules = $ref({
  lineId: [{required: true, message: '请选择所属线路', trigger: 'blur'}],
  maxBalancedRepairs: [{required: true, message: '请输入', trigger: 'blur'}],
  maxMileageChecks: [{required: true, message: '请输入', trigger: 'blur'}],
})

let onedayMaxId = $ref('');
let formdata = $ref('');
let lines = $ref([]);
let visible = $ref(false);
let edit = $ref(false);
let form = $ref('');
const init = async function (id, editable) {
  await selectLine();
  onedayMaxId = id;
  edit = editable
  if (isNew) {
    formdata = {}
  } else {
    let body = await getById(onedayMaxId);
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
    await add(formdata)
        .then(r => {
          emit("afterSubmit");
          visible = false;
        });
  } else {
    await update(formdata)
        .then(r => {
          emit("afterSubmit");
          visible = false;
        });
  }

};

const selectLine = async function () {
  get("/api/line_list")
      .then(result => {
        lines = [];
        result.forEach(i => lines.push(
            {
              "name": i.name,
              "id": i.id
            }
        ))
      }, () => {
        lines = []
        console.log("⽹络请求失败")
      })
};

defineExpose({
  init,
});
</script>

<style scoped>
</style>
