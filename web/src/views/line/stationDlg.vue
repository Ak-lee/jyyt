<template>
  <el-dialog :title="title" v-model="visible" width="50%" :before-close="close">
    <el-form ref="form" :model="formdata" label-width="100px">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="线路选择">
            <el-select v-model="formdata.lineId" :disabled="!isNew">
              <el-option
                  :key="index" v-for="(item, index) in lines"
                  :label="item.name"
                  :value="item.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="12">
          <el-form-item label="站点名称">
            <el-input v-model="formdata.name"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="站点经度">
            <el-input v-model="formdata.longitude"/>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="10">
        <el-col :span="12">
          <el-form-item label="站点纬度">
            <el-input v-model="formdata.latitude"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="附近车场">
            <el-select v-model="formdata.nearYard">
              <el-option
                  :key="index" v-for="(item, index) in yards"
                  :label="item.name"
                  :value="item.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="10">
        <el-col :span="12">
          <el-form-item label="所在区">
            <el-input v-model="formdata.belongto"/>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <template #footer>
      <el-button @click="close">取 消</el-button>
      <el-button type="primary"
                 @click="submit">确 定
      </el-button>
    </template>
  </el-dialog>
</template>

<script>
import {get} from '@/utils/request'
import {add, update} from '@/service/station'
import {ElMessage} from 'element-plus';

export default {
  name: "stationDlg",
  data: () => {
    return {
      formdata: {},
      visible: false,
      lines: [],
      yards: [],
    }
  },
  computed: {
    isNew() {
      return this.formdata.id === undefined;
    },
    title() {
      return this.isNew ? '车站新增' : '车站信息编辑'
    }
  },
  methods: {
    init(data) {
      this.formdata = data;
      this.visible = true;
    },
    close() {
      this.formdata = {};
      this.visible = false;
    },
    submit() {
      // 提交，有可能是新增insert，也可能是更新update
      if (this.isNew) {
        add(this.formdata)
            .then((res) => {
              ElMessage.success("成功新增一个站点");
              this.$emit("afterSubmit");
              this.visible = false;
            })
      } else {
        update(this.formdata)
            .then((res) => {
              ElMessage.success("更新成功");
              this.$emit("afterSubmit");
              this.visible = false;
            })
      }
    }
  },
  mounted() {
    get("/api/line_list")
        .then(result => {
              this.lines = []
              result.forEach(i => this.lines.push(
                  {
                    "name": i.name,
                    "id": i.id
                  }
              ))
            },
            () => {
              this.lines = []
              console.log("网络请求失败")
            })
  },
  watch: {
    "formdata.lineId": {
      handler: function (newVal, oldVal) {
        get("/api/yard/list", {lineId: newVal})
            .then(result => {
                  this.yards = [];
                  result.data.forEach(i => this.yards.push(
                      {
                        "name": i.name,
                        "id": i.id
                      }
                  ))
                },
                () => {
                  this.yards = [];
                  console.log("网络请求失败")
                })
      }
    }
  },
  emits: ["afterSubmit"],
}
</script>

<style scoped>

</style>