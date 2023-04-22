package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.YardTeamInfo;
import com.example.yjyt.domain.YardTeamInfoVO;
import com.example.yjyt.mapper.YardTeamMapper;
import com.example.yjyt.serv.YardTeamInfoServ;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class YardTeamInfoServImpl extends ServiceImpl<YardTeamMapper, YardTeamInfo> implements YardTeamInfoServ {
    public List<YardTeamInfoVO> getByYardId(String yardId) {
        return baseMapper.getVOByYardId(yardId);
    }
}
