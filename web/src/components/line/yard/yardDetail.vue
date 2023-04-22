<template>
  <div class="Breadcrumb">
    <span>线路资源管理 > 线路配属车场管理 > 车场详情信息配置</span>
  </div>

  <div class="container">
    <div class="title">车场信息配置（车场关联班制、班组信息）</div>
    <div class="content">
      <el-table
          :data="tableData" border style="width: 100%"
      >
        <el-table-column align="center" prop="id" label="车场编码"/>
        <el-table-column align="center" prop="name" label="车场名称"/>

        <el-table-column align="center" label="班组信息关联">
          <template #default="{row}">
            <el-button size="small" @click="openTeamDlg(row)">编辑</el-button>
          </template>
        </el-table-column>

        <el-table-column align="center" label="车场检修任务类型配置">
          <template #default="{row}">
            <el-button size="small" @click="openTaskTypeDlg(row)">编辑</el-button>
          </template>
        </el-table-column>
        <el-table-column align="center" label="班制信息关联">
          <template #default="{row}">
            <el-button size="small" @click="openShiftsDlg(row)">编辑</el-button>
          </template>
        </el-table-column>
        <el-table-column align="center" label="检修任务类型-适用检修地点">
          <template #default="{row}">
            <el-button size="small" v-show="row.beDepot && (row.hasServiceShop || row.hasOperationShop)"
                       @click="openTasktypeShopDlg(row)">编辑
            </el-button>
          </template>
        </el-table-column>
        <el-table-column align="center" label="检修任务类型-适用班制">
          <template #default="{row}">
            <el-button size="small" @click="openTasktypeShiftDlg(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
          v-model:currentPage="pageNum"
          v-model:page-size="pageSize"
          hide-on-single-page
          :disabled="disabled"
          :background="background"
          layout="->,total, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
      />
      <teamListDlg ref="teamListDlgRef"/>
      <shifits-dlg ref="shifitsDlgRef"/>
      <tasktype-list-dlg ref="tasktypeListDlgRef"/>
      <tasktype-shift-dlg ref="tasktypeShiftDlgRef"/>
      <tasktype-shop-dlg ref="tasktypeShopDlgRef"/>
    </div>
  </div>
</template>

<script>
import {table} from "@/service/yard";
import teamListDlg from "@/views/teamListDlg";
import shifitsDlg from "@/views/line/shifitsDlg";
import TasktypeListDlg from "@/views/line/tasktypeListDlg";
import TasktypeShiftDlg from "@/views/line/tasktypeShiftDlg";
import TasktypeShopDlg from "@/views/line/tasktypeShopDlg";
import {toRaw} from "vue"

export default {
  name: "yardDetail",
  data: () => {
    return {
      tableData: [],
      pageNum: 1,
      pageSize: 15,
      total: '',
    }
  },
  components: {
    TasktypeShiftDlg,
    TasktypeListDlg,
    teamListDlg,
    shifitsDlg,
    TasktypeShopDlg,
  },
  methods: {
    renderTable: async function (key = null) {
      let body = await table(this.pageNum, this.pageSize, key)
      this.tableData = body.data.records
      this.total = body.data.total
      this.pageNum = body.data.current
      this.pageSize = body.data.size
    },
    openTeamDlg(row) {
      this.$refs.teamListDlgRef.init(row.id, row.name);
    },
    openTaskTypeDlg(row) {
      this.$refs.tasktypeListDlgRef.init(row.id, row.name);
    },
    openShiftsDlg(row) {
      this.$refs.shifitsDlgRef.init(row.id, row.name);
    },
    openTasktypeShiftDlg(row) {
      this.$refs.tasktypeShiftDlgRef.init(row.id, row.name);
    },
    openTasktypeShopDlg(row) {
      this.$refs.tasktypeShopDlgRef.init(toRaw(row));
    },
    // 分页
    handleSizeChange: (number) => {
      this.pageSize = number
      this.renderTable()
    },
    handleCurrentChange: (number) => {
      this.pageNum = number
      this.renderTable()
    },
  },
  mounted() {
    this.renderTable()
  }
}
</script>

<style scoped>
.Breadcrumb {
  padding: 10px 0px;
}

.container {
  min-height: calc(100vh - 150px);
  background-color: white;
  border: 1px solid #9c9c9c;
}

.title {
  font-weight: bold;
  font-size: 16px;
  margin: 10px;
}

.content {
  padding: 10px;
}

</style>