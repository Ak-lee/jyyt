package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.BriefYard;
import com.example.yjyt.domain.YardInfo;
import com.example.yjyt.exception.BusinessException;
import com.example.yjyt.mapper.YardMapper;
import com.example.yjyt.serv.YardInfoServ;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class YardInfoServImpl extends ServiceImpl<YardMapper, YardInfo> implements YardInfoServ {
    public List<BriefYard> getAllYards() {
        List<YardInfo> yards = baseMapper.selectList(null);
        List<BriefYard> briefYards = new ArrayList<>();

        for (YardInfo yard : yards) {
            BriefYard bf = new BriefYard();
            BeanUtils.copyProperties(yard, bf);
            briefYards.add(bf);
        }
        return briefYards;
    }

    public boolean save(YardInfo yardInfo) {
        YardInfo item = baseMapper.selectById(yardInfo.getId());
        if (item == null) {
            baseMapper.insert(yardInfo);
            return true;
        } else {
            throw new BusinessException("id 已存在");
        }
    }
}
