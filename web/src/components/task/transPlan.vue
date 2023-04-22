<template>
  <div class="Breadcrumb">
    <span>计划制定管理&nbsp;>&nbsp;运输任务管理</span>
  </div>
  <div class="container">
    <div class="content">
      <div class="selector">
        <span style="font-size: 14px">线路选择: </span>
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
        <el-button size="small" type="primary" style="margin-left: 10px" @click="searchbtn">
          <el-icon>
            <search/>
          </el-icon>
          <span>查询</span>
        </el-button>
        <el-button size="small" type="success" @click="openDlg('')">
          <span>新增</span>
        </el-button>
      </div>
      <div>
        <el-tabs v-model="activeName" @tab-click="handleClick" type="border-card">
          <el-tab-pane label="工作日" name="first" :key="'first'">
            <div style="display: flex; align-items: center;">
              <span style="font-size: 14px;">工作日-运营计划所需热备车辆数量：</span>
              <div style="width: 100px;">
                <el-input type="number" size="small" v-model="workDayHotBackTrainNumObj.hotBackupTrainNum"/>
              </div>
              <el-button style="margin-left: 6px;" size="small" @click="updateWorkDayHotBackupTrainNum">更新</el-button>
            </div>
            <el-divider/>
            <el-table
                :data="tableData" border v-model="tableData" v-if="isFirst">
              <el-table-column align="center" prop="" label="序号" sortable>
                <template #default="scope">
                  {{ scope.$index + 1 }}
                </template>
              </el-table-column>
              <el-table-column prop="undercarId" align="center" label="车底ID" sortable/>
              <el-table-column prop="outstorageSite" align="center" sortable label="出库位置"/>
              <el-table-column prop="instorageSite" align="center" sortable label="入库位置"/>
              <el-table-column prop="outyardTime" align="center" sortable label="出车场时间"/>
              <el-table-column prop="inyardTime" align="center" sortable label="回车场时间"/>
              <el-table-column label="操作" align="center" width="180px" fixed="right">
                <template #default="{row}">
                  <div style="display: flex;justify-content: center">
                    <el-button size="small" @click="openDlg(row.id)">
                      <el-icon>
                        <edit/>
                      </el-icon>
                      <span>编辑</span>
                    </el-button>
                    <el-button size="small" @click="deleteRow(row.id)">
                      <el-icon>
                        <delete/>
                      </el-icon>
                      <span>删除</span>
                    </el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="周末(休息日)" name="second" :key="'second'">
            <div style="display: flex; align-items: center;">
              <span style="font-size: 14px;">周末-运营计划所需热备车辆数量：</span>
              <div style="width: 100px;">
                <el-input type="number" size="small" v-model="weekDayHotBackTrainNumObj.hotBackupTrainNum"/>
              </div>
              <el-button style="margin-left: 6px;" size="small" @click="updateWeekDayHotBackupTrainNum">更新</el-button>
            </div>
            <el-divider/>
            <el-table
                :data="tableData" border v-model="tableData" v-if="isSecond">
              <el-table-column align="center" prop="" label="序号" sortable>
                <template #default="scope">
                  {{ scope.$index + 1 }}
                </template>
              </el-table-column>
              <el-table-column prop="undercarId" align="center" label="车底ID" sortable/>
              <el-table-column prop="outstorageSite" align="center" sortable label="出库位置"/>
              <el-table-column prop="instorageSite" align="center" sortable label="入库位置"/>
              <el-table-column prop="outyardTime" align="center" sortable label="出车场时间"/>
              <el-table-column prop="inyardTime" align="center" sortable label="回车场时间"/>
              <el-table-column label="操作" align="center" width="180px" fixed="right">
                <template #default="{row}">
                  <div style="display: flex;justify-content: center">
                    <el-button size="small" @click="openDlg(row.id)">
                      <el-icon>
                        <edit/>
                      </el-icon>
                      <span>编辑</span>
                    </el-button>
                    <el-button size="small" @click="deleteRow(row.id)">
                      <el-icon>
                        <delete/>
                      </el-icon>
                      <span>删除</span>
                    </el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
        <transPlan-dlg ref="transPlanDlgRef" @afterSubmit="searchbtn()"></transPlan-dlg>
        <div>
          <el-pagination
              v-model:currentPage="pageNum"
              v-model:page-size="pageSize"
              small
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
import {get} from "@/utils/request";
import {Search, Edit, Delete} from '@element-plus/icons-vue'
import {onMounted} from "vue";
import {getTransPlan, removeById} from "@/service/transplan";
import transPlanDlg from "@/views/line/transPlanDlg";
import {getItem, addOrUpdate} from "@/service/hotBackUpTrainNum";
import {ElMessage} from "element-plus";

let transPlanDlgRef = $ref(null);
let tableData = $ref([]);

let lineId = $ref(17);//先默认17号线
let pageNum = $ref(1);
let pageSize = $ref(15);
let total = $ref(0);
let background = $ref(false);
let disabled = $ref(false);
let lines = $ref([]);
let activeName = $ref('first')
let applicableTime = $ref('workday')//默认读取工作日的
let isFirst = $ref(true);
let isSecond = $ref(false);
let workDayHotBackTrainNumObj = $ref({hotBackupTrainNum: 0});
let weekDayHotBackTrainNumObj = $ref({hotBackupTrainNum: 0});

const handleClick = function (tab) {
  if (tab.props.name === 'first') {
    isFirst = true
    isSecond = false
    applicableTime = 'workday'
  } else if (tab.props.name === 'second') {
    isFirst = false
    isSecond = true
    applicableTime = 'weekday'
  }
  searchbtn();
}


const handleSizeChange = function (val) {
  pageSize = val;
  searchbtn();
};
const handleCurrentChange = function (val) {
  pageNum = val;
  searchbtn();
};

const openDlg = function (id = '', editable = true) {
  transPlanDlgRef.init(id, editable)
};

const updateWorkDayHotBackupTrainNum = async function () {
  let data = await addOrUpdate(workDayHotBackTrainNumObj)
  if (data.code === 0) {
    ElMessage.success("更新成功")
  } else {
    ElMessage.error("更新失败")
  }
}
const updateWeekDayHotBackupTrainNum = async function () {
  let data = await addOrUpdate(weekDayHotBackTrainNumObj)
  if (data.code === 0) {
    ElMessage.success("更新成功")
  } else {
    ElMessage.error("更新失败")
  }
}

const deleteRow = async function (id = '') {
  await removeById(id);
  await searchbtn();//读数据的限制条件不一样
};

const searchbtn = async function () {
  let body = await getTransPlan(lineId, applicableTime, pageNum, pageSize)
  if (body.code !== 0) {
    ElMessage.error("网络错误");
    return;
  }
  tableData = body.data.records
  total = body.data.total
  pageNum = body.data.current
  pageSize = body.data.size

  let data = await getItem(lineId, applicableTime);
  if (data.code !== 0) {
    workDayHotBackTrainNumObj = {hotBackupTrainNum: 0};
    weekDayHotBackTrainNumObj = {hotBackupTrainNum: 0};
    ElMessage.error("网络错误");
    return;
  } else if (data.data === null || data.data.length === 0) {
    console.log("data.data === null || data.data.length === 0 ")
    workDayHotBackTrainNumObj = {hotBackupTrainNum: 0};
    weekDayHotBackTrainNumObj = {hotBackupTrainNum: 0};
    return;
  }
  if (applicableTime === "workday") {
    workDayHotBackTrainNumObj = data.data[0];
  } else if (applicableTime === "weekday") {
    weekDayHotBackTrainNumObj = data.data[0]
  }
}

const selectLine = async function () {
  // 挂载到页面上时
  get("/api/line_list")
      .then(result => {
        lines = []
        result.forEach(i => lines.push(
            {
              "name": i.name,
              "id": i.id
            }
        ))
      }, () => {
        lines = []
        console.log("网络请求失败")
      })
}

onMounted(async () => {
  await selectLine();
  // await renderTable();这里是默认全部的
  await searchbtn();//默认17号线得，因为默认第一条线没有数据
})


</script>

<style lang="css" scoped>
.Breadcrumb {
  padding: 10px 0px;
}

.container {
  min-height: calc(100vh - 150px);
  background-color: white;
  border: 1px solid #9c9c9c;
}

.content {
  margin: 10px;
}

.selector {
  margin: 10px 0;
}


</style>