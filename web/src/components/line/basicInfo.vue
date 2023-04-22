<template>
  <div class="Breadcrumb">
    <span>线路资源管理 > 线路基本信息</span>
  </div>
  <div class="container">
    <div class="content">
      <div class="title">线路基本信息设置</div>
      <div style="display: flex; align-items: center;">
        <div class="selector" style="margin-right: 10px;">
          <span style="font-size: 14px; margin-right: 8px">线路名称:</span>
          <el-input size="small"  clearable v-model="key"></el-input>
          <el-button size="small" type="success" style="margin-left: 10px" @click="filterTable">
            <el-icon>
              <search/>
            </el-icon>
            <span>查询</span>
          </el-button>
        </div>
        <el-button size="small" @click="openDlg('')" type="primary">
          新建线路
        </el-button>
      </div>

      <el-table
          :data="tableData1"
          border
      >
        <el-table-column type="index" :index="indexMethod" min-width="30" label="序号" align="center"/>
        <el-table-column prop="id" label="线路号" align="center"/>
        <el-table-column prop="name" label="线路名称" align="center"/>
        <el-table-column prop="trainNum" label="线路配属列车数量（列）" align="center"/>
        <el-table-column prop="lineLength" label="线路长度（千米）" align="center"/>
        <el-table-column prop="journeyTime" label="单程运行时间(分钟)" align="center"/>
        <el-table-column prop="remark" show-overflow-tooltip label="备注" align="center"/>
        <el-table-column label="操作" min-width="130px" align="center">
          <template #default="{row}">
            <el-button size="small" @click="openDlg(row.id)">
              <el-icon>
                <edit/>
              </el-icon>
              <span>编辑</span>
            </el-button>

            <el-button size="small" @click="openDlg(row.id,false)">
              <el-icon>
                <notebook/>
              </el-icon>
              <span>查看</span>
            </el-button>
          </template>
        </el-table-column>

      </el-table>
      <el-pagination
          v-model:currentPage="pageNum"
          v-model:page-size="pageSize"
          hide-on-single-page
          layout="->,total, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
      />
      <line-dlg ref="lineDlg" @afterSubmit="renderTable"></line-dlg>
    </div>
  </div>
</template>

<script setup>
import {Search, Edit, Notebook, Delete} from '@element-plus/icons-vue'
import {onMounted} from "vue";
import {table, removeById} from '@/service/line'
import LineDlg from "@/views/line/lineDlg.vue";
import {ElMessage} from 'element-plus'

let tableData1 = $ref([]);
let lineDlg = $ref(null);
let key = $ref('');
let pageNum = $ref(1);
let pageSize = $ref(15);
let total = $ref(2);

// 分页
const handleSizeChange = (number) => {
  pageSize = number
  renderTable()
};
const handleCurrentChange = (number) => {
  pageNum = number
  renderTable()
};

const deleteRow = async (id) => {
  removeById(id)
      .then(() => {
        ElMessage.success("成功删除一条数据")
      });
  renderTable();
};

const filterTable = function () {
  if (key !== '') {
    renderTable(key);
  } else {
    renderTable();
  }
};
const openDlg = function (id = '', editable = true) {
  lineDlg.init(id, editable)
}

const renderTable = async function (key = null) {
  let body = await table(pageNum, pageSize, key)
  tableData1 = body.data.records
  total = body.data.total
  pageNum = body.data.current
  pageSize = body.data.size
};

const indexMethod = (idx) => {
  return (pageNum - 1) * pageSize + idx + 1;
}

onMounted(async () => {
  key = ''
  await renderTable()
})

</script>

<style scoped>
.Breadcrumb {
  padding: 10px 0px;
}

.container {
  background-color: white;
  border: 1px solid #9c9c9c;
  display: block;
  min-height: calc(100vh - 150px);
}

.title {
  font-size: 16px;
  font-weight: bold;
}

.content {
  padding: 10px;
}

.selector {
  margin: 10px 0;
}

.el-input {
  width: 150px;
}

.date-picker-container {
  display: inline-block;
  width: 180px;
}

a, a:link, a:visited, a:active {
  text-decoration: none;
  color: inherit;
}

</style>
