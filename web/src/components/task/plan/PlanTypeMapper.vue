<template>
  <div class="Breadcrumb">
    <span>计划制定管理 > 计划任务管理 > 计划类型和检修任务的对应</span>
  </div>

  <div class="container">
    <div class="content">
      <div class="selector">
        <span style="font-size: 14px; margin-right: 8px">线路选择: </span>
        <el-select v-model="key"
                   filterable
                   size="small"
                   clearable
                   placeholder="请选择线路名">
          <el-option
              :key="index" v-for="(item, index) in lines"
              :label="item.name"
              :value="item.id"
          />
        </el-select>
        <el-button size="small" type="primary" style="margin-left: 10px" @click="filterTable">
          <el-icon>
            <search/>
          </el-icon>
          <span>查询</span>
        </el-button>
        <el-button size="small" type="success" style="margin-left: 10px" @click="openDlg('')">
          <el-icon>
            <CirclePlus/>
          </el-icon>
          <span>新增检修计划类型</span>
        </el-button>
      </div>
      <el-table
          :data="tableData1"
          border
          style="width: 70%;margin: auto;text-align: center"
      >
        <el-table-column type="index" label="序号" sortable align="center"/>
        <el-table-column prop="lineName" label="所属线路" sortable align="center"/>
        <el-table-column prop="name" label="检修计划类型" sortable align="center"/>
        <el-table-column prop="taskTypeName" label="针对的检修任务类型" sortable align="center"/>
        <el-table-column label="操作" width="240" align="center">
          <template #default="{row}">
            <div style="display: flex;justify-content: center">
              <el-button @click="openDlg(row.id)" size="small">
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
          small
          :disabled="disabled"
          :background="background"
          layout="->,total, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
      />
      <!--弹窗-->
      <plan-type-mapper-dlg ref="plantypemapperDlg" @afterSubmit="renderTable"></plan-type-mapper-dlg>
    </div>
  </div>
</template>

<script setup>
import {Search, Edit, Delete, CirclePlus} from '@element-plus/icons-vue'
import {onMounted} from "vue";
import {removeById, table, tableAll} from '@/service/plantype'
import PlanTypeMapperDlg from "@/views/line/plantypemapperDlg.vue";
import {selectLine} from "@/service/selector"

let tableData1 = $ref([]);
let plantypemapperDlg = $ref(null);
let key = $ref(null);
let lines = $ref([]);
//分页
let pageNum = $ref(1);
let pageSize = $ref(15);
let total = $ref(0);
let small = $ref(false);
let background = $ref(false);
let disabled = $ref(false);

// 分页
const handleSizeChange = function (val) {
  pageSize = val;
  filterTable();
};
const handleCurrentChange = function (val) {
  pageNum = val;
  filterTable();
};

const filterTable = function () {
  renderTable(key);
};
const openDlg = function (id = '', editable = true) {
  plantypemapperDlg.init(id, editable)
};
const deleteRow = function (id = '') {
  removeById(id);
  filterTable();
};
const renderTable = async function (key = null) {
  let body;
  if (key == null) {
    body = await tableAll(pageNum, pageSize)
  } else {
    body = await table(key, pageNum, pageSize)
  }
  tableData1 = body.data.records
  total = body.data.total
  pageNum = body.data.current
  pageSize = body.data.size
};

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
