package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.ProductionCalendar;
import com.example.yjyt.domain.WorkCalendarInfo;
import com.example.yjyt.serv.impl.ProductionCalendarServiceImpl;
import com.example.yjyt.serv.impl.WorkCalendarInfoServImpl;
import com.example.yjyt.util.DateRange;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

@RequestMapping("/calendar")
@RestController
public class calendarController {
    @Autowired
    private ProductionCalendarServiceImpl serv;

    @Autowired
    private WorkCalendarInfoServImpl workCalendarServ;

    @GetMapping("/table")
    public R tableAll(
            @RequestParam(name = "lineId", required = false, defaultValue = "-1") Integer lineId,
            @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
            @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<ProductionCalendar> page = new Page<>(curPage, size);
        serv.getPageByLineId(page, lineId);
        return R.ok().put("data", page);
    }

    @GetMapping("/tableNoPage")
    public R tableAllNoPage(@RequestParam(name = "lineId", required = false, defaultValue = "-1") Integer lineId) {
        List<ProductionCalendar> result = serv.getByLineId(lineId);
        return R.ok().put("list", result);
    }

    @PostMapping("/")
    public R saveItem(@RequestBody ProductionCalendar calendar) {
        Integer lineId = calendar.getLineId();
        Date startDate = calendar.getStartDate();
        Date endDate = calendar.getEndDate();

        boolean exists = serv.isExists(lineId, startDate, endDate);

        ProductionCalendar result = serv.getById(calendar.getId());
        if (result != null) {
            return R.error("id 已存在");
        } else if (exists) {
            return R.error("该计划与其他计划存在时间重叠");
        } else if (startDate == null || endDate == null) {
            return R.error("起止时间不能为空");
        } else {
            boolean succ = serv.save(calendar);
            if (succ) {
                Calendar c = Calendar.getInstance();
                Date startDateFlag = startDate;
                List<WorkCalendarInfo> list = new ArrayList<>();
                while (startDateFlag.compareTo(endDate) <= 0) {
                    c.setTime(startDateFlag);
                    WorkCalendarInfo item = new WorkCalendarInfo();
                    item.setDate(c.getTime());
                    item.setLineId(lineId);
                    item.setProductionCalendarId(calendar.getId());
                    if (c.get(Calendar.DAY_OF_WEEK) == Calendar.SATURDAY || c.get(Calendar.DAY_OF_WEEK) == Calendar.SUNDAY) {
                        item.setAttribute("休息");
                    } else {
                        item.setAttribute("工作");
                    }
                    list.add(item);
                    // 当前日期加一天
                    c.add(Calendar.DATE, 1);
                    startDateFlag = c.getTime();
                }
                if (!list.isEmpty()) {
                    workCalendarServ.saveBatch(list);
                }
                return R.ok().put("result", calendar);
            } else {
                return R.error("保存失败");
            }
        }
    }

    @PutMapping("/")
    public R updateItem(@RequestBody ProductionCalendar calendar) {
        QueryWrapper<ProductionCalendar> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("id", calendar.getId());
        ProductionCalendar prev = serv.getById(calendar.getId());

        serv.update(calendar, queryWrapper);

        // update work_calendar table.
        DateRange prevRange = new DateRange(prev.getStartDate(), prev.getEndDate());
        DateRange currentRange = new DateRange(calendar.getStartDate(), calendar.getEndDate());

        List<Date> prevSubCurrent = prevRange.subRange(currentRange);
        List<Date> currentSubPrev = currentRange.subRange(prevRange);

        if (!prevSubCurrent.isEmpty()) {
            QueryWrapper<WorkCalendarInfo> removeQW = new QueryWrapper<>();
            removeQW.eq("production_calendar_id", calendar.getId());
            removeQW.in("date", prevSubCurrent);
            workCalendarServ.remove(removeQW);
        }
        if (!currentSubPrev.isEmpty()) {
            List<WorkCalendarInfo> addList = new ArrayList<>();
            currentSubPrev.forEach(item -> {
                WorkCalendarInfo i = new WorkCalendarInfo();
                i.setLineId(calendar.getLineId());
                i.setProductionCalendarId(calendar.getId());
                i.setDate(item);

                Calendar c = Calendar.getInstance();
                c.setTime(item);
                if (c.get(Calendar.DAY_OF_WEEK) == Calendar.SATURDAY || c.get(Calendar.DAY_OF_WEEK) == Calendar.SUNDAY) {
                    i.setAttribute("休息");
                } else {
                    i.setAttribute("工作");
                }
                ;
                addList.add(i);
            });
            workCalendarServ.saveBatch(addList);
        }

        return R.saveOk(calendar);
    }

    @GetMapping("/getItem")
    public R getItem(@RequestParam Integer lineId, @RequestParam("date") @DateTimeFormat(pattern = "yyyy-MM-dd") Date date) {
        WorkCalendarInfo item = serv.getItem(lineId, date);
        return R.ok().put("data", item);
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
