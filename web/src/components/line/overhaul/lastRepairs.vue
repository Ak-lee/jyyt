<template>
  <div class="Breadcrumb">
    <span>线路资源管理 > 检修任务管理 > 历史检修数据管理</span>
  </div>

  <div class="container">
    <div class="content">
      <div class="selector">
        <span>线路选择: </span>
        <el-select
            class="selector"
            v-model="lineId"
            filterable
            clearable
            size="small"
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
              {{ (pageNum - 1) * pageSize + scope.$index + 1 }}
            </template>
          </el-table-column>

          <el-table-column align="center" prop="trainId" label="车辆编号" sortable/>
          <el-table-column prop="mileageCheck" align="center" label="里程检" sortable/>
          <el-table-column prop="topCheck" align="center" label="登顶检" sortable/>

          <el-table-column label="均衡修" align="center">
            <el-table-column prop="balancedRepairDate" align="center" label="时间" sortable/>
            <el-table-column prop="balancedRepair" align="center" label="检修编号" sortable/>
          </el-table-column>
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
        <lastRepairsDlg ref="lastRepairsDlg" @afterSubmit="renderTable()"></lastRepairsDlg>
        <div>
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
    </div>
  </div>
</template>

<script setup>
import {Search, Edit, Delete} from '@element-plus/icons-vue'
import {onMounted} from "vue";
import {getlastRepairs, removeById, table} from '@/service/lastRepairs'
import {selectLine} from "@/service/selector"
import LastRepairsDlg from "@/views/line/lastRepairsDlg"

let lastRepairsDlgRef = $ref(null);
let key = ''
let trains = $ref([]);
let lineId = $ref('');
let lines = $ref([]);
let pageNum = $ref(1);
let pageSize = $ref(15);
let total = $ref(0);
let small = $ref(false);
let background = $ref(false);
let disabled = $ref(false);
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
  lastRepairsDlgRef.init(id, editable)
};

const deleteRow = async function (id = '') {
  await removeById(id);
  await renderTable();
};

const renderTable = async function () {
  let body = await getlastRepairs(lineId, pageNum, pageSize)
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