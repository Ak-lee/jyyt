package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.toolkit.IdWorker;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.ScheduleDay;
import com.example.yjyt.domain.ScheduleDayVO;
import com.example.yjyt.serv.impl.ScheduleDayServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RequestMapping("/schedule_day")
@RestController
public class ScheduleDayController {

    @Autowired
    private ScheduleDayServImpl serv;

    @GetMapping("/table")
    public R table(@RequestParam(name = "scheduleId", required = true) String scheduleId) {
        List<ScheduleDayVO> scheduleDayList = serv.getContentByScheduleId(scheduleId);
        return R.ok().put("data", scheduleDayList);
    }

    /**
     * 信息
     */
    @GetMapping("/info/{id}")
    public R info(@PathVariable("id") Integer id) {
        ScheduleDay scheduleDay = serv.getById(id);
        return R.ok().put("data", scheduleDay);
    }


    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody ScheduleDay scheduleDay) {
        serv.save(scheduleDay);
        return R.ok();
    }

    @PostMapping("/list")
    public R saveList(@RequestBody List<ScheduleDay> list) {
        List<ScheduleDay> insertData = list.stream().filter(i -> i.getId() == null).collect(Collectors.toList());
        List<ScheduleDay> updateData = list.stream().filter(i -> i.getId() != null).collect(Collectors.toList());

        insertData.forEach(i -> {
            i.setId(IdWorker.getId());
        });
        serv.saveBatch(insertData);
        if (!updateData.isEmpty()) {
            serv.updateBatchById(updateData);
        }
        return R.ok();
    }

    @GetMapping("/clear")
    public R clearByScheduleId(@RequestParam("scheduleId") String scheduleId) {
        serv.clearByScheduleId(scheduleId);
        return R.ok();
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody ScheduleDay scheduleDay) {
        serv.updateById(scheduleDay);
        return R.ok();
    }

    /**
     * 删除
     */
    @DeleteMapping("/{id}")
    public R delete(@PathVariable String id) {
        serv.removeById(id);
        return R.ok();
    }
}

