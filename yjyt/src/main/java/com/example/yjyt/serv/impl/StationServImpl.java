package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.Station;
import com.example.yjyt.domain.StationVO;
import com.example.yjyt.mapper.StationMapper;
import com.example.yjyt.serv.StationServ;
import org.springframework.stereotype.Service;

@Service
public class StationServImpl extends ServiceImpl<StationMapper, Station> implements StationServ {
    @Override
    public void getPageByLineId(Page<StationVO> page, Integer lineId) {
        baseMapper.getPage(page, lineId);
    }

    public void getPage(Page<StationVO> page) {
        baseMapper.getPageAll(page);
    }
}
