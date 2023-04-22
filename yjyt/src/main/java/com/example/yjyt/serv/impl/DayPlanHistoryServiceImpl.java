package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.DayPlanHistory;
import com.example.yjyt.serv.DayPlanHistoryService;
import com.example.yjyt.mapper.DayPlanHistoryMapper;
import org.springframework.stereotype.Service;

import java.sql.Date;
import java.util.List;

/**
* @author 29547
* @description 针对表【day_plan_history】的数据库操作Service实现
* @createDate 2023-03-24 16:57:32
*/
@Service
public class DayPlanHistoryServiceImpl extends ServiceImpl<DayPlanHistoryMapper, DayPlanHistory>
    implements DayPlanHistoryService{
    public List<DayPlanHistory> getByLineIdAndDate(Integer lineId, Date date) {
        QueryWrapper<DayPlanHistory> wrapper = new QueryWrapper<>();
        wrapper.eq("line_id", lineId).eq("date", date);
        return baseMapper.selectList(wrapper);
    }
}




