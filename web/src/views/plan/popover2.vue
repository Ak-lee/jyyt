<template #default="scope">
  <div>
    <el-popover
        class="popover1"
        v-if="item.id && (plantype === '年计划' || plantype === '月计划' || plantype === '周计划')"
        ref="popoverRef"
        placement="right"
        width="250px"
        trigger="hover">

      <el-button style="width: 200px" @click="editTime(item.id)">
        <span>检修任务提前或延后</span>
      </el-button>

      <template #reference>
        {{ item.content }}
      </template>
    </el-popover>
    <span v-if="!item.id">{{
        item.content
      }}</span>
  </div>
</template>

<script>
export default {
  name: "popover2",
  emits: ['editTime'],
  props: {
    item: Object,
    plantype: String,
  },
  methods: {
    //编辑时间：检修任务提前或延后
    editTime: function (id) {
      this.$emit("editTime", id);
    }
  }
}

</script>


<style scoped>
.popover1 {
  margin: auto;
  text-align: -webkit-center;
}
</style>
