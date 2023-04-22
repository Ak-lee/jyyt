package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.ProductionCalendar;
import com.example.yjyt.domain.WorkCalendarInfo;
import com.example.yjyt.serv.ProductionCalendarService;
import com.example.yjyt.mapper.ProductionCalendarMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.text.DateFormat;
import java.util.Date;
import java.util.List;

/**
 * @author 29547
 * @description 针对表【production_calendar(生产日历信息)】的数据库操作Service实现
 * @createDate 2022-11-07 15:33:09
 */
@Service
public class ProductionCalendarServiceImpl extends ServiceImpl<ProductionCalendarMapper, ProductionCalendar>
        implements ProductionCalendarService {
    @Autowired
    WorkCalendarInfoServImpl serv2;

    public void getPageByLineId(Page<ProductionCalendar> page, Integer lineId) {
        if (lineId == -1) {
            baseMapper.selectPage(page, null);
        } else {
            baseMapper.getPage(page, lineId);
        }
    }

    public List<ProductionCalendar> getByLineId(Integer lineId) {
        if (lineId == -1) {
            return null;
        } else {
            return baseMapper.getList(lineId);
        }
    }

    public boolean isExists(Integer lineId, Date startDate, Date endDate) {
        QueryWrapper<ProductionCalendar> wrapper = new QueryWrapper<>();
        wrapper.eq("line_id", lineId);
        wrapper.le("start_Date", startDate);
        wrapper.ge("end_Date", startDate);
        wrapper.or(wq -> {
            wq.ge("start_Date", endDate).le("end_Date", endDate);
        });

        List<ProductionCalendar> list = baseMapper.selectList(wrapper);
        if (!list.isEmpty()) {
            return true;
        } else {
            return false;
        }
    }

    public WorkCalendarInfo getItem(Integer lineId, Date date) {
        ProductionCalendar item = baseMapper.getItem(lineId, new java.sql.Date(date.getTime()));
        if (item == null) {
            return null;
        } else {
            String id = item.getId();
            return serv2.getItem(id, new java.sql.Date(date.getTime()));
        }
    }
}




