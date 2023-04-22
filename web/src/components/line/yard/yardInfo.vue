<template>
  <div class="Breadcrumb">
    <span>线路资源管理 > 线路配属车场管理 > 车库基本信息</span>
  </div>

  <div class="container">
    <div class="title">车库信息配置</div>
    <el-button  style="margin-left: 10px;" type="primary" @click="openDlg('')">
      <span>新建车场</span>
    </el-button>
    <div class="content">
      <el-table
          :data="tableData1"
          border
      >
        <el-table-column prop="id" align="center" label="车库编码"/>
        <el-table-column prop="name" label="车库名称" align="center"/>
        <el-table-column prop="longitude" label="车库-经度" align="center"/>
        <el-table-column prop="latitude" label="车库-纬度" align="center"/>
        <el-table-column label="是否为车辆段" align="center">
          <template #default="{row}">
            {{ row.beDepot ? "是" : "否" }}
          </template>
        </el-table-column>
        <el-table-column label="检修库-股道数量（根）" align="center">
          <template #default="{row}">
            {{ row.beDepot && row.hasServiceShop ? row.serviceShopTrackwayNum : '' }}
          </template>
        </el-table-column>
        <el-table-column label="运用库-股道数量（根）" align="center">
          <template #default="{row}">
            {{ row.beDepot && row.hasOperationShop ? row.operationShopTrackwayNum : '' }}
          </template>
        </el-table-column>

        <el-table-column label="操作" min-width="180" align="center">
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

      <yard-dlg ref="yardDlg" @afterSubmit="renderTable"></yard-dlg>
    </div>
  </div>
</template>

<script setup>
import {table, removeById} from "@/service/yard";
import {Search, Edit, Delete} from '@element-plus/icons-vue'
import YardDlg from "@/views/line/yardDlg.vue";
import {get} from "@/utils/request";
import {onBeforeMount, onMounted, watch} from "vue";
import {useRoute} from 'vue-router';

let route = useRoute();
let tableData1 = $ref([]);
let yardDlg = $ref(null);
let key = $ref(route.query.lineId);
let pageNum = $ref(1);
let pageSize = $ref(15);
let total = $ref('');
let small = $ref(false);
let background = $ref(false);
let disabled = $ref(false);


// 分页
const handleSizeChange = (number) => {
  pageSize = number
  renderTable()
};
const handleCurrentChange = (number) => {
  pageNum = number
  renderTable()
};

const filterTable = function () {
  if (key !== '') {
    renderTable(key);
  } else {
    renderTable();
  }
};
const openDlg = function (id = '', editable = true) {
  yardDlg.init(id, editable)
}

const renderTable = async function (key = null) {
  let body = await table(pageNum, pageSize, key)
  tableData1 = body.data.records
  total = body.data.total
  pageNum = body.data.current
  pageSize = body.data.size
};

const deleteRow = async function (id = '') {
  if (id) {
    await removeById(id);
  } else {
    await renderTable();
  }
};

onBeforeMount(async () => {
  await renderTable(key)
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

.title {
  font-weight: bold;
  font-size: 16px;
  margin: 10px;
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
