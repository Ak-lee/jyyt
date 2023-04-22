<template>
  <el-dialog :title="title" v-model="visible" width="50%" :before-close="close">
    <span style="margin-bottom: 10px">默认判定周末为休息日，其余时间为工作日。更多内容请在生产日历编辑弹窗中配置</span>
    <el-form ref="form" :model="formdata" label-width="100px">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="线路选择">
            <el-select v-model="formdata.lineId">
              <el-option
                  :key="index" v-for="(item, index) in lines"
                  :label="item.name"
                  :value="item.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="12">
          <el-form-item label="日历编号">
            <el-input :disabled="!isNew" v-model="formdata.id"/>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="日历名称">
            <el-input type="textarea" v-model="formdata.name"/>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="10">
        <el-col :span="12">
          <el-form-item label="开始日期">
            <el-date-picker
                v-model="formdata.startDate"
                type="date"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="结束日期">
            <el-date-picker
                v-model="formdata.endDate"
                type="date"
                :disabled-date="this.DatePicker2disabled"
            />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <el-table
        v-if="!this.isNew"
        :data="workDatatotal" border v-model="workDatatotal"
        max-height="400"
    >
      <el-table-column align="center" prop="" label="序号" sortable>
        <template #default="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>
      <el-table-column prop="year" align="center" label="年" sortable/>
      <el-table-column prop="month" align="center" sortable label="月"/>
      <el-table-column prop="workDays" align="center" sortable label="工作天数"/>
      <el-table-column prop="restDays" align="center" sortable label="休息天数"/>
      <el-table-column label="操作" align="center" width="180px" fixed="right">
        <template #default="{row}">
          <div style="display: flex;justify-content: center">
            <el-button size="small" @click="openDlg(row.productionCalendarId, row.year, row.month)">
              <el-icon>
                <edit/>
              </el-icon>
              <span>按月查看日历内容</span>
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <template #footer>
      <el-button @click="close">取 消</el-button>
      <el-button type="primary"
                 @click="submit">确 定
      </el-button>
    </template>
    <calendarmonth-dlg ref="calendarmonthDlg" @afterSubmit="handleAfterSubmit"/>
  </el-dialog>
</template>

<script>
import {get} from '@/utils/request'
import {add, update} from '@/service/calendar'
import {ElMessage} from 'element-plus';
import calendarmonthDlg from '@/views/line/calendarmonthDlg'
import {getCategoryInfoByCalendarId} from "@/service/workcalendar";
import {Edit} from '@element-plus/icons-vue'

export default {
  name: "calendarDlg",
  components: {
    calendarmonthDlg,
    Edit
  },
  data: () => {
    return {
      workcalendarId: '',
      formdata: {},
      visible: false,
      lines: [],
      isNew: false,
      workDatatotal: [{
        year: '',
        month: '',
        workdays: '',
        calendarId: '',
      }]//与日历名称对应的日例详细内容---总共
    }
  },
  computed: {
    title() {
      return this.isNew ? '生产日历新增' : '生产日历信息编辑'
    }
  },
  methods: {
    async init(data, isNew) {
      this.formdata = data;
      this.visible = true;
      this.isNew = isNew;
      if (!isNew) {
        await this.renderTable();
      }
    },
    async renderTable() {
      let result = await getCategoryInfoByCalendarId(this.formdata.id);
      this.workDatatotal = result.list;
    },
    close() {
      this.formdata = {};
      this.visible = false;
    },
    async handleAfterSubmit() {
      await this.renderTable();
    },
    submit() {
      // 提交，有可能是新增insert，也可能是更新update
      if (this.isNew) {
        add(this.formdata)
            .then((res) => {
              if (res.code == 0) {
                ElMessage.success("成功新增一条记录");
                this.$emit("afterSubmit");
                this.visible = false;
              } else {
                ElMessage.success(res.msg);
              }
            }, () => {
              ElMessage.error("网络错误");
            })
      } else {
        update(this.formdata)
            .then((res) => {
              ElMessage.success("更新成功");
              this.$emit("afterSubmit");
              this.visible = false;
            }, () => {
              ElMessage.error("网络错误");
            })
      }
    },
    async openDlg(calendarId, year, month) {
      this.$refs.calendarmonthDlg.init(calendarId, year, month);
    },
    DatePicker2disabled(date) {
      return date.getTime() < new Date(this.formdata.startDate).getTime()
    }
  },
  mounted() {
    get("/api/line_list")
        .then(result => {
              this.lines = []
              result.forEach(i => this.lines.push(
                  {
                    "name": i.name,
                    "id": i.id
                  }
              ))
            },
            () => {
              this.lines = []
              console.log("网络请求失败")
            })
  },
  emits: ["afterSubmit"],
}
</script>

<style scoped>

</style>