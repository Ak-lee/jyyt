<template>
  <div class="Breadcrumb">
    <span>计划制定管理 > 计划任务管理 > {{ planType }}信息管理</span>
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
        <el-button size="small" type="success" style="margin-left: 10px" @click="opennewDlg(planType)">
          <el-icon>
            <CirclePlus/>
          </el-icon>
          <span>新增{{ planType }}</span>
        </el-button>
      </div>
      <div style="color: red; font-size: 16px; margin: 6px 0;">
        <div style="margin-bottom: 6px;">注意，新建线路日计划之前，请确保线路年计划、月计划、周计划已创建并下发.</div>
        <div>注意，每个线路只能有一个日计划，若需新建计划请删除该线路已存在的日计划.</div>
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
        <el-table-column label="操作" width="150" align="center">
          <template #default="{row}">
            <div style="display: flex;justify-content: center">
              <el-button @click="opendlDlg(row.id)" size="small">
                <el-icon>
                  <edit/>
                </el-icon>
                <span>查看</span>
              </el-button>
              <el-button @click="deletePlan(row.id)" size="small">
                <el-icon>
                  <edit/>
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
      <newplan-dlg ref="newplanDlg" @afterSubmit="renderTable"></newplan-dlg>
      <plandl-dlg ref="plandlDlg"></plandl-dlg>
      <dayplan-dlg ref="dayplandlg"></dayplan-dlg>
      <delete-plan-dlg @afterSubmit="renderTable" ref="deletePlanDlgRef"></delete-plan-dlg>
      <dayPlanHistoryDlg @afterDayPlanHistorySubmit="opennewDlg2" ref="dayPlanHistoryDlgRef"></dayPlanHistoryDlg>

    </div>
  </div>
</template>

<script setup>
import {Search, Edit, CirclePlus} from '@element-plus/icons-vue'
import {onMounted} from "vue";
import {table, tableAll} from '@/service/plan/planmanage'
import {selectLine} from "@/service/selector"
import NewplanDlg from "@/views/plan/newplanDlg.vue";
import PlandlDlg from "@/views/plan/plandlDlg.vue";
import DayplanDlg from "@/views/plan/dayplanDlg";
import DeletePlanDlg from "@/views/plan/deletePlanDlg.vue";
import DayPlanHistoryDlg from "@/views/plan/dayPlanHistoryDlg.vue"

//初始条件
let planType = $ref('日计划');
let tableData1 = $ref([]);
let newplanDlg = $ref(null);
let plandlDlg = $ref(null);
let dayplandlg = $ref(null);
let deletePlanDlgRef = $ref(null);
let dayPlanHistoryDlgRef = $ref(null);
let key = $ref(null);
let lines = $ref([]);
//分页
let pageNum = $ref(1);
let pageSize = $ref(20);
let total = $ref(2);
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

const opennewDlg = function () {
  dayPlanHistoryDlgRef.init();
};
const opennewDlg2 = function (planType = '日计划') {
  newplanDlg.init(planType);
}

const opendlDlg = function (id = '') {
  dayplandlg.init(id);
};

const deletePlan = function (id) {
  deletePlanDlgRef.init(id);
}

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
