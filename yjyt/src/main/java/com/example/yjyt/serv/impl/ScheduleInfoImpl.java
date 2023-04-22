
package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.ScheduleInfo;
import com.example.yjyt.domain.ScheduleInfoVO;
import com.example.yjyt.mapper.ScheduleMapper;
import com.example.yjyt.serv.ScheduleInfoServ;
import org.springframework.stereotype.Service;

import java.sql.Date;
import java.util.Comparator;
import java.util.List;

@Service
public class ScheduleInfoImpl extends ServiceImpl<ScheduleMapper, ScheduleInfo> implements ScheduleInfoServ {
    @Override
    public void getPageByLineId(Page<ScheduleInfoVO> page, String planType, Integer lineId) {
        baseMapper.getPage(page, planType, lineId);
    }

    public void getPage(Page<ScheduleInfoVO> page, String planType) {
        baseMapper.getPageAll(page, planType);
    }

    public ScheduleInfoVO getOneById(String id) {
        return baseMapper.getByIdOne(id);
    }


    public boolean dispatchByIds(List<String> ids) {
        List<ScheduleInfo> list = baseMapper.selectBatchIds(ids);
        list.forEach(i -> {
            i.setDispatchStatus("已下发");
        });
        return updateBatchById(list);
    }

    public void setFeedbackStatus(String scheduleId, boolean feedbackStatus) {
        ScheduleInfo item = baseMapper.selectById(scheduleId);
        item.setFeedbackStatus(feedbackStatus);
        baseMapper.updateById(item);
    }

    public ScheduleInfo getLeastItem(Integer lineId, String planType) {
        QueryWrapper<ScheduleInfo> wrapper = new QueryWrapper<>();
        wrapper.eq("line_id", lineId);
        wrapper.eq("plan_type", planType);
        List<ScheduleInfo> list = baseMapper.selectList(wrapper);
        if (list.isEmpty()) {
            return null;
        } else {
            list.sort(Comparator.comparing(ScheduleInfo::getStartTime));
            return list.get(list.size() - 1);
        }
    }

    public boolean isExists(Integer lineId, String planType, Date starDate, Date endDate) {
        QueryWrapper<ScheduleInfo> wrapper = new QueryWrapper<>();
        wrapper.eq("line_id", lineId);
        wrapper.eq("plan_type", planType);
        wrapper.ge("start_time", starDate);
        wrapper.le("end_time", starDate);
        wrapper.or(wq -> {
            wq.ge("start_time", endDate).le("end_time", endDate);
        });

        List<ScheduleInfo> list = baseMapper.selectList(wrapper);
        if (!list.isEmpty()) {
            return true;
        } else {
            return false;
        }
    }
}

