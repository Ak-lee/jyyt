package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.predResult;
import com.example.yjyt.mapper.predictResultMapper;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class predResultsServImpl extends ServiceImpl<predictResultMapper, predResult> {
    public List<predResult> getPredResultList() {
        return baseMapper.predResultPage();
    }

    public List<predResult> gettrainingEndtimes() {
        return baseMapper.getendTrainingList();
    }
}
