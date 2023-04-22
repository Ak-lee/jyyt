<template>
  <div class="Breadcrumb">
    <spn>里程预测管理 > 模型预测结果</spn>
  </div>
  <div class="container">
    <div class="content">
      <el-table
          :data="predictReslist2"
          style="width: 100%;margin-top:20px"
          border
          max-height="500px"
      >
        <el-table-column label="列车号" prop="trainId" sortable fixed align="center" width="100"/>
        <el-table-column label="查看趋势图" prop="picture" fixed align="center" width="150">
          <template #default="scope">
            <el-button type="primary" class="picButton" size="small" @click="openDialog(scope.row)">
              点击查看图片
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
    </div>
    <el-dialog
        title="趋势图"
        v-model="dialogVisible"
        width="40%">

      <el-image :src="'data:image/png;base64,'+ this.imgSrc"></el-image>
    </el-dialog>
  </div>
</template>
<script>
import {get} from "@/utils/request";
import moment from "moment";

export default {
  data() {
    return {
      predictReslist: [],
      predictReslist2: [],
      tableHeaddate: [],
      endTrainingdates: [],
      pos: -1,
      prop: '',
      nowTime: '',
      imgSrc: '',
      dialogVisible: false,
    }
  },
  mounted() {
    this.getPredres();
  },
  methods: {
    async openDialog(row) {
      this.dialogVisible = true;
      let trainId = row.trainId

      get("/api/mileage_history/getPredImg?trainId=" + trainId)
          .then(res => {
            this.imgSrc = res;
          })
    },
    getPredres() {
      get("/api/mileage_history/getPredres")
          .then(res => {
            this.predictReslist = res.data;
            this.nowTime = this.getCurrentTime()
            this.updateListform();
          }, () => {
            console.log("网络错误")
            this.predictReslist = [];
          })
    },
    //修改list形式（把日期作为表头一部分）
    updateListform() {
      var trainId = '';
      var obj = {};
      var dateList = [];
      this.predictReslist.forEach((item, index) => {
        if (trainId != item.trainId) {
          if (obj != null && obj['trainId'] != null) {
            this.endTrainingdates.forEach((i, index) => {
              if (obj["trainId"] === i.trainId) {
                var endDate = this.formateDate(i.date);
                obj["endTrainingdate"] = endDate;
                obj['startTrainingdate'] = moment(endDate).subtract(1, 'month').format('YYYY-MM-DD')
              }
            })
            obj['predDays'] = 7;
            this.predictReslist2.push(obj);
          }
          obj = {};
          trainId = item.trainId;
          obj["trainId"] = item.trainId;
        }
        item.calendar = this.formateDate(item.calendar);
        obj["picture"] = item.picture
        obj[item.calendar] = item.mileage;
        dateList.push(item.calendar);
      })
      this.tableHeaddate = this.listUnique(dateList);
    },
    //对日期表头数组去重
    listUnique(arr) {
      var hash = [];
      for (var i = 0; i < arr.length; i++) {
        if (arr.indexOf(arr[i]) == i) {
          hash.push(arr[i]);
        }
      }
      return hash;
    },
    //日期转换
    formateDate(datetime) {
      // let  = "2019-11-06T16:00:00.000Z"
      function addDateZero(num) {
        return (num < 10 ? "0" + num : num);
      }

      let d = new Date(datetime);
      let formatdatetime = d.getFullYear() + '-' + addDateZero(d.getMonth() + 1) + '-' + addDateZero(d.getDate());
      return formatdatetime;
    },
//点击单元格
    async cellClick(index, prop1) {
      this.pos = index;
      this.prop = prop1;
    },
    //单元格复原
    async reback() {
      this.prop = '';
    },
    getCurrentTime() {
      //获取当前时间并打印
      var _this = this;
      let yy = new Date().getFullYear();
      let mm = new Date().getMonth() + 1;
      let dd = new Date().getDate();
      let hh = new Date().getHours();
      let mf = new Date().getMinutes() < 10 ? '0' + new Date().getMinutes() : new Date().getMinutes();
      let ss = new Date().getSeconds() < 10 ? '0' + new Date().getSeconds() : new Date().getSeconds();
      _this.gettime = yy + '年' + mm + '月' + dd + '日' + hh + ':' + mf + ':' + ss;
      return _this.gettime;
    },
    getrows(row) {
      this.imgSrc = row.picture;
    }
  }
}
</script>
<style scoped>
.Breadcrumb {
  padding: 10px 0px;
}

.container {
  background-color: white;
  border: 1px solid #9c9c9c;
  min-height: calc(100vh - 150px);
}

.content {
  margin: 10px;
}

.timTip {
  font-size: 13px;
}

.picButton {
  font-size: 13px;
  margin: 10px auto;
}
</style>

