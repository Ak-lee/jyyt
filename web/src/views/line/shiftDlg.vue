<template>
  <el-dialog append-to-body :title="title" v-model="visible" width="50%" :before-close="close">
    <el-form ref="form" :model="formdata" label-width="100px">
      <el-row :gutter="10">
        <el-col :span="12">
          <el-form-item label="班制编码">
            <el-input placeholder="BZ+'年份'+车场ID+2位编码" v-model="formdata.code"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="班制类型">
            <el-select v-model="formdata.type">
              <el-option label="白班" value="白班" />
              <el-option label="夜班" value="夜班" />
              <el-option label="双班" value="双班" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="10">
        <el-col :span="12">
          <el-form-item label="开始时间" >
            <el-time-picker
                format="HH:mm:ss"
                value-format="HH:mm:ss"
                v-model="formdata.beginTime"
                type="date"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="结束时间" >
            <el-time-picker
                format="HH:mm:ss"
                value-format="HH:mm:ss"
                v-model="formdata.endTime"
                type="date"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="10">
        <el-col :span="12">
          <el-form-item label="是否跨日">
              <el-radio-group v-model="formdata.iscrossday">
                <el-radio :label="1">是</el-radio>
                <el-radio :label="0">否</el-radio>
              </el-radio-group>
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
import {add, update} from '@/service/shifts'
import {ElMessage} from 'element-plus';

export default {
  name: "shiftDlg",
  data: () => {
    return {
      formdata: {},
      visible: false,
      lines: [],
      isNew: false,
      yardId: '',
    }
  },
  computed: {
    title() {
      return this.isNew ? '班制新增' : '班制信息编辑'
    }
  },
  methods: {
    init(data, isNew, yardId) {
      this.yardId = yardId;
      this.formdata = JSON.parse(JSON.stringify(data));
      this.visible = true;
      this.isNew = isNew;
    },
    close() {
      this.formdata = {};
      this.visible = false;
    },
    submit() {
      // 提交，有可能是新增insert，也可能是更新update
      if (this.isNew) {
        this.formdata.yardId = this.yardId;
        add(this.formdata)
            .then((res) => {
              ElMessage.success("成功新增一条班制");
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
    },
    mounted() {

    },
  },
  emits: ["afterSubmit"],
}
</script>

<style scoped>

</style>