<template>
  <el-dialog :title="title" v-model="visible" width="50%" :before-close="close">
    <el-table :data="tableData">
      <el-table-column label="车场名称" prop="yardName" align="center"/>
      <el-table-column label="检修任务名称" prop="tasktypeName" align="center"/>
      <el-table-column label="班制" align="center">
        <template #default="{row}">
          <el-select
              v-model="row.yardShiftsId"
              @change="shiftChange(row)"
              size="small"
          >
            <el-option
                :key="item.id"
                :value="item.id"
                :label="item.type"
                v-for="(item, index) in this.shifts"
            />
          </el-select>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>
<script>
// 用于车场的 检修任务类型 - 班制关联
import {get, post, put} from "@/utils/request";
import {ElMessage} from "element-plus";

export default {
  name: "tasktypeShiftDlg",
  data: () => {
    return {
      yardId: "",
      yardName: "",
      visible: false,
      tasktypes: [],  // 存储该车场支持的检修任务类型。
      shifts: [], // 存储该车场的班制信息
      mapper: [], // 存储目前已经配置的 检修任务类型 - 班制 配对信息
    }
  },
  computed: {
    title() {
      return this.yardName + " 检修任务类型-班制 配对"
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
        obj.yardShiftsId = ''
        arr.push(obj)
      })
      this.mapper.forEach(j => {
        let index = arr.findIndex(k => {
          return k.yardId === j.yardId && k.tasktypeId === j.tasktypeId
        })
        if (index > -1) {
          arr[index].yardShiftsId = j.yardShiftsId;
          arr[index].id = j.id;
        }
      })
      return arr;
    }
  },
  methods: {
    async init(yardId, yardName) {
      this.yardId = yardId;
      this.yardName = yardName;
      this.visible = true;

      let params = {yardId: this.yardId};
      get("/api/shifts/tableByYardId", params)
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
      get("/api/shifts/table", params)
          .then(res => {
            this.shifts = res.data;
          }, () => {
            console.log("网络错误")
          })
    },
    async shiftChange(row) {
      // 既要处理新增的逻辑，又要处理更新的逻辑
      console.log("handleShiftChange,,,", row);
      let result;
      if (row.id) {
        result = await put("/api/shifts/", row)
      } else {
        result = await post("/api/shifts/", row)
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
      this.shifts = [];
      this.mapper = [];
    }
  },
}
</script>

<style scoped>

</style>