package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.WorkCalendarCategoryByMonth;
import com.example.yjyt.domain.WorkCalendarInfo;
import com.example.yjyt.mapper.WorkCalendarMapper;
import com.example.yjyt.serv.WorkCalendarInfoServ;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.sql.Date;
import java.util.List;

@Service
public class WorkCalendarInfoServImpl extends ServiceImpl<WorkCalendarMapper, WorkCalendarInfo> implements WorkCalendarInfoServ {
    @Autowired
    private WorkCalendarMapper WorkCalendarMapper;

    public List<WorkCalendarCategoryByMonth> categoryByMonth(String productionCalendarId) {
        return baseMapper.categoryByMonth(productionCalendarId);
    }

    public List<WorkCalendarInfo> tableWithCond(String calendarId, Integer year, Integer month) {
        return baseMapper.tableWithCond(calendarId, year, month);
    }

    public WorkCalendarInfo getItem(String calendarId, Date date) {
        QueryWrapper<WorkCalendarInfo> wrapper = new QueryWrapper<>();
        wrapper.eq("production_calendar_id", calendarId);
        wrapper.eq("date", date);
        List<WorkCalendarInfo> list = baseMapper.selectList(wrapper);
        if (list.isEmpty()) {
            return null;
        } else {
            // 查询的结果应该只有一个
            return list.get(0);
        }
    }
}
