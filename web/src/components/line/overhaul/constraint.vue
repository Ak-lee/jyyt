<template>
  <div class="Breadcrumb">
    <span>线路资源管理 > 检修任务管理 > 线路检修约束管理</span>
  </div>

  <div class="container">
    <div class="content">
      <div class="selector">
        <span style="font-size: 14px">线路选择: </span>
        <el-select
            class="selector"
            v-model="lineId"
            size="small"
            filterable
            clearable
            placeholder="请选择">
          <el-option
              :key="index" v-for="(item, index) in lines"
              :label="item.name"
              :value="item.id"
          />
        </el-select>
        <el-button size="small" type="primary" style="margin-left: 10px" @click="renderTable">
          <el-icon>
            <search/>
          </el-icon>
          <span>查询</span>
        </el-button>
      </div>
      <div>
        <el-table
            :data="tableData" border v-model="tableData">
          <el-table-column align="center" prop="" label="序号" sortable>
            <template #default="scope">
              {{ scope.$index + 1 }}
            </template>
          </el-table-column>
          <el-table-column prop="lineName" align="center" label="线路名称" sortable/>
          <el-table-column prop="maxBalancedRepairs" align="center" sortable label="单计划日最大均衡修数量/个"/>
          <el-table-column prop="maxMileageChecks" align="center" sortable label="单计划日最大里程检数量/个"/>
          <el-table-column label="操作" align="center" width="180px" fixed="right">
            <template #default="{row}">
              <div style="display: flex;justify-content: center">
                <el-button size="small" @click="openDlg(row.id)">
                  <el-icon>
                    <edit/>
                  </el-icon>
                  <span>编辑</span>
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <constraint-dlg ref="constraintDlg" @afterSubmit="renderTable()"></constraint-dlg>
      </div>
      <el-pagination
          v-model:currentPage="pageNum"
          v-model:page-size="pageSize"
          :disabled="disabled"
          :background="background"
          layout="->,total, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
      />

    </div>
  </div>
</template>

<script setup>
import {get} from "@/utils/request";
import {Search, Edit, Delete} from '@element-plus/icons-vue'
import {onMounted} from "vue";
import {getOnedayMax, removeById, table, tableAll} from '@/service/constraint'
import ConstraintDlg from "@/views/line/constraintDlg.vue";
import {selectLine} from "@/service/selector"

let constraintDlg = $ref(null);
let pageNum = $ref(1);
let pageSize = $ref(15);
let total = $ref(0);
let small = $ref(false);
let background = $ref(false);
let disabled = $ref(false);
let key = ''
let lineId = $ref('');//先默认17号线
let lines = $ref([]);
let tableData = $ref([]);


const handleSizeChange = function (val) {
  pageSize = val;
  renderTable();
};
const handleCurrentChange = function (val) {
  pageNum = val;
  renderTable();
};

const openDlg = function (id = '', editable = true) {
  constraintDlg.init(id, editable)
};

const deleteRow = async function (id = '') {
  await removeById(id);
  await renderTable();

};


const renderTable = async function () {
  let body;
  if (lineId == null || lineId == '') {
    body = await tableAll(pageNum, pageSize)
  } else {
    body = await table(lineId, pageNum, pageSize)
  }

  tableData = body.data.records
  total = body.data.total
  pageNum = body.data.current
  pageSize = body.data.size

}
onMounted(async () => {
  key = ''
  let result;
  result = await selectLine();
  result.forEach(i => lines.push(
      {
        "name": i.name,
        "id": i.id
      }
  ));
  await renderTable();
  await selectLine();

})
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

.content {
  padding: 10px;
  margin: 10px;
}

.selector {
  margin: 10px 0;
}


</style>