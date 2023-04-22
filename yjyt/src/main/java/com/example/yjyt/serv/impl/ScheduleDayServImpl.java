
package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.OperationPlan;
import com.example.yjyt.domain.ScheduleDay;
import com.example.yjyt.domain.ScheduleDayVO;
import com.example.yjyt.mapper.ScheduleDayMapper;
import com.example.yjyt.serv.ScheduleDayServ;
import org.springframework.stereotype.Service;

import java.util.Comparator;
import java.util.List;

@Service
public class ScheduleDayServImpl extends ServiceImpl<ScheduleDayMapper, ScheduleDay> implements ScheduleDayServ {
    public List<ScheduleDayVO> getContentByScheduleId(String scheduleId) {
        return baseMapper.getContent(scheduleId);
    }

    public int clearByScheduleId(String scheduleId) {
        QueryWrapper<ScheduleDay> wrapper = new QueryWrapper<>();
        wrapper.eq("schedule_id", scheduleId);
        return baseMapper.delete(wrapper);
    }
}
