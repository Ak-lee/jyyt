package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.MileageHistory;
import com.example.yjyt.mapper.MileageHistoryMapper;
import com.example.yjyt.serv.MileageHistoryServ;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.sql.Date;
import java.util.List;
import java.util.Map;

@Service
public class MileageHistoryServImpl extends ServiceImpl<MileageHistoryMapper, MileageHistory> implements MileageHistoryServ {
    @Autowired
    MileageHistoryMapper mileageHistoryMapper;

    public int saveMileageHistory(List<MileageHistory> list) {
        int count = 0;
        for (MileageHistory data : list) {
            count += mileageHistoryMapper.insert(data);
        }
        return count;
    }

    public List<MileageHistory> getMileageHistory() {
        return mileageHistoryMapper.selectList(null);
    }

    public List<MileageHistory> getMileageList(Integer lineId, Date sdate, Date edate) {
        return mileageHistoryMapper.getMileageList(lineId, sdate, edate);
    }

    public MileageHistory getItemByTrainIdAndDate(String trainId, Date date) {
        QueryWrapper<MileageHistory> wrapper = new QueryWrapper<>();
        wrapper.eq("train_id", trainId).eq("date", date);
        MileageHistory result = baseMapper.selectOne(wrapper);
        return result;
    }

    public Map<String, java.util.Date> getPagesOverview(Integer lineId) {
        return baseMapper.getPagesOverview(lineId);
    }
}
