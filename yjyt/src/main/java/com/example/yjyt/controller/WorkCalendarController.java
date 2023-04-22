package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.WorkCalendarCategoryByMonth;
import com.example.yjyt.domain.WorkCalendarInfo;
import com.example.yjyt.serv.impl.WorkCalendarInfoServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.sql.Date;
import java.util.List;

@RequestMapping("/workcalendar")
@RestController
public class WorkCalendarController {

    @Autowired
    private WorkCalendarInfoServImpl serv;

    @GetMapping("/tableNoPage")
    public R tableNoPage(@RequestParam(name = "sdate") Date sdate,
                         @RequestParam(name = "edate") Date edate
    ) {

        QueryWrapper<WorkCalendarInfo> wrapper = new QueryWrapper<>();
        wrapper.between("date", sdate, edate);
        List<WorkCalendarInfo> result = serv.list(wrapper);
        return R.ok().put("list", result);
    }

    @GetMapping("/tableWithCond")
    public R tableWithCond(@RequestParam(name = "calendarId") String calendarId, @RequestParam(name = "year") Integer year, @RequestParam(name = "month") Integer month) {
        List<WorkCalendarInfo> list = serv.tableWithCond(calendarId, year, month);
        return R.ok().put("list", list);
    }

    @GetMapping("getCategoryInfoByCalendarId")
    public R getInfoByCalendarId(@RequestParam("calendarId") String calendarId) {
        List<WorkCalendarCategoryByMonth> result = serv.categoryByMonth(calendarId);
        return R.ok().put("list", result);
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody WorkCalendarInfo workCalendarInfo) {
        serv.updateById(workCalendarInfo);
        return R.ok();
    }
}
