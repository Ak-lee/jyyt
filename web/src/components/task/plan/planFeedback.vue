<template>
  <div class="Breadcrumb">
    <span>计划制定管理 > 计划任务管理 > 计划反馈</span>
  </div>

  <div class="container">
    <div class="content">
      <div class="selector">
        <span style="font-size: 14px; margin-right: 8px">线路选择: </span>
        <el-select v-model="key"
                   filterable
                   clearable
                   size="small"
                   placeholder="请选择线路名">
          <el-option
              :key="index" v-for="(item, index) in lines"
              :label="item.lineName"
              :value="item.lineId"
          />
        </el-select>
        <el-button size="small" type="primary" style="margin-left: 10px" @click="filterTable">
          <el-icon>
            <search/>
          </el-icon>
          <span>查询</span>
        </el-button>
      </div>
      <el-table
          :data="tableData1"
          border
          style="width: 100%;margin: auto;text-align: center"
      >
        <el-table-column type="index" label="序号" sortable align="center"/>
        <el-table-column prop="lineName" label="所属线路" sortable align="center"/>
        <el-table-column prop="id" label="任务编号" sortable align="center"/>
        <el-table-column prop="name" label="任务名称" sortable align="center"/>
        <el-table-column prop="makeTime" label="计划制定时间" sortable align="center"/>
        <el-table-column prop="startTime" label="计划开始时间" sortable align="center"/>
        <el-table-column prop="endTime" label="计划结束时间" sortable align="center"/>
        <el-table-column label="操作" width="140" align="center">
          <template #default="{row}">
            <div style="display: flex;justify-content: center">
              <el-button :disabled="row.feedbackStatus" @click="opendlDlg(row.id)" size="small">
                <el-icon>
                  <edit/>
                </el-icon>
                <span>查看与反馈</span>
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
          v-model:currentPage="pageNum"
          v-model:page-size="pageSize"
          :page-sizes="[20,30, 40]"
          small
          :disabled="disabled"
          :background="background"
          layout="->,sizes, total, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
      />
      <!--弹窗-->
      <plan-feedback-dlg ref="planfeedbackdlg"></plan-feedback-dlg>
    </div>
  </div>
</template>

<script setup>
import {Search, Edit} from '@element-plus/icons-vue'
import {onMounted} from "vue";
import {table, tableAll} from '@/service/plan/planmanage'
import {selectLine} from "@/service/selector"
import PlanFeedbackDlg from "@/views/plan/planFeedbackDlg";

//初始条件
let planType = $ref('日计划');
let tableData1 = $ref([]);
let planfeedbackdlg = $ref(null);
let key = $ref(null);
let lines = $ref([]);
//分页
let pageNum = $ref(1);
let pageSize = $ref(20);
let total = $ref(2);
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

const opendlDlg = function (id = '') {
  planfeedbackdlg.init(id);
};

const renderTable = async function (key = null) {
  let body;
  if (key == null || key === '') {
    body = await tableAll(pageNum, pageSize, planType)
  } else {
    body = await table(key, pageNum, pageSize, planType)
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
        "lineName": i.name,
        "lineId": i.id
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
