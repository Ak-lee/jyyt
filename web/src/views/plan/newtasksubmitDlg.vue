<template>
  <el-dialog
      v-model="visible"
      title="注意："
      width="30%"
  >
    <span>确定提交吗？</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="submit">
          确定提交
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import {ElMessage} from "element-plus";
import {saveBatch} from "@/service/planFeedback";


let tabledata2 = []
let visible = $ref(false);
const emit = defineEmits(['afterSubmit']);

const init = function (tabledata) {
  tabledata2 = []
  tabledata2 = tabledata
  visible = true;
};

const submit = async function () {
  let res = await saveBatch(tabledata2);
  if (res.code === 0) {
    ElMessage.success("提交成功");
  } else {
    ElMessage.error("提交失败");
  }
  emit("afterSubmit");
  visible = false;
}
defineExpose({
  init,
});

</script>
<style scoped>
.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>

