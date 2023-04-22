package com.example.yjyt.controller;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.*;
import com.example.yjyt.serv.impl.ApplyMonthServiceImpl;
import com.example.yjyt.serv.impl.ScheduleContentHistoryImpl;
import com.example.yjyt.serv.impl.ScheduleInfoImpl;
import com.example.yjyt.serv.impl.TypeInfoServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.sql.Date;
import java.util.*;

@RequestMapping("/schedule_content_history")
@RestController
public class ScheduleContentHistoryController {
    @Autowired
    private ScheduleContentHistoryImpl serv;

    @Autowired
    private ScheduleInfoImpl serv2;

    @Autowired
    private TypeInfoServImpl serv3;

    @Autowired
    private ApplyMonthServiceImpl serv4;

    @GetMapping("/table")
    public R table(@RequestParam(name = "scheduleId") String scheduleId) {
        List<ScheduleContentHistoryVO> result = serv.getListByScheduleId(scheduleId);
        return R.ok().put("list", result);
    }

    @GetMapping("/tableAll")
    public R tableAll() {
        List<ScheduleContentHistoryVO> result = serv.getList();
        return R.ok().put("list", result);
    }

    @GetMapping("/tableWithCond")
    public R tableWithCond(@RequestParam(name = "lineId") Integer lineId,
                           @RequestParam(name = "planTypes", required = false) List<String> planTypes,
                           @RequestParam(name = "sdate", required = false) Date sdate,
                           @RequestParam(name = "edate", required = false) Date edate,
                           @RequestParam(name = "status", required = false) String status
    ) {

        List<ScheduleContentHistoryVO> result = serv.tableWithCond(lineId, planTypes, sdate, edate, status);
        return R.ok().put("list", result);
    }

    @GetMapping("/getPagesOverview")
    public R getPagesOverview(@RequestParam(name = "lineId") Integer lineId,
                              @RequestParam(name = "planTypes", required = false) List<String> planTypes
    ) {
        Map<String, Object> result = serv.getPagesOverview(lineId, planTypes);
        return R.ok().put("data", result);
    }

    @GetMapping("/lastMultiModeRepair")
    public R getLastMultiModeRepairByLineIdAndDeadline(Integer lineId, Date deadline) {
        // 我们的 ScheduleContentHistory 表支持 lineId 字段.
        // 1. 获取所有的检修任务
        List<TaskTypeInfo> all = serv3.getAll();
        List<TaskTypeInfo> multiModeTaskTypeList = new ArrayList<>();
        all.stream().filter(TaskTypeInfo::isBeMultiMode).forEach(multiModeTaskTypeList::add);

        ArrayList<List<ScheduleContentHistory>> result = new ArrayList<>();
        multiModeTaskTypeList.forEach(i -> {
            // 获取检修任务类型:
            String taskTypeName = i.getTaskTypeName();
            // 获取该检修任务类型中支持多修程的月份
            Long id = i.getId();

            List<ApplyMonthVO> table = serv4.table(id);

            Map<Integer, List<ApplyMonthVO>> map = new HashMap<>();
            // table 按照 month 进行聚合。
            table.forEach(j -> {
                if (!map.containsKey(j.getApplyMonth())) {
                    List<ApplyMonthVO> list = new ArrayList<>();
                    list.add(j);
                    map.put(j.getApplyMonth(), list);
                } else {
                    map.get(j.getApplyMonth()).add(j);
                }
            });
            // 现在我们过滤掉哪些 数组长度仅为 1 的 月份。
            ArrayList<Integer> month_arr = new ArrayList<>();
            for (Integer key : map.keySet()) {
                List<ApplyMonthVO> list = map.get(key);
                if (list.size() > 1) {
                    month_arr.add(key);
                }
            }

            // month_arr: 4月、5月、11月
            month_arr.forEach(k -> {
                List<ScheduleContentHistory> item = serv.filterByLineIdMonthTaskTypeNameDeadline(lineId, k, taskTypeName, deadline);
                result.add(item);
            });
        });
        return R.ok().put("data", result);
    }

    @GetMapping("/lastRepairType")
    // 获取所有列车的上一次均衡修检修模式
    public R getLastRepairType(@RequestParam("lineId") Integer lineId) {
        ScheduleInfo item = serv2.getLeastItem(lineId, "年计划");
        Date deadline = item.getStartTime();

        List<ScheduleContentHistory> result = serv.getLastRepairType(lineId, deadline);
        return R.ok().put("data", result);
    }

    // 适用月份
    @GetMapping("/lastRepairMode")
    public R getLastRepairMode(@RequestParam("lineId") Integer lineId, @RequestParam("month") Integer month) {
        ScheduleInfo item = serv2.getLeastItem(lineId, "年计划");
        Date deadline = item.getStartTime();
        List<ScheduleContentHistory> result = serv.getLastRepairMode(lineId, deadline, month);
        return R.ok().put("data", result);
    }

    @GetMapping("/lastMonthRepair")
    public R getLastMonthRepair(@RequestParam("lineId") Integer lineId) {
        ScheduleInfo item = serv2.getLeastItem(lineId, "月计划");
        Date deadline = item.getStartTime();

        List<ScheduleContentHistory> result = serv.getLastMonthRepairType(lineId, deadline);
        return R.ok().put("list", result);
    }

    @GetMapping("/lastWeekRepair")
    public R getLastWeekRepair(@RequestParam("lineId") Integer lineId) {
        ScheduleInfo item = serv2.getLeastItem(lineId, "周计划");
        Date deadline = item.getStartTime();

        List<ScheduleContentHistory> result = serv.getLastWeekRepairType(lineId, deadline);
        return R.ok().put("list", result);
    }

    @GetMapping("/allTypeLeast")
    public R getAllTypeLeast(@RequestParam("lineId") Integer lineId,
                             @RequestParam("deadline") Date deadline) {
        JSONObject jsonObject = new JSONObject();
        List<ScheduleContentHistory> lastRepairType = serv.getLastRepairType(lineId, deadline);// 上一次的年计划内容
        List<ScheduleContentHistory> lastMonthRepairType = serv.getLastMonthRepairType(lineId, deadline);
        List<ScheduleContentHistory> lastWeekRepairType = serv.getLastWeekRepairType(lineId, deadline);
        jsonObject.put("year", lastRepairType);
        jsonObject.put("month", lastMonthRepairType);
        jsonObject.put("week", lastWeekRepairType);

        return R.ok().put("data", jsonObject);
    }

    @GetMapping("/lastDayRepair")
    public R lastDayRepair(@RequestParam("lineId") Integer lineId) {
        ScheduleInfo item = serv2.getLeastItem(lineId, "日计划");
        Date deadline = item.getStartTime();

        JSONObject jsonObject = new JSONObject();
        List<ScheduleContentHistory> lastRepairType = serv.getLastRepairType(lineId, deadline);// 上一次的年计划内容
        List<ScheduleContentHistory> lastMonthRepairType = serv.getLastMonthRepairType(lineId, deadline);
        List<ScheduleContentHistory> lastWeekRepairType = serv.getLastWeekRepairType(lineId, deadline);
        jsonObject.put("year", lastRepairType);
        jsonObject.put("month", lastMonthRepairType);
        jsonObject.put("week", lastWeekRepairType);

        return R.ok().put("data", jsonObject);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody ScheduleContentHistory scheduleContentHistory) {
        serv.save(scheduleContentHistory);
        return R.ok();
    }

    @PostMapping("/batch")
    public R save(@RequestBody List<ScheduleContentHistory> list) {
        serv.saveBatch(list);
        return R.ok();
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody ScheduleContentHistory scheduleContentHistory) {
        QueryWrapper<ScheduleContentHistory> wrapper = new QueryWrapper<>();
        wrapper.eq("id", scheduleContentHistory.getId());
        serv.update(scheduleContentHistory, wrapper);
        return R.ok();
    }

    /**
     * 删除
     */
    @DeleteMapping("/{id}")
    public R delete(@PathVariable String id) {
        QueryWrapper<ScheduleContentHistory> wrapper = new QueryWrapper<>();
        wrapper.eq("id", id);
        serv.remove(wrapper);
        return R.ok();
    }
}
