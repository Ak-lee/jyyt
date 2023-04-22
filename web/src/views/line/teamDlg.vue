<template>
  <el-dialog :title="title" v-model="visible" width="50%" :before-close="close">

    <el-form ref="form"
             v-model="formdata"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="检修班组名称">
            <el-input v-model="formdata.teamType"
                      autocomplete="off"
                      :disabled="!isNew && edit"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="技能掌握类型">
            <el-select v-model="formdata.skills" multiple clearable placeholder="点击选择" :disabled="!isNew && !edit">
              <el-option label="里程检" value="里程检"/>
              <el-option label="登顶检" value="登顶检"/>
              <el-option label="均衡修" value="均衡修"/>
              <el-option label="季节专检" value="季节专检"/>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="班组人员数量">
            <el-input v-model="formdata.staffNum"
                      :disabled="!edit"
                      autocomplete="off"
            ></el-input>
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
import {add, getById, update} from '@/service/team.js'
import {get} from "@/utils/request";
// import {ref, reactive} from "vue";

const emit = defineEmits(['afterSubmit']);
let isNew = $computed(() => {
  return teamId === ''
})
let title = $computed(() => {
  return isNew ? '检修班组新增' : '班组信息修改'
})
let teamId = $ref('');
let formdata = $ref('');
let visible = $ref(false);
let edit = $ref(false);
let form = $ref(null);

const init = async function (id, editable) {
  teamId = id;
  edit = editable
  formdata = ''
  form = null;
  if (isNew) {
    formdata = {}
  } else {
    let body = await getById(teamId);
    formdata = body.data
    formdata.skills = formdata.skills.split("+")
  }
  visible = true;
};

const close = function () {
  form.resetFields();
  visible = false;
};

const submit = async function () {
  formdata.skills = formdata.skills.join("+")//把列表改成字符串
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

defineExpose({
  init,
});

</script>

<style scoped>

</style>
