<template>
  <el-dialog :title="title" v-model="visible" class="container">
    <el-button type="primary" style="margin-bottom: 4px;" @click="openDlg()">新增班制</el-button>
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="序号"/>
      <el-table-column prop="code" label="班制编码"/>
      <el-table-column prop="type" label="班制类型"/>
      <el-table-column prop="beginTime" label="开始时间"/>
      <el-table-column prop="endTime" label="结束时间"/>
      <el-table-column prop="isCrossDay" label="是否跨日">
        <template #default="{row}">
          <div>{{ row.iscrossday === 1 ? "是" : "否" }}</div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template #default="{row}">
          <el-button @click="openDlg(row.id)">编辑</el-button>
          <el-button @click="deleteRow(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <shiftDlg ref="shiftDlg" @afterSubmit="renderTable"/>
  </el-dialog>
</template>

<script>
import {table, removeById} from "@/service/shifts.js"
import shiftDlg from "@/views/line/shiftDlg"
import {ElMessage} from "element-plus";

export default {
  name: "shiftsDlg",
  components: {shiftDlg},
  data: () => {
    return {
      visible: false,
      tableData: [],
      pageNum: 1,
      pageSize: 10,
      total: '',
      yardId: '',
      yardName: '',
    }
  },
  computed: {
    title() {
      return this.yardName + " 班制信息配置";
    }
  },
  methods: {
    // 分页
    handleSizeChange: function (val) {
      this.pageSize = val;
      this.renderTable();
    },
    handleCurrentChange: function (val) {
      this.pageNum = val;
      this.renderTable();
    },
    renderTable() {
      table(this.yardId)
          .then((res) => {
            this.tableData = res.data;
          })
    },
    openDlg(id = '') {
      let formdata = {};
      if (id) {
        formdata = this.tableData.filter(i => i.id === id).at(0)
        this.$refs.shiftDlg.init(formdata, false, this.yardId)
      } else {
        this.$refs.shiftDlg.init(formdata, true, this.yardId)
      }
    },
    deleteRow(id) {
      removeById(id);
      this.renderTable();
      ElMessage.success("成功删除 1 条数据");
    },
    init(yardId, yardName) {
      this.visible = true;
      this.yardId = yardId;
      this.yardName = yardName;
      this.renderTable();
    },
  },
}
</script>

<style scoped>

</style>