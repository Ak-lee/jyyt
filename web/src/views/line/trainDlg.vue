<template>
  <el-dialog :title="title" v-model="visible" width="50%" :before-close="close">
    <el-form ref="form" :model="formdata" label-width="100px">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="线路选择">
            <el-select v-model="formdata.lineId">
              <el-option
                  :key="index" v-for="(item, index) in lines"
                  :label="item.name"
                  :value="item.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="12">
        <el-col :span="10">
          <el-form-item label="列车号">
            <el-input v-model="formdata.id" placeholder="城市拼音首字母（大写） + 线路号 + 三位列车编码"/>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="10">
        <el-col :span="12">
          <el-form-item label="出厂日期">
            <el-date-picker
                v-model="formdata.serviceStartDate"
                type="date"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="列车状态">
            <el-select v-model="formdata.trainStatus">
              <el-option label="可用" value="可用" key="可用"></el-option>
              <el-option label="架大修" value="架大修" key="架大修"></el-option>
            </el-select>
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
import {add, update} from '@/service/train'
import {ElMessage} from 'element-plus';

export default {
  name: "trainDlg",
  data: () => {
    return {
      formdata: {trainStatus: "可用"},
      visible: false,
      lines: [],
      isNew: false,
    }
  },
  computed: {
    title() {
      return this.isNew ? '列车新增' : '列车信息编辑'
    }
  },
  methods: {
    init(data, isNew) {
      if (!isNew) {
        this.formdata = data;
      }
      this.visible = true;
      this.isNew = isNew;
    },
    close() {
      this.formdata = {trainStatus: "可用"};
      this.visible = false;
    },
    submit() {
      // 提交，有可能是新增insert，也可能是更新update
      if (this.isNew) {
        add(this.formdata)
            .then((res) => {
              ElMessage.success("成功新增一列车");
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
  emits: ["afterSubmit"],
}
</script>

<style scoped>

</style>