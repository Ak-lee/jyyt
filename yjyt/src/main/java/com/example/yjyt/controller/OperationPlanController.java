package com.example.yjyt.controller;

import com.example.yjyt.common.R;
import com.example.yjyt.domain.HotBackupTrainNum;
import com.example.yjyt.domain.OperationPlan;
import com.example.yjyt.serv.impl.OperationPlanServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping("/operationPlan")
@RestController
public class OperationPlanController {
    @Autowired
    private OperationPlanServiceImpl serv;

    @GetMapping("/getByDayScheduleId")
    public R getByDayPlanScheduleId(
            @RequestParam("dayScheduleId") String dayScheduleId
    ) {
        List<OperationPlan> list = serv.getByDayScheduleId(dayScheduleId);
        if (list.isEmpty()) {
            return R.error("该日计划不存在");
        } else {
            return R.ok().put("data", list.get(0)); // 一个计划一天只有一个条目
        }
    }

    @GetMapping("/clear")
    public R clearByDayScheduleId(@RequestParam("dayScheduleId") String dayScheduleId) {
        serv.clearByDayScheduleId(dayScheduleId);
        return R.ok();
    }

    @PostMapping("/")
    public R save(@RequestBody OperationPlan operationPlan) {
        serv.save(operationPlan);
        return R.ok();
    }
}
