package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.ScheduleContentHistory;
import com.example.yjyt.domain.ScheduleContentHistoryVO;
import com.example.yjyt.serv.ScheduleContentHistoryService;
import com.example.yjyt.mapper.ScheduleContentHistoryMapper;
import org.springframework.stereotype.Service;

import java.sql.Date;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * @author 29547
 * @description 针对表【schedule_content_history】的数据库操作Service实现
 * @createDate 2022-12-08 15:26:13
 */
@Service
public class ScheduleContentHistoryImpl extends ServiceImpl<ScheduleContentHistoryMapper, ScheduleContentHistory>
        implements ScheduleContentHistoryService {

    public Map<String, Object> getPagesOverview(Integer lineId, List<String> planTypes) {
        return baseMapper.getPagesOverview(lineId, planTypes);
    }

    public List<ScheduleContentHistoryVO> tableWithCond(Integer lineId, List<String> planTypes, Date sdate, Date edate, String status) {
        return baseMapper.tableWithCond(lineId, planTypes, sdate, edate, status);
    }

    public List<ScheduleContentHistoryVO> getListByScheduleId(String scheduleId) {
        return baseMapper.getContent(scheduleId);
    }

    public List<ScheduleContentHistoryVO> getList() {
        return baseMapper.getAllContent();
    }

    //    public List<ScheduleContentHistory> getLastRepairMode(String scheduleId, Date deadline, Integer month) {
//        String monthStr = "\\d*Y" + month + "[A-Z]?";
//        return baseMapper.getLastRepairMode(scheduleId, deadline, monthStr);
//    }
    public List<ScheduleContentHistory> getLastRepairMode(String scheduleId, Date deadline, Integer month) {
        return baseMapper.getLastRepairMode(scheduleId, deadline, month);
    }

    //    public List<ScheduleContentHistory> getLastRepairMode(Integer lineId, Date deadline, Integer month) {
//        String monthStr = "\\d*Y" + month + "[A-Z]?";
//        return baseMapper.getLastRepairMode2(lineId, deadline, monthStr);
//    }
    public List<ScheduleContentHistory> getLastRepairMode(Integer lineId, Date deadline, Integer month) {
        return baseMapper.getLastRepairMode2(lineId, deadline, month);
    }

    public List<ScheduleContentHistory> getLastRepairType(String scheduleId, Date deadline) {
        return baseMapper.getLastRepairType(scheduleId, deadline);
    }

    public List<ScheduleContentHistory> getLastRepairType(Integer lineId, Date deadline) {
        return baseMapper.getLastRepairType2(lineId, deadline);
    }

    public List<ScheduleContentHistory> getLastMonthRepairType(String scheduleId, Date deadline) {
        return baseMapper.getLatestMonthRepairType(scheduleId, deadline);
    }

    public List<ScheduleContentHistory> getLastMonthRepairType(Integer lineId, Date deadline) {
        return baseMapper.getLatestMonthRepairType2(lineId, deadline);
    }

    public List<ScheduleContentHistory> getLastWeekRepairType(String scheduleId, Date deadline) {
        return baseMapper.getLatestWeekRepairType(scheduleId, deadline);
    }

    public List<ScheduleContentHistory> getLastWeekRepairType(Integer lineId, Date deadline) {
        return baseMapper.getLatestWeekRepairType2(lineId, deadline);
    }

    public List<ScheduleContentHistory> lastAnyTypeRepairByLineId(Integer lineId, Date deadline) {
        return baseMapper.lastAnyTypeRepairByLineId(lineId, deadline);
    }

    public List<ScheduleContentHistory> filterByLineIdMonthTaskTypeNameDeadline(Integer lineId,
                                                                                Integer month,
                                                                                String tasktypeName, Date deadline) {
        return baseMapper.filterByLineIdMonthTaskTypeNameDeadline(lineId, month, tasktypeName, deadline);
    }
}




