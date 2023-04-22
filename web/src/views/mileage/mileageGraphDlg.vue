<template>
  <el-dialog append-to-body :title="title" v-model="visible" width="50%" :before-close="close">
    <echartLineGraph @itemClick="handleItemClick" :trainId="trainId" :data="data" :data2="data2"/>
    <div>
      <el-form ref="form"
               v-show="this.editItem.date"
      >
        <el-form-item label="日期" :label-width="120" prop="date">
          <el-date-picker
              v-model="editItem.date"
              disabled
              type="date"
          />
        </el-form-item>
        <el-form-item label="里程值" :label-width="120" prop="mileage">
          <el-input-number v-model="editItem.mileage" :min="0" :step="1"/>
        </el-form-item>
      </el-form>
      <el-form v-show="this.mileageChangeTableThisPage.length">
        <el-scrollbar max-height="300px">
          <el-table :data="this.mileageChangeTableThisPage">
            <el-table-column prop="date" label="日期"/>
            <el-table-column prop="prevMileage" label="更新前里程值"/>
            <el-table-column prop="mileage" label="更新后里程值"/>
            <el-table-column label="操作">
              <template #default="{row}">
                <el-button @click="this.handleEditItemRemove(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-scrollbar>
        <div style="text-align: right">
          <el-button @click="mileageChangeSubmit" style="margin-top: 10px;margin-right: 10px; align-self: end;"
                     type="primary">确认
          </el-button>
        </div>
      </el-form>
    </div>
  </el-dialog>
</template>

<script>
import echartLineGraph from "@/views/mileage/echart-line-graph";
import {mapGetters, mapMutations, mapState} from "vuex";
import moment from "moment";

export default {
  name: "mileageGraphDlg",
  data: () => {
    return {
      visible: false,
      mileageData: {},
      trainId: '',
      editItem: {date: '', mileage: ''}, // 当编辑里程值的时候，用于保存当前修改后的里程值
    }
  },
  emits: ["updated"],
  computed: {
    title() {
      return this.trainId + " 列车里程增长图"
    },
    data() {
      let obj = JSON.parse(JSON.stringify(this.mileageData));
      delete obj['trainId'];
      let arr = [];
      for (let key in obj) {
        let arr2 = [];
        arr2.push(key);
        arr2.push(obj[key]);
        arr.push(arr2)
      }
      arr.sort((a, b) => {
        let dateA = moment(a.date);
        let dateB = moment(b.date);
        return dateA.isSameOrBefore(dateB);
      })
      return arr;
    },
    mileageChangeTableThisPage() {
      return this.mileageChangeTable.filter(item => item.trainId === this.trainId)
    },
    data2() {
      let obj = JSON.parse(JSON.stringify(this.mileageData)); // 其中保存了每一天的里程值
      delete obj['trainId'];

      this.mileageChangeTableThisPage.forEach(item => {
        obj[item.date] = item.mileage;
      })

      let arr = [];
      for (let key in obj) {
        let arr2 = [];
        arr2.push(key);
        arr2.push(obj[key]);
        arr.push(arr2)
      }
      arr.sort((a, b) => {
        let dateA = new Date(a[0]);
        let dateB = new Date(b[0]);
        return dateA - dateB;
      })
      return arr;
    },
    ...mapState(["mileageChangeInsideTable"]),
    ...mapGetters(["mileageChangeTable"])
  },
  methods: {
    init(data) {
      this.mileageData = JSON.parse(JSON.stringify(data));
      // this.mileageData = data;
      this.trainId = this.mileageData.trainId;
      this.visible = true;
      this.editIndex = -1;
      this.data2 = [];
    },
    close() {
      this.visible = false;
    },
    handleItemClick(data) {
      this.editItem.date = data.x;
      this.editItem.mileage = data.y;
    },
    mileageChangeSubmit() {
      let arr = this.mileageChangeTable.filter(item => item.trainId === this.trainId)
      this.$emit("updated", arr);
      this.visible = false;
    },
    handleEditItemRemove(item) {
      if (!item.type) {
        this.mileageChangeInsideTableRemoveItem(item);
      } else {
        this.mileageChangeOutsideTableRemoveItem(item);
      }
      this.editItem.date = '';
      this.editItem.mileage = '';
    },
    ...mapMutations(["mileageChangeInsideTableAddItem", "mileageChangeInsideTableRemoveItem", "mileageChangeOutsideTableRemoveItem",
      "mileageChangeInsideTableClearAll", "mileageChangeOutsideTableClearByTrainId"])
  },
  components: {
    echartLineGraph
  },
  watch: {
    "editItem.mileage": function (newVal, oldVal) {
      // this.data 是一个二维数组
      if (newVal && this.editItem.date) {
        let j = this.data.find((a) => {
          return a[0] === this.editItem.date
        })
        let originMileage = j[1];
        let obj = {};
        obj.trainId = this.trainId;
        obj.date = this.editItem.date;
        obj.mileage = newVal;
        if (newVal !== originMileage) {
          obj.prevMileage = originMileage
          obj.type = "修改"
          this.mileageChangeInsideTableAddItem(obj)
        } else {
          this.mileageChangeInsideTableRemoveItem(obj);
        }
      }
    },
    "mileageData": function (newVal, oldVal) {
      this.mileageChangeInsideTableClearAll();
      this.editItem.date = '';
      this.editItem.mileage = '';
    }
  }
}
</script>

<style scoped>

</style>