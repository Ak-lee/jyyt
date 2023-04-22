<template>
  <div class="header clearfix">
    <div class="wrapper" :class="{'active': leftNavFold}">
      <div class="CRRC-logo">
        <img src="../assets/image/CRRC-logo.png">
      </div>
      <div class="btn" @click="switchLeftNavStatus()">
        <el-icon :size="30" v-show="!leftNavFold">
          <fold/>
        </el-icon>
        <el-icon :size="30" v-show="leftNavFold">
          <expand/>
        </el-icon>
      </div>
      <div class="titleWrapper">
        <span id="title">城轨列车检运一体化系统</span>
      </div>
    </div>
  </div>
</template>

<script>
import {Expand, Fold} from '@element-plus/icons-vue'
import {mapState, mapMutations} from "vuex";

export default {
  data() {
    return {
      status: true
    }
  },
  components: {
    Expand,
    Fold,
  },
  computed: {
    ...mapState(['leftNavFold'])
  },
  methods: {
    ...mapMutations(['switchLeftNavStatus']),
  },
}
</script>


<style scoped>
.header {
  /*background-color: rgb(25, 40, 55);*/
  background-color: rgb(37, 60, 83);
  background-size: cover;
  position: fixed !important;
  top: 0;
  right: 0;
  left: 0;
  z-index: 10;
  height: 60px;
  min-width: 800px;
}

.CRRC-logo {
  display: inline-block;
  align-items: center;
  position: relative;
  top: 5px;
}


.wrapper {
  margin-left: 230px;
  display: inline-block;
  transition: margin-left 0.3s;
}

.wrapper.active {
  margin-left: 40px;
  transition: margin-left 0.3s;
}

.header .btn {
  float: left;
  vertical-align: middle;
  font-size: 30px;
  /*margin-left: 197px;*/
  margin-top: 15px;
  color: rgb(228, 231, 237);
  display: inline-block;
}

.header .titleWrapper {
  display: inline-block;
}

#title {
  font-size: 20px;
  font-weight: bold;
  line-height: 60px;
  /*color: darkgreen;*/
  color: rgb(228, 231, 237);
  letter-spacing: 2px;
  padding-left: 10px;
  margin-left: 10px;
  box-sizing: border-box;
  border-left: 1px solid #fcfcfc;
}

</style>
