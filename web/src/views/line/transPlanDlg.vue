<template>
  <el-dialog class="container" :title="title" v-model="visible" width="45%" :before-close="close">

    <el-form ref="form"
             :model="formdata"
             :rules="rules"
    >
      <el-row :gutter="10">
        <el-col :span="10">
          <el-form-item label="线路名称" :label-width="120" prop="lineId">
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
        <el-col :span="10">
          <el-form-item label="运输适用类型"
                        :label-width="120" prop="applicableTime">
            <el-select
                class="selector"
                v-model="formdata.applicableTime"
                :disabled="!isNew && !edit"
                filterable
                clearable
                placeholder="请选择">
              <el-option
                  :key="index" v-for="(item, index) in times"
                  :label="item.label"
                  :value="item.value"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="10">
        <el-col :span="10">
          <el-form-item label="出库位置"
                        :label-width="120" prop="outstorageSite">
            <el-input v-model="formdata.outstorageSite"
                      :disabled="!edit"
                      autocomplete="off"
            ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="入库位置"
                        :label-width="120" prop="instorageSite">
            <el-input v-model="formdata.instorageSite"
                      :disabled="!edit"
                      autocomplete="off"
            ></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="10">
        <el-col :span="10">
          <el-form-item label="出车场时间"
                        :label-width="120" prop="outyardTime">
            <el-time-picker
                v-model="formdata.outyardTime"
                format="HH:mm:ss"
                value-format="HH:mm:ss"
                :disabled="!edit"
                autocomplete="off"
            />
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="回车场时间"
                        :label-width="120" prop="inyardTime">
            <el-time-picker
                v-model="formdata.inyardTime"
                format="HH:mm:ss"
                value-format="HH:mm:ss"
                :disabled="!edit"
                autocomplete="off"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="10">
          <el-form-item label="车底ID"
                        :label-width="120" prop="undercarId">
            <el-input v-model="formdata.undercarId"
                      autocomplete="off"
                      :disabled="!isNew && edit"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div slot="footer"
         v-show="!showStations"
         class="dialog-footer">
      <el-button @click="visible = false">取 消</el-button>
      <el-button type="primary"
                 @click="submit">确 定
      </el-button>
    </div>
  </el-dialog>

</template>

<script setup>
import {ref, reactive} from "vue";
import {get} from "@/utils/request";
import {add, getById, update, table} from '@/service/transplan'


const emit = defineEmits(['afterSubmit']);

let isNew = $computed(() => {
  return transPlanId === ''
})

let title = $computed(() => {
  return isNew ? '新增运输任务' : '运输任务编辑'
})

//校验规则
let rules = $ref({
  lineId: [{required: true, message: '请选择所属线路', trigger: 'change'}],
  applicableTime: [{required: true, message: '请输入', trigger: 'change'}],
  undercarId: [{required: true, message: '请输入', trigger: 'blur'}],
})


let transPlanId = $ref('');
let formdata = $ref('');
let lines = $ref([]);
let visible = $ref(false);
let edit = $ref(false);
let form = $ref(null);
let times = $ref([{
  label: '工作日',
  value: 'workday'
}, {
  label: '周末',
  value: 'weekday'
}, {
  label: '节假日',
  value: 'holiday'
}]);

const init = async function (id, editable) {
  await selectLine();
  transPlanId = id;
  edit = editable
  if (isNew) {
    formdata = {}
    // multiTrainRouting = true
  } else {
    let body = await getById(transPlanId);
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
