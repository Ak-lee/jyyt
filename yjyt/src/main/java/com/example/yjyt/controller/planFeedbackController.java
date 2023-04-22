package com.example.yjyt.controller;

import com.example.yjyt.common.R;
import com.example.yjyt.domain.PlanFeedbackTemp;
import com.example.yjyt.domain.ScheduleContentHistory;
import com.example.yjyt.serv.impl.PlanFeedbackTempServiceImpl;
import com.example.yjyt.serv.impl.ScheduleContentHistoryImpl;
import com.example.yjyt.serv.impl.ScheduleInfoImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

@RequestMapping("/planFeedback")
@RestController
public class planFeedbackController {
    @Autowired
    private ScheduleContentHistoryImpl scServ;

    @Autowired
    private PlanFeedbackTempServiceImpl serv;

    @Autowired
    private ScheduleInfoImpl scheduleInfoServ;

    @PostMapping("/batch")
    @Transactional
    public R save(@RequestBody List<PlanFeedbackTemp> list) {
        String scheduleId = list.get(0).getScheduleId();
        ArrayList<ScheduleContentHistory> arr = new ArrayList<>();
        ArrayList<PlanFeedbackTemp> arr2 = new ArrayList<>();
        list.forEach(i -> {
            if (i.getDuration() == null || (i.getDuration() == 1) ||
                    Objects.equals(i.getDuration(), i.getOffsetDay())) {
                ScheduleContentHistory item = new ScheduleContentHistory();
                item.setTrainId(i.getTrainId());
                item.setTaskType(i.getTaskType());
                item.setTaskContent(i.getTaskContent());
                item.setScheduleId(i.getScheduleId());
                item.setWorkYard(i.getTaskSegment());
                item.setTaskSite(i.getTaskSite());
                item.setTaskTeam(i.getTaskTeam());
                item.setPerformDate(i.getDate());
                item.setDuration(i.getDuration());
                item.setOffsetDay(i.getOffsetDay());
                item.setLineId(i.getLineId());
                arr.add(item);
            } else {
                arr2.add(i);
            }
            if (i.getDuration() > 1 && Objects.equals(i.getDuration(), i.getOffsetDay())) {
                serv.removeItem(i.getScheduleId(), i.getTrainId(), i.getTaskType());
            }
        });
        scServ.saveBatch(arr);
        serv.saveBatch(arr2);
        scheduleInfoServ.setFeedbackStatus(scheduleId, true);
        return R.ok();
    }

    @GetMapping("/clear")
    public R clearByScheduleId(String scheduleId) {
        serv.clearByScheduleId(scheduleId);
        return R.ok();
    }
}
