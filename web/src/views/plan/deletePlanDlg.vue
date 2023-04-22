<template>
  <el-dialog
      v-model="visible"
      :title="title"
      width="30%"
  >
    <span>计划删除将同步删除该计划及其下属计划内容，是否确认删除？</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="submit">
          确定删除
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import {removeById} from "@/service/plan/planmanage"
import {ElMessage} from "element-plus";

export default {
  name: "DeletePlanDlg",
  data: () => {
    return {
      visible: false,
      id: '',
      title: "计划删除"
    }
  },
  methods: {
    init: function (id) {
      this.id = id;
      this.visible = true;
    },
    submit: async function () {
      let r = await removeById(this.id);
      if (r.code === 0) {
        ElMessage.success("删除成功");
        this.visible = false;
        this.$emit("afterSubmit");
      } else {
        ElMessage.error("网络错误");
      }

    }
  },
}
</script>
<style scoped>
.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>