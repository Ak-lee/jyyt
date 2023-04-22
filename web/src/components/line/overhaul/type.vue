<template>
  <div class="Breadcrumb">
    <span>线路资源管理 > 检修任务管理 > 检修任务类型基础信息</span>
  </div>

  <div class="container">
    <div class="content">
      <div class="title">检修任务类型基础信息</div>
      <el-button type="primary" style="margin-bottom: 4px;" @click="openDlg('', true)">
        新建检修类型
      </el-button>
      <el-table
          :data="tableData1"
          border
      >
        <el-table-column type="index" :index="indexMethod" label="序号" width="140"/>
        <el-table-column prop="taskTypeName" label="检修任务名称" width="140"/>

        <el-table-column align="center" prop="mileagePeriod" label="里程周期"></el-table-column>
        <el-table-column align="center" prop="timePeriod" label="时间周期"></el-table-column>
        <el-table-column align="center" label="单修程/多修程">
          <template #default="{row}">
            {{ row.beMultiMode ? "多修程" : "单修程" }}
          </template>
        </el-table-column>
        <el-table-column align="center" prop="multiModeNum" label="多修程-子修程数量"/>
        <el-table-column label="操作" width="160">
          <template #default="{row}">
            <div style="display: flex;justify-content: center">
              <el-button @click="openDlg(row.id, false)" size="small">
                <el-icon>
                  <edit/>
                </el-icon>
                <span>编辑</span>
              </el-button>

              <el-button @click="deleteRow(row.id)" size="small">
                <el-icon>
                  <delete/>
                </el-icon>
                <span>删除</span>
              </el-button>
            </div>
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
      <type-dlg2 ref="typeDlg" @afterSubmit="renderTable"></type-dlg2>
    </div>
  </div>
</template>

<script setup>
import {Search, Edit, Delete} from '@element-plus/icons-vue'
import {onMounted} from "vue";
import {removeById, table} from '@/service/type'
import TypeDlg2 from "@/views/line/taskTypeDlgMeta.vue";
import {selectLine} from "@/service/selector"

let tableData1 = $ref([]);
let typeDlg = $ref(null);
let key = $ref(null);
let lines = $ref([]);
let pageNum = $ref(1);
let pageSize = $ref(15);
let total = $ref(2);
let small = $ref(false);
let background = $ref(false);
let disabled = $ref(false);

// 分页
const handleSizeChange = function (val) {
  pageSize = val;
  renderTable();
};
const handleCurrentChange = function (val) {
  pageNum = val;
  renderTable();
};

const indexMethod = function (i) {
  return (pageNum - 1) * pageSize + i + 1;
}

const filterTable = function () {
  renderTable(key);
};
const openDlg = function (id = '', isNew = false) {
  typeDlg.init(id, isNew);
};
const deleteRow = function (id = '') {
  removeById(id);
  renderTable();
};
const renderTable = async function (key = null) {
  let body = await table(pageNum, pageSize, key)
  tableData1 = body.data.records
  tableData1.forEach(i => {
    if (i.mileagePeriod == 0) {
      i.mileagePeriod = '';
    }
    if (i.timePeriod == 0) {
      i.timePeriod = '';
    }
  })
  total = body.data.total
  pageNum = body.data.current
  pageSize = body.data.size
};

onMounted(async () => {
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

.title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

.title {
  font-size: 16px;
  font-weight: bold;
}

.selector {
  margin: 10px 0;
}

</style>
