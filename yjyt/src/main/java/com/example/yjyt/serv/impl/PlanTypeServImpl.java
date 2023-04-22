package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.PlanTypeInfo;
import com.example.yjyt.domain.PlanTypeInfoVO;
import com.example.yjyt.mapper.PlanTypeMapper;
import com.example.yjyt.serv.PlanTypeInfoServ;
import org.springframework.stereotype.Service;

@Service
public class PlanTypeServImpl extends ServiceImpl<PlanTypeMapper, PlanTypeInfo> implements PlanTypeInfoServ {

    @Override
    public void getPageByLineId(Page<PlanTypeInfoVO> page, Integer lineId) {
        baseMapper.getPage(page, lineId);
    }

    public void getPage(Page<PlanTypeInfoVO> page) {
        baseMapper.getPageAll(page);
    }

//    public PlanTypeInfoVO getById(String id){
//        return baseMapper.getOneById(id);
//    }
}
