<template>
  <div class="Breadcrumb">
    <span>里程预测管理 > 历史数据导入</span>
  </div>
  <div class="tabContainer">
    <div class="content">
      <div style="display: flex;">
        <el-upload
            action
            accept=".xlsx, .xls, .csv"
            :auto-upload="false"
            :show-file-list="false"
            :on-change="handleUploadChange"
        >
          <el-tooltip content="上传里程数据请保持与已保存数据日期连续" placement="top">
            <el-button size="small" type="primary">打开里程 excel 文件</el-button>
          </el-tooltip>
        </el-upload>
        <el-button size="small" @click="downloadTemplateFile" type="primary" style="margin-left: 20px;">里程文件模板下载</el-button>
      </div>
      <div id="dataImportTabs">
        <el-tabs v-model="activeName">
          <el-tab-pane label="历史里程" name="first">
            <div style="display: flex; margin: 8px 0;">
              <div>
                <span style="font-size: 14px">线路名：</span>
                <el-select
                    size="small"
                    v-model="lineId"
                    clearable
                    placeholder="请选择线路名"
                >
                  <el-option
                      :key="index" v-for="(item, index) in lines"
                      :label="item.name"
                      :value="item.id"
                  />
                </el-select>
              </div>
              <div style="margin-left: 10px;">
                <el-button size="small" @click="handleSearchBtnClick" class="search" type="success">
                  <el-icon>
                    <search/>
                  </el-icon>
                  <span>查询</span>
                </el-button>
              </div>
            </div>

            <el-empty v-show="!mileageHistoryPageTotalDays" description="请先选择线路号"/>

            <div v-show="mileageHistoryPageTotalDays">
              <mileagePageTable @updated="handleMileageDataUpdated" type="edit" :startDate="this.pageMinDate"
                                :endDate="this.pageMaxDate" :list="this.mileageHistory2"/>
              <el-config-provider :locale="i18n">
                <el-pagination
                    style="margin-top: 6px;"
                    @size-change="(val)=>historyPageSizeChange(this.mileageHistory2, val)"
                    @current-change="(val)=>historyPageCurrentChange(this.mileageHistory2, val)"
                    :current-page="mileagePageNo"
                    :page-sizes="[60,90, 120]"
                    :page-size="mileagePageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    small
                    :total="mileageHistoryTotalDays">
                </el-pagination>
              </el-config-provider>
            </div>
          </el-tab-pane>

          <el-tab-pane label="正确数据" name="correctData">
            <el-button type="success"
                       size="small"
                       class="submitCorrectDataBtn"
                       v-bind:disabled="this.getCorrectData.length === 0"
                       @click="submit">正确数据提交
            </el-button>
            <el-table
                style="width: 100%;"
                :data="getCorrectData"
                max-height="600px"
                border
            >
              <el-table-column prop="trainId" label="列车号" align="center"/>
              <el-table-column prop="date" label="日期" align="center">
                <template #default="{row}">
                  {{
                    this.$moment(row.date).format("YYYY年MM月DD日")
                  }}
                  <!--                  {{ dateFormatter(row.date, "YYYY年MM月DD日") }}-->
                </template>
              </el-table-column>
              <el-table-column prop="mileage" label="里程值" align="center"/>
            </el-table>
          </el-tab-pane>

          <el-tab-pane label="错误数据" name="incorrectData">
            <el-table
                style="width: 100%"
                :data="getIncorrectData"
                border
                max-height="500px"
                class="incorrectDataTable"
            >
              <el-table-column prop="id" label="序号" width="80px" align="center"/>
              <el-table-column prop="trainId" label="列车号" align="center">
                <template #default="scope">
                  <div>
                    <span> {{ scope.row.trainId }} </span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="日期" prop="date" align="center">
                <template #default="{row}">
                  {{
                    this.$moment(row.date).format("YYYY年MM月DD日")
                  }}
                </template>
              </el-table-column>
              <el-table-column prop="mileage" label="里程值" width="100px" align="center">
                <template #default="scope">
                  <div @click="cellClick(scope.$index,'mileage')" @mouseout="reback">
                    <el-input v-model="scope.row.mileage" v-if="scope.$index == pos && prop == 'mileage'"></el-input>
                    <span v-else> {{ scope.row.mileage }} </span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="reviewMsg" label="错误说明" align="center"/>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
    `
  </div>
</template>

<script>
import {get, post} from '@/utils/request';
import xlsx from 'xlsx';
import {character, getFormatDate_XLSX, readFile} from "@/utils/upload";
import {ElMessage} from "element-plus";
import {Search} from '@element-plus/icons-vue';
import mileagePageTable from "@/views/mileage/mileagePageTable";
import {mapMutations} from "vuex";
import moment from "moment/moment";

export default {
  data() {
    return {
      activeName: 'first', // 用于切换tab
      lines: [],  // 线路号
      lineId: '', // 历史里程数据筛选线路号
      tempData: [], // 用于excel数据解析
      mileagePageSize: 60,
      mileagePageNo: 1,
      pos: -1,
      prop: '',
      pageNum: 1,
      pageSize: 20,
      mileageHistory1: [],  // mileageHistory1 存储表示原始从后台读取的里程数据
      mileageHistory2: [],
      min_date: '', // 已保存的里程记录中，时间最小者。
      max_date: '', // 已保存的里程记录中，时间最大者。
      checkTag: '',
      i18n: {
        el: {
          pagination: {
            goto: '前往',
            pagesize: '天/页',
            total: `共 {total} 天`,
            pageClassifier: '页'
          }
        }
      },
    }
  },
  components: {
    Search,
    mileagePageTable,
  },
  computed: {
    getCorrectData() {
      return [...this.tempData.filter(item => item.reviewStatus)];
    },
    getIncorrectData() {
      return [...this.tempData.filter(item => !item.reviewStatus)];
    },
    mileageHistoryTotalDays() {
      // 总共有多少天;
      if (this.max_date && this.max_date) {
        return moment(this.max_date).diff(this.min_date, "days") + 1;
      } else {
        return 0;
      }
    },
    mileageHistoryPageTotalDays() {
      if (this.pageMinDate && this.pageMaxDate) {
        return moment(this.pageMinDate).diff(this.pageMaxDate, "days") + 1;
      } else {
        return 0;
      }
    },
    pageMaxDate() {
      let date = moment(this.max_date).subtract(
          (this.mileagePageNo - 1) * this.mileagePageSize, "days"
      )
      return moment.max(date, moment(this.min_date)).format("YYYY-MM-DD");
    },
    pageMinDate() {
      let date = moment(this.pageMaxDate)
          .subtract(this.mileagePageSize - 1, "days")
      return moment.max(date, moment(this.min_date)).format("YYYY-MM-DD");
    },
    tableHeaddate() {
      let arr = [];
      let date1 = moment(this.pageMinDate);
      let date2 = moment(this.pageMaxDate);
      while (date1.isBefore(date2)) {
        arr.push(date1.format("YYYY-MM-DD"));
        date1 = date1.add(1, "days");
      }
      arr.push(date2.format("YYYY-MM-DD"))
      return arr;
    },
  },
  methods: {
    async handleSearchBtnClick() {
      if (!this.lineId) {
        ElMessage.error("请选择线路号.")
        return;
      }
      this.min_date = '';
      this.max_date = '';
      await this.getPageOverview()
      await this.renderTable()
    },
    async handleMileageDataUpdated(trainId) {
      await this.renderTable();
      if (trainId) {
        this.reviewTendGraph(trainId);
      }
    },
    reviewTendGraph(trainId) {
      let temp = this.mileageHistory2.find(item => {
        return item.trainId === trainId
      })
      this.$refs.mileageGraphDlg.init(temp);
    },
    //page改变时的回调函数
    historyPageCurrentChange(list, val) {
      this.mileagePageNo = val;
      this.renderTable()
    },
    //size改变时
    historyPageSizeChange(list, val) {
      this.mileagePageSize = val;
      this.mileagePageNo = 1;
      this.renderTable()
    },
    async handleUploadChange(ev) {
      let file = ev.raw;
      if (!file) return;

      let data = await readFile(file)
      let workbook = xlsx.read(data, {type: 'binary'});
      let worksheet = workbook.Sheets[workbook.SheetNames[0]];
      let list = xlsx.utils.sheet_to_json(worksheet);
      let arr = [];
      list.forEach((item, index) => {
        let isError = false;
        let obj = {}
        obj["reviewStatus"] = true
        for (let key in character) {
          if (!character.hasOwnProperty(key)) break;
          let v = character[key],
              text = v.text,
              type = v.type
          v = item[text] || ''
          if (v === '') {
            isError = true;
          } else {
            if (type === 'string') {
              v = String(v)
            }
            if (type === 'number') {
              let w = Number(v)
              if (isNaN(w)) {
                isError = true;
              } else {
                v = w;
              }
            }
            if (type === 'date') {
              let w = Number(v)
              if (isNaN(w)) {
                isError = true;
              } else {
                v = getFormatDate_XLSX(w);
                v = moment(v).format("YYYY-MM-DD");
              }
            }
          }
          obj[key] = v
          obj["id"] = index + 1
        }
        if (isError) {
          obj["reviewStatus"] = false
          obj["reviewMsg"] = "解析错误"
        }
        arr.push(obj)
      })
      // 展示到页面中, 会将返回的数据写入到 this.tempData 中。
      await this.reviewOnline(arr);
    },

    //和数据库内的数据进行对比
    downloadTemplateFile() {
      let arr1 = ["CARRRIAGE", "MILEAGE", "MILE_DATE"];
      let arr2 = ["CD17001(即列车号)", "221000(即公里数)", "2021/03/05 (即日期)"]
      this.exportFile([arr1, arr2], "里程数据上传模板");
    },
    // 数组转 Excel
    exportFile: (data, fileName) => {
      /* 把转换 JS数据数组的数组为工作表 */
      const ws = xlsx.utils.aoa_to_sheet(data);
      /* 生成的工作部病添加工作表 */
      const wb = xlsx.utils.book_new();
      xlsx.utils.book_append_sheet(wb, ws, 'Sheet1')
      /* 保存到文件 */
      xlsx.writeFile(wb, fileName + '.xlsx');
    },
    async reviewOnline(arr) {
      let a = arr.filter(i => i.reviewStatus);
      return post("/api/excel/review", a)
          .then((res) => {
            res.forEach(item => {
              let data = a.filter(i => i.id === item.id).at(0)
              if (item.type === "新增") {
                data.reviewStatus = true;
                data.reviewMsg = item.type;
              } else {
                data.reviewStatus = false;
                data.reviewMsg = item.type;
              }
            })
            let result = JSON.parse(JSON.stringify(a));
            result.forEach(i => {
              let index = arr.findIndex(j => j.id === i.id);
              arr[index] = i;
            })
            this.tempData = JSON.parse(JSON.stringify(arr));
          }, () => {
            console.log("请求后台校验数据发生网络错误");
          })
    },
    async submit() {
      post("/api/excel/saveBatch", this.getCorrectData)
          .then((res) => {
            ElMessage.success("成功提交 " + res + " 条数据");
            this.activeName = "first";
          }, () => {
            ElMessage.error("数据提交失败");
            console.log("数据提交失败")
          })
    },
    handleCurrentChange(val) {
      this.pageNum = val;
      this.renderTable();
    },
    handleSizeChange(val) {
      this.pageSize = val;
      this.renderTable();
    },
    async getPageOverview() {
      return get("/api/mileage_history/getPagesOverview", {
        lineId: this.lineId
      }).then((res) => {
        let data = res.data;
        this.min_date = data.min_date;
        this.max_date = data.max_date;
      }, () => {
        ElMessage.error("网络错误，请求失败.")
      })
    },
    async renderTable() {
      // 根据 线路号、开始时间、结束时间进行数据查询。
      // get("/api/mileage_history/table?curPage=" + this.pageNum + "&size=" + this.pageSize)
      this.mileageChangeOutsideTableClearAll();
      return get("/api/mileage_history/table", {
        lineId: this.lineId,
        sdate: this.pageMinDate,
        edate: this.pageMaxDate,
      })
          .then((res) => {
            if (res.code == 0) {
              this.mileageHistory1 = res.data;
              this.updateListform();
            } else {
              ElMessage.error("网络请求失败")
            }
          }, () => {
            ElMessage.error("网络请求失败")
          });
    },
    //修改 list 形式（把日期作为表头一部分）
    updateListform() {
      var trainId = '';
      var obj = {};
      this.mileageHistory2 = [];
      this.mileageHistory1.forEach((item) => {
        if (trainId !== item.trainId) {   // 处理所有的列车, 这里有一个重要的假设，即所有的列车都是连续出现的，都是按列车号拍过序的。
          if (obj['trainId'] != null) {
            this.mileageHistory2.push(obj);
          }
          obj = {};
          trainId = item.trainId;
          obj["trainId"] = item.trainId;
        }
        // 下面开始处理所有的日期
        obj[item.date] = item.mileage;
      })
    },
    ...mapMutations(["mileageChangeOutsideTableClearAll"])
  },
  mounted() {
    // 挂载到页面上时
    get("/api/line_list")
        .then(result => {
          this.lines = []
          result.forEach(i => this.lines.push(
              {
                "name": i.name,
                "id": i.id
              }
          ))
        }, () => {
          this.lines = []
          ElMessage.error("网络请求失败")
        })
  }
  ,
  component: {
    Search,
  }
}
</script>

<style scoped>

.Breadcrumb {
  padding: 10px 0px;
}

.tabContainer {
  border: 1px solid #e1e1e1;
  background-color: white;
  min-height: calc(100vh - 150px);
}

.content {
  padding: 10px;
}

.submitCorrectDataBtn {
  margin: 10px;
}

.incorrectDataTable {
  margin: 10px;
}

#dataImportTabs /deep/ .el-tabs__active-bar {
  display: none;
}

#dataImportTabs /deep/ .el-tabs__item:nth-child(2) {
  padding-left: 20px;
}

#dataImportTabs /deep/ .el-tabs__item:last-child {
  padding-right: 20px;
}

#dataImportTabs ::v-deep(.el-tabs__item.is-active) {
  /*border: none !important;*/
  margin-bottom: 2px;
}

#dataImportTabs /deep/ .el-tabs__header.is-top {
  margin: 0;
}
</style>