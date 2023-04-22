package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.PlanFeedbackTemp;
import com.example.yjyt.serv.PlanFeedbackTempService;
import com.example.yjyt.mapper.PlanFeedbackTempMapper;
import org.springframework.stereotype.Service;

/**
* @author 29547
* @description 针对表【plan_feedback_temp】的数据库操作Service实现
* @createDate 2023-04-21 11:10:50
*/
@Service
public class PlanFeedbackTempServiceImpl extends ServiceImpl<PlanFeedbackTempMapper, PlanFeedbackTemp>
    implements PlanFeedbackTempService{
    public int removeItem(String scheduleId, String trainId, String taskType) {
        QueryWrapper<PlanFeedbackTemp> wrapper = new QueryWrapper<>();
        wrapper.eq("schedule_id", scheduleId);
        wrapper.eq("train_id", trainId);
        wrapper.eq("task_type", taskType);
        return baseMapper.delete(wrapper);
    }

    public int clearByScheduleId(String scheduleId) {
        QueryWrapper<PlanFeedbackTemp> wrapper = new QueryWrapper<>();
        wrapper.eq("schedule_id", scheduleId);
        return baseMapper.delete(wrapper);
    }
}




