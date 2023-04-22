<template>
  <div class="Breadcrumb1">
    <span>线路资源管理 > 线路详情信息</span>
  </div>
  <div class="container">
    <div class="content">
      <div class="title">线路详情信息查看</div>
      <el-table :data="tableData" border style="width: 100%">
        <el-table-column align="center" prop="id" label="线路号"/>
        <el-table-column align="center" prop="name" label="线路名称"/>
        <el-table-column align="center" label="线路车库信息">
          <template #default="{row}">
            <el-button size="small" @click="openYardlistDig(row.id)">
              选择查询
            </el-button>
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
    <yardListDlg ref="yardListDlg" @afterSubmit="renderTable"/>
  </div>
</template>
<script>
import {table} from "@/service/line.js"
import yardListDlg from '@/views/line/yardListDlg'
import shiftsDlg from '@/views/line/shifitsDlg'

export default {
  name: "lineDetail",
  components: {
    // LineSelector,
    yardListDlg,
    shiftsDlg,
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
    // "$route.query.lineId": {
    //   handler: "getRouteLineId",
    //   immediate: true,
    // }
  },
  methods: {
    // getRouteLineId(newVal, oldVal) {
    //   if (newVal) {
    //     this.lineId = Number(newVal);
    //     this.renderTable();
    //   }
    // },
    // handleLineSearch(e) {
    //   this.lineId = e;
    //   this.renderTable();
    // },
    // 分页
    handleSizeChange: function (val) {
      this.pageSize = val;
      this.renderTable();
    },
    handleCurrentChange: function (val) {
      this.pageNum = val;
      this.renderTable();
    },
    openYardlistDig(id) {
      this.$refs.yardListDlg.init(id);
    },
    renderTable() {
      // if (this.lineId) {
      //   table(this.lineId, this.pageNum, this.pageSize)
      //       .then((body) => { // get records by lineId
      //         this.tableData = body.data.records
      //         this.tableData.forEach((item) => {
      //           item.lineId = Number(item.lineId);
      //         })
      //         this.total = body.data.total
      //         this.pageNum = body.data.current
      //         this.pageSize = body.data.size
      //       })
      // } else {
      //   tableAll(this.pageNum, this.pageSize)
      //       .then((body) => {
      //         this.tableData = body.data.records
      //         this.total = body.data.total
      //         this.pageNum = body.data.current
      //         this.pageSize = body.data.size
      //       })
      // }
      table(this.pageNum, this.pageSize)
          .then((body) => {
            this.tableData = body.data.records
            this.total = body.data.total
            this.pageNum = body.data.current
            this.pageSize = body.data.size
          })
    }
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
  background-color: white;
  border: 1px solid #9c9c9c;
  display: block;
  min-height: 600px;
  height: calc(100vh - 150px);
}

.content {
  margin: 10px;
}

.title {
  font-weight: bold;
  font-size: 16px;
  margin: 10px;
}
</style>