<template>
  <div>
    <span>线路选择：</span>
    <el-select
        v-model="selectedLine"
        placeholder="请选择线路名"
    >
      <el-option
          :key="index" v-for="(item, index) in lines"
          :label="item.name"
          :value="item.id"
      />
    </el-select>
    <span>
      列车号：
    </span>
    <el-select
        v-model="selectedTrain"
        placeholder="请选择列车号"
        @change="changeTrainID"
    >
      <el-option v-for="(item, index) in trains"
                 :key="index" :label="item.name" :value="item.id"
      />
    </el-select>
  </div>
</template>

<script>
import {get} from '../../utils/request'
import {mapState, mapMutations} from "vuex";

export default {
  name: "LineAndTrainSelector",
  data() {
    return {
      lines: [],
      trains: [],
      trainID: ''
    }
  },
  computed: {
    ...mapState(["lineId", "trainId"]),
    selectedLine: {
      get() {
        return this.lineId
      },
      set(val) {
        this.updateLineId(val)
        get("/train_list?lineId=" + val)
            .then(res => {
              this.trains = res
              this.selectedTrain = ""
            }, () => {
              console.log("网络错误")
              this.trains = [];
            })
      }
    },
    selectedTrain: {
      get() {
        return this.trainId
      },
      set(val) {
        this.updateTrainId(val)
      }
    }
  },

  methods: {
    changeTrainID() {
      this.$emit("getTrainID", this.trainId)
    },
    ...mapMutations(['updateLineId', 'updateTrainId'])
  },
  beforeMount() {
    // 挂载到页面上时
    get("//line_list")
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
          console.log("网络请求失败")
        })
  }
}
</script>

<style scoped>

</style>