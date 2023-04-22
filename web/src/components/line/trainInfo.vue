<template>
  <div class="Breadcrumb1">
    <span>线路资源管理 > 列车信息管理</span>
  </div>
  <div class="container">
    <div class="content">
      <div class="title">列车信息管理</div>
      <div style="display: flex; align-items: center;">
        <LineSelector :presetLineId="this.lineId" @lineSearch="handleLineSearch"></LineSelector>
        <el-button size="small" type="primary" @click="openDlg()">新增列车</el-button>
      </div>

      <el-table :data="tableData" border style="width: 100%">
        <el-table-column align="center" prop="id" label="列车号"/>
        <el-table-column align="center" prop="lineName" label="线路号"/>
        <el-table-column align="center" prop="serviceStartDate" label="出厂日期"/>
        <el-table-column align="center" prop="trainStatus" label="列车状态"/>
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
      <trainDlg ref="trainDlg" @afterSubmit="renderTable"/>
    </div>
  </div>
</template>
<script>
import LineSelector from "@/components/common/LineSelector";
import {table, tableAll, removeById} from "@/service/train.js"
import trainDlg from '@/views/line/trainDlg'

export default {
  name: "trainInfo",
  components: {
    LineSelector,
    trainDlg,
  },
  data: () => {
    return {
      tableData: [],
      pageNum: 1,
      pageSize: 15,
      total: '',
      lineId: '',
    }
  },
  watch: {
    "$route.query.lineId": {
      handler: "getRouteLineId",
      immediate: true,
    }
  },
  methods: {
    getRouteLineId(newVal, oldVal) {
      if (newVal) {
        this.lineId = Number(newVal);
        this.renderTable();
      }
    },
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
      if (this.lineId) {
        table(this.lineId, this.pageNum, this.pageSize)
            .then((body) => { // get records by lineId
              this.tableData = body.data.records
              this.tableData.forEach((item) => {
                item.lineId = Number(item.lineId);
              })
              this.total = body.data.total
              this.pageNum = body.data.current
              this.pageSize = body.data.size
            })
      } else {
        tableAll(this.pageNum, this.pageSize)
            .then((body) => {
              this.tableData = body.data.records
              this.total = body.data.total
              this.pageNum = body.data.current
              this.pageSize = body.data.size
            })
      }
    },
    openDlg(trainId = '') {
      let formdata = {};
      if (trainId) {
        formdata = this.tableData.filter(i => i.id === trainId).at(0)
        this.$refs.trainDlg.init(formdata, false);
      } else {
        this.$refs.trainDlg.init(formdata, true);
      }
    },
    deleteRow(id) {
      removeById(id);
      this.renderTable();
    },
  },
  mounted() {
    this.renderTable();
  },
}
</script>

<style scoped>
.Breadcrumb1 {
  padding: 10px 0px;
}

.container {
  min-height: 500px;
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