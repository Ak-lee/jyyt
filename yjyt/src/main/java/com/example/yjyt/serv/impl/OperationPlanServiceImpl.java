package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.OperationPlan;
import com.example.yjyt.mapper.OperationPlanMapper;
import com.example.yjyt.serv.OperationPlanService;
import org.springframework.stereotype.Service;

import java.util.List;

/**
* @author 29547
* @description 针对表【operation plan(运营计划推荐列车表)】的数据库操作Service实现
* @createDate 2023-03-29 11:48:12
*/
@Service
public class OperationPlanServiceImpl extends ServiceImpl<OperationPlanMapper, OperationPlan>
    implements OperationPlanService {
    public List<OperationPlan> getByDayScheduleId(String dayScheduleId) {
        QueryWrapper<OperationPlan> wrapper = new QueryWrapper<>();
        wrapper.eq("day_schedule_id", dayScheduleId);
        return baseMapper.selectList(wrapper);
    }

    public int clearByDayScheduleId(String dayScheduleId) {
        QueryWrapper<OperationPlan> wrapper = new QueryWrapper<>();
        wrapper.eq("day_schedule_id", dayScheduleId);
        return baseMapper.delete(wrapper);
    }
}




