<template>
  <div class="mainContent" style="display: flex;">
    <div ref="left"
         :style="{width: this.width}"
    >
      <el-scrollbar ref="left">
        <el-button type="success" v-show="this.type === 'upload' ">上传里程数据</el-button>
        <el-table :data="this.tableData"
        >
          <el-table-column prop="trainId" label="列车号" sortable fixed width="100px"/>
          <el-table-column label="查看折线图" sortable fixed width="100px">
            <template #default="{row}">
              <el-button size="small" @click="reviewTendGraph(row.trainId)" type="primary">查看</el-button>
            </template>
          </el-table-column>

          <el-table-column label="空白位置插值填充" sortable fixed width="100px">
            <template #default="{row, $index}">
              <el-button
                  size="small"
                  v-show="showAutoInterpolationBtn[$index]"
                  @click="autoInterpolation(row)" type="primary">自动插值
              </el-button>
            </template>
          </el-table-column>

          <el-table-column
              v-for="(item, index) in tableHeaddate"
              :label="item"
              :key="index"
              :prop="item"
              align="center"
              width="100">
          </el-table-column>
        </el-table>
      </el-scrollbar>
    </div>

    <mileageGraphDlg @updated="handleMileageDataUpdated" ref="mileageGraphDlg"/>

    <div v-show="this.mileageChangeOutsideTable.length" :style="{height: this.height}" class="rightColumn">
      <el-scrollbar style="height: 100%;">
        <span>插值数据 </span>
        <el-button size="small" type="success" @click="iterpolationValueSubmit">插值数据提交</el-button>
        <el-button size="small" type="success" @click="mileageChangeOutsideTableClearAll">清空</el-button>
        <el-table :data="this.mileageChangeOutsideTable">
          <el-table-column prop="trainId" label="列车号"/>
          <el-table-column prop="date" label="日期"/>
          <el-table-column prop="mileage" label="里程值"/>
          <el-table-column label="操作">
            <template #default="{row}">
              <el-button type="info" @click="this.mileageChangeOutsideTableRemoveItem(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-scrollbar>
    </div>
  </div>

</template>

<script>
import moment from "moment";
import mileageGraphDlg from "@/views/mileage/mileageGraphDlg";
import {mapMutations, mapState} from "vuex";
import {put, post} from "@/utils/request";
import {ElMessage} from "element-plus";

export default {
  name: "mileagePageTable",
  props: {
    list: Array,
    startDate: String,
    endDate: String,
    type: {
      // type: edit 表示为编辑状态。可以上传 mileageChangeOutsideTable 中的数据到数据库。
      // type: upload 表示上述状态。需要把 mileageChangeOutsideTable 中的数据合并二维表中的数据一起上传。
      required: true,
      type: String
    },
  },
  data: () => {
    return {
      height: 0,  // 用于确定右边插值数据提交边栏的高度的。
      width: "calc(100% - 10px)",
    }
  },
  emits: ["updated"],
  computed: {
    tableHeaddate() {
      let arr = [];
      if (this.startDate && this.endDate) {
        let date1 = moment(this.startDate);
        let date2 = moment(this.endDate);
        while (date1.isBefore(date2)) {
          arr.push(date1.format("YYYY-MM-DD"));
          date1 = date1.add(1, "days");
        }
        arr.push(date2.format("YYYY-MM-DD"))
      }
      return arr;
    },

    tableData() {
      let arr = JSON.parse(JSON.stringify(this.list));

      arr.forEach(item => {
        let trainId = item.trainId;
        let a = this.mileageChangeOutsideTable.filter(i => i.trainId === trainId);
        a.forEach(j => {
          item[j.date] = j.mileage;
        })
      })
      return arr;
    },
    showAutoInterpolationBtn() {
      let arr = [];
      this.list.forEach(item => { // 遍历每一行
        let flag = false;
        let date1 = moment(this.startDate);
        let date2 = moment(this.endDate);

        if (Object.keys(item).length < 1) {
          arr.push(false);
          return;
        }

        while (date1.isBefore(date2)) {
          let dateFormat = date1.format("YYYY-MM-DD");
          if (!item[dateFormat]) {
            flag = true;
            arr.push(flag);
            break;
          }
          date1 = date1.add(1, "days");
        }
        if (date1.isSame(date2, "day")) {// 搜索到了最后
          if (item[date1.format("YYYY-MM-DD")]) {
            flag = false;
          } else {
            flag = true;
          }
          arr.push(flag);
        }
      })
      return arr;
    },
    ...mapState(['mileageChangeOutsideTable']),
  },
  methods: {
    reviewTendGraph(trainId) {
      let temp = this.list.find(item => {
        return item.trainId === trainId
      })
      this.$refs.mileageGraphDlg.init(temp);
    },
    handleMileageDataUpdated(arr) {
      if (this.type === 'edit') {
        // 当 type 为 edit 的时候，直接提交数据。若 type 为 upload 的时候，则不处理，后续使用一个全局的 upload 按钮来上传数据。
        // 其实对于新增数据我们是要进行插入操作，而非 更新操作的，不过这里不管，具体逻辑由后端处理
        return put("/api/mileage_history", arr).then((res) => {
          if (res.code === 0) {
            ElMessage.success("更新成功");
            this.mileageChangeInsideTableClearAll();
            this.mileageChangeOutsideTableClearByTrainId(this.trainId);
            this.$emit("updated", this.trainId);
          } else {
            ElMessage.success("更新失败");
          }
        }, (res) => {
          ElMessage.success("更新失败");
        })
      }
    },
    autoInterpolation(e) {
      // 插值的时候，对于某一日的缺失值，随便找两个值，如前后各一个值，两个都是前面的值、两个都是后面的值，
      // 用周围的两个值，做一个线性直线，来插值这个元素。
      // 甚至可能只能找到一个值，则填充为相同的这个值.
      let date1 = moment(this.startDate);
      let date2 = moment(this.endDate);
      let trainId = e.trainId;
      // let arr = [];
      while (date1.isSameOrBefore(date2)) {
        let dateFormat = date1.format("YYYY-MM-DD");
        if (!e[dateFormat]) {
          // 遇到缺失值
          // item : {trainId: '', date: '', mileage: '', prevMileage: '', type: ''}
          let obj = {};
          obj.trainId = trainId;
          obj.date = dateFormat;
          obj.mileage = this.getInterpolationValue(e, dateFormat);
          obj.type = "插值";
          obj.prevMileage = "新插值";
          this.mileageChangeOutsideTableAddItem(obj);
        }
        date1 = date1.add(1, "days");
      }
    },
    getInterpolationValue(e, dateFormat) {
      // e 在 date 这一天是没有值的，需要向前或向后找
      // 两个指针同时往前和往后找。找到两个值即可。或者只能找到一个值。
      let startDate = moment(this.startDate);
      let endDate = moment(this.endDate);
      let date = moment(dateFormat);
      let prevDate = moment(dateFormat);
      let postDate = moment(dateFormat);
      let prevDateFormat = prevDate.format("YYYY-MM-DD");
      let postDateFormat = postDate.format("YYYY-MM-DD");

      while (prevDate.isSameOrAfter(startDate)) {
        prevDateFormat = prevDate.format("YYYY-MM-DD");
        if (e[prevDateFormat]) {
          break;
        } else {
          prevDate.subtract(1, "days");
        }
      }
      while (postDate.isSameOrBefore(endDate)) {
        postDateFormat = postDate.format("YYYY-MM-DD");
        if (e[postDateFormat]) {
          break;
        } else {
          postDate.add(1, "days");
        }
      }

      if (e[prevDateFormat] && e[postDateFormat]) {
        let value1 = e[prevDateFormat];
        let value2 = e[postDateFormat];
        let k = (value2 - value1) / (postDate.diff(prevDate));
        return parseInt(value1 + k * (date.diff(prevDate)));
      } else if (e[prevDateFormat] && postDate.isAfter(endDate, "day")) {
        return e[prevDateFormat]
      } else if (e[postDateFormat] && prevDate.isBefore(startDate, "day")) {
        return e[postDateFormat]
      }
      return null;
    },
    iterpolationValueSubmit() {
      // 处理插值数据提交
      return post("/api/mileage_history", this.mileageChangeOutsideTable).then((res) => {
        if (res.code === 0) {
          ElMessage.success("保存成功");
          this.mileageChangeOutsideTableClearAll();
          this.$emit("updated");
        } else {
          ElMessage.success("更新失败");
        }
      }, (res) => {
        ElMessage.success("更新失败");
      })
    },
    ...mapMutations(["mileageChangeOutsideTableAddItem", "mileageChangeOutsideTableRemoveItem",
      "mileageChangeOutsideTableClearAll", "mileageChangeInsideTableClearAll",
      "mileageChangeOutsideTableClearByTrainId", "closeLeftNav"
    ])
  },
  watch: {
    list: {
      handler() {
        this.$nextTick(() => {
          this.height = `${this.$refs.left.offsetHeight}px`
        })
      },
      immediate: true
    },
    mileageChangeOutsideTable: {
      handler(newVal, oldVal) {
        if (newVal.length !== 0) {
          this.closeLeftNav();
          this.width = "calc(100% - 400px)"
        } else {
          this.width = "calc(100% - 10px)"
        }
      },
      immediate: true,
      deep: true,
    },
  },
  components: {
    mileageGraphDlg
  },
}
</script>

<style scoped>
.rightColumn {
  border: 1px solid #e1e1e1;
  width: 400px;
  padding: 10px;
  background-color: #fcfcfc;
}

/*最外层透明*/
.rightColumn ::v-deep .el-table,
.rightColumn ::v-deep .el-table__expanded-cell {
  background-color: transparent !important;
}

/* 表格内背景颜色 */
.rightColumn ::v-deep .el-table th,
.rightColumn ::v-deep .el-table tr,
.rightColumn ::v-deep .el-table td {
  background-color: transparent !important;
  border: 0;
}

/*去除底边框*/
.rightColumn ::v-deep.el-table td.el-table__cell {
  border: 0;
}

.rightColumn ::v-deep.el-table th.el-table__cell.is-leaf {
  border: 0;
}
</style>