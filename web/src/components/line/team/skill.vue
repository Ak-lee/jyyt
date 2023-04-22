<template>
  <div class="Breadcrumb">
    <span>线路资源管理 > 检修班组管理 > 人员技能管理</span>
  </div>
  <div class="container">
    <div style="margin-left: 10px;margin-top: 10px;">
      <div class="title">班组技能管理(编制信息)</div>
      <el-button type="primary" @click="openDlg('')">
        <span>新增检修班组</span>
      </el-button>
    </div>

    <div class="content">
      <el-table
          :data="tableData1"
          border
      >
        <el-table-column type="index" label="序号"/>
        <el-table-column prop="teamType" label="检修班组类型" sortable/>
        <el-table-column prop="skills" label="技能掌握" sortable/>
        <el-table-column prop="staffNum" label="人员数量(人/班组)" sortable/>
        <el-table-column label="操作">
          <template #default="{row}">
            <el-button size="small" @click="openDlg(row.id)">
              <el-icon>
                <edit/>
              </el-icon>
              <span>编辑</span>
            </el-button>
            <el-button size="small" @click="deleteRow(row.id)">
              <el-icon>
                <Delete/>
              </el-icon>
              <span>删除</span>
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <team-dlg ref="teamDlg" @afterSubmit="renderTable"></team-dlg>
    </div>
  </div>
</template>

<script setup>
import {tableall, removeById} from "@/service/team";
import {Search, Edit, Delete} from '@element-plus/icons-vue'
import TeamDlg from "@/views/line/teamDlg.vue";
import {onMounted} from "vue";

let tableData1 = $ref([]);
let teamDlg = $ref(null);

const openDlg = function (id = '', editable = true) {
  teamDlg.init(id, editable)
}

const deleteRow = function (id = '') {
  removeById(id);
  renderTable();
};

const renderTable = async function () {
  let body = await tableall();
  tableData1 = body.data;
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
  /*border: 1px solid #c1c2c6;*/
}

.title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

.selector {
  margin: 10px 0;
}

.el-input {
  width: 150px;
}

</style>
