<template>
  <el-dialog :title="title" v-model="visible" width="50%" :before-close="close">
    <el-form ref="form"
             v-model="formdata"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="车库编码">
            <el-input v-model="formdata.id" :disabled="!isNew"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="车场名称">
            <el-input v-model="formdata.name"
                      autocomplete="off"
                      :disabled="!isNew && !edit"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="车场-经度">
            <el-input v-model="formdata.longitude"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="车场-纬度">
            <el-input v-model="formdata.latitude"
                      autocomplete="off"
                      :disabled="!isNew && !edit"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="是否为车辆段">
            <el-radio-group v-model="formdata.beDepot">
              <el-radio :label="true">是</el-radio>
              <el-radio :label="false">否</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="是否有检修库" v-show="formdata.beDepot">
            <el-radio-group v-model="formdata.hasServiceShop">
              <el-radio :label="true">是</el-radio>
              <el-radio :label="false">否</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-show="formdata.beDepot" label="是否有运用库">
            <el-radio-group v-model="formdata.hasOperationShop">
              <el-radio :label="true">是</el-radio>
              <el-radio :label="false">否</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="检修库-股道数量(根)" v-show="formdata.hasServiceShop && formdata.beDepot">
            <el-input v-model="formdata.serviceShopTrackwayNum">
              <el-radio :label="true">是</el-radio>
              <el-radio :label="false">否</el-radio>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="运用库-股道数量(根)" v-show="formdata.hasOperationShop && formdata.beDepot">
            <el-input v-model="formdata.operationShopTrackwayNum">
              <el-radio :label="true">是</el-radio>
              <el-radio :label="false">否</el-radio>
            </el-input>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div slot="footer"
         class="dialog-footer">
      <el-button @click="visible = false">取 消</el-button>
      <el-button type="primary"
                 @click="submit">确 定
      </el-button>
    </div>
  </el-dialog>
</template>

<script setup>
import {add, getById, update} from '@/service/yard.js'
import {get} from "@/utils/request";
import {ElMessage} from "element-plus";
import {watch} from 'vue'

const emit = defineEmits(['afterSubmit']);
let isNew = $computed(() => {
  return yardId === ''
})
let title = $computed(() => {
  return isNew ? '车场新增' : '车场信息修改'
})
let yardId = $ref('');
let formdata = $ref('');
let visible = $ref(false);
let edit = $ref(false);
let form = $ref(null);
let lines = $ref([]);

const init = async function (id, editable) {
  yardId = id;
  edit = editable
  formdata = ''
  form = null;
  if (isNew) {
    formdata = {}
  } else {
    let body = await getById(yardId);
    formdata = body.data
  }
  visible = true;
};

const close = function () {
  form.resetFields();
  visible = false;
};

const submit = async function () {
  let tempFormdata = JSON.parse(JSON.stringify(formdata));
  if (!tempFormdata.beDepot) {
    tempFormdata.hasServiceShop = false;
    tempFormdata.hasOperationShop = false;
  }
  if (!tempFormdata.hasServiceShop) {
    tempFormdata.serviceShopTrackwayNum = 0;
  }
  if (!tempFormdata.hasOperationShop) {
    tempFormdata.operationShopTrackwayNum = 0;
  }
  //formdata.skills = formdata.skills.join("+")//把列表改成字符串
  if (isNew) {
    let r = await add(tempFormdata)
    if (r.code == 0) {
      emit("afterSubmit");
      visible = false;
    } else {
      ElMessage(r.msg);
    }
  } else {
    await update(tempFormdata)
        .then(r => {
          emit("afterSubmit");
          visible = false;
        });
  }
};

defineExpose({
  init,
});
</script>

<style scoped>

</style>
