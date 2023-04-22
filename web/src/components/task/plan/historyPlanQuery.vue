<template>
  <div class="Breadcrumb">
    <span>计划制定管理 > 计划任务管理 > 历史检修计划查询</span>
  </div>
  <div class="container">
    <div class="content">
      <div class="selector">
        <el-row :gutter="10" style="margin-bottom: 10px;">
          <el-col :span="8">
            <span style="font-size: 12px; color: red;">* </span>
            <span style="font-size: 14px; margin-right: 8px;">线路选择: </span>
            <el-select v-model="lineId"
                       filterable
                       clearable
                       size="small"
                       placeholder="请选择线路名">
              <el-option
                  :key="index" v-for="(item, index) in this.lines"
                  :label="item.name"
                  :value="item.id"
              />
            </el-select>
          </el-col>

          <el-col :span="8">
            <span style="font-size: 14px; margin-right: 8px;">计划类型:</span>
            <el-select
                multiple
                v-model="planTypes"
                clearable
                size="small"
                placeholder="下拉选择(可多选)">
              <el-option label="年计划" value="年计划" key="年计划"/>
              <el-option label="月计划" value="月计划" key="月计划"/>
              <el-option label="周计划" value="周计划" key="周计划"/>
            </el-select>
          </el-col>
        </el-row>

        <el-row :gutter="10">
          <el-col :span="8">
            <span>开始时间: </span>
            <el-date-picker size="small" v-model="sdate" label="开始时间"/>
          </el-col>
          <el-col :span="8">
            <span>结束时间: </span>
            <el-date-picker size="small" v-model="edate" label="结束时间"/>
          </el-col>
        </el-row>
        <el-button size="small" type="primary" @click="query">查询</el-button>
      </div>
      <el-divider/>
      <el-empty v-show="!(originData && originData.length)" description="暂无内容展示"></el-empty>
      <!-- 这里的分页并不是真正的分页，只是按天查看而已 -->
      <div v-show="originData && originData.length">
        <div style="display: flex; justify-content: space-between">
          <el-button style="margin-left: 10px; margin-bottom: 4px;" size="small" @click="exportExcel" type="success">导出</el-button>
          <el-config-provider :locale="i18n">
            <el-pagination
                :currentPage="pageNum"
                :page-size="pageSize"
                hide-on-single-page
                layout="->, sizes, total, prev, pager, next, jumper"
                :total="days"
                :page-sizes="[30,60,90]"
                small
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
            />
          </el-config-provider>
        </div>

        <el-table
            :data="tableData2"
            border
            max-height="500"
        >
          <el-table-column label="日期" prop="performDate" fixed align="center" width="100"/>
          <el-table-column label="星期" prop="weekDays" fixed align="center" width="60"/>
          <el-table-column
              v-for="(item, index) in trains"
              :label="item"
              :key="index"
              :prop="item"
              align="center">
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import {get} from "@/utils/request";
import {selectTrain} from "@/service/selector";
import {ElMessage} from 'element-plus';
import moment from "moment/moment";
import XLSX from "xlsx";
import {getPagesOverview, tableWithCond} from "@/service/plan/historyPlanQuery";

export default {
  name: "historyPlanQuery",
  data: () => {
    return {
      lines: [],
      lineId: '',
      planTypes: [],
      sdate: '',  // 筛选条件 开始日期
      edate: '',  // 筛选条件 结束日期
      days: '',  // 开始时间和结束时间之间有多少天。
      status: '', // 执行状态筛选
      trains: [],
      originData: [],
      pageNum: 1,
      pageSize: 30,
      pageStartDate: '',  // 所有page开始时间
      i18n: {
        el: {
          pagination: {
            goto: '前往',
            pagesize: '天/页',
            total: `共 {total} 天`,
            pageClassifier: '页'
          }
        }
      }
    }
  },
  methods: {
    selectLine() {
      get("/api/line_list")
          .then(result => {
            this.lines = [];
            result.forEach(i => this.lines.push(
                {
                  "name": i.name,
                  "id": i.id
                }
            ))
          }, () => {
            this.lines = []
            console.log("⽹络请求失败")
          })
    },
    async getPageOverview() {
      let body = await getPagesOverview(this.lineId, this.planTypes);
      this.days = body.data.count;
      if (this.sdate) {
        this.pageStartDate = this.sdate
      } else {
        this.pageStartDate = body.data.start_date
      }
    },
    async renderTable() {
      // 动态加载表头, 不同的线路有不同车
      let result = await selectTrain(this.lineId);
      let traintemp = [];
      result.forEach(i => traintemp.push(i.id))
      // 对动态增加的表头进行排序 1-10
      this.trains = traintemp.sort();

      let contentAll = await tableWithCond(this.lineId, this.planTypes, this.pageStart, this.pageEnd, this.status)
      this.originData = contentAll.list;
      this.tableVisible = true;
    },
    async query() {
      if (!this.lineId) {
        ElMessage.error("请选择线路");
      } else {
        this.resetData();
        await this.getPageOverview();
        await this.renderTable();
      }
    },
    async exportExcel() {
      let fileName = this.lineId + "-" + Number(new Date());
      let EndDate = moment(this.pageStartDate).add(this.days - 1, "days").format("YYYY-MM-DD");
      let contentAll = await tableWithCond(this.lineId, this.planTypes, this.pageStartDate, EndDate, this.status)
      let origin = contentAll.list;
      let objdata = {};
      origin.forEach(i => {
        this.durationSplit(i, objdata);
      })
      let tableData = [];
      let endDate = moment(this.pageStartDate).add(this.days, 'days');
      tableData = this.handleTableData2(this.pageStartDate, endDate, objdata);

      let arr = [];
      arr.push(Object.keys(tableData[0]));
      tableData.forEach(i => {
            let arr2 = [];
            for (let key of Object.keys(i)) {
              if (i[key].content === undefined) {
                arr2.push(i[key])
              } else {
                arr2.push(i[key].content);
              }
            }
            arr.push(arr2);
          }
      )
      this.exportFile(arr, fileName);
    },

    exportFile(data, fileName) {
      // 数组转Excel
      const ws = XLSX.utils.aoa_to_sheet(data);
      /* 生成的工作部病添加工作表 */
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Sheet1')
      /* 保存到文件 */
      XLSX.writeFile(wb, fileName + '.xlsx');
    },
    handleSizeChange(e) {
      this.pageNum = 1;
      this.pageSize = e;
      this.renderTable();
    },
    handleCurrentChange(e) {
      this.pageNum = e;
      this.renderTable();
    },
    resetData() {
      this.days = '';
      this.status = '';
      this.trains = [];
      this.pageNum = 1;
      this.pageSize = 30;
      this.pageStartDate = '';
    },
    durationSplit(i, objdata) {  // 跨越多天的任务拆分
      let dur = i.duration;
      for (let j = 0; j < dur; j++) {
        let temp = JSON.parse(JSON.stringify(i));
        let str = moment(temp.performDate).add(j, 'days').format('YYYY/MM/DD')  // 开始时间+偏置日期，得到目标时间
        temp.performDate = str
        temp.duration = 1

        if (!objdata[temp.performDate]) {
          objdata[temp.performDate] = {};
        }
        if (!objdata[temp.performDate][temp.trainId]) {
          objdata[temp.performDate][temp.trainId] = {};
        }
        objdata[temp.performDate][temp.trainId][temp.planType] = temp;
      }
    },
    handleTableData2(pageStart, pageEnd_, obj) {
      let arr = [];
      let weekdaysoption = ["日", "一", "二", "三", "四", "五", "六"];

      let i = moment(pageStart)
      let pageEnd = moment(pageEnd_)
      for (; pageEnd.diff(i) >= 0; i.add(1, "days")) {
        let str = i.format('YYYY/MM/DD');
        let row = {}
        row.performDate = str; //日期渲染
        row.weekDays = weekdaysoption[moment(str).day()] //星期渲染
        arr.push(row)
        let item = obj[row.performDate];
        for (let j = 0; j < this.trains.length; j++) {
          if (item !== undefined && item[this.trains[j]] !== undefined) {
            let tasktypes = [];
            for (let pt of Object.keys(item[this.trains[j]])) { // 遍历年计划、月计划、周计划
              if (item[this.trains[j]][pt].taskType === "均衡修") {
                tasktypes.push(item[this.trains[j]][pt].taskContent)
              } else {
                tasktypes.push(item[this.trains[j]][pt].taskType)
              }
            }
            row[this.trains[j]] = tasktypes.join('+')
          } else {
            row[this.trains[j]] = ''
          }
        }
      }
      return arr;
    },
  },
  async mounted() {
    this.lineId = '';
    await this.selectLine();
  },
  computed: {
    obj() {
      let objdata = {};
      // 跨越多天的任务拆分，
      this.originData.forEach(
          (i) => {
            this.durationSplit(i, objdata);
          })
      return objdata
    },
    tableData2() {
      let arr = []
      arr = this.handleTableData2(this.pageStart, this.pageEnd, this.obj);
      return arr;
    },
    tableData2Excel() {
      // 用于excel 下载的对象
      let arr = [];
      arr.push(Object.keys(this.tableData2[0]));
      this.tableData2.forEach(i => {
            let arr2 = [];
            for (let key of Object.keys(i)) {
              if (i[key].content === undefined) {
                arr2.push(i[key])
              } else {
                arr2.push(i[key].content);
              }
            }
            arr.push(arr2);
          }
      )
      return arr;
    },
    pageStart() {
      return moment(this.pageStartDate).add((this.pageNum - 1) * this.pageSize, "days").format("YYYY-MM-DD");
    },
    pageEnd() {
      let date1 = moment(this.pageStart).add(this.pageSize - 1, "days");
      let date2 = moment(this.pageStartDate).add(this.days - 1, "days")
      let minDate = moment.min(date1, date2)
      return minDate.format("YYYY-MM-DD");
    },
  },

}
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
  margin: 10px;
}

.selector {
  margin: 10px;
}
</style>