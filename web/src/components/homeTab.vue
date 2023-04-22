<template>
  <el-row class="container">
    <el-col :span="4">
      <span class="title">检运一体化系统</span>
    </el-col>
    <el-col :span="20" style="overflow: hidden">
      <div
          style="-webkit-user-select: none;
           -moz-user-select: none;
           -ms-user-select: none;
           user-select: none;">
        <img :src="photo"/>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import deImg from '@/assets/image/photo.jpg'

export default {
  name: "home",
  data() {
    return {
      photo: deImg
    }
  }
}
</script>

<style scoped>
.row1 {
  margin-top: 20px;
  margin-left: 200px;
}

.title {
  color: #6495ed;
  font-size: 40px;
  font-weight: bold;
  writing-mode: vertical-lr;
  letter-spacing: 1em;
  vertical-align: center;
  margin-left: 40px;
}

.container {
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>