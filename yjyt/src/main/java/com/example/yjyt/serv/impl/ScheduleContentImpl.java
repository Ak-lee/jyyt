
package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.ScheduleContent;
import com.example.yjyt.domain.ScheduleContentVO;
import com.example.yjyt.mapper.ScheduleContentMapper;
import com.example.yjyt.serv.ScheduleContentServ;
import org.springframework.stereotype.Service;

import java.sql.Date;
import java.util.List;

@Service
public class ScheduleContentImpl extends ServiceImpl<ScheduleContentMapper, ScheduleContent> implements ScheduleContentServ {
    @Override
    public List<ScheduleContentVO> getContentByScheduleId(String scheduleId) {
        return baseMapper.getContent(scheduleId);
    }

    @Override
    public List<ScheduleContentVO> getContentBylineId(Integer lineId) {
        return baseMapper.getContentAll(lineId);
    }

    public ScheduleContent getLastTask(ScheduleContent content) {
        return baseMapper.getLastTask(content);
    }

    public ScheduleContent getNextTask(ScheduleContent content) {
        return baseMapper.getNextTask(content);
    }

    public ScheduleContent getNextTaskItem(Date planDate, String taskType, String trainId) {
        return baseMapper.getNextTaskItem(planDate, taskType, trainId);
    }

    public List<ScheduleContent> getLastRepairType(String scheduleId, Date deadline) {
        return baseMapper.getLastRepairType(scheduleId, deadline);
    }

    public List<ScheduleContent> getLastRepairType(Integer lineId, Date deadline) {
        return baseMapper.getLastRepairType(lineId, deadline);
    }


    public List<ScheduleContent> getListByScheduleIdAndRange(String ScheduleId, Date start, Date end) {
        return baseMapper.listByScheduleIdAndRange(ScheduleId, start, end);
    }

    public List<ScheduleContent> getListByRange(Integer lineId, Date start, Date end) {
        return baseMapper.listByRangeAndLineId(lineId, start, end);
    }

    public List<ScheduleContentVO> getListByLineIdAndDate(Integer lineId, Date date) {
        return baseMapper.listByLineIdAndDate(lineId, date);
    }
}

