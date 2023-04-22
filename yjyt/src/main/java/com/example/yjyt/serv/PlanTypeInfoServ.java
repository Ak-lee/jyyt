package com.example.yjyt.serv;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.example.yjyt.domain.PlanTypeInfo;
import com.example.yjyt.domain.PlanTypeInfoVO;

public interface PlanTypeInfoServ extends IService<PlanTypeInfo> {
    void getPageByLineId(Page<PlanTypeInfoVO> page, Integer lineId);
}
