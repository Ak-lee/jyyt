<template>
  <div class="innerContainer">
    <span style="font-size: 14px">线路名：</span>
    <el-select
        v-model="lineId"
        clearable
        size="small"
        placeholder="请选择线路名"
    >
      <el-option
          :key="index" v-for="(item, index) in lines"
          :label="item.name"
          :value="item.id"
      />
    </el-select>
    <el-button size="small" @click="$emit('lineSearch', lineId)" class="search" type="success">
      <el-icon>
        <search/>
      </el-icon>
      <span>查询</span>
    </el-button>
  </div>
</template>

<script>
import {get} from '@/utils/request'
import {Search} from '@element-plus/icons-vue';

export default {
  name: "LineAndTrainSelector",
  props: {
    'presetLineId': Number
  },
  data() {
    return {
      lines: [],
      lineId: this.presetLineId,
    }
  },
  beforeMount() {
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
          console.log("网络请求失败")
        })
  },
  components: {
    Search,
  }
}
</script>

<style scoped>
.innerContainer {
  margin: 10px;
}

.search {
  margin-left: 10px;
}
</style>