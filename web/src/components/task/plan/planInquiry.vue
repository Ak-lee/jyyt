<template>
  <div class="Breadcrumb">
    <span>计划制定管理 > 计划任务管理 > 执行计划查询与下发</span>
  </div>

  <div class="container">
    <div class="content">
      <div class="selector">
        <el-row>
          <span style="font-size: 14px; margin-right: 8px;">线路选择: </span>
          <el-select v-model="key"
                     filterable
                     clearable
                     size="small"
                     placeholder="请选择线路名">
            <el-option
                :key="index" v-for="(item, index) in lines"
                :label="item.name"
                :value="item.id"
            />
          </el-select>
          <span style="font-size: 14px; margin-right: 8px;">&nbsp;&nbsp;任务单号:</span>
          <el-input size="small" v-model="id" clearable></el-input>
          <span style="font-size: 14px; margin-right: 8px;">&nbsp;&nbsp;任务名称:</span>
          <el-input size="small" v-model="name" clearable></el-input>
          <el-button size="small" type="primary" style="margin-left: 10px" @click="filterTable">
            <el-icon>
              <search/>
            </el-icon>
            <span>查询</span>
          </el-button>
          <el-button size="small" style="margin-left: 10px" type="warning"
                     :disabled="batchSelection.length===0"
                     @click="BatchDispatch()">
            <span>批量下发</span>
          </el-button>
        </el-row>

        <el-button style="margin-top: 10px"
                   @click="show = !show" size="small">
          <el-icon>
            <CirclePlus/>
          </el-icon>
          <span>更多选项</span>
        </el-button>
        <el-row class="row" v-show="show">
          <span style="font-size: 14px; margin-right: 8px;margin-top: 5px">&nbsp;&nbsp;年份:</span>
          <el-select v-model="year" clearable placeholder="点击选择" size="small">
            <el-option label="2019" value="2019"/>
            <el-option label="2020" value="2020"/>
            <el-option label="2021" value="2021"/>
            <el-option label="2022" value="2022"/>
          </el-select>
          <span style="font-size: 14px; margin-right: 8px;margin-top: 5px">&nbsp;&nbsp;计划类型:</span>
          <el-select v-model="planType" clearable placeholder="点击选择" size="small">
            <el-option label="年计划" value="年计划"/>
            <el-option label="月计划" value="月计划"/>
            <el-option label="周计划" value="周计划"/>
            <el-option label="日计划" value="日计划"/>
          </el-select>
          <span style="font-size: 14px; margin-right: 8px;margin-top: 5px">&nbsp;&nbsp;计划开始时间大于:</span>
          <el-date-picker
              v-model="date1"
              type="date"
              placeholder="选择时间"
              clearable size="small"
          />
          <span style="font-size: 14px; margin-right: 8px;margin-top: 5px">&nbsp;&nbsp;计划开始时间小于:</span>
          <el-date-picker
              v-model="date2"
              type="date"
              placeholder="选择时间"
              clearable size="small"
          />
          <br>
        </el-row>
      </div>

      <el-table
          :data="tableData1"
          border
          @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" :selectable="selectEnable"/>
        <el-table-column type="index" label="序号" sortable align="center"/>
        <el-table-column prop="lineId" label="所属线路" sortable align="center"/>
        <el-table-column prop="id" label="任务编号" sortable align="center"/>
        <el-table-column prop="name" label="任务名称" sortable align="center"/>
        <el-table-column prop="makeTime" label="计划制定时间" sortable align="center"/>
        <el-table-column prop="startTime" label="计划开始时间" sortable align="center"/>
        <el-table-column prop="endTime" label="计划结束时间" sortable align="center"/>
        <el-table-column label="操作" width="180" align="center">
          <template #default="{row}">
            <el-button @click="openDlg(row.id)" size="small">
              <el-icon>
                <search/>
              </el-icon>
              <span>查看</span>
            </el-button>
            <el-button :disabled="row.dispatchStatus === '已下发' " @click="dispatch(row.id)" size="small">
              <span>计划下发</span>
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
          v-model:currentPage="pageNum"
          v-model:page-size="pageSize"
          hide-on-single-page
          :page-sizes="[20,30,40]"
          small
          :disabled="disabled"
          :background="background"
          layout="->,sizes,total, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
      />
      <plan-inquiry-dlg ref="planinquirydlg"></plan-inquiry-dlg>
      <dayplan-dlg ref="dayplandlg"></dayplan-dlg>
      <dispatch-dlg ref="dispatchdlg"></dispatch-dlg>
    </div>
  </div>
</template>

<script setup>
import {table} from "@/service/planInquiry";
import {Search, CirclePlus} from '@element-plus/icons-vue';
import {get} from "@/utils/request";
import {onMounted} from "vue";
import {getById} from "@/service/plan/planmanage";
import PlanInquiryDlg from "@/views/plan/planInquiryDlg";
import DayplanDlg from "@/views/plan/dayplanDlg";
import DispatchDlg from "@/views/plan/dispatchDlg";

let tableData1 = $ref([]);
let lines = $ref([]);
let key = $ref('');

let pageNum = $ref(1);
let pageSize = $ref(20);
let total = $ref(0);
let background = $ref(false);
let disabled = $ref(false);

let id = $ref('');
let name = $ref('');
let year = $ref('');
let planType = $ref('');
let date1 = $ref('');
let date2 = $ref('');
let batchSelection = $ref([]);
let show = $ref(false);

//弹窗
let planinquirydlg = $ref(null);
let dayplandlg = $ref(null);
let dispatchdlg = $ref(null);

// 分页
const handleSizeChange = (number) => {
  pageSize = number
  renderTable(key, id, name, year, planType, date1, date2)
};
const handleCurrentChange = (number) => {
  pageNum = number
  renderTable(key, id, name, year, planType, date1, date2)
};

const openDlg = async function (id = '') {
  let body = await getById(id);
  planType = body.data.planType
  if (planType === "年计划" || planType === "月计划" || planType === "周计划")
    planinquirydlg.init(id)
  else
    dayplandlg.init(id)
}

const filterTable = function () {
  renderTable(key, id, name, year, planType, date1, date2);
};

const renderTable = async function (key = null, id = null, name = null, year = null, planType = null, date1 = null, date2 = null) {
  let body = await table(pageNum, pageSize, key, id, name, year, planType, date1, date2)
  tableData1 = body.data.records
  total = body.data.total
  pageNum = body.data.current
  pageSize = body.data.size
};

const handleSelectionChange = (val) => {
  batchSelection = val;
}

const selectEnable = (row, rowIndex) => {
  if (row.dispatchStatus === "已下发") {
    return false;
  } else {
    return true;
  }
}

const BatchDispatch = function () {
  let ids = [];
  batchSelection.forEach(i => {
    ids.push(i.id);
  })
  dispatchdlg.initAll(ids);
};
const dispatch = async function (id = '') {
  let ids = [];
  ids.push(id)
  dispatchdlg.initAll(ids)
}


const selectLine = async function () {
  get("/api/line_list")
      .then(result => {
        lines = [];
        result.forEach(i => lines.push(
            {
              "name": i.name,
              "id": i.id
            }
        ))
      }, () => {
        lines = []
        console.log("⽹络请求失败")
      })
};

onMounted(async () => {
  key = ''
  await renderTable()
  await selectLine()

})
</script>

<style scoped>
.row {
  margin-top: 10px;
}

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
  /*border: 1px solid #c1c2c6;*/
}

.selector {
  margin: 10px 0;
}

.el-input {
  width: 150px;
}


</style>
