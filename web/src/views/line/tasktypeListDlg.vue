<template>
  <el-dialog :title="title" v-model="visible" width="60%" :before-close="close">
    <el-tag
        v-for="tag in tasktyes"
        :key="tag"
        class="tag"
        @click="goToTaskTypeInfo(tag)"
    >
      {{ tag.name }}
    </el-tag>
    <el-button size="small" :icon="Edit" @click="innerVisible = true">
      <el-icon>
        <Edit/>
      </el-icon>
      <span>配属检修任务类型</span>
    </el-button>

    <el-button type="primary"
               size="small"
               @click="submit">确定
    </el-button>

    <div v-show="innerVisible">
      <el-divider/>
      <el-container
          class="selectYard"
          title="检修任务类型选择">
        <el-check-tag
            v-for="tag in allTasktypes"
            :key="tag"
            class="tag"
            :checked="isTagSelect(tag)"
            @change="checkTagChange(tag)"
            size="small"
        >
          {{ tag.name }}
        </el-check-tag>
        <el-button type="primary"
                   size="small"
                   @click="innerClose"
        >
          取消
        </el-button>
        <el-button type="primary"
                   size="small"
                   @click="innerConfirm"
        >
          确定
        </el-button>
      </el-container>
    </div>
  </el-dialog>
</template>

<script>
import {table} from "@/service/yard";
import {get, post} from "@/utils/request";
import {ElMessage} from "element-plus";
import {Edit} from '@element-plus/icons-vue'

export default {
  name: "tasktypeListDlg",
  data: () => {
    return {
      visible: false,
      formdata: {},
      yardId: "",
      yardName: '',
      tasktyes: [],
      tempTasktypes: [],  // innerDialog 临时保存选中的检修任务类型
      allTasktypes: [],
      innerVisible: false
    }
  },
  computed: {
    title() {
      return this.yardName + " 配属检修任务类型选择"
    }
  },
  methods: {
    init(yardId, yardName) {
      this.yardId = yardId;
      this.yardName = yardName;
      this.visible = true;
      this.innerVisible = false;
    },
    close() {
      this.visible = false;
    },
    checkTagChange(tag) {
      if (this.isTagSelect(tag)) {
        this.tempTasktypes = this.tempTasktypes.filter(item => item.id !== tag.id);
      } else {
        this.tempTasktypes.push(tag)
      }
    },
    isTagSelect(tag) {
      let flag = false;
      this.tempTasktypes.forEach(item => {
        if (item.id === tag.id) {
          flag = true;
        }
      })
      return flag;
    },
    innerClose() {
      this.innerVisible = false;
      this.tempTasktypes = [...this.tasktyes];
    },
    innerConfirm() {
      this.innerVisible = false;
      this.tasktyes = [...this.tempTasktypes];
    },
    goToTaskTypeInfo() {
      this.$router.push("/line/overhaul/type");
    },
    submit() {
      const data = {};
      data.yardId = this.yardId;
      data.list = [];
      this.tasktyes.forEach((item) => {
        let obj = {};
        obj.yardId = this.yardId;
        obj.tasktypeId = item.id;
        data.list.push(obj)
      })
      post("/api/yardTasktype/batch", data)
          .then((res) => {
            if (res.code == 0) {
              ElMessage.success("更新成功");
            } else {
              ElMessage.info(res.msg);
            }
            this.visible = false;
          }, () => {
            ElMessage.error("更新失败");
            this.visible = false;
            console.log("更新失败");
          })
    }
  },
  async updated() {
    get("/api/yardTasktype/byYard", {yardId: this.yardId})
        .then(result => {
              this.tasktyes = [];
              if (result.data) {
                result.data.forEach(i => this.tasktyes.push(
                    {
                      "name": i.taskTypeName,
                      "id": i.taskTypeId
                    }
                ))
              }
              this.tempTasktypes = [...this.tasktyes];
            },
            () => {
              this.tasktyes = [];
              console.log("网络请求失败")
            })
    get("/api/tasktype/tableAll")
        .then(result => {
          this.allTasktypes = [];
          if (result.data) {
            result.data.forEach(i => this.allTasktypes.push(
                {
                  "name": i.taskTypeName,
                  "id": i.id
                }
            ))
          }
        }, () => {
          this.allTasktypes = [];
          console.log("网络请求失败");
        })
  },
  components: {
    Edit,
  }
}
</script>

<style scoped>
.tag {
  margin: 2px 4px;
  cursor: pointer;
}

.selectYard {
  display: flex;
  align-items: center;
}
</style>