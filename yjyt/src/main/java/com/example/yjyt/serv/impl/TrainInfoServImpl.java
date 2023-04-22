package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.TrainInfo;
import com.example.yjyt.domain.TrainInfoVO;
import com.example.yjyt.mapper.TrainMapper;
import com.example.yjyt.serv.TrainInfoServ;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TrainInfoServImpl extends ServiceImpl<TrainMapper, TrainInfo> implements TrainInfoServ {
    public void getPageByLineId(Page<TrainInfoVO> page, Integer lineId) {
        baseMapper.getPage(page, lineId);
    }

    public List<TrainInfoVO> getByLineId(Integer lineId) {
        return baseMapper.getListByLineId(lineId);
    }

    public void getPage(Page<TrainInfoVO> page) {
        baseMapper.getPageAll(page);
    }
}
