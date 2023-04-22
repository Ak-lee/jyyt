package com.example.yjyt.controller;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.IdWorker;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.ScheduleContent;
import com.example.yjyt.domain.ScheduleContentVO;
import com.example.yjyt.domain.ScheduleInfo;
import com.example.yjyt.serv.impl.ScheduleContentImpl;
import com.example.yjyt.serv.impl.ScheduleInfoImpl;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.management.Query;
import java.sql.Date;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@RequestMapping("/schedule_content")
@RestController
public class ScheduleContentController {

    @Autowired
    private ScheduleContentImpl serv;

    @Autowired
    private ScheduleInfoImpl serv2;

    @GetMapping("/table")
    public R table(@RequestParam(name = "scheduleId", required = true) String scheduleId) {
        List<ScheduleContentVO> scheduleContentVOList = serv.getContentByScheduleId(scheduleId);
        return R.ok().put("data", scheduleContentVOList);
    }

    @GetMapping("/tableall")
    public R tableAll(@RequestParam(name = "lineId", required = true) Integer lineId) {
        List<ScheduleContentVO> scheduleContentVOList = serv.getContentBylineId(lineId);
        return R.ok().put("data", scheduleContentVOList);
    }

    @GetMapping("/getListByLineIdAndDate")
    public R getListByLineIdAndDate(@RequestParam("lineId") Integer lineId,
                                    @RequestParam("date") Date date) {
        List<ScheduleContentVO> list = serv.getListByLineIdAndDate(lineId, date);
        return R.ok().put("data", list);
    }

    @GetMapping("/lastRepairType")
    // 获取所有列车的上一次均衡修检修模式
    public R getLastRepairType(@RequestParam("lineId") Integer lineId) {
        ScheduleInfo item = serv2.getLeastItem(lineId, "年计划");
        Date deadLine = item.getStartTime();

        List<ScheduleContent> result = serv.getLastRepairType(lineId, deadLine);
        return R.ok().put("data", result);
    }

    /**
     * 信息
     */
    @GetMapping("/info/{id}")
    public R info(@PathVariable("id") Integer id) {
        ScheduleContent scheduleContent = serv.getById(id);
        return R.ok().put("data", scheduleContent);
    }

    @GetMapping("/getLastTask/{id}")
    public R getLastTask(@PathVariable("id") Integer id) {
        // 获取上一次该检修任务的信息。
        ScheduleContent scheduleContent = serv.getById(id);
        ScheduleContent data = serv.getLastTask(scheduleContent);
        return R.ok().put("data", data);
    }

    @GetMapping("/getNextTask/{id}")
    public R getNextTask(@PathVariable("id") Integer id) {
        // 获取下一次该检修任务的信息。
        ScheduleContent scheduleContent = serv.getById(id);
        ScheduleContent data = serv.getNextTask(scheduleContent);
        return R.ok().put("data", data);
    }

    @GetMapping("/getNextTaskItem")
    public R getNextTaskItem(@RequestParam("planDate") Date planDate,
                             @RequestParam("taskType") String taskType,
                             @RequestParam("trainId") String trainId) {
        ScheduleContent data = serv.getNextTaskItem(planDate, taskType, trainId);
        return R.ok().put("data", data);
    }

    @GetMapping("/getListByScheduleIdAndRange")
    public R getListByScheduleIdAndRange(@RequestParam("scheduleId") String scheduleId,
                                         @RequestParam("start") Date start,
                                         @RequestParam("end") Date end) {
        List<ScheduleContent> list = serv.getListByScheduleIdAndRange(scheduleId, start, end);
        return R.ok().put("list", list);
    }

    @GetMapping("/getListByLineIdAndRange")
    public R getListByLineIdAndRange(
            @RequestParam("lineId") Integer lineId,
            @RequestParam("start") Date start,
            @RequestParam("end") Date end) {
        List<ScheduleContent> list = serv.getListByRange(lineId, start, end);
        return R.ok().put("list", list);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody ScheduleContent scheduleContent) {
        Long id = IdWorker.getId();
        scheduleContent.setId(String.valueOf(id));
        serv.save(scheduleContent);
        return R.ok();
    }

    @GetMapping("/clear")
    public R clearScheduleContent(@RequestParam("scheduleId") String scheduleId) {
        QueryWrapper<ScheduleContent> wrapper = new QueryWrapper<>();
        wrapper.eq("schedule_id", scheduleId);
        serv.remove(wrapper);
        return R.ok("删除成功");
    }

    @PostMapping("/list")
    public R saveList(@RequestBody List<ScheduleContent> list) {
        List<ScheduleContent> insertData = list.stream().filter(i -> i.getId() == null).collect(Collectors.toList());
        List<ScheduleContent> updateData = list.stream().filter(i -> i.getId() != null).collect(Collectors.toList());

        insertData.forEach(i -> {
            i.setId(String.valueOf(IdWorker.getId()));
        });
        serv.saveBatch(insertData);
        if (!updateData.isEmpty()) {
            serv.updateBatchById(updateData);
        }
        return R.ok();
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody List<ScheduleContent> scheduleContent) {
        scheduleContent.forEach(item -> {
            QueryWrapper<ScheduleContent> wrapper = new QueryWrapper<>();
            wrapper.eq("id", item.getId());
            serv.update(item, wrapper);
        });
        return R.ok();
    }


    /**
     * 删除
     */
    @DeleteMapping("/{id}")
    public R delete(@PathVariable String id) {
        QueryWrapper<ScheduleContent> wrapper = new QueryWrapper<>();
        wrapper.eq("id", id);
        serv.remove(wrapper);
        return R.ok();
    }
}
