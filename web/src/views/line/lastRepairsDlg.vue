<template>
  <el-dialog class="container" :title="title" v-model="visible" width="45%" :before-close="close">

    <el-form ref="form"
             :model="formdata"
    >
      <el-row :gutter="10">
        <el-col :span="10">
          <el-form-item label="线路名称" :label-width="120">
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
          <el-form-item label="车辆编号"
                        :label-width="120">
            <el-input v-model="formdata.trainId"
                      :disabled="!isNew && edit"
                      autocomplete="off"
            ></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="10">
          <el-form-item label="里程检" :label-width="120">
            <el-date-picker
                v-model="formdata.mileageCheck"
                value-format="YYYY-MM-DD"
                format="YYYY-MM-DD"
                :disabled="!edit"
                autocomplete="off"
            />
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="登顶检"
                        :label-width="120">
            <el-date-picker
                v-model="formdata.topCheck"
                value-format="YYYY-MM-DD"
                format="YYYY-MM-DD"
                :disabled="!edit"
                autocomplete="off"
            />

          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="10">
          <el-form-item label="均衡修-时间"
                        :label-width="120">
            <el-date-picker
                v-model="formdata.balancedRepairDate"
                value-format="YYYY-MM-DD"
                format="YYYY-MM-DD"
                :disabled="!edit"
                autocomplete="off"
            />
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="均衡修-检修编号"
                        :label-width="120">
            <el-input v-model="formdata.balancedRepair"
                      :disabled="!edit"
                      autocomplete="off"
            ></el-input>
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
import {get} from "@/utils/request";
import {add, getById, update, table} from '@/service/lastRepairs'

const emit = defineEmits(['afterSubmit']);

let isNew = $computed(() => {
  return lastRepairsId === ''
})

let trainId = $ref('CD17001');
let lastRepairsId = $ref('');
let formdata = $ref('');
let lines = $ref([]);
let visible = $ref(false);
let edit = $ref(false);
let form = $ref(null);


const init = async function (id, editable) {
  await selectLine();
  lastRepairsId = id;
  edit = editable
  if (isNew) {
    formdata = {}
  } else {
    let body = await getById(lastRepairsId);
    formdata = body.data
  }
  visible = true;
};

const close = function () {
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
