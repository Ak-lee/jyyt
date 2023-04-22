<template>
  <div class="Breadcrumb1">
    <span>线路资源管理 > 线路站点信息管理</span>
  </div>
  <div class="container">
    <div class="content">
      <div class="title">线路站点信息管理</div>
      <div style="display: flex; align-items: center;">
        <LineSelector :presetLineId="this.lineId" @lineSearch="handleLineSearch"></LineSelector>
        <el-button size="small" type="primary" @click="openDlg()">新增站点</el-button>
      </div>
      <el-table :data="tableData" border style="width: 100%">
        <el-table-column align="center" prop="id" label="id"/>
        <el-table-column align="center" prop="name" label="站点名"/>
        <el-table-column align="center" prop="lineName" label="所属线路"/>
        <el-table-column align="center" prop="longitude" label="经度"/>
        <el-table-column align="center" prop="latitude" label="纬度"/>
        <el-table-column align="center" prop="nearYardName" label="附近车场"/>
        <el-table-column align="center" prop="belongto" label="所属区"/>
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
    <stationDlg @afterSubmit="renderTable" ref="stationDlg"/>
  </div>
</template>

<script>
import LineSelector from "@/components/common/LineSelector";
import {table, tableAll, removeById} from "@/service/station.js"
import stationDlg from '@/views/line/stationDlg'

export default {
  name: "stationInfo",
  components: {
    LineSelector,
    stationDlg,
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
    deleteRow(id) {
      removeById(id);
      this.renderTable();
    },
    renderTable() {
      if (this.lineId) {
        table(this.lineId, this.pageNum, this.pageSize)
            .then((body) => { // get records by lineId@click="openDlg(row.id)
              this.tableData = body.data.records
              this.tableData.forEach((item) => {
                item.turnLines = Number(item.turnLines);
              })
              this.total = body.data.total
              this.pageNum = body.data.current
              this.pageSize = body.data.size
            })
      } else {
        tableAll(this.pageNum, this.pageSize)
            .then((body) => {
              this.tableData = body.data.records
              this.tableData.forEach((item) => {
                item.turnLines = Number(item.turnLines);
              })
              this.total = body.data.total
              this.pageNum = body.data.current
              this.pageSize = body.data.size
            })
      }
    },
    openDlg(stationId = '') {
      let formdata = {};
      if (stationId) {
        formdata = this.tableData.filter(i => i.id === stationId).at(0)
      }
      this.$refs.stationDlg.init(formdata)
    },
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
  background-color: white;
  border: 1px solid #9c9c9c;
  display: block;
  min-height: calc(100vh - 150px);
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