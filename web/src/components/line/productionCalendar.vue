<template>
  <div class="Breadcrumb1">
    <span>线路资源管理 > 生产日历信息管理</span>
  </div>
  <div class="container">
    <div class="content">
      <div class="title">生产日历信息管理</div>
      <div style="display: flex; align-items: center;">
        <LineSelector :presetLineId="this.lineId" @lineSearch="handleLineSearch"></LineSelector>
        <el-button size="small" type="primary" @click="openDlg()">新增日历</el-button>
      </div>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column align="center" type="index" label="序号"/>
        <el-table-column align="center" prop="lineId" label="所属线路"/>
        <el-table-column align="center" prop="id" label="日历编号"/>
        <el-table-column align="center" prop="name" label="日历名称"/>
        <el-table-column align="center" label="开始日期">
          <template #default="{row}">
            {{ dateFormatter(new Date(row.startDate), "YYYY年MM月DD日") }}
          </template>
        </el-table-column>
        <el-table-column align="center" prop="endDate" label="结束日期">
          <template #default="{row}">
            {{ dateFormatter(new Date(row.endDate), "YYYY年MM月DD日") }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作" width="160">
          <template #default="{row}">
            <el-button size="small" @click="openDlg(row.id)">编辑</el-button>
            <el-button size="small" @click="deleteRow(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
          v-model:currentPage="pageNum"
          v-model:page-size="pageSize"
          hide-on-single-page
          layout="->,total, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
      />
    </div>
    <calendarDlg ref="calendarDlg" @afterSubmit="renderTable"/>
  </div>
</template>

<script>
import LineSelector from "@/components/common/LineSelector";
import {removeById, table} from "@/service/calendar"
import calendarDlg from '@/views/line/calendarDlg'
import {dateFormatter} from "@/utils/upload";
import {ElMessage} from "element-plus";

export default {
  name: "productionCalendar",
  components: {
    LineSelector,
    calendarDlg,
  },
  data: () => {
    return {
      tableData: [],
      pageNum: 1,
      pageSize: 10,
      total: '',
      lineId: '',
    }
  },
  methods: {
    handleLineSearch(e) {
      this.lineId = e;
      this.renderTable();
    },
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
      table(this.lineId, this.pageNum, this.pageSize)
          .then((body) => {
            this.tableData = body.data.records
            this.tableData.forEach((item) => {
              item.lineId = Number(item.lineId);
            })
            this.total = body.data.total
            this.pageNum = body.data.current
            this.pageSize = body.data.size
          })
    },
    openDlg(trainId = '') {
      let formdata = {};
      if (trainId) {
        formdata = this.tableData.filter(i => i.id === trainId).at(0)
        this.$refs.calendarDlg.init(formdata, false);
      } else {
        this.$refs.calendarDlg.init(formdata, true);
      }
    },
    deleteRow(id) {
      removeById(id)
          .then(() => {
            ElMessage.success("成功删除一条数据")
          }).finally(this.renderTable)
    },
    dateFormatter,
  },
  mounted() {
    this.renderTable();
  }
}
</script>

<style scoped>
.Breadcrumb1 {
  padding: 10px 0px;
}

.container {
  min-height: calc(100vh - 150px);
  background-color: white;
  border: 1px solid #9c9c9c;
  display: block;
}

.content {
  margin: 10px;
}

.title {
  font-weight: bold;
  font-size: 16px;
  margin: 10px 0;
}


</style>