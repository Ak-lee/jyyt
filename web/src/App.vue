<template>
  <router-view/>
</template>

<script setup>
import * as echarts from "echarts"
import {provide} from "vue"

provide("echarts", echarts)

</script>

<style scoped>

nav {
  padding: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

/deep/ .el-table .el-table__cell {
  padding: 0;
}
/deep/ .el-table .el-select {
  margin: 6px 4px;
}
/deep/ .el-table .el-button {
  margin: 6px 4px;
}
</style>
