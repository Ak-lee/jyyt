<template>
  <el-upload
      class="upload-demo"
      action="/api/upload"
      :limit="1"
      accept="text/csv, application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  >
    <el-button type="primary">点击上传</el-button>
    <template #tip>
      <div class="el-upload__tip">
        只能上传 excel表格文件和csv文件。
      </div>
    </template>
  </el-upload>
</template>

<script>
// 文件上传，主要需要设置 el-upload 中的 action 属性。

export default {
  name: "excelUpload"
}
</script>

<style scoped>

</style>