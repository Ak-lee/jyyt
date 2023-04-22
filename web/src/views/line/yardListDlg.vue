<template>
  <el-dialog :title="title" v-model="visible" width="60%" :before-close="close">
    <el-tag
        v-for="tag in yards"
        :key="tag"
        class="tag"
        @click="goToYardInfo(tag)"
    >
      {{ tag.name }}
    </el-tag>
    <el-button size="small" :icon="Edit" @click="innerVisible = true">
      <el-icon>
        <Edit />
      </el-icon>
      <span>配属车场</span>
    </el-button>

    <el-button type="primary"
               size="small"
               @click="submit">确定
    </el-button>

    <div v-show="innerVisible">
      <el-divider/>
      <el-container
          class="selectYard"
          title="车场选择">
        <el-check-tag
            v-for="tag in allYards"
            :key="tag"
            class="tag"
            :checked="isTagSelect(tag)"
            @change="checkTagChange(tag)"
            :before-close="innerDialogClose"
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
  name: "yardListDlg",
  data: () => {
    return {
      visible: false,
      formdata: {},
      title: "线路配属车场选择",
      lineId: "",
      yards: [],
      tempYards: [],  // innerDialog 临时保存选中的车场
      allYards: [],
      innerVisible: false
    }
  },
  methods: {
    init(lineId) {
      this.lineId = lineId;
      this.visible = true;
      this.innerVisible = false;
    },
    close() {
      this.visible = false;
    },
    checkTagChange(tag) {
      if (this.isTagSelect(tag)) {
        this.tempYards = this.tempYards.filter(item => item.id !== tag.id);
      } else {
        this.tempYards.push(tag)
      }
    },
    isTagSelect(tag) {
      let flag = false;
      this.tempYards.forEach(item => {
        if (item.id == tag.id) {
          flag = true;
        }
      })
      return flag;
    },
    innerClose() {
      this.innerVisible = false;
      this.tempYards = [...this.yards];
    },
    innerConfirm() {
      this.innerVisible = false;
      this.yards = [...this.tempYards];
    },
    goToYardInfo() {
      this.$router.push("/line/yard/yard-info");
    },
    submit() {
      const data = {};
      data.lineId = this.lineId;
      data.list = [];
      this.yards.forEach((item) => {
        let obj = {};
        obj.lineId = this.lineId;
        obj.yardId = item.id;
        data.list.push(obj)
      })
      post("/api/lineyard/batch", data)
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
    get("/api/yard/list", {lineId: this.lineId})
        .then(result => {
              this.yards = [];
              if (result.data) {
                result.data.forEach(i => this.yards.push(
                    {
                      "name": i.name,
                      "id": i.id
                    }
                ))
              }
              this.tempYards = [...this.yards];
            },
            () => {
              this.yards = [];
              console.log("网络请求失败")
            })
    get("/api/yard/tableNoPage")
        .then(result => {
          this.allYards = [];
          if (result.data) {
            result.data.forEach(i => this.allYards.push(
                {
                  "name": i.name,
                  "id": i.id
                }
            ))
          }
        }, () => {
          this.allYards = [];
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