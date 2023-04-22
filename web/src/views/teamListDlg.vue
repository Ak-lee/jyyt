<template>
  <el-dialog :title="title" v-model="visible" width="60%" :before-close="close">
    <el-form v-show="this.addItemVisible">
      <el-form-item label="班组类型">
        <el-select size="small" v-model="this.newItem.teamId">
          <el-option v-for="item in teamLeft" :key="item.id" :label="item.teamType" :value="item.id"/>
        </el-select>
      </el-form-item>
      <el-form-item label="班组个数">
        <el-input-number :min="0" size="small" v-model="this.newItem.num"/>
      </el-form-item>
      <el-button size="small" @click="submitNewItem">提交</el-button>
      <el-button size="small" @click="cancel">取消</el-button>
      <el-divider/>
    </el-form>
    <el-button type="primary" size="small" @click="addItemVisible=!addItemVisible" v-show="!addItemVisible">新增
    </el-button>

    <el-table
        :data="tabledata"
    >
      <el-table-column label="车场名" prop="yardName"/>
      <el-table-column label="班组" prop="teamType"/>
      <el-table-column label="数量（个）" align="center">
        <template #default="{row}">
          <el-input-number :min="1" v-model="row.num" v-show="row.editStatus" size="small"/>
          <span v-show="!row.editStatus">{{ row.num }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="100">
        <template #default="{row}">
          <el-button @click="itemEdit(row)" size="small">
            <span v-show="!row.editStatus">
              <el-icon>
                <Edit/>
              </el-icon>
              <span>编辑</span>
            </span>
            <span v-show="row.editStatus">
              <el-icon>
                <Select/>
              </el-icon>
              <span>确认</span>
            </span>
          </el-button>

          <el-button size="small" @click="removeItem(row)">
            <el-icon>
              <Delete/>
            </el-icon>
            <span>删除</span>
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
import {table, add, update, remove} from "@/service/yardteam"
import {tableall as teamTable} from "@/service/team"
import {Edit, Delete, Select} from '@element-plus/icons-vue'
import {ElMessage} from "element-plus";

export default {
  name: "teamListDlg",
  data: () => {
    return {
      visible: false,
      tabledata: [],
      yardId: '',
      yardName: '',
      teamAll: [],  // 存储所有的班组类型，当前能够新增的班组类型只能是所有班组类型中未选择的。
      newItem: {
        teamId: '',
        num: 0,
        yardId: '',
      },
      addItemVisible: false,
    }
  },
  methods: {
    init(yardId, yardName) {
      this.yardId = yardId;
      this.yardName = yardName;
      this.visible = true;
      this.tabledata = [];
      this.teamAll = [];
      this.newItem = {
        teamId: '',
        num: 1,
        yardId: '',
      }
      this.addItemVisible = false;
      this.renderTable();
    },
    close() {
      this.visible = false;
    },
    async renderTable() {
      if (this.yardId) {
        let result = await table(this.yardId)
        this.tabledata = result.data;
        this.tabledata.forEach(item => {
          item.editStatus = false;  // 保存每个条目是否处于编辑状态
        })
        result = await teamTable(this.yardId);

        this.teamAll = result.data;
        this.newItem = {};
        this.newItem.yardId = this.yardId;
        this.newItem.num = 1;
      }
    },
    async submitNewItem() {
      if (this.newItem.teamId && this.newItem.num) {
        await add(this.newItem)
        ElMessage.success("添加成功");
        await this.renderTable();
        this.addItemVisible = false;
      } else {
        ElMessage.error("数据不合法");
      }
    },
    cancel() {
      this.newItem = {};
      this.newItem.yard = this.yard;
      this.newItem.num = 1;
      this.addItemVisible = false;
    },
    async itemEdit(row) {
      if (row.editStatus) {
        // 点击了确认按钮,更新操作
        await update(row)
        ElMessage.success("更新成功")
        this.renderTable();
      }
      row.editStatus = !row.editStatus
    },
    async removeItem(row) {
      await remove(row);
      ElMessage.success("删除成功");
      this.renderTable();
    },
    table,
  },
  computed: {
    teamLeft() {
      let arr = [];
      this.teamAll.forEach(item => {
        let flag = true;
        for (let i = 0; i < this.tabledata.length; i++) {
          if (item.id === this.tabledata[i].teamId) {
            flag = false;
            break;
          }
        }
        if (flag) {
          arr.push(item);
        }
      })
      return arr;
    },
    title() {
      return this.yardName + " 班组关联"
    }
  },
  components: {Edit, Delete, Select},
}
</script>

<style scoped>

</style>