<template>
  <el-dialog id="dayPlanHistoryDlg" :title="title" v-model="visible" width="800" :before-close="close">
    <el-button size="small" style="margin-bottom: 6px;" @click="clearTable">清空</el-button>
    <el-tooltip
        placement="bottom"
        content="自动填充，尝试使用上一日检修计划的作业场填充回库场，无检修任务列车使用运输任务最后一个车底任务的入库位置填充回库场."
        effect="light">
      <el-button size="small" style="margin-bottom: 6px;" @click="autoFill">自动填充</el-button>
    </el-tooltip>
    <el-button type="primary" size="small" style="margin-bottom: 6px;" @click="submit">提交</el-button>
    <div style="margin-bottom: 6px;">
      <span style="font-size: 14px; color: red;">数据校验规则：最后车底任务id， 回库场，二者至少填一个。</span>
    </div>

    <div>
      <span style="font-size: 14px;">选择线路: </span>
      <el-select size="small" v-model="lineId">
        <el-option v-for="item in lineList" :label="item.lineName" :value="item.lineId" :key="item.lineId"/>
      </el-select>
    </div>
    <div style="margin-bottom: 6px;">
      <span style="font-size: 14px;">日期: </span>
      <el-date-picker format="YYYY-MM-DD" disabled v-model="date" size="small"/>
      <span style="margin-left: 6px;" v-show="dateType">{{ "日期类型：" + dateType + '日' }}</span>
    </div>
    <el-table
        height="400" :data="tableData" border>
      <el-table-column label="列车号" prop="trainId"></el-table-column>
      <el-table-column label="最后车底任务id">
        <template #default="{row}">
          <el-select size="small" v-model="row.lastUndercarId">
            <el-option
                v-for="item in undercarIds"
                :key="item"
                :label="item"
                :value="item"
            />
          </el-select>
        </template>
      </el-table-column>

      <el-table-column label="作业场" prop="workYard">
        <template #default="{row}">
          <el-select size="small" v-model="row.workYard">
            <el-option
                v-for="item in yardList"
                :key="item"
                :label="item.name"
                :value="item.id"
            />
          </el-select>
        </template>
      </el-table-column>

      <el-table-column label="回库场" prop="backYard">
        <template #default="{row}">
          <el-select size="small" v-model="row.backYard">
            <el-option
                v-for="item in yardList"
                :key="item"
                :label="item.name"
                :value="item.id"
            />
          </el-select>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
import {tableNoPage} from "@/service/train";
import {getTransPlan2} from "@/service/transplan"
import {getItem} from "@/service/calendar";
import {getByLineId} from "@/service/yard";
import {tableWithCond} from "@/service/plan/historyPlanQuery";
import {ElMessage} from "element-plus";
import {clearAndAdd} from "@/service/dayPlanHistory";
import {selectLine} from "@/service/selector";

export default {
  name: "dayPlanHistoryDlg",
  data: () => {
    return {
      title: "确认上一个日计划相关信息",
      visible: false,
      formdata: {},
      trains: [],
      tableData: [],
      lineId: '',
      lineList: [],
      date: '',
      dateType: '',
      undercarIds: [],
      yardList: [],
      lastUndercarId: '',
    }
  },
  methods: {
    close() {
      this.formdata = {};
      this.trains = [];
      this.tableData = [];
      this.lineId = '';
      this.lineList = [];
      this.date = '';
      this.visible = false;
      this.dateType = '';
      this.undercarIds = [];
      this.yardList = [];
      this.lastUndercarId = '';
    },
    async init() {
      this.visible = true;
      this.date = "2022-05-31"; // 后续需要更改，改为前一天
      // this.date = Date.now();
      this.renderLineList();
    },
    async renderLineList() {
      let result;
      result = await selectLine();
      result.forEach(i => this.lineList.push(
          {
            "lineName": i.name,
            "lineId": i.id
          }
      ));
    },
    async renderTable() {
      let res = await tableNoPage(this.lineId);

      this.trains = res.data;
      this.trains.forEach(i => {
        this.tableData.push({lineId: this.lineId, trainId: i.id})
      })
    },
    async renderDate() {
      let res = await getItem(this.lineId, this.date);
      this.dateType = res.data.attribute;
      let s = ''
      if (this.dateType === "工作") {
        s = 'workday'
      } else if (this.dateType === '休息') {
        s = 'weekday'
      }
      res = await getTransPlan2(this.lineId, s);
      let list = res.data;
      list.forEach(i => {
        this.undercarIds.push(i.undercarId);
      })
      this.lastUndercarId = this.undercarIds[this.undercarIds.length - 1];
    },
    async renderYardList() {
      let res = await getByLineId(this.lineId);
      this.yardList = res.data;
    },
    async autoFill() {
      if (!this.lineId) {
        ElMessage.error("请先选择线路号");
        return;
      }
      let res = await tableWithCond(this.lineId, null, this.date, this.date, null);
      let list = res.list;
      list.forEach(i => {
        for (let j = 0; j < this.yardList.length; j++) {
          if (i.workYard === this.yardList[j].name) {
            i.workYardId = this.yardList[j].id;
            break;
          }
        }
      })

      list.forEach(i => {
        for (let j = 0; j < this.tableData.length; j++) {
          if (this.tableData[j].trainId == i.trainId) {
            this.tableData[j].workYard = i.workYardId;
            this.tableData[j].backYard = i.workYardId;
            break;
          }
        }
      })

      this.tableData.forEach(k => {
        if (!k.workYard && !k.backYard) {
          k.lastUndercarId = this.lastUndercarId;
        }
      })
    },
    clearTable() {
      this.tableData = [];
      this.trains.forEach(i => {
        this.tableData.push({lineId: this.lineId, trainId: i.id})
      })
    },
    async submit() {
      if (!this.lineId) {
        ElMessage.error("请先选择线路号");
        return;
      }
      let flag = true;
      this.tableData.forEach(i => {
        if (!i.lastUndercarId && !i.backYard) {
          flag = false;
        }
      })
      if (flag) {
        this.tableData.forEach(i => {
          i.date = this.date;
          i.lineId = this.lineId;
        })
        let res = await clearAndAdd(this.tableData);
        if (res.code === 0) {
          ElMessage.success("上传成功");
          this.$emit("afterDayPlanHistorySubmit")
          this.close();
        } else {
          ElMessage.error("上传失败");
        }
      } else {
        ElMessage.error("校验失败");
      }
    }
  },
  watch: {
    lineId: async function () {
      await this.renderTable();
      await this.renderDate();
      await this.renderYardList();
    },
  }
}
</script>

<style scoped>
/deep/ .el-table_1_column_1 {
  vertical-align: top;
}

/deep/ .el-table_1_column_1 .el-input {
  margin-top: 8px;
}
</style>