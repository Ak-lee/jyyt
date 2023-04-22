<template>
  <el-dialog
      v-model="visible"
      title="注意："
      width="30%"
  >
    <span>确定下发计划吗，下发之后若想要取消，则需重新编辑！</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="cancel">取消</el-button>
        <el-button type="primary" @click="submit">
          确定下发
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import {dispatchByIds} from "@/service/planInquiry"
import {ElMessage} from "element-plus";

let ids = []
let visible = $ref(false);

const initAll = function (ids1) {
  ids = []
  ids = [...ids1];
  visible = true;
};

const submit = async function () {
  let r = await dispatchByIds(ids);
  if (r.code === 0) {
    ElMessage.success("下发成功");
    this.$emit("afterSubmit");
  } else {
    ElMessage.error("网络错误");
  }
}
const cancel = function () {
  ids = [];
  visible = false;
}
defineExpose({
  initAll,
});

</script>
<style scoped>
.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>

