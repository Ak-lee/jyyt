<template>
  <el-dialog :title="title" v-model="visible" width="50%" :before-close="close">
    <el-table
        :data="yardInfo"
        border
        size="small"
    >
      <el-table-column prop="id" align="center" label="车库编码"/>
      <el-table-column prop="name" label="车库名称" align="center"/>
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
    </el-table>
    <el-divider/>
    <el-table :data="tableData">
      <el-table-column label="车场名称" prop="yardName" align="center"/>
      <el-table-column label="检修任务名称" prop="tasktypeName" align="center"/>
      <el-table-column label="检修地点" align="center">
        <template #default="{row}">
          <el-select
              multiple placeholder="点击选择"
              v-model="row.shopNameArr"
              @change="() => shopChange(row)"
              size="small"
          >
            <el-option v-if="yardInfo[0].hasServiceShop" label="检修库" value="检修库"/>
            <el-option v-if="yardInfo[0].hasOperationShop" label="运用库" value="运用库"/>
          </el-select>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
// 用于车场的 检修任务类型和检修地点（检修库、运用库）关联
import {get, post, put} from "@/utils/request";
import {ElMessage} from "element-plus";
import {toRaw} from 'vue'

export default {
  name: "tasktypeShopDlg",
  data: () => {
    return {
      yardId: "",
      yardName: "",
      yardInfo: null,
      visible: false,
      tasktypes: [],  // 存储该车场支持的检修任务类型。
      mapper: [], // 存储目前已经配置的 检修任务类型 - 检修地点 配对信息
    };
  },
  computed: {
    title() {
      return this.yardName + " 检修任务类型-检修地点 配对"
    },
    tableData() {
      let arr = [];
      this.tasktypes.forEach(i => {
        let obj = {};
        obj.id = '';
        obj.yardId = this.yardId;
        obj.yardName = this.yardName;
        obj.tasktypeName = i.taskTypeName;
        obj.tasktypeId = i.taskTypeId;
        obj.shopNameString = "";
        obj.shopNameArr = [];
        arr.push(obj)
      })
      this.mapper.forEach(j => {
        let index = arr.findIndex(k => {
          return k.yardId === j.yardId && k.tasktypeId === j.tasktypeId
        })
        if (index > -1) {
          arr[index].shopNameString = j.shopNameString;
          arr[index].id = j.id;
          arr[index].shopNameArr = arr[index].shopNameString.split(",");
        }
      })
      return arr;
    },
  },
  methods: {
    async init(row) {
      this.yardInfo = [row];
      this.yardId = row.id;
      this.yardName = row.name;
      this.visible = true;

      let params = {yardId: this.yardId};
      get("/api/yardShopTasktypes/tableByYardId", params)
          .then(res => {
            this.mapper = res.data;
          }, () => {
            console.log("网络错误")
          })
      get("/api/yardTasktype/byYard", params)
          .then(res => {
            this.tasktypes = res.data
          }, () => {
            console.log("网络错误")
          })
    },
    async shopChange(row) {
      row.shopNameString = row.shopNameArr.join(",");
      // let obj = toRaw(row);
      let result;
      if (row.id) {
        result = await put("/api/yardShopTasktypes/", row)
      } else {
        result = await post("/api/yardShopTasktypes/", row)
      }
      if (result.code === 0) {
        ElMessage.success("更新成功")
      } else {
        ElMessage.error("更新失败")
      }
    },
    close() {
      this.yardId = "";
      this.yardName = "";
      this.visible = false;
      this.tasktypes = [];
      this.mapper = [];
    }
  }
}
</script>

<style scoped>

</style>