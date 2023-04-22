<template>
  <div class="Breadcrumb">
    <span>线路资源管理 > 检修任务管理 > 检修任务类型详情信息</span>
  </div>

  <div class="container">
    <div class="title">检修任务类型详情信息</div>
    <div class="content">
      <div v-show="showEditApplyMonth">
        <el-button @click="this.showEditApplyMonth = false" size="small" type="primary">返回</el-button>

        <el-select v-model="applyMonthNewMonth" style="margin: 0 10px" size="small">
          <el-option :key="n" v-for="n in 12" :label="n + '月'" :value="n"/>
        </el-select>

        <el-select v-model="applyMonthNewMode" style="margin: 0 10px" size="small">
          <el-option
              :key="item.id"
              :value="item.id"
              :label=" '修程' + (index + 1)"
              v-for="(item, index) in this.applyMonthModeList"
          />
        </el-select>
        <el-button @click="newApplyMonth" size="small" type="success">新增月份</el-button>
        <el-table border :data="applyMonthArr">
          <el-table-column label="服役月份" align="center">
            <template #default="scope">
              {{ scope.row.applyMonth + "月" + this.applyMonthMonthStr[scope.$index] }}
            </template>
          </el-table-column>
          <el-table-column label="单日检修耗费时间(小时)" align="center">
            <template #default="{row}">
          <span>
            {{ this.filterContent(row, "requireHour") }}
          </span>
            </template>
          </el-table-column>
          <el-table-column :prop="requireDay" label="检修耗费天数(天)" align="center">
            <template #default="{row}">
          <span>
            {{ this.filterContent(row, "requireDay") }}
          </span>
            </template>
          </el-table-column>
          <el-table-column :prop="requireHeadcount" label="所需人员数量(人)" align="center">
            <template #default="{row}">
          <span>
            {{ this.filterContent(row, "requireHeadcount") }}
          </span>
            </template>
          </el-table-column>
          <el-table-column label="修程切换" align="center">
            <template #default="{row}">
              <el-select size="small" v-model="row.tasktypeModeId" @change="applyMonthChange(row) ">
                <el-option
                    :key="item.id"
                    :value="item.id"
                    :label=" '修程' + (index + 1)"
                    v-for="(item, index) in this.applyMonthModeList"
                />
              </el-select>
            </template>
          </el-table-column>

          <el-table-column label="操作">
            <template #default="{row}">
              <el-button size="small" @click="applyMonthDelete(row)">
                <el-icon>
                  <Delete/>
                </el-icon>
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div v-show="!showEditApplyMonth">
        <el-form ref="addForm" v-show="this.addItemVisible" :rules="rules" prop="newItem">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item prop="taskTypeId" label="检修任务类型">
                <el-select size="small" v-model="newItem.taskTypeId">
                  <el-option
                      v-for="item in tasktypeLeft"
                      :key="item.id"
                      :label="item.taskTypeName"
                      :value="item.id"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item prop="requireHour" label="单日检修耗费小时数">
                <el-input v-model="newItem.requireHour" size="small"/>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item prop="requireDay" label="检修耗费天数">
                <el-input v-model="newItem.requireDay" size="small" :min="1"/>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item prop="requireHeadcount" label="所需人员数量">
                <el-input v-model="newItem.requireHeadcount" size="small" :min="1"/>
              </el-form-item>
            </el-col>
          </el-row>
          <el-button size="small" @click="submitNewItem">提交</el-button>
          <el-button size="small" @click="cancel">取消</el-button>
          <el-divider/>
        </el-form>
        <el-button style="margin-bottom: 6px;" @click="showAddItem" v-show="!addItemVisible" type="primary"
                   size="small">
          新增
        </el-button>
        <el-table
            :data="this.tableData"
            border
            :span-method="objectSpanMethod"
        >
          <el-table-column type="index" label="序号"/>
          <el-table-column align="center" label="检修任务类别">
            <template #default="{row}">
              <span>{{ row.taskTypeName }}</span>
              <el-button type="success" size="small" @click="showApplyMonth(row)" v-if="row.beMultiMode">
                <span>适用月份</span>
              </el-button>
            </template>
          </el-table-column>
          <el-table-column label="单日检修耗费时间（小时）" align="center">
            <template #default="{row}">
              <el-input v-show="row.editStatus" size="small" v-model="row.requireHour"/>
              <span v-show="!row.editStatus">{{ row.requireHour }}</span>
            </template>
          </el-table-column>
          <el-table-column label="检修耗费天数（天）" align="center">
            <template #default="{row}">
              <el-input-number :min="1" v-show="row.editStatus" size="small" v-model="row.requireDay"/>
              <span v-show="!row.editStatus">{{ row.requireDay }}</span>
            </template>
          </el-table-column>

          <el-table-column label="所需人员数量（人)" align="center">
            <template #default="{row}">
              <el-input-number :min="1" v-show="row.editStatus" size="small" v-model="row.requireHeadcount"/>
              <span v-show="!row.editStatus">{{ row.requireHeadcount }}</span>
            </template>
          </el-table-column>

          <el-table-column align="center" label="操作" fixed="right" width="160">
            <template #default="{row}">
              <div style="display: flex;justify-content: center">
                <el-button @click="itemEdit(row)" size="small">
                  <span v-show="!row.editStatus">
                    <el-icon>
                      <edit/>
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
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import {ElMessage} from "element-plus";
// import {add, update, removeById} from "@/service/yardTasktype"

import {
  updateDetail,
  tableAll as tableAllTaskTypes,
  getWithTasktypeDetail,
  byTasktypeId
} from "@/service/type";
import {Edit, Delete, Select} from "@element-plus/icons-vue";
import {
  table as applyMonthTable,
  update as updateApplyMonth,
  add as addApplyMonth,
  removeById as removeApplyMonthById
} from "@/service/applyMonth"

export default {
  name: "taskType-ModeDetail",
  data() {
    return {
      visible: false,
      tableData: [],
      originData: {},
      tasktypeAll: [],  // 存储所有的检修任务类型。当前能够新增的检修任务类型智能是所有检修任务晒造型中未选择的
      spanRow: 0,   // 表格合并单元格时候使用
      start: 0,   // 表格合并单元格时候使用，
      addItemVisible: false,
      newItem: {
        taskTypeId: '',
        requireHour: '',
        requireDay: '',
        requireHeadcount: ''
      },
      rules: {
        "taskTypeId": [{
          required: true,
          message: '请选择检修任务类型',
          trigger: 'blur',
        }],
        "requireHour": [{
          required: true,
          message: '请输入单日检修耗费小时数',
          trigger: 'blur',
        }],
        "requireDay": [{
          required: true,
          message: '请输入检修耗费天数',
          trigger: 'blur',
        }],
        "requireHeadcount": [{
          required: true,
          message: '请输入所需人员数量',
          trigger: 'blur',
        }]
      },
      applyMonthArr: [],
      applyMonthModeList: [],
      applyMonthTaskTypeId: '',
      applyMonthNewMonth: '',
      applyMonthNewMode: '',
      showEditApplyMonth: false,
    }
  },
  computed: {
    tasktypeLeft() {
      let arr = []
      this.tasktypeAll.forEach(item => {
        let flag = true;
        for (let i = 0; i < this.originData.length; i++) {
          if (item.id === this.originData[i].taskTypeId) {
            flag = false;
            break;
          }
        }
        if (flag || item.beMultiMode) {
          arr.push(item);
        }
      })
      return arr;
    },
    applyMonthMonthStr() {
      let arr = [];
      let strArr = [];
      this.applyMonthArr.forEach(i => {
        arr.push(i.applyMonth);
      })
      // 1 2 3 4 4 5 5 6 7 8
      // 表示这个月份的下一个可使用的字母。初始值都是 A。
      let alphabetUse = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A']; // 12 个月
      for (let j = 0; j < arr.length; j++) {
        let month = arr[j] - 1;
        strArr.push(alphabetUse[month]);
        alphabetUse[month] = String.fromCharCode(alphabetUse[month].charCodeAt(0) + 1)
      }

      for (let k = 0; k < alphabetUse.length; k++) {
        if (alphabetUse[k] === 'B') {
          // 这个月份字母只使用了一次，则 A 不需要保留.
          let month = k + 1;
          let index = arr.findIndex((n) => {
            return n === month
          });
          strArr[index] = '';
        }
      }
      return strArr;
    }
  },
  methods: {
    async init() {
      this.visible = true;
      this.addItemVisible = false;
      this.showEditApplyMonth = false;
      await this.renderTable();
      this.applyMonthArr = []
    },
    close() {
      this.visible = false;
    },
    async renderTable() {
      this.tableData = [{requireDay: ''}];

      let body = await getWithTasktypeDetail();
      this.originData = body.data;
      let arr = []
      this.originData.forEach((item) => {
        let first = true;
        item.list.forEach((i) => {
          let obj = JSON.parse(JSON.stringify(i));
          if (first && item.list.length > 1) {
            obj.spanRow = item.list.length;
            first = false;
          } else if (!first && item.list.length > 1) {
            obj.spanRow = 0;
          } else {
            obj.spanRow = 1;
          }
          obj.editStatus = false; // 保存每个条目是否处于编辑状态
          arr.push(obj)
        })
      })
      this.tableData = arr;
      body = await tableAllTaskTypes();
      this.tasktypeAll = body.data
    },
    async itemEdit(row) {
      if (row.editStatus) {
        // 点击了确认按钮,更新操作
        await updateDetail(row)
        ElMessage.success("更新成功")
        this.renderTable();
      }
      row.editStatus = !row.editStatus
    },
    async submitNewItem() {
      let flag = true
      await this.$refs.addForm.validate((valid) => {
        if (!valid) {
          ElMessage.error("数据校验失败");
          flag = false
          return false;
        }
      })
      if (!flag) {
        return;
      }
      let r = await add(this.newItem);
      if (r.code == 0) {
        this.$emit("afterSubmit");
        this.addItemVisible = false;
        this.renderTable();
      } else {
        ElMessage.info(r.msg);
      }
    },
    showAddItem() {
      this.addItemVisible = true;
      this.newItem = {
        taskTypeId: '',
        requireHour: '',
        requireDay: '',
        requireHeadcount: ''
      };
    },
    async showApplyMonth(row) {
      this.applyMonthTaskTypeId = row.taskTypeId;
      await this.renderApplyMonth(this.applyMonthTaskTypeId);
      this.showEditApplyMonth = true;
    },
    async renderApplyMonth(taskTypeId) {
      this.applyMonthArr = []
      for (let i = 1; i <= 12; i++) {
        let obj = {};
        obj.id = '';
        obj.applyMonth = i;
        obj.tasktypeModeId = '';
        this.applyMonthArr.push(obj);
      }
      let result = await applyMonthTable(taskTypeId);
      result.data.forEach(i => {
        let index = this.applyMonthArr.findIndex(j => {
          return j.applyMonth == i.applyMonth;
        })

        if (this.applyMonthArr[index].id) {
          this.applyMonthArr.push(i);
        } else {
          this.applyMonthArr[index] = i;
        }
      })
      this.applyMonthArr.sort((a, b) => {
        if (a.applyMonth !== b.applyMonth) {
          return a.applyMonth - b.applyMonth;
        } else {
          if (a.id && b.id) {
            return a.id - b.id;
          }
          if (!a.id && b.id) {
            return Number.POSITIVE_INFINITY - b.id;
          }
          if (a.id && !b.id) {
            return a.id - Number.POSITIVE_INFINITY
          }
          if (!a.id && !b.id) {
            return 0;
          }
        }
      })

      result = await byTasktypeId(taskTypeId); // 获取该检修任务对应的所有检修模式 mode
      this.applyMonthModeList = result.data.list;
    },
    cancel() {
      this.newItem = {
        taskTypeId: '',
        requireHour: '',
        requireDay: '',
        requireHeadcount: ''
      };
      this.addItemVisible = false;
    },
    objectSpanMethod: function ({
                                  row,
                                  column,
                                  rowIndex,
                                  columnIndex
                                }) {
      if (columnIndex < 2) {
        if (row.spanRow > 0) {
          return {
            rowspan: row.spanRow,
            colspan: 1,
          }
        } else {
          return {
            rowspan: 0,
            colspan: 0
          }
        }
      }
    },
    filterContent(row, requireStr) {
      let result = this.applyMonthModeList.filter(i => {
        return i.id === row.tasktypeModeId
      })
      if (result.length) {
        result = result.at(0)[requireStr]
      } else {
        result = null;
      }
      return result;
    },
    async applyMonthChange(row) {
      let result;
      if (row.id) {
        result = await updateApplyMonth(row);
      } else {
        result = await addApplyMonth(row);
      }
      if (result.code === 0) {
        ElMessage.success("更新成功")
      } else {
        ElMessage.success("更新失败")
      }
    },
    async applyMonthDelete(row) {
      let res = await removeApplyMonthById(row.id);
      if (res.code === 0) {
        await this.renderApplyMonth(this.applyMonthTaskTypeId)
        ElMessage("删除成功");
      }
    },
    async newApplyMonth() {
      if ((!this.applyMonthNewMonth) || (!this.applyMonthNewMode)) {
        ElMessage.error("数据不完整")
      } else {
        let obj = {};
        obj.id = '';
        obj.applyMonth = this.applyMonthNewMonth;
        obj.tasktypeModeId = this.applyMonthNewMode;
        let result = await addApplyMonth(obj)
        if (result.code == 0) {
          await this.renderApplyMonth(this.applyMonthTaskTypeId)
          ElMessage.success("添加成功")
        } else {
          ElMessage.error("网络错误" + result.msg);
        }
      }
    },
    applyMonthTable,
    updateApplyMonth
  },
  mounted() {
    this.init();
  },
  components: {
    Edit, Delete, Select
  },
}
</script>

<style scoped>
.Breadcrumb {
  padding: 10px 0px;
}

.container {
  min-height: calc(100vh - 150px);
  background-color: white;
  border: 1px solid #9c9c9c;
}

.title {
  font-weight: bold;
  font-size: 16px;
  margin: 10px;
}

.content {
  padding: 10px;
  /*border: 1px solid #c1c2c6;*/
}
</style>