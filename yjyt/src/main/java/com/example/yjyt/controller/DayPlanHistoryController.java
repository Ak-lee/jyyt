package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.DayPlanHistory;
import com.example.yjyt.mapper.DayPlanHistoryMapper;
import com.example.yjyt.serv.impl.DayPlanHistoryServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.sql.Date;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/dayPlanHistory")
public class DayPlanHistoryController {
    @Autowired
    private DayPlanHistoryServiceImpl serv;

    @GetMapping()
    public R getBylineId(@RequestParam("lineId") Integer lineId,
                         @RequestParam("date") Date date
    ) {

        List<DayPlanHistory> data = serv.getByLineIdAndDate(lineId, date);
        return R.ok().put("data", data);
    }

    @PostMapping("/clearAndAdd")
    public R postData(@RequestBody List<DayPlanHistory> list) {
        QueryWrapper<DayPlanHistory> wrapper = new QueryWrapper<>();
        List<String> trainIds = new ArrayList<>();
        list.forEach(i -> {
            trainIds.add(i.getTrainId());
        });
        wrapper.in("train_id", trainIds);

        serv.remove(wrapper);
        serv.saveBatch(list);
        return R.ok();
    }
}
