<template>
  <el-dialog :title="title" v-model="visible" width="50%" :before-close="close">
    <el-form ref="formRef"
             :model="formdata"
             v-model="formdata"
             v-show="!showStations"
             label-width="40%"
    >
      <el-form-item label="所属线路"
                    prop="lineId"
                    :rules="[
                            {required: true,message: '请选择所属线路', trigger:'change'}
                            ]">
        <el-select v-model="formdata.lineId"
                   filterable
                   clearable
                   :disabled="!isNew && edit"
                   :placeholder="formdata.lineId">
          <el-option
              :key="index" v-for="(item, index) in lines"
              :label="item.lineName"
              :value="item.lineId"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="检修计划类型"
                    prop="name"
                    :rules="[
                            {required: true,message: '请选择检修计划类型', trigger:'change'}
                            ]">
        <el-select v-model="formdata.name"
                   filterable
                   clearable
                   :disabled="!isNew && edit"
                   :placeholder="formdata.name">
          <el-option label="年计划" value="年计划" />
          <el-option label="月计划" value="月计划" />
          <el-option label="周计划" value="周计划" />
          <el-option label="日计划" value="日计划" />
        </el-select>
      </el-form-item>
      <el-form-item label="针对的检修任务类型"
                    prop="tasktypeId">
        <el-select v-model="formdata.tasktypeId"
                   filterable
                   clearable
                   :disabled="!edit"
                   :placeholder="formdata.tasktypeId">
          <el-option
              :key="index" v-for="(item, index) in tasktypes"
              :label="item.taskTypeName"
              :value="item.typeId"
          />
        </el-select>
      </el-form-item>
    </el-form>

    <div slot="footer"
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
import {add, getById, table, update} from '@/service/plantype'
import {selectLine, selectTasktype} from "@/service/selector"
import {ref} from "vue";

const emit = defineEmits(['afterSubmit']);

let isNew = $computed(() => {
  return plantypeId === ''
})
let title = $computed(() => {
  return isNew ? '新建检修计划类型' : '检修计划类型编辑'
})
let plantypeId = $ref('');
let formdata = $ref('');
let visible = $ref(false);
let edit = $ref(false);
let showStations = $ref(false);
let lines = $ref([]);
let tasktypes = $ref([]);

const formRef = ref('');

const init = async function (id, editable) {
  plantypeId = id;
  edit = editable;
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
  //加载检修任务类型列表
  let restype;
  restype = await selectTasktype();
  restype.forEach(i => tasktypes.push(
      {
        "taskTypeName": i.taskTypeName,
        "typeId": i.id,
      }
  ));

  if (isNew) {
    formdata = {};
  } else {
    let body = await getById(plantypeId);
    formdata = body.data
  }
  visible = true;
};

const close = function () {
  visible = false;
};

const submit = async function (formEl) {
  await formEl.validateField((valid) => {
    if (valid){
      //检验成功
      console.log("校验成功！");
    }else {
      //校验失败
      console.log("校验失败！");
      alert("校验失败！");
      return
    }
  });

  if (isNew) {
    //一个线路最多有4中计划：年计划、月计划、周计划、日计划
    let body = await table(formdata.lineId,1,4)
    let datatable = body.data.records
    let plantypes = $ref([]);
    let flag = 0;

    datatable.forEach(i => {
      if(i.name===formdata.name){
        alert("此线路中，" + i.name + "已经制定！请选择其他计划类型")
        //校验失败
        console.log("校验失败！");
        flag = 1;
        }
    } )
    //如果校验成功，提交
    if (0===flag){
      await add(formdata)
          .then(r => {
            emit("afterSubmit");
            visible = false;
          });
    }
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
